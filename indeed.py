import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'    
    
def extract_indeed_pages():
    html = requests.get(URL)
    soup = BeautifulSoup(html.text, 'html.parser')
    pagination = soup.find('div', {'class':'pagination'})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1] # 마지막 페이지
    return max_page

def extract_jobs(html):
    title = html.find('div', {'class': 'title'}).find('a')['title']
    company = html.find('span', {'class': 'company'})
    company_anchor = company.find('a')
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = html.find('div', {'class': 'recJobLoc'})['data-re-loc']
    job_id = html['data-jk']
    return {
        'title': title, 
        'company': company, 
        'location':location,
        'link':f'https://www.indeed.com/viewjob?jk={job_id}'
    }

def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping page {page}')
        result = requests.get(f'{URL}&start={page*LIMIT}')
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})
        for result in results:
            job = extract_jobs(result)
            jobs.append(job)
    return jobs
        
