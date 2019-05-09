from tkinter import *

window = Tk()

def check():
    pass
''''''''''''''''''''''''''''''''''''''''''''#frame 1 (기본 메뉴 제작)

frame1 = Frame(window)
frame1.pack(side=LEFT)

RadioVariety_1=IntVar()     # 저장된 value값은 변수이름.get()을 통해서 불러올 수 있다.
radio1=Radiobutton(window, text="1번", value=3, variable=RadioVariety_1, command=check)
radio1.pack(side=LEFT)

radio2=Radiobutton(window, text="2번", value=6, variable=RadioVariety_1, command=check)
radio2.pack(side=LEFT)

radio3=Radiobutton(window, text="3번", value=9, variable=RadioVariety_1, command=check)
radio3.pack(side=LEFT)



''''''''''''''''''''''''''''''''''''''''''''#frame 2 (지도 및 기타 추가 메뉴 제작)
frame2 = Frame(window)
frame2.pack(side=RIGHT)

button2 = Button(frame2, text="test")
button2.pack(side=RIGHT)

window.mainloop()