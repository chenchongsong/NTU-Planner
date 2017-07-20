#------------19/09/2016------------
#From MainPage of NTU Website
#Pull the value of option buttons
#Store value into 'option_list.json'

from xml.dom import minidom
import json




#input file
xml = minidom.parse('Class Schedule.xml')
#Original Url = https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main


option_tags = xml.getElementsByTagName('option')

courses = []

for i in range(len(option_tags)):
	option = option_tags[i]
	course = option.attributes['value'].value

	if course:
		courses.append(course)


#output file
write_json = open('option_list.json' , 'w+')
write_json.write(json.dumps(courses,ensure_ascii=False,indent=2))

write_json.close()


