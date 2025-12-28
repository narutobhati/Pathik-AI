import { useState } from "react";
import { createCampaign } from "../api/campaigns";
import type { CreateCampaignPayload } from "../types/campaign";

interface Props {
  onCreated: () => void;
}

const initialState: CreateCampaignPayload = {
  name: "",
  objective: "TRAFFIC",
  campaign_type: "SEARCH",
  daily_budget: undefined as unknown as number,
  start_date: "",
  end_date: "",
  ad_group_name: "",
  ad_headline: "",
  ad_description: "",
};

export default function CampaignForm({ onCreated }: Props) {
  const [form, setForm] = useState<CreateCampaignPayload>(initialState);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;

    setForm({
    ...form,
    [name]: type === "number" ? Number(value) : value,
  });
};


  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
    await createCampaign(form);
    setForm(initialState);
    onCreated();
    alert("Campaign created successfully");
  } catch (err: any) {
    alert(err.message);
  }
  };

  return (
    <form onSubmit={submit} className="card">
      <h2>Create Campaign</h2>

      <input
        name="name"
        placeholder="Campaign name"
        value={form.name}
        onChange={handleChange}
        required
      />

      <input
        name="daily_budget"
        type="number"
        min={1}
        placeholder="Daily budget in INR "
        value={form.daily_budget}
        onChange={handleChange}
        required
      />

      <label>Start Date</label>
      <input
        name="start_date"
        type="date"
        value={form.start_date}
        onChange={handleChange}
        required
      />

      <label>End Date</label>
      <input
        name="end_date"
        type="date"
        value={form.end_date}
        onChange={handleChange}
        required
      />

      <input
        name="ad_group_name"
        placeholder="Ad group name"
        value={form.ad_group_name}
        onChange={handleChange}
        required
      />

      <input
        name="ad_headline"
        placeholder="Ad headline"
        value={form.ad_headline}
        onChange={handleChange}
        required
      />

      <input
        name="ad_description"
        placeholder="Ad description"
        value={form.ad_description}
        onChange={handleChange}
        required
      />

      <button type="submit">Create Campaign</button>
    </form>
  );
}
