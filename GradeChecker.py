import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

TIME_DELAY_IN_MINUTES = 5
loginUrl = 'https://central.carleton.ca/prod/twbkwbis.P_ValLogin'
gradeUrl = 'https://central.carleton.ca/prod/bwskogrd.P_ViewGrde'

loginData = {}
termData = {'term_in': '201630'} # This corresponds to Fall 2016

# This loop gathers login information and breaks once the login is successful
while True:
    sid = input('Please input your student id (10XXXXXXX): ')
    pin = input('Please input your PIN: ')
    loginData['sid'] = sid
    loginData['PIN'] = pin

    # We need a new session to store the cookies for Carleton Central
    s = requests.Session()
    loginPage = s.get(loginUrl)
    cookies = dict(loginPage.cookies)
    r = s.post(loginUrl, data=loginData)
    soup = BeautifulSoup(r.content, 'html.parser')
    if 'Failure' not in soup.get_text(): # 'Failure' shows up in the failed login page
        print('Login Successful')
        break
    print('Login Failed\n')

# This loop continuously checks the final grades page, printing courses which have grades posted
while True:
    print('\n'+str(datetime.now().strftime('%H:%M:%S')))
    print('Courses with grades posted')
    r = s.post(gradeUrl, data=termData)
    soupTable = BeautifulSoup(r.content, 'html.parser').body.find('div', class_='pagebodydiv').find('table', class_='datadisplaytable').find_next_sibling('table')
    numTR = len(soupTable.find_all('tr'))
    result = soupTable.find('tr')
    for i in range(1,numTR): # The first tr tag contains the grade table headers, so it is skipped
        result = result.find_next_sibling('tr')
        resultData = result.find_all('td')
        print(resultData[1].get_text()+resultData[2].get_text())
    time.sleep(TIME_DELAY_IN_MINUTES*60)
