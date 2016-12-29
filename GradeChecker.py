import requests
from bs4 import BeautifulSoup
import time

loginUrl = 'https://central.carleton.ca/prod/twbkwbis.P_ValLogin'
gradeUrl = 'https://central.carleton.ca/prod/bwskogrd.P_ViewGrde'
TIME_DELAY_IN_MINUTES = 5

loginData = {}
termData = {'term_in': '201630'} # This corresponds to Fall 2016

while True:
    sid = input('Please input your student id (10XXXXXXX): ')
    pin = input('Please input your PIN: ')
    loginData['sid'] = sid
    loginData['PIN'] = pin

    s = requests.Session()
    loginPage = s.get(loginUrl)
    cookies = dict(loginPage.cookies)
    r = s.post(loginUrl, data=loginData)
    soup = BeautifulSoup(r.content, 'html.parser')
    if 'Failure' not in soup.get_text():
        print('Login Successful\n')
        break
    print('Login Failed\n')

while True:
    print('Courses with grades posted')
    r = s.post(gradeUrl, data=termData)
    soupTable = BeautifulSoup(r.content, 'html.parser').body.find('div', class_='pagebodydiv').find('table', class_='datadisplaytable').find_next_sibling('table')
    numTR = len(soupTable.find_all('tr'))
    result = soupTable.find('tr')
    for i in range(1,numTR):
        result = result.find_next_sibling('tr')
        resultData = result.find_all('td')
        print(resultData[1].get_text()+resultData[2].get_text())
    time.sleep(TIME_DELAY_IN_MINUTES*60)
