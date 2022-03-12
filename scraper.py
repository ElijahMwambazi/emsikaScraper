import os
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

print(
    "======================================= START ======================================="
)
print("Ensure all instances of 'Data.csv' are closed to prevent data lose.")

# Initialize logger.
logging.basicConfig(
    filename="log.txt", level=logging.DEBUG, format="%(asctime)s - %(message)s"
)
# logging.disable(logging.CRITICAL) # <====== REMEMBER TO COMMENT THIS.

# Get location of working directory.
working_dir = os.getcwd()

# Create empty list variables that will contain scraped data.
product_types = []
categories = []
product_types_col = []
categories_col = []
product_names_col = []
prices_col = []
suppliers_col = []
verification_status_col = []

# Declare chromedriver options.
chrome_options = webdriver.ChromeOptions()

window_vis = int(
    input(" Press 1: To show window.\n Press 2: To hide window.\n")
)  # Hide window option

if window_vis != (1 or 2):
    raise Exception("You didn't pick either one of the specified options...")

try:
    if window_vis == 1:
        pass
    elif window_vis == 2:
        chrome_options.add_argument("--headless")
except Exception as e:
    print(e)

chrome_options.add_argument("--no-zygote")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-breakpad")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-certificate-errors-spki-list")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Set desired capabilities to ignore SSL stuff
desired_capabilities = chrome_options.to_capabilities()
desired_capabilities["acceptInsecureCerts"] = True
desired_capabilities["acceptSslCerts"] = True

# Get th e start time.
start_time = time.process_time()

# Set up Chromedriver.
url = "https://www.emsika.com/"
driver_location = os.path.join(working_dir, r"chromedriver.exe")

driver = webdriver.Chrome(
    driver_location,
    options=chrome_options,
    desired_capabilities=desired_capabilities,
)

# Run Chromedriver
logging.debug("Loading chromedriver...")
try:
    driver.maximize_window()
    logging.debug("Loading URL...")
    driver.get(url)
except (TimeoutException):
    logging.error("Took too long to load webpage. Check your internet connection...")

# Locate Website element containing product types.
try:
    logging.debug("Attempting to locate product bar element...")
    product_bar = driver.find_element(By.CSS_SELECTOR, ".z-20")
    products = product_bar.find_elements_by_tag_name("li")
    logging.debug("Product bar element located...")

    # Loop through product types website elements to obtain text.
    for item in products:
        logging.debug("Getting elements from product bar...")
        if item.text == None
        product_type = item.text
    # Filter out empty strings from list.
    product_types = list(filter(None, product_types))

    # Iterate through each product types website element, scraping out categories, product names, suppliers, prices and verification status.
    for product_type in product_types:
        print("Opening product.")
        product_bar.find_element(By.LINK_TEXT, product_type).click()
        print("product openned.")
        time.sleep(5)
        # Get category element text.
        try:
            print("Locating category element.")
            categories_bar = driver.find_element(By.CSS_SELECTOR, ".px-1.pb-4")
            print("Category element located.")
            categories_parent = categories_bar.find_elements_by_tag_name("a")
            categories_child = categories_bar.find_elements_by_tag_name("span")
            print("Categories parent and child located.")

            categories_whole = []
            categories_end = []

            for element in categories_parent:
                categories_whole.append(element.text)
            for element in categories_child:
                categories_end.append(element.text)

            # Remove unwanted text from categories_whole.
            for whole, end in zip(categories_whole, categories_end):
                _ = whole.replace(end, "")
                stripped_category = _.rstrip()
                categories.append(stripped_category)
                print("Categories child and parent separated.")

                # Get product name, supplier, price and verification status for individual category.
                try:
                    for category in categories:
                        current_count = True
                        max_count = False

                        # Product page navigation goes here.
                        while current_count != max_count:
                            print("Clicking on a category.")
                            product_bar.find_element(By.LINK_TEXT, category).click()
                            time.sleep(5)

                            print("Getting catgory element text.")
                            category_element = driver.find_elements_by_class_name(
                                "m-2 bg- shadow-lg px-2 py-2"
                            ).text
                            print("Getting product name element text.")
                            product_name = category_element.find_elements_by_tag_name(
                                "h1"
                            ).text
                            print("Getting price element text.")
                            price = category_element.find_element_by_class_name(
                                "title-font font-medium text-2xl text-gray-900"
                            ).text
                            print("Getting supplier element text.")
                            supplier = category_element.find_elements_by_class_name(
                                "text-gray-600 font-bold ml-3"
                            ).text
                            print("Getting verified element text.")
                            verified = category_element.find_elements_by_link_text(
                                "Verified"
                            ).text

                            # Append Respective string to respective list.
                            print("Appending to lists.")
                            product_types_col.append(product_type)
                            categories_col.append(category)
                            product_names_col.append(product_name)
                            prices_col.append(price)
                            suppliers_col.append(supplier)
                            verification_status_col.append(verified)
                            print("Appended to lists was successfull.")

                            try:
                                item_counter = driver.find_element_by_css_selector(
                                    "p[class='text-sm text-gray-700 leading-5']"
                                )
                                current_count = (
                                    item_counter.find_element_by_css_selector(
                                        "body div p span:nth-child(4)"
                                    ).text
                                )
                                max_count = item_counter.find_element_by_css_selector(
                                    "body div p span:nth-child(6)"
                                ).text
                                print("Going to next page.")

                                int(current_count)
                                int(max_count)
                            except NoSuchElementException:
                                break

                            # Toggal next page button.
                            try:
                                driver.find_element_by_xpath(
                                    "//button[@aria-label='Next &raquo;']"
                                ).click()
                            except NoSuchElementException:
                                break
                    else:
                        break
                except NoSuchElementException:
                    pass
        except NoSuchElementException:
            pass

except Exception as e:
    print(e)

finally:
    driver.quit()

# Create dataframe
parsed_data = []
parsed_data.append(
    product_names_col,
    categories_col,
    product_names_col,
    prices_col,
    suppliers_col,
    verification_status_col,
)

column_names = [
    "ProductType",
    "Category",
    "ProductName",
    "Price",
    "Supplier",
    "VerificationStatus",
]

data_frame = pd.DataFrame(parsed_data, columns=column_names)
# Convert dataframe to csv file and save it to working directory.

print(
    "======================================== END ========================================"
)
