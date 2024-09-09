from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pyperclip
import time
import os
import sys



class ChatGPTClass:

    response_id_list = []
    response_list = []
    tabs_window_handles = []
    final_copy_text_tags_id_list = []
    copy_code_tags_list_id = []
    code_list = []
    # Define the spinner characters
    spinner = ["-", "\\", "|", "/"]
    
    
                    
    chrome_debugging_port = 9222  # Make sure this matches the port used above
    chrome_profile_path = "C:/Users/M/AppData/Local/Google/Chrome/User Data"

    # "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 -- "%1"
    

    driver_path = r"C:/Users/M/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"


    def __init__(self):

        self.service = Service(executable_path=self.driver_path)
        self.options = Options()
        self.options.add_argument("--remote-debugging-port=9222")
        self.options.add_argument(f"user-data-dir={self.chrome_profile_path}")
        
        self.options.add_argument("--log-level=5")  # Set logging level
        

        # Disable the "Chrome is being controlled by automated software" message
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Disable the automation extension to prevent detection
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Initialize the WebDriver
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def start_chat_load(self):
        
        self.driver.get("https://chat.openai.com")
        time.sleep(2)
        self.driver.refresh()
        time.sleep(5)


        self.driver.switch_to.window(self.driver.window_handles[-1])

        self.check_puzzle()


        new_chat = self.driver.find_element(
            By.CSS_SELECTOR,
            f"body > div.relative.flex.h-full.w-full.overflow-hidden.transition-colors.z-0 > div.flex-shrink-0.overflow-x-hidden.bg-token-sidebar-surface-primary > div > div > div > nav > div.flex-col.flex-1.transition-opacity.duration-500.relative.-mr-2.pr-2.overflow-y-auto > div.bg-token-sidebar-surface-primary.pt-0 > div > a"
        )
        new_chat.click()
        time.sleep(3)

        # Store the current URL
        current_url = self.driver.current_url

        self.driver.execute_script("window.open('');")
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(current_url)
        # Refresh the new tab to apply the cookies
        time.sleep(2)
        self.driver.refresh()
        time.sleep(2)

        self.driver.switch_to.window(self.driver.window_handles[-2])

        self.tabs_window_handles = self.driver.window_handles


    # Function to display the spinner
    def check_puzzle(self):
        waitbuttion=None
        
        time.sleep(2)
        waitbuttion = self.driver.find_elements(By.ID, f"challenge-form")
        waitbuttion = self.driver.find_elements(By.ID, f"cf-spinner-please-wait")

        while len(waitbuttion) > 0:

            try:

                waitbuttion = self.driver.find_elements(By.ID, f"challenge-form")
                waitbuttion = self.driver.find_elements(By.ID, f"cf-spinner-please-wait")

            except NoSuchElementException:
                # If the button is not found, set button to None
                waitbuttion = None

            for char in self.spinner:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.1)
                sys.stdout.write("\b")  # Move the cursor back one position


        # Initialize button as None
        button = None

        try:
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

            self.driver.switch_to.frame(iframes[0])

            iframes_nested = self.driver.find_elements(By.TAG_NAME, "iframe")

            self.driver.switch_to.frame(iframes_nested[0])

            button = self.driver.find_element(By.TAG_NAME, "button")

        except NoSuchElementException:
            # If the button is not found, set button to None
            button = None
        except Exception as e:
            button = None

        while button != None:

            try:

                button = self.driver.find_element(By.TAG_NAME, "button")

            except NoSuchElementException:
                # If the button is not found, set button to None
                button = None

            for char in self.spinner:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.1)
                sys.stdout.write("\b")  # Move the cursor back one position

        time.sleep(5)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.default_content()

        return None
    
    # Select one of the answers, whenever ChatGPT  shows two answers.
    def check_two_responses(self):
        
        try:
            

            # Select all buttons matching the given structure
            response_buttons = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class, '-mb-2') and contains(@class, 'snap-x')]//button" 
                #"//div[contains(@class, '-mb-2') and contains(@class, 'snap-x')]//div[position()=1 or position()=2]//button"
                )

            if len(response_buttons) >0:
                response_buttons[0].click()
                time.sleep(1)
        except Exception as e:
            time.sleep(.001)


        


    def ask_query(self, window_handle: str, query: str, file_address: str):

        self.driver.switch_to.window(window_handle)
        #self.driver.refresh()
        time.sleep(1)
        pyperclip.copy(query)

        if os.path.exists(file_address):
            file_input = self.driver.find_element(
                By.CSS_SELECTOR, f"input[type='file']"
            )
            file_input.send_keys(file_address)

        chat_input = self.driver.find_element(By.ID, f"prompt-textarea")

        final_copy_text_tags = None
        is_finished_response = False

        chat_input.click()

        chat_input.send_keys(Keys.LEFT_CONTROL + "v")

        send_button = self.driver.find_element(
            By.CSS_SELECTOR,
            f"body > div.relative.flex.h-full.w-full.overflow-hidden.transition-colors.z-0 > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.composer-parent.flex.h-full.flex-col.focus-visible\:outline-0 > div.md\:pt-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.w-full > div > div.text-base.px-3.md\:px-4.m-auto.w-full.md\:px-5.lg\:px-1.xl\:px-5 > div > form > div > div.group.relative.flex.w-full.items-center > div > div > button"
        )

        try:
            # wait untile file upload successfully and evrything beeng ready to send.
            while not (send_button.is_enabled() and send_button.is_displayed()):
                time.sleep(1)
        except Exception as e:
            time.sleep(1)
            send_button = self.driver.find_element(
                    By.CSS_SELECTOR,
                    f"body > div.relative.flex.h-full.w-full.overflow-hidden.transition-colors.z-0 > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.composer-parent.flex.h-full.flex-col.focus-visible\:outline-0 > div.md\:pt-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.w-full > div > div.text-base.px-3.md\:px-4.m-auto.w-full.md\:px-5.lg\:px-1.xl\:px-5 > div > form > div > div.group.relative.flex.w-full.items-center > div > div > button"
                )

        send_button.click()

        # Refresh the new tab to apply the cookies
        time.sleep(2)

        self.check_puzzle()

        return self.wait_until_finishing_response()
    
    def wait_until_finishing_response(self)->str:
        
        response = ""
        is_finished_response = False
        while  not is_finished_response:

            self.check_two_responses()

            try:

                final_copy_text_tags = chat_input = self.driver.find_elements(
                    By.XPATH,
                    f"//button[contains(@class, 'rounded-lg') and contains(@class, 'text-token-text-secondary') and @aria-label='Copy']",
                )

                if final_copy_text_tags[-1].id not in self.final_copy_text_tags_id_list:
                    # Copy tag, click for copy all information has been provided
                    final_copy_text_tags[-1].click()
                    response = pyperclip.paste()
                    print(response)
                    time.sleep(1)
                    is_finished_response = True
                    self.final_copy_text_tags_id_list.append(final_copy_text_tags[-1].id)

            except Exception as e:
                final_copy_text_tags = None
                time.sleep(1)
            
                
            time.sleep(1)
        return response
        
    
    def extract_code(self)->list[str]:
        
        copy_code =  self.driver.find_elements(By.XPATH, "//div[contains(@class, 'group/conversation-turn')]/div/div[contains(@class, 'flex')]/div/div/div/pre/div/div[contains(@class, 'flex')]/div/span/button")
        
        codes: list[str] =[]

        for tag in copy_code:
            # Putting all copy_tag id in list for future checking
            if tag.id not in self.copy_code_tags_list_id:
                self.copy_code_tags_list_id.append(tag.id)
                self.driver.execute_script("arguments[0].click();", tag)
                time.sleep(1)
                codes.append(pyperclip.paste())
                    
        # Asking to regenrate the code just in one part         
        return codes
        
        
    
