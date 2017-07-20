import json
import requests

url = "https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1"

data = {
    'acadsem' : '2016;2',
    'r_course_yr' :'ACC;GA;1;F',
    'r_subj_code' : 'Enter Keywords or Course Code',
    'r_search_type' : 'F',
    'boption' : 'CLoad' ,
    'staff_access' : 'false'
}

headers = {
    'Cache-Control' : 'no-cache',
    'Cookie':'_ga=GA1.3.1394424444.1491997769',
    'Connection' : 'keep-alive',
    'Referer' : 'https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display'
}
r = requests.post(url, data = data , headers = headers , verify=False)
#r = requests.post(url, data = data, verify = False)
with open("test.html", "w") as fout:
    fout.write(str(r.text.encode('utf-8')))

fout.close()

