import requests
from bs4 import BeautifulSoup

def scrape_career_page_links(companies, keywords, location, radius):
    job_results = []
    for company in companies:
        try:
            careers_url = f"https://careers.{company.lower().replace(' ', '')}.com"
            response = requests.get(careers_url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    href = link['href']
                    if any(kw.lower() in href.lower() for kw in keywords):
                        full_link = href if href.startswith('http') else f"{careers_url}/{href}"
                        job_results.append({
                            "company": company,
                            "job_title": link.get_text(strip=True),
                            "location": location,
                            "url": full_link
                        })
        except Exception as e:
            print(f"Failed to scrape {company}: {e}")
    return job_results