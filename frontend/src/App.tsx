import { useEffect, useState } from "react";
import { fetchCampaigns } from "./api/campaigns";
import type { Campaign } from "./types/campaign";
import CampaignForm from "./components/CampaignForm";
import CampaignList from "./components/CampaignList";

export default function App() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);

  const load = async () => {
    const data = await fetchCampaigns();
    setCampaigns(data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="container">
      <h1>Pathik AI – Campaign Manager</h1>

      <div className="grid">
        <CampaignForm onCreated={load} />
        <CampaignList campaigns={campaigns} refresh={load} />
      </div>
    </div>
  );
}
