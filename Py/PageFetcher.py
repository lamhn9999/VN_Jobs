import time
import urllib.request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

URL = "https://www.topcv.vn/viec-lam/chuyen-vien-kinh-doanh-phan-mem-giao-duc-edtech/1713847.html?ta_source=JobSearchList_LinkDetail&u_sr_id=4O2v40O3Au2FINPzCFcHBUIJFjUxpXd6B3fJUgas_1749008499"
#URL = "https://itviec.com/it-jobs?job_selected=senior-fullstack-developer-java-reactjs-vuejs-bolt-tech-2008&page=51"

Request = urllib.request.Request (
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)
while(True):
    try:
        with urllib.request.urlopen(Request) as Response:
            Soup = BeautifulSoup(Response.read().decode(), "html.parser")
        with open(f"Py/FatherPage.html", "w") as f:
            f.write(Soup.prettify())
        break
    except urllib.error.URLError as e:
        print(f"    URL Error: {e.reason}")
        time.sleep(2)

