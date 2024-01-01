import time
import sheets
import sys
import A2F
# Change console encoding to UTF-8

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys  # Import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options



#######     https://docs.google.com/spreadsheets/d/10yJZ7lQGKxqKY0664oF3XAvDDcZvqvwv5eXNia05g7A/edit#gid=0


sys.stdout.reconfigure(encoding='utf-8')

def write_list_to_file(file_path, data_list):
    with open(file_path, "w", encoding="utf-8") as output_file:
        for element in data_list:
            try:
                print(element, file=output_file)
            except UnicodeEncodeError:
                print("Unable to print element due to encoding issues.", file=output_file)
    
def get_chat_and_msg(row):
    chat = ""
    my_msg = ""
    with open(f"write_CMD/write_CMD{row}.txt", "r", encoding="utf-8") as file:
        line = file.readline()
        print(f"My CMD {row} is {line}")
    if line == '':
        return None

    with open(f"write_CMD/write_CMD_chatName{row}.txt", "r", encoding="utf-8") as file:
        chatName = file.readline()

    with open(f"write_CMD/write_CMD_date{row}.txt", "r", encoding="utf-8") as file:
        date = file.readline()

    # Split the line into two values at the first |
    values = line.strip().split('|', 1)
    chat, my_msg_with_line = values
    my_msg = my_msg_with_line.split('\n', 1)[0]

    print("Variable 1:", repr(chat))
    print("Variable 2:", my_msg)

    return chat, my_msg, chatName, date

def click_on_chat(chat, chatName, date):
    # We then try to find the element using the chat name instead
    # this too could fail if there are emojis in the name
    # or if the name is in Arabic letters -- still not sure about this
    try:
        xpath_expression = f"//span[@title='{chatName}']"
        chat_element = driver.find_element(By.XPATH, xpath_expression)
        try:
            chat_element.click()
        except ElementClickInterceptedException:
            try:
                scroll_into_view(chat_element)
                chat_element.click()
            except ElementClickInterceptedException:
                print("Unclickable for some reason")


    except NoSuchElementException:
        # Try to find the element using the last text appearing on chat from outside
        # this could fail when there are emojis in the text
        try:
            xpath_expression = f"//span[text()='{chat}']"
            chat_element = driver.find_element(By.XPATH, xpath_expression)
            try:
                chat_element.click()
            except ElementClickInterceptedException:
                try:
                    scroll_into_view(chat_element)
                    chat_element.click()
                except ElementClickInterceptedException:
                    print("Unclickable for some reason")


        # for a third try, we try to find it using the date that we have stored for the last message sent from our friend
        # this too could have some problems if there are multiple last messages with the same time
        except NoSuchElementException:
            try:
                xpath_expression = f"//span[text()='{date}']"
                chat_element = driver.find_element(By.XPATH, xpath_expression)
                try:
                    chat_element.click()
                except ElementClickInterceptedException:
                    try:
                        scroll_into_view(chat_element)
                        chat_element.click()
                    except ElementClickInterceptedException:
                        print("Unclickable for some reason")
            except ElementClickInterceptedException:
                print("something went wrong during writing")


def scroll_into_view(element):
    #driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].scrollIntoView({block: 'end', inline: 'nearest'});", element)



def write_to_chat_and_send(my_msg):
    actions = ActionChains(driver)
    #actions.send_keys(my_msg, Keys.RETURN)
    actions.send_keys(my_msg)
    actions.perform()

def reset_WCMD_contents():
    for row in range(1,13):
        delete_file_contents(f"write_CMD/write_CMD{row}.txt")
        delete_file_contents(f"write_CMD/write_CMD_chatName{row}.txt")
        delete_file_contents(f"write_CMD/write_CMD_date{row}.txt")


def delete_file_contents(file_name):
    open(file_name, "w", encoding="utf-8").close()


##################################################################################################################################
######################################## Code start ##############################################################################
##################################################################################################################################

#PC verison
# service =  Service(executable_path=r"C:\Users\ahmed\Desktop\WhatsScrap\MiniWhatsApp\geckodriver.exe")
# firefox_options = Options()
# firefox_options.set_preference("browser.cache.disk.enable", False)
# firefox_options.set_preference("browser.cache.memory.enable", False)
# firefox_options.set_preference("browser.cache.offline.enable", False)
# firefox_options.set_preference("network.http.use-cache", False)
# driver = webdriver.Firefox(service=service, options=firefox_options)

# Work version
service = Service(executable_path=r"C:\Users\aabdelf5\Desktop\PersonalProjects\MiniWhatsApp\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get('https://web.whatsapp.com/')
sheets.init()
driver.implicitly_wait(50)
first_iteration = True


while True:

    elements_list = []
    message_list = []
    sender_list = []
    date_list = []

    if not first_iteration:
        sheets.readMyMsgAtCol(5)

        for row in range(1,14):
            write_CMD_info = get_chat_and_msg(row)
            if write_CMD_info == None:
                continue
            #chat header - the message to be sent - person's name - date
            chat, my_msg, chatName, date = write_CMD_info
    
            click_on_chat(chat,chatName,date)
            time.sleep(2)
            write_to_chat_and_send(my_msg)
            
        # Delete contents from the write_CMD files to wait for another call by writing to it.
        reset_WCMD_contents()
        sheets.delete_col(5)

    
    for i in range(1, 14):
        xpath_person = f"/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[{i}]/div/div/div/div[2]/div[1]/div[1]/div/span"
        xpath_group = f"/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[{i}]/div/div/div/div[2]/div[1]/div[1]/span"
        xpath_person_msg = f"/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[{i}]/div/div/div/div[2]/div[2]/div[1]/span/span"
        xpath_group_msg = f"/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[{i}]/div/div/div/div[2]/div[2]/div[1]/span/span[2]"
        xpath_sender = f"/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[{i}]/div/div/div/div[2]/div[2]/div[1]/span/div/span"
        xpath_date = f"/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[{i}]/div/div/div/div[2]/div[1]/div[2]/span"

        if i == 2:
            driver.implicitly_wait(3)

        try:
            element = driver.find_element(By.XPATH, xpath_person)
            msg = driver.find_element(By.XPATH, xpath_person_msg)
            sender = element
            print(f"found element {i}")

        # If the person XPath fails, try the group XPath
        except NoSuchElementException:
            try:
                element = driver.find_element(By.XPATH, xpath_group)
                msg = driver.find_element(By.XPATH, xpath_group_msg)
                sender = driver.find_element(By.XPATH, xpath_sender)
                print(f"found group {i}")

            # Handle the case when both XPaths fail, e.g., raise an error or log a message
            except NoSuchElementException:
                print(f"Element not found for both XPaths at index {i}")
                continue  # Skip to the next iteration

        date = driver.find_element(By.XPATH, xpath_date)

        # Get the text value of the element and append it to the list

        elemTxt = A2F.check_and_convert_to_franco(element.text)
        msgTxt = A2F.check_and_convert_to_franco(msg.text)
        senderTxt = A2F.check_and_convert_to_franco(sender.text)

        if msgTxt == '':
            msgTxt = "Emoji or React."
        elements_list.append(elemTxt)
        message_list.append(msgTxt)
        date_list.append(date.text)
        sender_list.append(senderTxt)

    write_list_to_file("output.txt", elements_list)
    write_list_to_file("msg.txt", message_list)
    write_list_to_file("sender.txt", sender_list)
    write_list_to_file("date.txt", date_list)

    sheets.write_sheet()

    first_iteration = False

    # This is the sleep before checking for msg_CMD it should be about 40 or 50 seconds but i'll see. 
    time.sleep(5)



# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[9]/div/div/div/div[2]/div[2]/div[1]/span/span[2]
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[7]/div/div/div/div[2]/div[2]/div[1]/span/span[2]
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[5]/div/div/div/div[2]/div[2]/div[1]/span/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[10]/div/div/div/div[2]/div[2]/div[1]/span/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[6]/div/div/div/div[2]/div[2]/div[1]/span/span[3]
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[6]/div/div/div/div[2]/div[1]/div[1]/span