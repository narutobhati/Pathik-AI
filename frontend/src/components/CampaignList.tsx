import { useState } from "react";
import type { Campaign } from "../types/campaign";
import { publishCampaign } from "../api/campaigns";

interface Props {
  campaigns: Campaign[];
  refresh: () => void;
}

export default function CampaignList({ campaigns, refresh }: Props) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [publishingId, setPublishingId] = useState<string | null>(null);

  const toggle = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const publish = async (id: string) => {
    try {
      setPublishingId(id); //  lock button
      await publishCampaign(id);
      await refresh();
    } finally {
      setPublishingId(null); // unlock
    }
  };

  return (
    <div className="card">
      <h2>Campaigns</h2>

      {campaigns.map((c) => (
        <div key={c.id} className="campaign-item">
       
          <div className="campaign-header">
            <div>
              <strong>{c.name}</strong>
              <div className="muted">Status: {c.status}</div>
            </div>

            <div className="actions">
              {c.status === "DRAFT" && (
                <button
                  onClick={() => publish(c.id)}
                  disabled={publishingId === c.id}
                >
                  {publishingId === c.id ? "Publishing..." : "Publish"}
                </button>
              )}

              <button onClick={() => toggle(c.id)}>
                {expandedId === c.id ? "Hide" : "Details"}
              </button>
            </div>
          </div>

          {expandedId === c.id && (
            <div className="campaign-details">
              <div><b>Objective:</b> {c.objective}</div>
              <div><b>Type:</b> {c.campaign_type}</div>
              <div><b>Daily Budget:</b> ₹{c.daily_budget}</div>
              <div><b>Start:</b> {c.start_date}</div>
              <div><b>End:</b> {c.end_date}</div>

              {c.google_campaign_id && (
                <div>
                  <b>Google Campaign ID:</b> {c.google_campaign_id}
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
