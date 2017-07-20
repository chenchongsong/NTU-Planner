#Analyze html documents
#Create course_data.py

#input 'Data_Base\_Class Schedule(i).html'
#output 'Data_Base\course_data.py'

from bs4 import BeautifulSoup

Dict_Day = {
    'MON': 0,
    'TUE': 1,
    'WED': 2,
    'THU': 3,
    'FRI': 4,
    'SAT': 5
}

data={}


def Append_Start_Duration(Day, Period, Ans):

    #Append Starting Time to Ans
    Hour = int(Period[0:2])
    Minute = int(Period[2:4])
    Start = (Hour - 8) * 2 + (Minute - 30) / 30
    Start += Dict_Day[Day] * 30
    Ans.append(int(Start))
    
    #Append Ending Time to Ans
    Hour = int(Period[5:7])
    Minute = int(Period[7:9])
    End = (Hour - 8) * 2 + (Minute - 30) / 30
    End += Dict_Day[Day] * 30
    Ans.append(int(End-1))

def Append_Week(Weeks, Ans):
    if Weeks == 'None':
        Ans.append(2**13-1)
        return
    Cnt = 0
    Weeks = ',' + Weeks[2:] + ','
    while Weeks.find('-') != -1:
        curr = prev = succ = Weeks.find('-')
        while Weeks[prev] != ',':
            prev -= 1
        while Weeks[succ] != ',':
            succ += 1
        for i in range(int(Weeks[prev+1:curr]), int(Weeks[curr+1:succ])+1):
            Cnt += 2**(i-1)
        Weeks = Weeks[:prev] + Weeks[succ:]
    Weeks = Weeks[1:]
    while Weeks.find(',') != -1:
        curr = Weeks.find(',')
        current_week = int(Weeks[:curr])
        Cnt += 2**(current_week-1)
        Weeks = Weeks[curr+1:]
    Ans.append(Cnt)


def Grab_Data():
    current_table = soup.table
    table_counter = 0
    global data
    while current_table is not None:
        table_counter+=1
        
        if table_counter % 2 == 1:  #A table for course title
            current_course = str(current_table.b.string)
            current_coursename = str(current_table.td.find_next('td').string)
            if current_course not in data.keys():
                data[current_course] = [0, current_coursename]
            current_table = current_table.find_next("table")
            continue;
        
        #A table for index of the course
        tr_list = current_table.find_all("tr")

        ans_index = [-1]
        ans_course = [0]

        for current_tr in tr_list[1:]:  #for each row of the table

            td_list = current_tr.find_all("td")
            current_index = td_list[0].string

            
            if current_index is None:
                ans_index[0] += 1

            else:
                #New Index Found
                ans_course[0] += 1
                ans_course.append(str(current_index))
                if current_index not in data[current_course]:
                    data[current_course][0] += 1
                    list_len = len(data[current_course])
                    data[current_course] = data[current_course][:list_len-1] + [str(current_index)] + data[current_course][list_len-1:]
                if ans_index[0] != -1:
                    fout.write(str(ans_index))                    
                    #data[current_index] = str(ans_index)
                    fout.write(",\n")

                ans_index = [1]  #Initialize numbers of rows for current_index
                
                fout.write("    '"+current_index+"':")


            #print str(td_list[3].string)

            if str(td_list[3].string) == ' ':  #Useless Course, e.g.Online Course    
                for i in range(3):
                    ans_index.append(0)

            else:
                #print 'OK1'
                Append_Start_Duration(str(td_list[3].string),str(td_list[4].string),ans_index)
                #print "OK2"
                #print str(td_list[6].string)
                Append_Week(str(td_list[6].string),ans_index)
                #print "OK3"

            #Using binary representation:

            




        #Handling the End of Last Index
        fout.write(str(ans_index))
        #data[current_index] = str(ans_index)
        fout.write(',\n')

        '''
        ans_course.append(current_coursename)
        fout.write("    '"+current_course+"':")
        fout.write(str(ans_course))
        fout.write(",\n")'''

        current_table = current_table.find_next("table")

fout = open("course_data.py", "w")
fout.write('#Usage: put it in the same working forlder, then import course_data\n#SCSE Year1 AY16-17\n')
fout.write('Data = {\n')
for i in range(1,9):
    fin = open("Data_Base"+"/"+"Class Schedule"+str(i)+'.html', 'r').read()
    print (str(i)+'------------------\n')

    fout.write('#From _Class Schedule'+str(i)+'.html\n')
    fin = fin.replace("&nbsp;"," ")
    #print fin
    soup = BeautifulSoup((fin),'html.parser')
    Grab_Data()

fout.write('#The relationship of Course-->Index\n')
for key, value in data.items():
    fout.write("    '"+key+"':"+str(value)+",\n")

print ("OK")
fout.write("}\n")
fout.close()
print ("OK")
