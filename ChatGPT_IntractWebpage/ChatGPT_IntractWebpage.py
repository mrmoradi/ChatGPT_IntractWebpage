from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Path to your WebDriver executable
driver_path = r'C:/Users/M/Downloads/Compressed/chromedriver-win64/chromedriver-win64/chromedriver.exe'
#driver_path = 'C:/Users/M/Downloads/Compressed/chromedriver-win64/chromedriver-win64'

#"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 -- "%1"

chrome_debugging_port = 9222  # Make sure this matches the port used above
chrome_profile_path = "C:/Users/M/AppData/Local/Google/Chrome/User Data"
#chrome_profile_path = "C:/Users/M/AppData/Local/Google/Chrome/User Data/Default"


service = Service(executable_path=driver_path)
options = Options()
options.add_argument(f"user-data-dir={chrome_profile_path}")
options.add_experimental_option("debuggerAddress", f"localhost:{chrome_debugging_port}")

# Initialize the WebDriver
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)


#driver.execute_script("window.open('');")
time.sleep(.5)
#driver = webdriver.Chrome(executable_path=driver_path)
#driver.switch_to.window(driver.window_handles[-1])
#driver.get("https://www.google.com")


# Open the ChatGPT page
#driver.get('https://chatgpt.com/c/d3408c8a-2647-4665-97ed-c6adedbfc186')

# Wait for the page to load
time.sleep(.5)

new_chat= driver.find_element(By.CSS_SELECTOR,f'div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.flex-shrink-0.overflow-x-hidden.bg-token-sidebar-surface-primary > div > div > div > div > nav > div.flex-col.flex-1.transition-opacity.duration-500.-mr-2.pr-2.overflow-y-auto > div.sticky.left-0.right-0.top-0.z-20.bg-token-sidebar-surface-primary.pt-3\.5.juice\:static.juice\:pt-0 > div > a')
new_chat.click()
# Find the chat input box (you may need to inspect the page to get the correct selector)
chat_input = driver.find_element(By.ID,'prompt-textarea')

# Send a message
chat_input.send_keys('I have some questions.')
chat_input.send_keys(Keys.RETURN)

# Wait for the response (adjust the sleep time as needed)
#time.sleep(10)


# Wait for the <p> element to be present
try:
    # Replace the CSS selector with the correct one for your use case
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'p'))
    )
    
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p'))
    )
    # Get the text content of the element
    response = element.text

    # Print the response
    print(response)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the driver
    driver.quit()
    
print(driver.page_source)
