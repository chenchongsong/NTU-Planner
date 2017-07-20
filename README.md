NTU-Planner is a project that helps NTU students sort out unclashed timetables on stars-planner
receiving help from Zhihao Sun & Lua

package requirement:

BeautifulSoup Requests etc.

Usage of NTU-Planner Project:
 

Class Schedule.xml ---(Option List Maker)---> option_list.json
 
option_list.json ---(HTML_crawler)---> Data_Base
 
Data_Base ---(HTML analyze)---> course_data
 
course_data ---(Main)---> Solution.txt
 
Solution.txt