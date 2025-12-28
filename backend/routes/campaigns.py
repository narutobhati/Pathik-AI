from flask import Blueprint, request, jsonify
from datetime import datetime
from extensions import db, logger
from models.campaign import Campaign
from services.google_ads_service import get_google_ads_client
from google.ads.googleads.errors import GoogleAdsException
import os
from google.ads.googleads.v22.enums.types.eu_political_advertising_status import (
    EuPoliticalAdvertisingStatusEnum,
)


campaigns_bp = Blueprint("campaigns", __name__)


@campaigns_bp.route("/", methods=["POST"])
def create_campaign():
    data = request.get_json()

    required_fields = [
        "name",
        "objective",
        "campaign_type",
        "daily_budget",
        "start_date",
        "end_date",
        "ad_group_name",
        "ad_headline",
        "ad_description",
    ]

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logger.warning(f"Missing fields: {missing_fields}")
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    if data["daily_budget"] <= 0:
        return jsonify({"error": "Daily budget must be greater than 0"}), 400

    try:
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    if start_date >= end_date:
        return jsonify({"error": "End date must be after start date"}), 400

    campaign = Campaign(
        name=data["name"],
        objective=data["objective"],
        campaign_type=data["campaign_type"],
        daily_budget=data["daily_budget"],
        start_date=start_date,
        end_date=end_date,
        status="DRAFT",
        ad_group_name=data["ad_group_name"],
        ad_headline=data["ad_headline"],
        ad_description=data["ad_description"],
        asset_url=data.get("asset_url"),
    )

    db.session.add(campaign)
    db.session.commit()

    logger.info(f"Campaign created with ID {campaign.id}")

    return jsonify({
        "id": campaign.id,
        "status": campaign.status,
        "message": "Campaign created successfully"
    }), 201


@campaigns_bp.route("/", methods=["GET"])
def get_campaigns():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()

    result = []
    for campaign in campaigns:
        result.append({
            "id": campaign.id,
            "name": campaign.name,
            "objective": campaign.objective,
            "campaign_type": campaign.campaign_type,
            "daily_budget": campaign.daily_budget,
            "start_date": campaign.start_date.isoformat(),
            "end_date": campaign.end_date.isoformat(),
            "status": campaign.status,
            "google_campaign_id": campaign.google_campaign_id,
            "created_at": campaign.created_at.isoformat()
        })

    logger.info(f"Fetched {len(result)} campaigns")
    return jsonify(result), 200


@campaigns_bp.route("/<campaign_id>/publish", methods=["POST"])
def publish_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)

    if not campaign:
        return jsonify({"error": "Campaign not found"}), 404

    if campaign.status != "DRAFT":
        return jsonify({"error": "Campaign already published"}), 400

    logger.info(f"Publishing campaign {campaign.id}")

    try:
        client = get_google_ads_client()
        customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID")

        budget_resource = campaign.google_budget_resource

        if not budget_resource:
            budget_service = client.get_service("CampaignBudgetService")
            budget_operation = client.get_type("CampaignBudgetOperation")

            budget = budget_operation.create
            budget.name = f"Budget for {campaign.name} ({campaign.id})"
            budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
            budget.amount_micros = int(campaign.daily_budget * 1_000_000)

            budget_response = budget_service.mutate_campaign_budgets(
                customer_id=customer_id,
                operations=[budget_operation]
            )

            budget_resource = budget_response.results[0].resource_name
            campaign.google_budget_resource = budget_resource
            db.session.commit()

            logger.info(f"Created budget {budget_resource}")
        else:
            logger.info(f"Reusing existing budget {budget_resource}")

 
        campaign_service = client.get_service("CampaignService")
        campaign_operation = client.get_type("CampaignOperation")

        google_campaign = campaign_operation.create
        google_campaign.name = campaign.name
        google_campaign.status = client.enums.CampaignStatusEnum.PAUSED
        google_campaign.advertising_channel_type = (
            client.enums.AdvertisingChannelTypeEnum.SEARCH
        )

        google_campaign.manual_cpc.enhanced_cpc_enabled = False

        google_campaign._pb.contains_eu_political_advertising = (
            EuPoliticalAdvertisingStatusEnum.EuPoliticalAdvertisingStatus.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
        )




        google_campaign.campaign_budget = budget_resource

        response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_operation]
        )

        google_campaign_id = response.results[0].resource_name.split("/")[-1]

        campaign.google_campaign_id = google_campaign_id
        campaign.status = "PUBLISHED"
        db.session.commit()

        logger.info(f"Campaign published with Google ID {google_campaign_id}")

        return jsonify({
            "message": "Campaign published successfully",
            "google_campaign_id": google_campaign_id
        }), 200

    except GoogleAdsException:
        logger.exception("Google Ads API error")
        return jsonify({"error": "Google Ads API error"}), 500

    except Exception:
        logger.exception("Unexpected error during campaign publish")
        return jsonify({"error": "Internal server error"}), 500

