# bonus/enrich_company_info.py

import pandas as pd

def tag_industry(company_name, website):
    name = company_name.lower()
    if "bathroom" in name or "plumb" in name:
        return "Plumbing - Domestic"
    elif "hvac" in name or "climate" in name:
        return "HVAC - Commercial"
    elif "lift" in name or "elevator" in name:
        return "Lift Maintenance"
    else:
        return "General Field Services"

def mock_founder(company_name):
    return f"{company_name.split()[0]} Founder (Mocked)"

df = pd.read_csv("leads_sme.csv")
df["Industry Tag"] = df.apply(lambda x: tag_industry(x["Company name"], x["Website"]), axis=1)
df["Founder"] = df["Company name"].apply(mock_founder)

df.to_csv("bonus/bonus_1_enriched_leads.csv", index=False)
print("✅ Enriched file saved to bonus/enriched_leads.csv")
