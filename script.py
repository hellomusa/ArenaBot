from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv

chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.op.gg/modes/arena?hl=en_US")

table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "table"))
)

header_row = table.find_element(By.TAG_NAME, "thead").find_element(By.TAG_NAME, "tr")

win_rate_header = None
for th in header_row.find_elements(By.TAG_NAME, "th"):
    if th.text.strip().lower() == "win rate":
        win_rate_header = th
        break

if win_rate_header:
    win_rate_header.click()
    time.sleep(2)
else:
    print("Could not find 'Win rate' header")

tbody = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "tbody"))
)

for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

rows = tbody.find_elements(By.TAG_NAME, "tr")

champion_data = []

for row in rows[:50]:  # get top 50 champions
    tds = row.find_elements(By.TAG_NAME, "td")
    if len(tds) >= 4:
        champion_name = tds[1].text
        win_rate = tds[3].text
        champion_data.append((champion_name, win_rate))

driver.quit()

csv_filename = "arena_champions_by_winrate.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Champion", "Win Rate"])
    csv_writer.writerows(champion_data)

print(f"Data has been saved to {csv_filename}")