import time
import urllib.request
import pandas 
from bs4 import BeautifulSoup

MainURL = "https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-tai-ha-noi-l1cr257?exp=2&type_keyword=1&sba=1&category_family=r257&locations=l1"
foundJobs = []
try:
    Results = pandas.read_csv("Data/Jobs_TopCV.csv")
except pandas.errors.EmptyDataError:
    Results = pandas.DataFrame()

def fetchPage(URL, PageIndex):
    if URL == "":
        return BeautifulSoup("", "html.parser")
    Request = urllib.request.Request (
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    print(f"Fetching Page_{PageIndex}")
    while(True):
        try:
            with urllib.request.urlopen(Request) as Response:
                Soup = BeautifulSoup(Response.read().decode(), "html.parser")
            break
        except urllib.error.URLError as e:
            print(f"    URL Error: {e.reason}")
            time.sleep(2)
    return Soup

def getJobTitles(Soup, PageIndex):
    for JobTag in Soup.find_all('div', class_ = 'avatar'):
        Anchor = JobTag.find('a')
        if Anchor and Anchor.get('aria-label'):
            foundJobs.append({"Job Title" : Anchor['aria-label'], "Job Link" : Anchor.get('href'), "Company" : Anchor.find('img').get('alt')})

def scrape():
    nextURL = MainURL
    for i in range(0, 100):
        Soup = fetchPage(nextURL, i+1)
        getJobTitles(Soup, i+1)
        try:
            nextURL = Soup.find('a', attrs={"aria-label" : lambda s: s and s.startswith("Next")}).get('data-href')
        except:
            break
        time.sleep(1)

scrape()
Results = pandas.concat([pandas.DataFrame(foundJobs), Results]).reset_index(drop=True)
Results = Results.loc[:, ~Results.columns.str.contains('^Unnamed')]
Results.to_csv("Data/Jobs_TopCV.csv")