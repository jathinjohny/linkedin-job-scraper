import datetime
import os
from selenium.webdriver.common.by import By
import time
import csv
from selenium import webdriver
# import undetected_chromedriver as uc
from datetime import datetime

# Initialize the Chrome driver
# driver = uc.Chrome()
driver = webdriver.Chrome()


def openBrowser(page):
    driver.get(f"https://www.linkedin.com/jobs/search/?currentJobId=4197598928&f_TPR=r86400&geoId=104738515&keywords=artificial%20intelligence%20ai&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&start={page}")
    time.sleep(5)  # Wait for the page to load

    try:
        driver.find_element(By.CSS_SELECTOR, '#base-contextual-sign-in-modal > div > section > div > div > div > div.sign-in-modal > button').click()
        time.sleep(2)  # Wait for the sign-in modal to load

        username_field = driver.find_element(By.CSS_SELECTOR, "#base-sign-in-modal_session_key")  # Replace with actual field name
        password_field = driver.find_element(By.CSS_SELECTOR, "#base-sign-in-modal_session_password")  # Replace with actual field name

        elem = driver.find_element(By.CSS_SELECTOR, "#base-sign-in-modal > div > section > div > div > form > div.flex.justify-between.sign-in-form__footer--full-width > button")  # Replace with actual button class name
        username_field.send_keys("jathinpjohny@gmail.com")  # Enter username
        password_field.send_keys("Jathin@125johny")  # Enter password
        elem.click()
        time.sleep(15)
    except:
        print("bypassed the login page or Something went wrong while opening the page.")
   


    # Locate the first scrollable element (replace with the correct selector for your case)
    scrollable_element = driver.find_element(By.CSS_SELECTOR, '#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > div')

    scroll_job_list(scrollable_element)  # Scroll the job list to load all job cards



def scroll_job_list(scrollable_element):
    """Scroll the job list container gradually to load all job cards."""
    last_height = 0

    while True:
        # Scroll down by a small amount
        driver.execute_script("arguments[0].scrollTop += 300", scrollable_element)
        time.sleep(1)  # Wait for the content to load

        # Get the current scroll height
        new_height = driver.execute_script("return arguments[0].scrollTop", scrollable_element)

        # Break if no new content is loaded
        if new_height == last_height:
            print("Reached the bottom of the job list.")
            break

        last_height = new_height

# Extract job details
def extractDetails():
    # jobList=driver.fing_element(By.CSS_SELECTOR, "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > div > ul")
    # jobList=driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/ul')
    


    """Extract job details from the current page starting from a specific index."""
    job_cards = driver.find_elements(By.CLASS_NAME, "job-card-list__entity-lockup")
    print(f"Total jobs found on page: {len(job_cards)}")
    
    job_list = []
    
    for count, job in enumerate(job_cards, start=1):
        print(f"Extracting job {len(all_jobs)+count}...")
       
        try:
            
            elem = job.find_element(By.CLASS_NAME, "disabled")
            elem.click()
            time.sleep(5)  # Wait for job details to load

            link = elem.get_attribute("href")
            job_title = elem.text
            # # Create an ActionChains object
            # actions = ActionChains(driver)

            # # Perform a double-click on the element
            # actions.double_click(elem).perform()

        except:
            job_title = "null"
            link = "null"

       

        # try:
        #     job_title = job.find_element(By.CLASS_NAME, "base-search-card__title").text
        # except:
        #     job_title = "null"

        try:
            company_name = job.find_element(By.CLASS_NAME, 'artdeco-entity-lockup__subtitle').text
        except:
            company_name = "null"
        try:
            location = job.find_element(By.CLASS_NAME, "artdeco-entity-lockup__caption").text
        except:
            location = "null"
        
        try:
            # Locate the <time> element
            datetime_value=driver.find_element(By.CSS_SELECTOR, "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.jobs-search__job-details--container > div > div.job-view-layout.jobs-details > div:nth-child(1) > div > div:nth-child(1) > div > div.relative.job-details-jobs-unified-top-card__container--two-pane > div > div.job-details-jobs-unified-top-card__primary-description-container > div > span:nth-child(3)").text
        except:
            datetime_value = "null"
        




        try:
            # Locate the button containing work mode and job type
            preference_button = driver.find_element(By.CLASS_NAME, "job-details-preferences-and-skills")
    
            # Locate all the pills inside the button
            preference_pills = preference_button.find_elements(By.CLASS_NAME, "job-details-preferences-and-skills__pill")
    
            # Initialize default values
            workMode = "null"
            jobType = "null"
    
            # Loop through the pills and identify work mode and job type based on their text
            for pill in preference_pills:
                text = pill.text.strip().lower()
                if "hybrid" in text or "on-site" in text or "remote" in text:
                    workMode = text.capitalize()  # Extract work mode
                elif "full-time" in text or "part-time" in text or "contract" in text:
                    jobType = text.capitalize()  # Extract job type
        except:
            workMode = "null"
            jobType = "null"

        try:
            jobDescription = driver.find_element(By.CSS_SELECTOR, "#job-details > div").text
        except:
            jobDescription = "null"

        try:
            # Locate the industry element
            industry_element = driver.find_element(By.CSS_SELECTOR, "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details > div > div.jobs-search__job-details--container > div > div.job-view-layout.jobs-details > div:nth-child(1) > div > section > section > div.jobs-company__box > div.t-14.mt5")
    
            # Extract the text content of the industry element
            industry = industry_element.text.strip()
        except Exception as e:
            industry = "null"  # Default value if not found
            print(f"Error extracting industry: {e}")

        # Print the extracted industry value
        print(f"Title: {job_title}\nCompany: {company_name}\nLocation: {location}\npost Date: {datetime_value}\nwork Mode: {workMode}\nJob Type: {jobType}\njob Description: {jobDescription}\nindustry: {industry}\nLink: {link}")
        print("-" * 80)
        
        job_list.append({
            "Job Title": job_title,
            "Company Name": company_name,
            "Location": location,
            "Post Date": datetime_value,
            "Work Mode": workMode,
            "Job Type": jobType,
            "Industries": industry,
            "Job Description": jobDescription,
            "Link": link
        })
    
    return job_list


# Number of pages to scrape
number_of_pages = 40
all_jobs = []

for i in range(29,number_of_pages):
    try:
        page = i * 25
        print(f"\n---------- Scraping page {i+1} ----------")
        openBrowser(page)
        # jobs = extractDetails()
        # all_jobs.extend(jobs)
    except:
        break

# Ensure the folder exists
folder_name = "weekly linkedin data"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)  # Create the folder if it doesn't exist



# Generate a unique filename with the current date and time
today = datetime.now().date() # Format the date as YYYY-MM-DD
current_time = datetime.now().strftime("%H:%M:%S")  # Add time to make the filename unique
csv_filename = os.path.join(folder_name, f"linkedin_jobs_{today}_{current_time}.csv")

# Open file in write mode ('w') to create a new file every time
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=all_jobs[0].keys())
    
    # Write the header
    writer.writeheader()
    
    # Write the job data
    writer.writerows(all_jobs)

print(f"Scraped job data saved to {csv_filename}")

driver.close()