import boto3
import vlc
import time
import keyboard
import urllib
import socket
import os
import re


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys  # Import Keys


def write_list_to_file(file_path, data_list):
    with open(file_path, "w", encoding="utf-8") as output_file:
        for element in data_list:
            try:
                print(element, file=output_file)
            except UnicodeEncodeError:
                print("Unable to print element due to encoding issues.", file=output_file)
    

service =  Service(executable_path=r"C:\Users\ahmed\Desktop\WhatsScrap\MiniWhatsApp\geckodriver.exe")

driver = webdriver.Firefox(service=service)
driver.get('https://web.whatsapp.com/')

driver.implicitly_wait(50)

first_iteration = True

while True:

    elements_list = []
    message_list = []
    sender_list = []
    date_list = []

    # Loop from 1 to 5

    if not first_iteration:
        # Read the content of the text file
        with open("write_CMD.txt", "r", encoding="utf-8") as file:
            line = file.readline()

        # Split the line into two values at the first space
        values = line.strip().split('|', 1)

        # Check if there are exactly two values
        if len(values) == 2:
            chat, my_msg = values
            print("Variable 1:", chat)
            print("Variable 2:", my_msg)
        else:
            print("Invalid format in the text file.")

        # Replace 'your_title_value' with the actual value you want to search for
        title_value_to_search = chat

        # Construct the XPath using the title attribute
        xpath_expression = f"//span[@title='{title_value_to_search}']"

        # Find the element using the constructed XPath
        driver.find_element(By.XPATH, xpath_expression).click()

        time.sleep(4)
        
        # Create an ActionChains object
        actions = ActionChains(driver)

        # Type your message
        actions.send_keys(my_msg, Keys.RETURN)

        # Press Enter
        #actions.send_keys(msg, Keys.RETURN)  # Include any other keys you want to simulate

        # Perform the actions
        actions.perform()

        # # Replace 'your_class_name' with the actual class name you want to search for
        # class_name_to_search = "to2l77zo"

        # # Find the element using the class name with XPath
        # xpath_expression = f"/html/body/div[1]/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]/div[1]"
        # # Find the element using the constructed XPath
        # driver.find_element(By.XPATH, xpath_expression).send_keys(my_msg)
        
        
        # data_icon_value_to_search = "send"

        # # Construct the XPath using the data-icon attribute
        # xpath_expression = f"//span[@data-icon='{data_icon_value_to_search}']"

        # # Find the element using the constructed XPath
        # driver.find_element(By.XPATH, xpath_expression).click()



    
    
    for i in range(1, 12):
        # Construct the XPath dynamically
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
        except NoSuchElementException:
            # If the person XPath fails, try the group XPath
            try:
                element = driver.find_element(By.XPATH, xpath_group)
                msg = driver.find_element(By.XPATH, xpath_group_msg)
                sender = driver.find_element(By.XPATH, xpath_sender)
                print(f"found group {i}")
            except NoSuchElementException:
                # Handle the case when both XPaths fail, e.g., raise an error or log a message
                print(f"Element not found for both XPaths at index {i}")
                continue  # Skip to the next iteration


        date = driver.find_element(By.XPATH, xpath_date)

        # Get the text value of the element and append it to the list
        elements_list.append(element.text)
        message_list.append(msg.text)
        date_list.append(date.text)
        sender_list.append(sender.text)


    # Example usage:
    write_list_to_file("output.txt", elements_list)
    write_list_to_file("msg.txt", message_list)
    write_list_to_file("sender.txt", sender_list)
    write_list_to_file("date.txt", date_list)

    with open("sheets.py") as f:
        exec(f.read())

    first_iteration = False
    time.sleep(10)

# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[10]/div/div/div/div[2]/div[1]/div[1]/div/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[9]/div/div/div/div[2]/div[1]/div[1]/div/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[8]/div/div/div/div[2]/div[1]/div[1]/div/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[7]/div/div/div/div[2]/div[1]/div[1]/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[6]/div/div/div/div[2]/div[1]/div[1]/span

# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[11]/div/div/div/div[2]/div[1]/div[1]/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[10]/div/div/div/div[2]/div[1]/div[1]/span


# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[11]/div/div/div/div[2]/div[2]/div[1]/span/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[8]/div/div/div/div[2]/div[2]/div[1]/span/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[7]/div/div/div/div[2]/div[2]/div[1]/span/span

# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/span/span[2]
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[10]/div/div/div/div[2]/div[2]/div[1]/span/span[2]

# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[10]/div/div/div/div[2]/div[2]/div[1]/span/div/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/span/div[1]/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[17]/div/div/div/div[2]/div[2]/div[1]/span/div/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[10]/div/div/div/div[2]/div[2]/div[1]/span/div/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[9]/div/div/div/div[2]/div[2]/div[1]/span/div/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[8]/div/div/div/div[2]/div[2]/div[1]/span/div/span
#/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/span/div/span

# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[11]/div/div/div/div[2]/div[1]/div[2]/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[17]/div/div/div/div[2]/div[1]/div[2]/span


# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div/div[2]/div[1]/div[2]/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[10]/div/div/div/div[2]/div[1]/div[2]/span


# # UNREAD
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/span[1]/div[2]/span

# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/div[2]/span[1]/div[2]/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[11]/div/div/div/div[2]/div[2]/div[2]/span[1]/div[2]/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[7]/div/div/div/div[2]/div[2]/div[2]/span[1]/div[2]/span
# /html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/div/div[10]/div/div/div/div[2]/div[2]/div[2]/span[1]/div/span
# /html/body/div[1]/div/span[5]

