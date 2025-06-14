import time
import urllib.request
import pandas 
from bs4 import BeautifulSoup

MainURL = "https://itviec.com/it-jobs?job_selected=software-engineer-net-wpf-english-speaking-eurofins-gsc-it-vietnam-company-limited-3226"
foundJobs = []
try:
    Results = pandas.read_csv("Data/Jobs_ITViec.csv")
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
    for JobTag in Soup.find_all('div', class_ = 'ipx-4 ipx-xl-3'):
        JobTitle = JobTag.find('h3', class_ = 'imt-3 text-break')
        Company = JobTag.find('span', class_ = 'ims-2 small-text text-hover-underline').find('a')
        if JobTitle:
            foundJobs.append({"Job Title" : JobTitle.contents[0].strip(), "Job Link" : JobTitle.get('data-url'), "Company" : Company.contents[0] if Company else None})

def scrape():
    nextURL = MainURL
    for i in range(0, 100):
        Soup = fetchPage(nextURL, i+1)
        getJobTitles(Soup, i+1)
        try:
            nextURL = Soup.find('link', rel = 'next').get('href')
        except:
            break
        time.sleep(1)

scrape()
Results = pandas.DataFrame(foundJobs)
Results = pandas.concat([pandas.DataFrame(foundJobs), Results]).reset_index(drop=True)
# Results = Results.loc[:, ~Results.columns.str.contains('^Unnamed')]
Results.to_csv("Data/Jobs_ITViec.csv")