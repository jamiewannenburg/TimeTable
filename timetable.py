##### This is the main UI function #####

from DisplayFunctions import *
from ParseFunctions import *
from Subjects import *
from TimeTables import *
import csv
import glob

##### Get time table from internet #####

clear_screen()
try:
    with open('data/all_courses.csv', 'r') as f:
        reader=csv.reader(f)
        all_courses = [row for row in reader]
        f.close()
        write_all_courses = yn_input("Do you want to reload the time table? \n(Please make sure you have an internet connection)\n","N")
except IOError as e:
	print "Could not find file \"data/all_courses.csv\" "
	write_all_courses = True

if write_all_courses:
    print "Fetching time table from http://www.up.ac.za/timetables/hatfield_timetable.html ..."

    import urllib
    f = urllib.urlopen("http://www.up.ac.za/timetables/hatfield_timetable.html")
    all_courses_html = f.read()
    f.close()
    
    print "Done"
    
    print "Converting and writing to csv..."
    
    all_courses = parse_to_csv(all_courses_html)

    f=open('data/all_courses.csv','w')
    writer = csv.writer(f)
    writer.writerows(all_courses)
    f.close()

    print "Done"
    
##### Get list of subject_names #####

clear_screen()

try:
    with open('data/subject_names.csv', 'r') as f:
        reader=csv.reader(f)
        subject_names = [row for row in reader]
        subject_names = subject_names[0]
        f.close()
        print "Your current list of subject_names is"
        for subject in subject_names:
            print subject
        write_subject_names = yn_input("Do you want to change this list?","N")
except IOError as e:
    print "Could not find file \"data/subject_names.csv\" "
    write_subject_names = True

if write_subject_names:
    subject_names = input('Enter subject_names in inverted commas seperated by commas: ')
    f = open('data/subject_names.csv', 'w')
    writer = csv.writer(f)
    writer.writerows([subject_names])
    f.close()
    
##### Generate subject structure #####

print "Getting Student data"

subjects = get_subjects(all_courses,subject_names)

print "Done"

print "Found data for:"

for subject in subjects:
    print subject.name, " for semester ", subject.semester

print "\n"

##### Enter amount of permissible clashes #####

clashes = int(input("How many clashes are allowed? "))

print "Calculating possible timetables..."

time_tables = get_valid_time_tables(subjects,clashes)

print "Done"

print "You have ",len(time_tables)," choise/s  with less than ",clashes," clashes."


##### Print and save possible time table choises #####

print "Saving Possibilities..."

possible_times = []
for i in range(15):
	hour = i + 7
	if hour < 10:
		time = '0'+str(hour)+':30:00'
	else:
		time = str(hour)+':30:00'
	possible_times.append(time)

possible_days = ['Monday','Tuesday','Wednesday','Thursday','Friday']

# remove files

directory='data'
os.chdir(directory)
files=glob.glob('sem*.csv')
for filename in files:
    os.remove(filename)
os.chdir('..')


# make time table for each option

count_1 = 0
count_2 = 0
for time_table in time_tables:
    grootstring = 'Time,Monday,Venue,Tuesday,Venue,Wednesday,Venue,Thursday,Venue,Friday,Venue\n'
    if time_table.semester == 1:
        A=open('data/sem1option'+str(count_1)+'.csv','w')
        count_1 = count_1 + 1
    elif time_table.semester == 2:
        A=open('data/sem2option'+str(count_2)+'.csv','w')
        count_2 = count_2 + 1
        
    for time in possible_times:
        grootstring += time+','
        for day in possible_days:
            # insert all subject names of a specific time seperated by " and ".
            count = 0
            for check_time in time_table.slots:
                if (time == check_time.time)&(day == check_time.day):
                    if count == 0:
                        grootstring += check_time.subject
                    else:
                        grootstring += ' and '+ check_time.subject
                    count = count + 1
            grootstring += ','
            # insert all venues of a specific time seperated by " and ".
            count = 0
            for check_time in time_table.slots:
                if (time == check_time.time)&(day == check_time.day):
                    if count == 0:
                        grootstring += check_time.venue
                    else:
                        grootstring += ' and '+ check_time.venue
                    count = count + 1
            grootstring += ','
        grootstring+='\n'
    grootstring+='\n'
    S=A.write(grootstring)
    A.close()

print "Done"

# print options to command line

do_possibilities = yn_input("Do you want to go through the possibilities?","Y")
while do_possibilities:
    sem = raw_input("Which semester? 1, 2, or q to quit ")
    if sem == "q":
        do_possibilities = False
        break
    clear_screen()
    possibilities = len([0 for t in time_tables if t.semester == int(sem)])
    if possibilities==0:
        print 'No time tables for semester '+sem
    else:
        print 'The number of possibilities for sem '+sem+' is '+str(possibilities)
        
        perm = raw_input('Insert the number for the configuration you are interested in, starting at 0\n')
        
        while perm!="q":
            if int(perm) >= possibilities:
                print "Not a valid possibility"
            else:
                ifile  = open('data/sem'+sem+'option'+perm+'.csv', "r")
                reader = csv.reader(ifile)
                
                print_time_table(reader)
                
                ifile.close()
                print 'The number of possibilities for sem '+sem+' is '+str(len([0 for t in time_tables if t.semester == int(sem)]))
            perm = raw_input("New configuration or q to quit: ")
            clear_screen()

##### Upload to drive #####

clear_screen()

do_drive = yn_input("Do you want to upload files to google drive?","N")
while do_drive:
    sem = raw_input("Which semester? ")
    option = raw_input("Which option? ")
    ##### import functions #####
    from DriveFunctions import get_credentials
    from DriveFunctions import build_service
    from DriveFunctions import write_files_to_drive

    ##### get credentials #####
    credentials = get_credentials()

    ##### write to my_credentials #####
    file = open("data/my_credentials.json","w")
    file.write(credentials.to_json())
    file.close()

    ##### get drive service #####
    drive_service = build_service(credentials)

    ##### write files to drive #####
    title = 'Rooster Sem '+sem
    description = 'A test document'
    filename = 'data/sem'+sem+'option'+option+'.csv'
    write_files_to_drive(drive_service,title,description,filename)

    do_drive = not(yn_input("Are you done?","Y"))
