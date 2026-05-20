from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import sys

def fetch_etfs_selenium():
    """
    Fetches a list of European Accumulating ETFs from justETF.com using Selenium.
    Has fallback to Edge if Chrome is not available (implied usage, simplified for now).
    """
    print("Initializing Selenium WebDriver...")
    
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") # Modern headless mode
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    # Masking automation (basic)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Failed to initialize Chrome Driver: {e}")
        print("Please ensure Google Chrome is installed.")
        return

    try:
        # URL with filters pre-applied:
        # Region: Europe
        # Distribution Policy: Accumulating
        url = "https://www.justetf.com/en/find-etf.html?groupField=index&region=Europe&distributionPolicy=accumulation"
        print(f"Navigating to {url}...")
        driver.get(url)

        wait = WebDriverWait(driver, 20)

        # 1. Handle Cookie Consent (if it appears)
        try:
            print("Checking for cookie banner...")
            # Common selectors for justetf cookie banner (adjust if needed)
            # Typically looks like a generic 'Accept' button or specific ID
            cookie_accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "cybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))
            cookie_accept_btn.click()
            print("Cookie banner accepted.")
            time.sleep(2) # Wait for overlay to disappear
        except TimeoutException:
            print("No cookie banner found or already accepted.")
        except Exception:
            # Maybe it's a different button or didn't appear
            pass

        # 2. Wait for ETF Table to load
        print("Waiting for ETF table...")
        # look for a row in the table
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))

        # 3. Scrape Data
        # For simplicity, we grab the current page. To get ALL, we would need to handle pagination.
        # Pagination usually has a 'next' button or a 'show all' option if available.
        # Let's try to scroll down to trigger lazy load if it exists, or just read the first page.
        # JustETF usually uses pagination.
        
        etfs = []
        
        # Determine number of pages or just iterate 'Next'
        page_num = 1
        max_pages = 5 # Limit for demo purposes, assume user can increase
        
        while page_num <= max_pages:
            print(f"Scraping page {page_num}...")
            
            # Re-locate rows to avoid stale element
            rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            
            for row in rows:
                try:
                    # Specific column indices depend on the default view.
                    # Usually: Name (contains link/Ticker), ISIN (inside name or separate), Currency, Fund Size, TER
                    
                    # Name is often in the column with class 'name' or just the first major text
                    name_el = row.find_element(By.CSS_SELECTOR, "td.name a")
                    name = name_el.text
                    link = name_el.get_attribute("href")
                    
                    # ISIN is often in a specific span or attributes, or part of the link
                    # link usually looks like /en/etf-profile.html?isin=IE00B4L5Y983
                    isin = ""
                    if "isin=" in link:
                        isin = link.split("isin=")[1].split("&")[0]
                    
                    # Columns: 
                    # We can iterate all 'td's but finding by class is safer if they exist.
                    # JustETF table columns are dynamic.
                    # Let's clean text from the whole row as fallback
                    text_content = row.text.split('\n')
                    # Usually formatted somewhat consistently.
                    
                    etfs.append({
                        "Name": name,
                        "ISIN": isin,
                        "Link": link
                    })
                except Exception as row_e:
                    continue # Skip malformed rows
            
            # Check for 'Next' button
            try:
                # Selector for next page navigation
                # Often a generic '>' icon or 'li.next a'
                # Inspecting justetf typical pagination: <li class="next"><a ...></a></li>
                next_btn = driver.find_elements(By.CSS_SELECTOR, "a.next")
                if next_btn and next_btn[0].is_displayed() and "disabled" not in next_btn[0].get_attribute("class"):
                    # Click might be intercepted by ads or overlays, scroll to it
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_btn[0])
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", next_btn[0])
                    time.sleep(3) # Wait for page load
                    page_num += 1
                else:
                    print("No more pages.")
                    break
            except Exception as nav_e:
                print(f"Pagination stopped: {nav_e}")
                break

        print(f"Scraped {len(etfs)} ETFs.")
        
        # Save to CSV
        if etfs:
            df = pd.DataFrame(etfs)
            df.to_csv("european_accumulating_etfs.csv", index=False)
            print("Saved to european_accumulating_etfs.csv")
            print(df.head())
        else:
            print("No data found.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Save screenshot for debugging
        try:
            driver.save_screenshot("debug_error.png")
            print("Saved screenshot to debug_error.png")
        except:
            pass
    finally:
        print("Closing driver...")
        driver.quit()

if __name__ == "__main__":
    fetch_etfs_selenium()
