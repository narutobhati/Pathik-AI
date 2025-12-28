import type { Campaign, CreateCampaignPayload } from "../types/campaign";

const API_BASE = "http://localhost:5000/api/campaigns";

export async function fetchCampaigns(): Promise<Campaign[]> {
  const res = await fetch(`${API_BASE}/`);
  return res.json();
}

export async function createCampaign(payload: CreateCampaignPayload) {
  const res = await fetch("http://localhost:5000/api/campaigns/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Something went wrong");
  }

  return data;
}


export async function publishCampaign(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/${id}/publish`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Publish failed");
  }
}
