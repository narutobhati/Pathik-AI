export interface Campaign {
  id: string;
  name: string;
  objective: string;
  campaign_type: string;
  daily_budget: number;
  start_date: string;
  end_date: string;
  status: "DRAFT" | "PUBLISHED";
  google_campaign_id?: string;
  created_at: string;
}

export interface CreateCampaignPayload {
  name: string;
  objective: string;
  campaign_type: string;
  daily_budget: number;
  start_date: string;
  end_date: string;
  ad_group_name: string;
  ad_headline: string;
  ad_description: string;
  asset_url?: string;
}
