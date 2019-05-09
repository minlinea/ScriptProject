from tkinter import *

window = Tk()


frame1 = Frame(window)
frame1.pack(side=LEFT)
frame2 = Frame(window)
frame2.pack(side=RIGHT)
button1 = Button(frame1, text="test")
button1.pack(side=LEFT)
button2 = Button(frame2, text="no")
button2.pack(side=RIGHT)

window.mainloop()