from tkinter import *
from tkinter import ttk
from tkinter import font
import kakao_parsing
import tkinter.messagebox

root = Tk()
root.title("휴게소 검색")
root.geometry('800x500')
root.resizable(False,False)
RESTAREA = {
    "0010" : "경부선", "0100" : "남해선", "0101" : "남해선(영암-순천)", "0120" : "88올림픽선",
    "0121" : "무안광주선", "0140" : "고창담양선", "0150" : "서해안선" , "0153" : "평택시흥선",
    "0160" : "울산선", "0170" : "평택화성선", "0200" : "대구포항선", "0201" : "익산장수선",
    "0251" : "호남선", "0252" : "천안논산선", "0270" : "순천완주선", "0300" : "청원상주선" ,
    "0301" : "당진대전선", "0351" : "중부선(대전통영)", "0352" : "중부선", "0370" : "제2중부선",
    "0400" : "평택제천선", "0500" : "중부내륙선", "0550" : "영동선"
}



def title():
    Title_frame = Frame(root, width=400, height=25)     #로고 프레임
    Title_frame.place(x=400, y=25)
    title = Label(Title_frame, text='로고')
    title.pack()
    #title.place(x=400, y=25)


def highway_list():
    Highway_frame = LabelFrame(root, text='고속도로 선택', width=150, height=10, padx=10, pady=15)
    Highway_frame.place(x=120, y=75)

    global RESTAREA
    Highway_stringlist = [
        RESTAREA["0010"], RESTAREA["0100"],RESTAREA["0101"],RESTAREA["0120"],
        RESTAREA["0121"],RESTAREA["0140"],RESTAREA["0150"],RESTAREA["0153"],
        RESTAREA["0160"],RESTAREA["0170"],RESTAREA["0200"],RESTAREA["0201"],
        RESTAREA["0251"],RESTAREA["0252"],RESTAREA["0270"],RESTAREA["0300"],
        RESTAREA["0301"],RESTAREA["0351"],RESTAREA["0352"],RESTAREA["0370"],
        RESTAREA["0400"],RESTAREA["0500"],RESTAREA["0550"]
    ]
    Highway_combo = ttk.Combobox(Highway_frame, width=30, height=20, values=Highway_stringlist, state='readonly')
    Highway_combo.pack()

def restarea_list():
    global Highway_List
    Highway_Listbar = Scrollbar(root)

    Highway_List = Listbox(root, height=5, yscrollcommand=Highway_Listbar.set)
    Highway_List.pack(side=LEFT)

    Highway_Listbar.config(command=Highway_List.yview)
    Highway_Listbar.pack(side=BOTTOM, fill = "y")
    Highway_List.config(yscrollcommand=Highway_Listbar.set)


def search_location():
    pass

def search_gas_station():
    pass

def meal():
    pass

def category():
    pass
title()
category()  # 라디오 버튼 함수
highway_list()  # 고속도로 리스트박스
restarea_list()

tkinter.mainloop()
