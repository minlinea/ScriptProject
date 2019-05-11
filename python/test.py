from tkinter import *

window = Tk()
window.title("test page")
window.geometry("640x400")
window.resizable(False, False)

def check():
    pass

def address_search():
    address_label = Label(frame1, text = "주소 입력")
    address_label.pack()
    address_entry = Entry(frame1)
    address_entry.pack()

def location_search():
    location_label = Label(frame1, text="주소 입력")
    location_label.pack()
    location_entry = Entry(frame1)
    location_entry.pack()
''''''''''''''''''''''''''''''''''''''''''''#frame 1 (기본 메뉴 제작)


frame1 = Frame(window)
frame1.pack(side=LEFT)


RadioVariety_1=IntVar()     # 저장된 value값은 변수이름.get()을 통해서 불러올 수 있다.
radio1=Radiobutton(frame1, text="주소입력", value=3, variable=RadioVariety_1, command=address_search)
radio1.pack(side=LEFT)

radio2=Radiobutton(frame1, text="위도 및 경도 입력", value=6, variable=RadioVariety_1, command=location_search)
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