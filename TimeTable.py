from Tkinter import *
import Tkinter
from AutocompleteEntry import AutocompleteEntry
from UserOptionsDB import UserOptionsDB
from AllCoursesDB import AllCoursesDB
from TimeTableDB import TimeTableDB

user_options = UserOptionsDB()
all_courses = AllCoursesDB()
time_table_db = TimeTableDB()

class RowCursor:
    def __init__(self):
        self.row = 0
    def get(self):
        self.row = self.row + 1
        return self.row

def Notice(context,message):
    NoticeLabel = Label(context, text = message)
    NoticeLabel.pack()
    NoticeLabel.after(2000, NoticeLabel.destroy)
    

top = Tk()

# Frames
GetCoursesFrame = Frame(top)
GetCoursesFrame.pack()

SubjectsFrame = Frame(top)
SubjectsFrame.pack()

TimeTablesFrame = Frame(top)
TimeTablesFrame.pack()

DriveFrame = Frame(TimeTablesFrame)
DriveFrame.pack(side = BOTTOM)

TimeTableFrame = Frame(TimeTablesFrame)
TimeTableFrame.pack(side = BOTTOM)

# Courses Functions
def GetCoursesCallback():
    # download from web
    try:
        Notice(GetCoursesNotice,"Downloading Courses")

        # add to database
        all_courses.parse(campuses)

        # Gui Respose
        #global course_list
        course_list = all_courses.get_courses()
        SubjectEntry.set_completion_list(tuple(course_list))
        Notice(GetCoursesNotice,"Succesfully Downloaded Courses")
    except IOError:
        Notice(GetCoursesNotice,"Connection Error")

    

# Get Courses Elements
courses_row = RowCursor()

GetCoursesNotice = Frame(GetCoursesFrame)
GetCoursesNotice.grid(row=courses_row.row, column=0)

campuses = {'Hatfield':['http://www.up.ac.za/timetables/hatfield_timetable.html',IntVar()],
        'Engineering':['http://www.up.ac.za/timetables/eng_timetable.html',IntVar()],
        'Mamelodi':['http://www.up.ac.za/timetables/mamelodi_timetable.html',IntVar()],
        'Groenkloof':['http://www.up.ac.za/timetables/groenkloof_timetable.html',IntVar()]}
courses_row.get()
for i,campus in enumerate(campuses):
    Checkbutton(GetCoursesFrame,text=campus,variable=campuses[campus][1]).grid(row=courses_row.row,column=i)

Button(GetCoursesFrame, text="Download Courses", command = GetCoursesCallback ).grid(row=courses_row.get(),column=0,columnspan=4)

# Subjects Functions
def add_subject(name):
    row = subject_row.row
    global col_counter
    if col_counter == 3:
        row = subject_row.get()
        col_counter = 0
        
    SubjectLabel = Label(SubjectsList, text=name)
    SubjectLabel.grid(row=row,column=col_counter*2)
    SubjectRemove = Button(SubjectsList, text="Remove", command = lambda: RemoveCallback(name,SubjectLabel,SubjectRemove)) 
    SubjectRemove.grid(row=row,column=col_counter*2+1)
    col_counter += 1

def RemoveCallback(name,s_label,s_button):
    global subject_names
    s_label.destroy()
    s_button.destroy()
    subject_names.remove(name)
    user_options.write('subject_names',subject_names)

def AddSubjectCallback(*args):
    global subject_names
    name = SubjectEntry.get().upper()
    # check if name already exists
    if name in subject_names:
        Notice(SubjectsNotice,"Already Chose This Subject")
    elif name == '':
        Notice(SubjectsNotice,"Can Not be Empty")
    else:
        add_subject(name)
        subject_names.append(name)
        user_options.write('subject_names',subject_names)

course_list = all_courses.get_courses()

# Subjects Elements

subject_frame_row = RowCursor()

SubjectsNotice = Frame(SubjectsFrame)
SubjectsNotice.grid(row=subject_frame_row.row,column=0,columnspan=2)

frame_row = subject_frame_row.get()
SubjectEntry = AutocompleteEntry(SubjectsFrame)
SubjectEntry.set_completion_list(tuple(course_list))
SubjectEntry.bind("<Return>",AddSubjectCallback)
SubjectEntry.grid(row=frame_row,column=0)

Button(SubjectsFrame, text="Add Subject", command = AddSubjectCallback ).grid(row=frame_row,column=1,sticky=W)

Label(SubjectsFrame,text = 'Current Courses Are:').grid(row=subject_frame_row.get(),column=0)

SubjectsList = Frame(SubjectsFrame)
SubjectsList.grid(column=0,columnspan=2)

subject_names = user_options.read('subject_names')
col_counter = 0
subject_row = RowCursor()

if subject_names:
    for name in subject_names:
        add_subject(name)
else:
    subject_names = []

# Time Table Functions

def RefreshTableCallback():
    
    user_options.write('user_semester',user_semester.get())
    user_options.write('user_permutation',user_permutation.get())
    UpdatePermSelect()
    make_table()

def TimeTableCallBack():
    
    user_options.write('user_clashes',user_clashes.get())
    
    len1,len2 = all_courses.get_valid_time_tables(subject_names,user_clashes.get())

    global options1,option2
    options1 = range(len1)
    options2 = range(len2)
    user_options.write('options1',options1)
    user_options.write('options2',options2)

    UpdatePermSelect()

    make_table()

def make_table():
    possible_days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    possible_times = []
    
    for i in range(15):
    	hour = i + 7
    	if hour < 10:
    		time = '0'+str(hour)+':30:00'
    	else:
    		time = str(hour)+':30:00'
    	possible_times.append(time)
    
    for i,time in enumerate(possible_times):
        for j,day in enumerate(possible_days):
            subject,venue = time_table_db.get_subject(user_semester.get(),user_permutation.get(),day,time)
            table_vars[i][j]['subject'].set(subject)
            table_vars[i][j]['venue'].set(venue)

def UpdatePermSelect():
    forget = user_permutation.get()
    if user_semester.get() == 1:
        PermSelect.config(values=tuple(options1),textvariable=user_permutation,command=RefreshTableCallback)
    else:
        PermSelect.config(values=tuple(options2),textvariable=user_permutation,command=RefreshTableCallback)  
    user_permutation.set(forget)

options1 = user_options.read("options1")
if not options1:
    options1 = [0]

options2 = user_options.read("options2")
if not options2:
    options2 = [0]
    

user_permutation = IntVar()
if user_options.read("user_permutation"):
    user_permutation.set(user_options.read("user_permutation"))
else:
    user_permutation.set(0)


user_semester = IntVar()
if user_options.read("user_semester"):
    user_semester.set(user_options.read("user_semester"))
else:
    user_semester.set(1)

user_clashes = IntVar()
if user_options.read("user_clashes"):
    user_clashes.set(user_options.read("user_clashes"))
else:
    user_clashes.set(0)

# Time Table Elements

Label(TimeTablesFrame,text="Clashes ").pack()
ClashesSelect = Spinbox(TimeTablesFrame,values=(0,1,2,3,4),textvariable=user_clashes)
ClashesSelect.pack()

Button(TimeTablesFrame, text="Calculate Time Tables", command=TimeTableCallBack ).pack()

SemesterLabel = Label(TimeTablesFrame,text="Semester ")
SemesterLabel.pack(side=LEFT)

SemesterSelect= Spinbox(TimeTablesFrame)
forget = user_semester.get()
SemesterSelect.config(values=(1,2),textvariable=user_semester,command=RefreshTableCallback)
user_semester.set(forget)
SemesterSelect.pack(side=LEFT)

OptionLabel = Label(TimeTablesFrame,text="Option ")
OptionLabel.pack(side=LEFT)

PermSelect = Spinbox(TimeTablesFrame)
UpdatePermSelect()
PermSelect.pack(side=LEFT)

RefreshButton = Button(TimeTablesFrame,text="Refresh",command = RefreshTableCallback)
RefreshButton.pack(side = LEFT)

possible_days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
possible_times = []

#TimeTableFrame
table_vars = []
for i in range(15):
    hour = i + 7
    if hour < 10:
        time = '0'+str(hour)+':30:00'
    else:
        time = str(hour)+':30:00'
    possible_times.append(time)

for j, day in enumerate(possible_days):
    Label(TimeTableFrame,text=day).grid(row=0,column=(j*2)+1)
    Label(TimeTableFrame,text='Venue').grid(row=0,column=(j*2)+2)
    
for i,time in enumerate(possible_times):
    Label(TimeTableFrame,text=time).grid(row=i+1,column=0)
    table_vars.append([])
    for j,day in enumerate(possible_days):
        #print user_semester.get(),user_permutation.get()
        subject,venue = time_table_db.get_subject(user_semester.get(),user_permutation.get(),day,time)
        
        table_vars[i].append({'subject':StringVar(),'venue':StringVar()})
        table_vars[i][j]['subject'].set(subject)
        table_vars[i][j]['venue'].set(venue)
        Label(TimeTableFrame,textvariable=table_vars[i][j]['subject']).grid(row=i+1,column=(j*2)+1)
        Label(TimeTableFrame,textvariable=table_vars[i][j]['venue']).grid(row=i+1,column=(j*2)+2)
    
# Drive Functions
def DriveCallback():
    ##### write csv #####
    
    possible_days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    possible_times = []
    
    for i in range(15):
    	hour = i + 7
    	if hour < 10:
    		time = '0'+str(hour)+':30:00'
    	else:
    		time = str(hour)+':30:00'
    	possible_times.append(time)

    big_string = ""    	

    for j, day in enumerate(possible_days):
        big_string += day + ',Venue,'
    big_string += '\n'
    for i,time in enumerate(possible_times):
        big_string += time + ','
        
        for j,day in enumerate(possible_days):
            subject,venue = time_table_db.get_subject(user_semester.get(),user_permutation.get(),day,time)
            big_string += subject + ',' + venue + ','
        big_string += '\n'
        
    with open('data/sem'+str(user_semester.get())+'.csv','w') as f:
        f.write(big_string)
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
    title = 'Time Table Sem '+str(user_semester.get())
    description = 'A test document'
    filename = 'data/sem'+str(user_semester.get())+'.csv'
    write_files_to_drive(drive_service,title,description,filename)

# Drive Elements
DriveButton = Button(DriveFrame, text="Add To Drive",command=DriveCallback)
DriveButton.pack()

top.mainloop()
