from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.zoomg.ir/archive/?groupings=32349&sort=Newest&publishDate=All&readingTime=All&pageNumber="
OUTPUT_FILE = "zoomg_links.txt"
links = set()

# Set up Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

for i in range(1, 10):  # Loop through pages 1 to 112
    print(f"Scraping page {i}...")
    driver.get(BASE_URL + str(i))
    time.sleep(3)  # Wait for JavaScript to load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all <a> inside <div class="scroll-m-16">
    for div in soup.find_all("div", class_="scroll-m-16"):
        a_tag = div.find("a")
        if a_tag and "href" in a_tag.attrs:
            link = "https://www.zoomg.ir" + a_tag["href"]
            links.add(link)

# Close the browser
driver.quit()

# Save the extracted URLs
with open(OUTPUT_FILE, "w") as f:
    for link in sorted(links):
        f.write(link + "\n")

print(f"Scraping completed! URLs saved in {OUTPUT_FILE}.")
