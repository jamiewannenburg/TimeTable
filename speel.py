from Tkinter import *

top = Tk()

GetCoursesFrame = Frame(top)
GetCoursesFrame.pack()

TimeTablesFrame = Frame(top)
TimeTablesFrame.pack()

TimeTableFrame = Frame(TimeTablesFrame)
TimeTableFrame.pack(side = BOTTOM)

def TimeTableCallBack():
    global perm
    perm = PermSelect.get()
    print perm
    global options
    options.append(perm+ClashesSelect.get())
    PermSelect.config(values=options)
    

Label(TimeTablesFrame,text="Clashes ").pack()
ClashesSelect = Spinbox(TimeTablesFrame,values=(0,1,2,3,4))
ClashesSelect.pack()
Button(TimeTablesFrame, text="Calculate Time Tables", command=TimeTableCallBack ).pack()

options=[0,1,2,3,4,5]
perm = 0
OptionLabel = Label(TimeTablesFrame,text="Option ")
OptionLabel.pack(side=LEFT)
#global PermSelect
PermSelect = Spinbox(TimeTablesFrame,values=options)
PermSelect.insert(0,perm)
PermSelect.pack(side=LEFT)

top.mainloop()