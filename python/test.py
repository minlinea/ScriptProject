# Commit Test by UiSai
from tkinter import *

window = Tk()

def check():
    pass

def search():
    address_label = Label(frame1, text = "주소 입력")
    address_label.pack(side=TOP)
    address_entry = Entry(frame1)
    address_entry.pack(side=BOTTOM)
''''''''''''''''''''''''''''''''''''''''''''#frame 1 (기본 메뉴 제작)


frame1 = Frame(window)
frame1.pack(side=LEFT)


RadioVariety_1=IntVar()     # 저장된 value값은 변수이름.get()을 통해서 불러올 수 있다.
radio1=Radiobutton(frame1, text="주소입력", value=3, variable=RadioVariety_1, command=search)
radio1.pack(side=LEFT)

radio2=Radiobutton(frame1, text="2번", value=6, variable=RadioVariety_1, command=check)
radio2.pack(side=LEFT)

radio3=Radiobutton(frame1, text="3번", value=9, variable=RadioVariety_1, command=check)
radio3.pack(side=LEFT)

''''''''''''''''''''''''''''''''''''''''''''#frame 2 (지도 및 기타 추가 메뉴 제작)

frame2 = Frame(window)
frame2.pack(side=RIGHT)

button1 = Button(frame2, text="210")
button1.pack(side=TOP)

button2 = Button(frame2, text="test")
button2.pack(side=TOP)

button3 = Button(frame2, text="1010")
button3.pack(side=TOP)

''''''''''''''''''''''''''''''''''''''''''''#frame 3 (입력, 명령 실행)

window.mainloop()