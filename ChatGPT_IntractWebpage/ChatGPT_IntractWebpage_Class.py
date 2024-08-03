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
    final_tags_id_list = []
    # Define the spinner characters
    spinner = ["-", "\\", "|", "/"]
    
    
    driver_path = r"C:/Users/M/Downloads/Compressed/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    chrome_debugging_port = 9222  # Make sure this matches the port used above
    chrome_profile_path = "C:/Users/M/AppData/Local/Google/Chrome/User Data"

    # "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 -- "%1"

    # Function to display the spinner
    def check_puzzle(self):
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
            
            response_buttons = self.driver.find_elements(
        By.XPATH,
        "//*[@id='__next']/div[contains(@class, 'relative')]/div[contains(@class, 'flex')]/main/div[contains(@class, 'flex')]/div[contains(@class, 'flex-1')]/div/div/div/div/div/div[7]/div/div/div[contains(@class, '-mb-2')]/div/div/button"
    )
            if len(response_buttons) >0:
                response_buttons[0].click()
                time.sleep(1)
        except Exception as e:
            time.sleep(.001)

    def __init__(self):

        self.service = Service(executable_path=self.driver_path)
        self.options = Options()
        self.options.add_argument("--remote-debugging-port=9222")
        self.options.add_argument(f"user-data-dir={self.chrome_profile_path}")
        
        self.options.add_argument("--log-level=5")  # Set logging level

        # Initialize the WebDriver
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        wait = WebDriverWait(self.driver, 10)

        self.driver.get("https://chat.openai.com")
        time.sleep(2)
        self.driver.refresh()
        time.sleep(2)


        self.driver.switch_to.window(self.driver.window_handles[-1])

        new_chat = self.driver.find_element(
            By.CSS_SELECTOR,
            f"#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.flex-shrink-0.overflow-x-hidden.bg-token-sidebar-surface-primary > div > div > div > div > nav > div.flex-col.flex-1.transition-opacity.duration-500.-mr-2.pr-2.overflow-y-auto > div.bg-token-sidebar-surface-primary.pt-0 > div > a",
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

    def ask_query(self, window_handle: str, query: str, file_address: str):

        self.driver.switch_to.window(window_handle)
        self.driver.refresh()
        time.sleep(1)

        if os.path.exists(file_address):
            file_input = self.driver.find_element(
                By.CSS_SELECTOR, f"input[type='file']"
            )

            file_input.send_keys(file_address)

        chat_input = self.driver.find_element(By.ID, f"prompt-textarea")

        final_tags = None
        is_finished_response = False

        chat_input.click()

        chat_input.send_keys(Keys.LEFT_CONTROL + "v")

        send_button = self.driver.find_element(
            By.CSS_SELECTOR,
            f"#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.flex.h-full.flex-col.focus-visible\:outline-0 > div.md\:pt-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.w-full > div.text-base.px-3.md\:px-4.m-auto.md\:px-5.lg\:px-1.xl\:px-5 > div > form > div > div.flex.w-full.items-center > div > div > button",
        )

        # wait untile file upload successfully and evrything beeng ready to send.
        while not (send_button.is_enabled() and send_button.is_displayed()):
            time.sleep(1)


        send_button.click()

        # Refresh the new tab to apply the cookies
        time.sleep(2)

        self.check_puzzle()
        response = ""

        while  not is_finished_response:

            self.check_two_responses()

            try:

                final_tags = chat_input = self.driver.find_elements(
                    By.XPATH,
                    "//*[@id='__next']/div[contains(@class, 'relative')]/div[contains(@class, 'relative')]/main/div[contains(@class, 'flex')]/div[contains(@class, 'flex-1')]/div/div/div/div/div/div/div/div[contains(@class, 'group/conversation-turn')]/div/div[contains(@class, 'mt-1')]/div/div/span[2]/button",
                )

                if final_tags[-1].id not in self.final_tags_id_list:
                    final_tags[-1].click()
                    response = pyperclip.paste()
                    print(response)
                    time.sleep(1)
                    is_finished_response = True
                    self.final_tags_id_list.append(final_tags[-1].id)

            except Exception as e:
                final_tags = None
                time.sleep(1)
            
                
            time.sleep(1)



        return response
