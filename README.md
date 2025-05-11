# 🔧 UK SME Field Service Lead Generator

This project automates the process of building a lead list of UK-based SME field service companies — specifically in HVAC, plumbing, and lift maintenance — with 5–50 employees.

---

## ✅ Project Goals

- Identify 10–15 qualified companies per industry
- Collect the following info:
  - ✅ Company name
  - ✅ Website
  - ✅ Industry
  - ✅ LinkedIn URL (company)
  - ✅ Estimated number of employees (from LinkedIn)

---

## ⚙️ Tools Used

- **Selenium**: Automates Bing and LinkedIn search using a headless Chrome browser
- **Bing Search**: Used to discover official company websites and LinkedIn pages
- **Regex + HTML Parsing**: Extract employee counts from LinkedIn pages
- **pandas**: Store and clean collected data
- **webdriver-manager**: Automatically downloads and manages the correct ChromeDriver

---

## 📌 Process Overview

1. Perform Bing search queries like:
   - `UK hvac company site:.co.uk`
   - `UK plumbing company site:.co.uk`
   - `UK lift maintenance company site:.co.uk`

2. For each company:
   - Scrape their official website and identify their industry
   - Use a secondary Bing query to find their LinkedIn company page
   - Visit the LinkedIn page and extract estimated employee count via regex

3. Filter the results:
   - Only include companies with **between 5 and 50 employees**

4. Export the final dataset to `phase2_bing_leads_filtered.csv`

---

## 📁 Output Sample

| Company name | Website | Industry | LinkedIn URL | Employees |
|--------------|---------|----------|--------------|-----------|
| HVAC Pros – Professional HVAC Experts | https://hvacpros.co.uk/ | HVAC | https://www.linkedin.com/company/hvacpros | 12 |

---

## 🌟 Bonus (Optional Enrichment)

A simple function (`generate_email`) can generate outreach messages per company using a fixed GPT-style template, ready to integrate with OpenAI API or Mail Merge tools.

```python
def generate_email(company_name, industry):
    return f"""Hi {company_name} team,

We admire your work in the {industry} sector and wanted to connect about possible ways we could support your field operations using AI and automation tools.

Would you be open to a quick chat?

Kind regards,
Luis Rodríguez
"""
