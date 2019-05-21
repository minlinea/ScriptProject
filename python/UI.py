from tkinter import *
from tkinter import font
import tkinter.messagebox

root = Tk()
root.geometry('800x500')

def main():
    Title_frame = Frame(root, width=400, height=25)     #로고 프레임
    Title_frame.pack()
    Title_frame.place(x=400, y=25)
    title = Label(Title_frame, text='로고')
    title.pack()
    #title.place(x=400, y=25)
    category()      # 라디오 버튼 함수



def category():
    #global RadioBox
    Category_frame = LabelFrame(root, text='찾을 장소 선택')      #라디오 버튼 프레임
    Category_frame.place(x=50, y=75)

    cat = IntVar()
    Category_radio1 = Radiobutton(Category_frame, text='휴게소', variable=cat, value=1)
    Category_radio1.pack()
    Category_radio1.select()
    Category_radio2 = Radiobutton(Category_frame, text='주유소', variable=cat, value=2)
    Category_radio2.pack()

def search_location():
    pass

def search_gas_station():
    pass

def meal():
    pass


main()


tkinter.mainloop()