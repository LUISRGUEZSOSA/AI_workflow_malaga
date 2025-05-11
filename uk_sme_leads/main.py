#!/usr/bin/env python3
# main.py

import time
import re
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ─── Logging ─────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

# ─── Headless Chrome ─────────────────────────────────────────────────────────────
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

# ─── Bing Search ─────────────────────────────────────────────────────────────────
def bing_search(query, max_results=10, pause=2.0):
    driver = get_driver()
    driver.get(f"https://www.bing.com/search?q={query}")
    time.sleep(pause)
    elements = driver.find_elements(By.CSS_SELECTOR, "li.b_algo h2 a")
    links = []
    for e in elements[:max_results]:
        try:
            title = e.text
            href = e.get_attribute("href")
            links.append((title, href))
        except:
            continue
    driver.quit()
    logging.info(f"Query: {query} → {len(links)} results")
    return links

# ─── Scrape Employee Count from LinkedIn ─────────────────────────────────────────
def extract_employee_count(linkedin_url):
    try:
        driver = get_driver()
        driver.get(linkedin_url)
        time.sleep(3)
        html = driver.page_source
        driver.quit()
        match = re.search(r"([0-9,]+)\s+employees", html)
        if match:
            return int(match.group(1).replace(",", ""))
    except Exception as e:
        logging.warning(f"Error extracting employees from LinkedIn: {e}")
    return None

# ─── Main Script ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    services = {
        'HVAC': 'hvac',
        'Plumbing': 'plumbing',
        'Lift Maintenance': 'lift maintenance'
    }

    records = []

    for industry, keyword in services.items():
        query = f"UK {keyword} company site:.co.uk"
        results = bing_search(query, max_results=10)

        for title, website in results:
            if not website:
                continue

            li_query = f"site:linkedin.com/company {title}"
            li_results = bing_search(li_query, max_results=1)
            linkedin_url = li_results[0][1] if li_results else None
            if not linkedin_url:
                continue

            employee_count = extract_employee_count(linkedin_url)
            if employee_count is None or not (5 <= employee_count <= 50):
                continue

            records.append({
                'Company name': title,
                'Website': website,
                'Industry': industry,
                'LinkedIn URL': linkedin_url,
                'Employees': employee_count
            })

    df = pd.DataFrame(records)
    df.drop_duplicates(subset=['Website'], inplace=True)
    df.to_csv("leads_sme.csv", index=False)
    logging.info(f"✅ Saved {len(df)} leads to leads_sme.csv")
