# -*- coding: utf-8 -*-

import sys
import requests
from queue import Queue, Empty
from threading import Thread
import json
from bs4 import BeautifulSoup

queue = Queue()

content = ""
with open('option_list.json', 'r') as content_file:
    content = content_file.read()

courses = json.loads(content)
#courses = ['ACC;GA;1;F']

result = {}

url = "https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1"

Cnt = 0

data = {
    'acadsem' : '2016;1',
    'r_course_yr' :'',
    'r_subj_code' : 'Enter Keywords or Course Code',
    'r_search_type' : 'F',
    'boption' : 'CLoad' , 
    'acadsem' : '2016;1',
    'staff_access' : 'false'
}

headers = {
    'Cache-Control' : 'no-cache',
    #'Cookie' : '__utma=149387945.1676156346.1459760584.1461222499.1461225759.2; __utmz=149387945.1461222499.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ezlibproxy1=l0X3MsJ6t9CuApE; NTU40B9E5E3814AF8F53F147BCF5859DE911336=8329F062A2A86C43636A563A93130BED3458174C7404FA10BEBC5D5291689B43A54C7F531D7C732A21981EA134A94F8E5; NTUC1B83482055D7101AC5D9BAD51BE96D30943=324328B52AB3E7F5A3514D23A0DA75ADA285B05A5F6E436D87CAF0961B968A25C27E43EF6678C9B09C5C7EF20D0F2DD8F; NTU045FAFB384C8720E28255E563E1894FE1644=28ECBE0A345795EC5DE92AC7DA34620BEEA5142679B006392E5A109F15E95BE7EDB1CC3758057F58420E1CB0F9FB831C2; cadata15F14350EF25460A97EB85F03D3A3D99="283a372d0-bc93-4e42-8f65-487c352df8bcqr0TYliTiO96H8cV50JlnftXZ/dNAuL3AqBF7hbCkZqmk8dhZOYbcKSxZwxrRfkoJT7QRNVJHLqXWTGIgeVDKqlNOTK3oVvujT4sWYYf5Pymr2QI6+hyfgzOLqrKMgCIO+6hTLvRtVoGZMB58lLvf+nAv8oHiSy18PXP68GQOu4="; NTU97D3FFD5D1504B332088748B7B1B1C602346=20BC54EEA8D16D3ADF4A05981BB6AA3B41F9006C358C3FCDE05D7B37D70C363A4731CF96D048C37F70995BB74D8AA7B6E; NTUBB4F504D69313AB9F82F385C6DB9D8E31921=3D01A47E89E5C355967B8350856EF967FD1242254215CBA9683C2E54A3271AF49D13492ED3490B06C22526D0EE6504A8C; NTU4FC194DEBCA832BD85CAD9222CCCE6811443=2C03B49E3B100523403F3A1F0C5BE2B5B097CE09EA2FDE61D7D6E842E8A495864331A55CC249376D5CD10A9AD063DDBA6; NTU789F9DA4E0AED8999D7CACD30D1B254C1732=7CB8C64860DA1D9BDEA58AD4AB812162EE5CE8789780C4139140510D2524D0AF83AE09FD51C7A8DF8DBE30B4447FC5266; ntutestcookie=TEST; NTU97C56748062BD09BD1E290A1AE78DBE42125=321FB73FD60104848A65081E836E938A5A4CA49F53C8A9F97250361B5C8566130BECFF4547DB00C52DAAE5FD57EB8A887; mstrImpersonateFlag=N; myNTUid=385DCFAB98B590DE4D8A705DD8A48A87CA44273310098B55FAFBEF6DEDC51C7A4497639FBB683D651; mobi=N; WT_FPC=id=172.22.180.182-3417577088.30510672:lv=1473993106290:ss=1473993099241; _ga=GA1.3.1676156346.1459760584',
    #'Cookie':'WT_FPC=id=172.20.164.178-2623109728.30557707:lv=1484213854441:ss=1484213849591; _ga=GA1.3.1866562666.1479961882; _gat=1',
    'Connection' : 'keep-alive',
    'Referer' : 'https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main'
}

def process(content):
    


    soup = BeautifulSoup(content, "html.parser")
    #process the html content
    global Cnt
    Cnt += 1
    print (str(Cnt)+'---------------------------')
    
    fout = open("Data_Base\_Class Schedule"+ str(Cnt) +".html","w")
    fout.write(content)
    fout.close()

    
    tables = soup.find_all('table')
    count = len(tables)

    modules = []
    even = True

    for table in tables:
        if even:
            even = False
            # print table.text
            # tr = table.find('TR')
            # tds = tr.find_all('TD')

            # module = ''

            # for td in tds:
            #     module += td.text.strip() + ';'

            # print module
            modules.append(table.text.strip())

        else:
            even = True
    return modules

def get_parser():

    def parse():
        try:
            while True:
                course = queue.get_nowait()
                
                data['r_course_yr'] = course

                r = requests.post(url, data = data , headers = headers , verify=False)

                print ('------------------------\n'+course+'\n')
                result[course] = process(r.text.encode('utf-8'))
                
        except Empty:
            pass

    return parse


parser = get_parser()

for course in courses:
    queue.put(course)
    result[course] = {}

workers = []
for i in range(425):
    worker = Thread(target=parser)
    worker.start()
    workers.append(worker)
for worker in workers:
    worker.join()

write_json = open('Data_Base\courses_result.json' , 'w+')
write_json.write(json.dumps(result,ensure_ascii=False,indent=2)
                 .encode('utf8'))
