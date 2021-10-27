from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import math
from time import gmtime, strftime
import random
import file_organizer as f
import numpy as np


#paths
#webdriver_path = 'C:\\Users\Franex\Desktop\python\chromedriver'
#login_password_path = 'C:\\Users\Franex\Desktop\python\login_password.json'


webdriver_path = 'chromedriver84'
login_password_path = 'login_password.json'


import json
with open(login_password_path,'r') as f_config:
    config = json.load(f_config)


def driver_settings():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if (head == False):
        chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--mute-audio") #mutes the audio
    chrome_options.add_argument('log-level=3') #prevents nonfatal console info from displaying
    return chrome_options


def initialization():
    chrome_options = driver_settings()
    browser = webdriver.Chrome(webdriver_path, options=chrome_options)
    browser.get('https://plemiona.pl')
    browser.set_window_size(1920, 1080)
    return browser 


def captcha_beater():
    if len(browser.find_elements_by_xpath('//*[@id="recaptcha-anchor"]/div[1]')) != 0:
        browser.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[1]').click()
        print("CAPTCHA!")
        time.sleep(1)


def is_existing(id, type):
    if type == "id":
        if len(browser.find_elements_by_id(id)) == 0:
            print(f"ERROR: {id} (type:{type}) cannot be found")
            quit()
    if type == "class":
        if len(browser.find_elements_by_class_name(id)) == 0:
            print(f"ERROR: {id} (type:{type}) cannot be found")
            quit()
    if type == "xpath":
        if len(browser.find_elements_by_xpath(id)) == 0:
            print(f"ERROR: {id} (type:{type}) cannot be found")
            quit()

def logging_in():
    sending_login()
    sending_password()
    login_button_click()
    time.sleep(0.7)
    choosing_world()
    daily_bonus()

def sending_login():
    is_existing("user", "id")
    browser.find_element_by_id("user").send_keys(config['user']['name'])

def sending_password():
    is_existing("password", "id")
    browser.find_element_by_id("password").send_keys(config['user']['password'])
    
def login_button_click():
    is_existing("btn-login", "class")
    browser.find_element_by_class_name("btn-login").click()

def choosing_world():
    is_existing("world_button_active", "class")
    browser.find_element_by_class_name("world_button_active").click()
    captcha_beater()

def farmer_assistant():
    browser.save_screenshot("webscreenshot.png")
    is_existing('//*[@id="manager_icon_farm"]', "xpath")
    browser.find_element_by_xpath('//*[@id="manager_icon_farm"]').click()
    captcha_beater()

def list_of_Bs():
    is_existing('//tr/td/a[contains(@class, "farm_icon_b")]', "xpath")
    B = browser.find_elements_by_xpath('//tr/td/a[contains(@class, "farm_icon_b")]')[1:]
    return B

def active_cavalry():
    is_existing('//*[@id="light"]', "xpath")
    return int(browser.find_element_by_xpath('//*[@id="light"]').get_attribute('innerHTML'))

def return_to_village():
    is_existing('//*[@id="menu_row2_village"]/a', "xpath")
    browser.find_element_by_xpath('//*[@id="menu_row2_village"]/a').click()
    time.sleep(0.1)
    captcha_beater()

def logs():
    with open("C:/Users/Franex/Desktop/plemiona_bot/logs.txt", "r+") as logs_file:
        content = logs_file.read()
    with open("C:/Users/Franex/Desktop/plemiona_bot/logs.txt", "w+") as logs_file:
        logs_file.write(strftime("%d.%m.%Y    %H:%M:%S", time.localtime()))
        if content != "":
            logs_file.write("\n")
        logs_file.write(content)

def sending_cavalry():
    farmer_assistant()
    time.sleep(1)
    B = list_of_Bs()
    light_cavalry_active = active_cavalry()
    print("Cavalry at the start:", light_cavalry_active)
    cavalry_sent = 0
    counter = 0
    browser.find_element_by_xpath('//*[@id="quickbar_contents"]/ul/li[7]/span/a').click() #farming onsite script
    captcha_beater()

    #first page
    
    while light_cavalry_active > counter and len(B) > counter and counter < limit:
        browser.save_screenshot("webscreenshot.png")
        B[counter].click()
        cavalry_sent += 1
        time.sleep(0.2 + random.random()/2)
        counter += 1
        captcha_beater()
    

    browser.execute_script("window.scrollTo(0, 0);")

    #second page if needed
    if limit > 100:
        browser.find_element_by_xpath('//*[@id="plunder_list_nav"]/table/tbody/tr/td/a').click()
        time.sleep(0.5)

        B = list_of_Bs()
        light_cavalry_active = active_cavalry()

        browser.find_element_by_xpath('//*[@id="quickbar_contents"]/ul/li[7]/span/a').click() #farming onsite script
        time.sleep(0.3)

        while light_cavalry_active > counter and len(B) + 100 > counter and counter < limit:
            browser.save_screenshot("webscreenshot.png")
            B[counter - 100].click()
            cavalry_sent += 1
            time.sleep(0.2 + random.random()/2)
            counter += 1
            captcha_beater()


    is_existing('//*[@id="light"]', "xpath")
    cavalry_at_the_end = browser.find_element_by_xpath('//*[@id="light"]').get_attribute("innerHTML")

    logs()
    print("Cavalry sent:", cavalry_sent)
    print("Cavalry at the end:", cavalry_at_the_end)
    print(strftime("%H:%M:%S", time.localtime()))
    return_to_village()

def reports_analyzer():
    is_existing('//*[@id="menu_row"]/td[4]/a', "xpath")
    browser.find_element_by_xpath('//*[@id="menu_row"]/td[4]/a').click() #clicking reports icon
    time.sleep(0.5)
    captcha_beater()
    is_existing("//*[text()[contains(., 'Asystent Farmera')]]", "xpath")
    browser.find_element_by_xpath("//*[text()[contains(., 'Asystent Farmera')]]").click() #farmer assistant
    captcha_beater()
    is_existing('//*[@id="report_list"]/tbody/tr[2]/td[2]/span[1]/span/a/span', "xpath")
    browser.find_element_by_xpath('//*[@id="report_list"]/tbody/tr[2]/td[2]/span[1]/span/a/span').click() #first report
    captcha_beater()
    file = f.open_file()
    file_array = f.file_to_array(file)
    while (len(browser.find_elements_by_xpath('//*[@id="report-prev"]/img')) != 0): #as long as next report exists
        village_name = browser.find_element_by_xpath('//*[@id="attack_info_def"]/tbody/tr[2]/td[2]/span/a[1]').get_attribute('innerHTML')
        if browser.find_element_by_xpath('//*[@id="content_value"]/table/tbody/tr/td[2]/table/tbody/tr/td/table[2]/tbody/tr[3]/td/h3').get_attribute("value") != "l337 wygrał": #battle lost
            loot = 0
        else: #battle won
            loot = browser.find_element_by_xpath('//*[@id="attack_results"]/tbody/tr/td[2]').get_attribute('innerHTML')
        if not f.village_in_the_file(file_array, village_name):
            f.add_village_to_file(file, village_name)
        time.sleep(0.2)
        if len(browser.find_elements_by_xpath('//*[@id="report-prev"]/img')) != 0:
            browser.find_element_by_xpath('//*[@id="report-prev"]/img').click() #to the next report
            captcha_beater()
    f.close_file(file)
    return_to_village()

def printing_last_time():
    with open("C:/Users/Franex/Desktop/plemiona_bot/logs.txt", "r+") as logs_file:
        print(logs_file.readlines()[0].split("\n")[0])

def printing_cavalry():
    if len(browser.find_elements_by_xpath('//*[text()[contains(., "Lekki kawalerzysta")]]')) == 2: #in case of premium account there are 2 occurrences of "Lekki kawalerzysta"
        is_existing('//*[text()[contains(., "Lekki kawalerzysta")]]', "xpath")
        cavalry = browser.find_element_by_xpath('//*[text()[contains(., "Lekki kawalerzysta")]]').get_attribute("innerHTML").split('data-count="light">')[0].split('</strong>')[0]
    elif len(browser.find_elements_by_xpath('//*[text()[contains(., "Lekkich kawalerzystów")]]')) != 0:
        is_existing('//*[text()[contains(., "Lekkich kawalerzystów")]]', "xpath")
        cavalry = browser.find_element_by_xpath('//*[text()[contains(., "Lekkich kawalerzystów")]]').get_attribute("innerHTML").split('data-count="light">')[1].split('</strong>')[0]
    else:
        cavalry = 0
    print("Cavalry at the village: ", cavalry)

def printing_materials():
    is_existing('//*[@id="wood"]', "xpath")
    wood = browser.find_element_by_xpath('//*[@id="wood"]').get_attribute("innerHTML")
    is_existing('//*[@id="stone"]', "xpath")
    stone = browser.find_element_by_xpath('//*[@id="stone"]').get_attribute("innerHTML")
    is_existing('//*[@id="iron"]', "xpath")
    iron = browser.find_element_by_xpath('//*[@id="iron"]').get_attribute("innerHTML")
    is_existing('//*[@id="storage"]', "xpath")
    storage = browser.find_element_by_xpath('//*[@id="storage"]').get_attribute("innerHTML")
    print(f"Materials: {wood}|{stone}|{iron} /{storage}")

def printing_exchange_rates():
    is_existing('//*[@id="map"]/area[10]', "xpath")
    browser.find_element_by_xpath('//*[@id="map"]/area[10]').click()
    captcha_beater()
    is_existing('//*[@id="content_value"]/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td/a', "xpath")
    browser.find_element_by_xpath('//*[@id="content_value"]/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td/a').click()
    captcha_beater()
    is_existing('//*[@id="premium_exchange_rate_wood"]/div[1]', "xpath")
    wood_rate = browser.find_element_by_xpath('//*[@id="premium_exchange_rate_wood"]/div[1]').get_attribute("innerHTML").split("> ")[1]
    is_existing('//*[@id="premium_exchange_rate_stone"]/div[1]', "xpath")
    stone_rate = browser.find_element_by_xpath('//*[@id="premium_exchange_rate_stone"]/div[1]').get_attribute("innerHTML").split("> ")[1]
    is_existing('//*[@id="premium_exchange_rate_iron"]/div[1]', "xpath")
    iron_rate = browser.find_element_by_xpath('//*[@id="premium_exchange_rate_iron"]/div[1]').get_attribute("innerHTML").split("> ")[1]
    print(f"Exchange rates: {wood_rate}|{stone_rate}|{iron_rate}")

def info():
    printing_last_time()
    printing_cavalry()
    printing_materials()
    printing_exchange_rates()
    return_to_village()

def scavenging(): #scavenging max
    browser.find_element_by_xpath('//*[@id="map"]/area[2]').click() #clicking rally point
    captcha_beater()
    browser.find_element_by_xpath('//*[@id="content_value"]/table[2]/tbody/tr/td[3]/a').click() #to scavenging
    captcha_beater()
    browser.find_element_by_xpath('//*[@id="scavenge_screen"]/div/div[1]/table/tbody/tr[2]/td[1]/a').click() #spear fighters
    captcha_beater()
    browser.find_element_by_xpath('//*[@id="scavenge_screen"]/div/div[1]/table/tbody/tr[2]/td[2]/a').click() #swordsmen
    captcha_beater()
    browser.find_element_by_xpath('//*[@id="scavenge_screen"]/div/div[2]/div[3]/div[3]/div/div[2]/a[1]').click() #starting
    captcha_beater()

def scavenging_split():
    browser.find_element_by_xpath('//*[@id="map"]/area[2]').click() #clicking rally point
    captcha_beater()
    browser.find_element_by_xpath('//*[@id="content_value"]/table[2]/tbody/tr/td[3]/a').click() #to scavenging
    captcha_beater()
    browser.find_element_by_xpath('//*[@id="quickbar_contents"]/ul/li[8]/span/a').click()
    captcha_beater()
    #third
    browser.find_element_by_xpath('//*[@id="scavenge_screen"]/div/div[2]/div[3]/div[3]/div/div[2]/a[1]').click()
    time.sleep(0.5)
    captcha_beater()
    browser.find_element_by_xpath('//*[@id="quickbar_contents"]/ul/li[8]/span/a').click()
    captcha_beater()
    #second
    browser.find_element_by_xpath('//*[@id="scavenge_screen"]/div/div[2]/div[2]/div[3]/div/div[2]/a[1]').click()
    time.sleep(0.5)
    captcha_beater()
    browser.find_element_by_xpath('//*[@id="quickbar_contents"]/ul/li[8]/span/a').click()
    captcha_beater()
    #first
    browser.find_element_by_xpath('//*[@id="scavenge_screen"]/div/div[2]/div[1]/div[3]/div/div[2]/a[1]').click()
    captcha_beater()

def calculate_daily_scavenging(entry):
    duration_exponent = 0.45
    duration_initial_seconds = 1800
    duration_factor = 1
    loot_factor = [0.1, 0.25, 0.5, 0.75]
    ratio = [1 * entry[0], (2/5)**(1/2) * entry[1], (2/10)**(1/2) * entry[2], (2/15)**(1/2) * entry[3]]
    sum = 0
    for r in ratio:
        sum += r
    max_loot = 8900
    number_of_splits = 0
    smallest_number = 3
    for i in range (4):
        if entry[i] == 1:
            if (smallest_number == 3):
                smallest_number = i
            number_of_splits += 1
    
    loot = math.floor((max_loot * (ratio[smallest_number]/ sum) * loot_factor[smallest_number]) * number_of_splits)
    time = math.floor((((max_loot * ratio[smallest_number]/ sum)**2 * 100 * loot_factor[smallest_number]**2)**duration_exponent + duration_initial_seconds) * duration_factor)
    daily_loot = math.floor(loot * (24 * 60 * 60 / time))
    print(entry, daily_loot)

def spliting_scavenging():
    calculate_daily_scavenging((0, 0, 0, 1))
    calculate_daily_scavenging((0, 0, 1, 0))
    calculate_daily_scavenging((0, 0, 1, 1))

    calculate_daily_scavenging((0, 1, 0, 0))
    calculate_daily_scavenging((0, 1, 0, 1))
    calculate_daily_scavenging((0, 1, 1, 0))
    calculate_daily_scavenging((0, 1, 1, 1))

    calculate_daily_scavenging((1, 0, 0, 0))
    calculate_daily_scavenging((1, 0, 0, 1))
    calculate_daily_scavenging((1, 0, 1, 0))
    calculate_daily_scavenging((1, 0, 1, 1))

    calculate_daily_scavenging((1, 1, 0, 0))
    calculate_daily_scavenging((1, 1, 0, 1))
    calculate_daily_scavenging((1, 1, 1, 0))
    calculate_daily_scavenging((1, 1, 1, 1))
    
def daily_bonus():
    for i in range (1, 9):
        if len(browser.find_elements_by_xpath(f'//*[@id="daily_bonus_content"]/div/div[{i}]/div/div/div[3]/a')) != 0:
            browser.find_element_by_xpath(f'//*[@id="daily_bonus_content"]/div/div[{i}]/div/div/div[3]/a').click()
            captcha_beater()

def input_of_coach():
    print("Coordinate X:")
    x = int(input())
    print("Coordinate Y:")
    y = int(input())
    return x, y

def new_tab(x, y): #opens and configurate new tab
    browser.execute_script('''window.open("https://pl151.plemiona.pl/game.php?screen=overview&intro", "_blank");''')
    time.sleep(2)
    browser.switch_to.window(browser.window_handles[1])
    time.sleep(2)
    is_existing('//*[@id="map"]/area[2]', 'xpath')
    browser.find_element_by_xpath('//*[@id="map"]/area[2]').click()
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="unit_input_axe"]').send_keys("30") #axes
    time.sleep(1.5)
    browser.find_element_by_xpath('//*[@id="place_target"]/input').send_keys(f"{x}|{y}")
    browser.save_screenshot("webscreenshot.png")
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="target_attack"]').click()

def sending_coach():
    #x, y = input_of_coach()

    new_tab(376, 509)

    #browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + Keys.TAB)

def main():
    logging_in()

    if farming == True:
        sending_cavalry()

    if scavenge == True:
        scavenging_split()

    #logs()

    if information == True:
        info()

    if calculate == True:
        spliting_scavenging()

    if coach == True:
        sending_coach()

    if need_help == True:
        print("Description coming soon!")

    browser.close()



#settings
scavenge = False
information = False
farming = False
calculate = False
coach = False
need_help = False
head = False
limit = 100

print ("If you need any help just type 'help'")
modes = input().lower().split()

help_array = ["help", "'help'", '"help"', "!help", "-help", "--help"]

for mode in modes:
    if mode == "s":
        scavenge = True
    if mode == "i":
        info = True
    if mode == "f":
        farming = True
    if mode == "c":
        calculate = True
    if mode == "coach" or mode == "kareta":
        scavenge = False
        information = False
        farming = False
        calculate = False
        coach = True
    if mode == "h":
        head = True
    if mode in help_array:
        need_help = True


if mode != "c":
    browser = initialization()

main()




production = {
    '1': '30',
    '2': '35',
    '3': '41',
    '4': '47',
    '5': '55',
    '6': '64',
    '7': '74',
    '8': '86',
    '9': '100',
    '10': '117',
    '11': '136',
    '12': '158',
    '13': '184',
    '14': '214',
    '15': '249',
    '16': '289',
    '17': '337',
    '18': '391',
    '19': '455',
    '20': '530',
    '21': '616',
    '22': '717',
    '23': '833',
    '24': '969',
    '25': '1127',
    '26': '1311',
    '27': '1525',
    '28': '1774',
    '29': '2063',
    '30': '2400'
}