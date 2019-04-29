import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

TIME_DELAY_IN_MINUTES = 5
gradeUrl = 'https://central.carleton.ca/prod/bwskogrd.P_ViewGrde'
termData = {'term_in': 201910}

cookie_input = input()
cookie = {'SESSID': cookie_input}
soupTable = None
s = requests.Session()

while True:
    print('*'*15)
    print(str(datetime.now().strftime('%H:%M:%S')) + '\n')
    r = s.post(gradeUrl, data=termData, cookies=cookie)
    try:
        soupTable = BeautifulSoup(r.content, 'html.parser').body.find_all('table')[6]
    except IndexError:
        print('No grades yet')

    if soupTable:
        number_of_TR_elements = len(soupTable.find_all('tr')) - 1
        currentRow = soupTable.find('tr')
        for i in range(1, number_of_TR_elements + 1):
            currentRow = currentRow.find_next('tr')
            rowData = currentRow.find_all('td')
            print(rowData[1].get_text()+rowData[2].get_text())
    time.sleep(TIME_DELAY_IN_MINUTES*60)