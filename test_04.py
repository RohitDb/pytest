import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def browser():
    # Path to the ChromeDriver executable
    chromedriver_path = 'path/to/chromedriver'

    # Initialize Chrome WebDriver
    # Initialize Chrome WebDriver with the configured options
    service = Service(executable_path=chromedriver_path)

    # Initialize Chrome WebDriver with the Service
    driver = webdriver.Chrome(service=service)
    

    # Set up any additional configurations for the driver

    # Return the driver instance
    yield driver

    # Quit the driver after the test
    driver.quit()

def test_amazon_search(browser):
    # Open Amazon website
    try:    
        browser.get('https://www.amazon.com')

        # Find the search input field
        search_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'twotabsearchtextbox')))

        # Enter the search query
        search_query = 'samsung s23 ultra'
        search_input.send_keys(search_query)

        # Submit the search
        search_input.submit()

        # Assert that search results are displayed
        #assert 'Amazon.com : Iphone14' in browser.title

        first_result = browser.find_element(By.CSS_SELECTOR, 'span.a-size-medium.a-color-base.a-text-normal')
        first_result_text = first_result.text
        #assert  search_query in first_result_text.lower()

        first_result_price = browser.find_element(By.CSS_SELECTOR, 'span.a-price')

        first_result_price_text = first_result_price.text
        assert first_result_price_text
        print("Cost",first_result_price_text)


    # Assert that the price has a currency symbol
        currency_symbols = ['$', '€', '£']
        currency_symbol = None
        for symbol in currency_symbols:
          if symbol in first_result_price_text:
           currency_symbol = symbol
           break

        assert currency_symbol in first_result_price_text
        print("price is ",currency_symbol)

        # Assert that the price is a number
        price_number = first_result_price_text.replace(',', '').replace('.', '').replace(' ', '')[1:]
        assert price_number>"0"
        print("Price greater then 0")

        
        
        first_result.click()

        cost_on_click= browser.find_element(By.CLASS_NAME, 'a-price-whole')
        cost_on_click=cost_on_click.text
        cost_on_click=cost_on_click.replace(',', '').replace('.', '').replace(' ', '')
        assert  cost_on_click==price_number.split('\n')[0]
        print("Price is same as mentioned outside",cost_on_click)

        table_element = browser.find_element(By.ID, 'productDetails_detailBullets_sections1')

        rows = table_element.find_elements(By.TAG_NAME, 'tr')

# Check if the table has at least 9 rows
        if len(rows) >= 13:
    # Fetch the 9th row (index 8) from the table
         weight_row = rows[12]

    # Extract the weight value from the corresponding cell
         weight_cell = weight_row.find_element(By.TAG_NAME, 'td')
         weight_text = weight_cell.text

        #weight_element = weight_row.find_element(By.CLASS_NAME, 'a-size-base prodDetAttrValue')
        #weight_text = weight_element.text
        weight_in_grams = float(weight_text.split()[0])  # Extract the numeric weight value
        print(weight_in_grams,"weight is greather then 0")
        assert weight_in_grams > 0  
        
         
        #first_result.click()

    except NoSuchWindowException:
        print("Window closed or refreshed before test completion.")
   

    #if __name__ == '__main__':
        # pytest.main(['-v', '--html=report.html', '--capture=sys'])

    
# Run the tests
pytest.main()
