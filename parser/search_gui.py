from Tkinter import *

master = Tk()
master.title("ICS Search")
master.geometry("1500x900")
frame = Frame(master)
frame.pack(side = TOP)
result_frame = Frame(master)
result_frame.pack(side = BOTTOM)

def callback():
    print text1.get()

text1 = Entry(frame, width =100)
text1.pack(side=LEFT)
b = Button(frame, text="Search", command= callback)
b.pack(side = RIGHT)

mainloop()