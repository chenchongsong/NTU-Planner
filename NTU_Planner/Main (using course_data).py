import course_data

Data = course_data.Data
Final_Ans = {}
Map = []
Num = int(input('How many courses do you have??\n'))
course_list = []
Cnt = 0



for i in range(300):
    Map.append(0)

def Solve(index_list):
    
    global Ans
    global Num
    global Map
    global course_list
    global Data
    global Cnt

    step = len(index_list)
    if step >= Num:
        Cnt += 1
        Final_Ans[Cnt] = index_list[:]

        #print ('Cnt ',Cnt)
        #print (index_list)
        #print ('Finally, ',Final_Ans)
        return
    #print ('step==',step)
    #print (index_list)

    for i in Data[course_list[step]][1:-1]:  #i is an index
        
        Tmp_Hour = []
        Tmp_Wk = []

        #print (Data[course_list[step]])
        #print ('i==',i)

        flag = True
        
        for j in range(1, 1 + 3*Data[i][0],3): #j is the current position in the list

            if flag == False:
                break

            #print ('    j==',j)

            for k in range(Data[i][j],Data[i][j+1]+1): #Hour

                #print ('        k==',k)

                cell = Map[k] & Data[i][j+2] # Week

                if cell == 0:
                    #print("Good")

                    Map[k] |= Data[i][j+2]
                    
                    Tmp_Hour.append(k)
                    Tmp_Wk.append(Data[i][j+2])

                    #print (Map[k])
                    #print (Tmp_Hour)
                    #print (Tmp_Wk)
                    

                else:            #Clash:useless index
                    #print ("Bad")
                    flag = False
                    break
        if flag == True: # no Clash at all
            #print ("ADDed")
            index_list.append(i)
            Solve(index_list)
            del index_list[step]

        for l in range(len(Tmp_Hour)):
            Map[Tmp_Hour[l]] ^= Tmp_Wk[l]

        #print (Map)
        #print (Tmp_Hour)
        #print (Tmp_Wk)
        
    
for i in range(1,Num+1):
    if i==1:
        print ("Enter the 1st course:")
    elif i==2:
        print ("Enter the 2nd course:")
    elif i==3:
        print ("Enter the 3rd course:")
    else:
        print ("Enter the "+str(i)+'th course:')
    course_list.append(input().upper())

Solve([])


#print (course_list)
#print (Final_Ans)


with open('Solution.txt','w') as f:

    for i in Final_Ans.keys():
    
        f.write ('\nSolution '+str(i)+' : \n')
        f.write (str(Final_Ans[i])+'\n')
    

