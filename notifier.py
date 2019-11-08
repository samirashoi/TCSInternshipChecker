from CREDENTIALS import TCSREFNUMBER, TCSPASSWORD

import notify2
import time
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  
chrome_options = Options()  
chrome_options.add_argument("--headless")  


from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

chromedriver = './chromedriver'



def connect(login_url, internships_home_url, internships_url, logout_url):
    
    driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)


    driver.get(login_url)

    uname_field = driver.find_element_by_id('user_name')
    uname_field.send_keys(TCSREFNUMBER)

    pass_field = driver.find_element_by_id('user_password')
    pass_field.send_keys(TCSPASSWORD)

    driver.find_element_by_css_selector('button.login').click()
    time.sleep(2)

    driver.get(internships_home_url)
    internship_str = driver.find_element_by_css_selector('.btn-primary>strong').text
    number_of_open_internship_links = int(re.match(r'Explore Internships \((\d*)\)', internship_str).group(1))

    open_internship_links = []
    open_internship_places = []

    if number_of_open_internship_links:
        driver.get(internships_url)
        open_internship_links = driver.find_elements_by_css_selector('a.mLink')
        open_internship_places = driver.find_elements_by_css_selector('.flexo>.a>.os>.scolor')
    
    ntfn_summary_msg = f'{number_of_open_internship_links} Internships Available'

    ntfn_body = ''

    print(ntfn_summary_msg)
    print('-'*50)
    for link, place in zip(open_internship_links, open_internship_places):
        desc = f'{link.text} - {place.text}'
        print(desc)
        ntfn_body += (desc + '\n')
        print(link.get_attribute('href'))
        print('-'*50)

    driver.get(logout_url)
    driver.quit()

    return (ntfn_summary_msg, ntfn_body)

            
LOGIN_URL = 'https://campuscommune.tcs.com/en-in/intro'
INTERNSHIPS_HOME_URL = 'https://campuscommune.tcs.com/exops_home'
INTERNSHIPS_URL = 'https://campuscommune.tcs.com/internships?category=1'  # 'https://campuscommune.tcs.com/my_closed_internships'
LOGOUT_URL = 'https://campuscommune.tcs.com/logout'


@tl.job(interval=timedelta(minutes=15))
def notify():    
    ntfn_summary_msg, ntfn_body = connect(LOGIN_URL, INTERNSHIPS_HOME_URL, INTERNSHIPS_URL, LOGOUT_URL)
    notify2.init('TCS Notify')
    n = notify2.Notification(ntfn_summary_msg, ntfn_body)
    n.show()

# @tl.job(interval=timedelta(seconds=20))
# def printHello():
#     print("Hello " + time.ctime())


if __name__ == '__main__':
    tl.start(block=True)
    # notify()

