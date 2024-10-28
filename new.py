from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

driver = webdriver.Edge()
driver.get("https://foundersuite.com/app/log_in")
time.sleep(1)

login_page = driver.find_element(By.CLASS_NAME, "css-6hs5yk")

email = login_page.find_element(By.NAME, "email")
email.send_keys("infiniagaming@gmail.com")

password = login_page.find_element(By.NAME, "password")
password.send_keys("newpass@123")

driver.execute_script("arguments[0].click();", login_page.find_element(By.CLASS_NAME, "css-zlgwmj"))

time.sleep(4)
driver.get("https://foundersuite.com/app/investor_database/firms/precursor-ventures")
time.sleep(6)

data = driver.find_element(By.CLASS_NAME, "css-spwthg")
name = data.find_element(By.TAG_NAME, "h1").text
address = data.find_element(By.TAG_NAME, "span").text

investor = driver.find_element(By.CLASS_NAME, "css-61ri6a")
rating = investor.find_element(By.CLASS_NAME, "css-njr90m").text
investor_type = investor.find_element(By.CLASS_NAME, "css-2ddsc7").text
sweet_spot_text = investor.find_element(By.CLASS_NAME, "css-18exx4i").text
sweet_spot = sweet_spot_text.split("\n")[-1]

industry_focus = investor.find_element(By.CLASS_NAME, "css-kzz0").text
formatted_industry_focus = " ".join(industry_focus.split("\n"))
desc = investor.find_element(By.CLASS_NAME, "css-1rrf6f8").text
contact_elements = driver.find_elements(By.CSS_SELECTOR, ".css-1a1u6mc li[data-testid='contact-person']")

more_inf = []
infos = investor.find_elements(By.CLASS_NAME, "css-1wi9cm3")

for info in infos:
    header = info.find_element(By.TAG_NAME, "header").text
    ul_elements = info.find_elements(By.TAG_NAME, "ul")
    if ul_elements:
        items = ul_elements[0].find_elements(By.TAG_NAME, "li")
        items_text = ', '.join(item.text.strip() for item in items)
        more_inf.append(f"{header}: {items_text}") 
    else:
        span_elements = info.find_elements(By.TAG_NAME, "span")
        for span in span_elements:
            more_inf.append(f"{header}: {span.text.strip()}") 


output_data = {
    "Name": name,
    "Address": address,
    "Rating": rating,
    "Type": investor_type,
    "Sweet Spot": sweet_spot,
    "More Info": more_inf,
    "Industry Focus": formatted_industry_focus,
    "Description": desc,
    "Contacts": []
}

for contact in contact_elements:
    name_person = contact.find_element(By.CSS_SELECTOR, ".css-piu05e").text
    position = contact.find_element(By.CSS_SELECTOR, ".position").text
    email_elements = contact.find_elements(By.CSS_SELECTOR, "[font-size='150']")
    email = email_elements[0].text if email_elements else "No email provided"
    output_data["Contacts"].append({
        "Name": name_person,
        "Position": position,
        "Email": email
    })

with open("investor_data.json", "w") as json_file:
    json.dump(output_data, json_file, indent=4)

print("JSON File saved successfully.")

time.sleep(5)
driver.quit()
