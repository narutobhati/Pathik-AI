#  Pathik AI — Google Ads Campaign Management Platform

Pathik AI is a **full-stack campaign management platform** that allows users to create, manage, and publish Google Ads campaigns through a clean web UI.  
It integrates **Google Ads API v22**, handles **mandatory compliance requirements**, and uses a **fully Dockerized setup** with automatic database migrations.

---

##  Key Features

-  Create & manage ad campaigns from UI  
-  Publish campaigns directly to **Google Ads**  
-  Google Ads API v22 compliant (EU political advertising enum handled correctly)  
-  PostgreSQL database with SQLAlchemy ORM  
-  Automatic DB migrations on container startup  
-  Fully Dockerized (Frontend + Backend + DB)  
-  Clean REST API design  
-  Production-grade backend structure  

---

##  Tech Stack

### Frontend
- React
- Tailwind CSS
- REST API integration

### Backend
- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Google Ads Python SDK (v22)
- PostgreSQL

### Infrastructure
- Docker
- Docker Compose
- PostgreSQL 14

---

##  Google Ads Integration

Pathik AI uses **Google Ads API v22** with:

- Campaign creation
- Budget creation (idempotent)
- Mandatory compliance fields

---

##  Docker Services

### Frontend
- Container: `pathik-frontend`
- URL: http://localhost:5173

### Backend
- Container: `pathik-backend`
- URL: http://localhost:5000

### Database
- Container: `pathik-db`
- PostgreSQL 14
- Accessible only inside Docker network

---

##  Environment Variables

Create a `.env` file in the root:

```env
# Database
POSTGRES_DB=campaigns
POSTGRES_USER=campaign_user
POSTGRES_PASSWORD=password
DATABASE_URL=postgresql://campaign_user:password@db:5432/campaigns

# Google Ads
GOOGLE_ADS_DEVELOPER_TOKEN=your_token
GOOGLE_ADS_CLIENT_ID=your_client_id
GOOGLE_ADS_CLIENT_SECRET=your_client_secret
GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token
GOOGLE_ADS_CUSTOMER_ID=1234567890
GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890
```
 

##  How to Get Google Ads API Credentials

To publish campaigns to Google Ads, you **must** configure official Google Ads API credentials.  
Follow the steps below **in order**.



## 1. Create a Google Ads Manager Account (If Not Already)

- Go to: https://ads.google.com/
- Sign in with your Google account
- Create an Ads account (or use an existing one)

👉 **Important:**  
You must have **admin access** to the Google Ads account.



## 2. Enable Google Ads API in Google Cloud Console

1. Go to: https://console.cloud.google.com/
2. Create a **new project** (recommended)
3. Navigate to:
4. Search for **Google Ads API**
5. Click **Enable**



## 3. Create OAuth 2.0 Credentials

1. In Google Cloud Console:
2. Click **Create Credentials → OAuth client ID**
3. Choose **Web application**
4. Set:
- Name: `Pathik AI`
- Authorized redirect URI:
  ```
  https://developers.google.com/oauthplayground
  ```
5. Click **Create**

You will get:
-  **Client ID**
-  **Client Secret**

Save them securely.



## 4. Get a Refresh Token (OAuth Playground)

1. Open:  
https://developers.google.com/oauthplayground
2. Click **Settings**
- Enable: **Use your own OAuth credentials**
- Paste:
  - Client ID
  - Client Secret
3. In the left panel, select:
https://www.googleapis.com/auth/adwords
4. Click **Authorize APIs**
5. Login with the **same Google Ads account**
6. Click **Exchange authorization code for tokens**

Copy the **Refresh Token**


## 5. Get Developer Token (Most Important)

1. Go to:  
https://ads.google.com/aw/apicenter
2. Sign in with your Google Ads account
3. Request a **Developer Token**
4. Initially, it will be: Test

 **Test tokens work for development**  
 Production approval required for live ads

Copy the **Developer Token**


## 6. Get Google Ads Customer ID

1. Open Google Ads UI
2. Look at the top-right corner
3. Copy the **10-digit Customer ID**
4. Remove dashes before using:

---
### API Endpoints


#### 1. Create Campaign
```
POST /api/campaigns
```
Creates a new campaign in the local database (status: DRAFT).

**Request Body**
```json
{
  "name": "Test Campaign",
  "objective": "TRAFFIC",
  "campaign_type": "SEARCH",
  "daily_budget": 10,
  "start_date": "2025-01-01",
  "end_date": "2025-01-10",
  "ad_group_name": "Test Ad Group",
  "ad_headline": "Buy Shoes Online",
  "ad_description": "Best shoes at best prices",
  "asset_url": "https://example.com"
}
```
**Response:**
```json
{
  "id": "92cc4c54-e553-4b28-a02d-60cb3344566c",
  "status": "DRAFT",
  "message": "Campaign created successfully"
}
```

#### 2. Get All Campaigns
```
GET /api/campaigns
```

**Response:**
```json
[
  {
    "id": "92cc4c54-e553-4b28-a02d-60cb3344566c",
    "name": "Test Campaign",
    "objective": "TRAFFIC",
    "campaign_type": "SEARCH",
    "daily_budget": 10,
    "start_date": "2025-01-01",
    "end_date": "2025-01-10",
    "status": "DRAFT",
    "google_campaign_id": null,
    "created_at": "2025-12-28T12:48:07.112Z"
  }
]

```


#### 3. Publish Campaign to Google Ads
```
POST /api/campaigns/<campaign_id>/publish
```
Description:
Publishes a DRAFT campaign to Google Ads:

Creates / reuses campaign budget

Creates Google Ads campaign (Paused)

Updates local DB with Google Campaign ID

**Response:**
```json
{
  "message": "Campaign published successfully",
  "google_campaign_id": "23405237018"
}
```
---
## Troubleshooting

**Database Issues:**

1. Ensure backend connects to host db, not localhost.

2. Run migrations on container startup.

3. Verify credentials match docker-compose environment.

**Google Ads Issues:**

1. Developer token must be approved.

2. Customer ID must include dashes (123-456-7890).

3. Billing must be enabled on account.

**CORS Errors:**

1. Ensure Flask-CORS is installed.

2. CORS(app) enabled in app.py.
---
## Author

**Sanchay Awana**

Full Stack Developer



