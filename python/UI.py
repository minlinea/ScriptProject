from tkinter import *
from tkinter import ttk
from tkinter import font
import tkinter.messagebox

root = Tk()
root.geometry('800x500')

def title():
    Title_frame = Frame(root, width=400, height=25)     #로고 프레임
    Title_frame.place(x=400, y=25)
    title = Label(Title_frame, text='로고')
    title.pack()
    #title.place(x=400, y=25)


def highway_list():
    #global Highway_List
    Highway_frame = LabelFrame(root, text='고속도로 선택', width=150, height=10, padx=10, pady=15)
    Highway_frame.place(x=120, y=75)
    #Highway_Listbar = Scrollbar(Highway_frame)
    #Highway_Listbar.grid(column=3, row=1)

    Highway_stringlist = ["경부 고속도로", "남해 고속도로", "무안광주 고속도로", "광주대구 고속도로", "서해안 고속도로",
                          "울산 고속도로", "평택화성 고속도로", "수원광명 고속도로", "익산포항 고속도로",
                          "호남 고속도로", "논산천안 고속도로", "순천완주 고속도로", "세종포천 고속도로",
                          "당진영덕 고속도로", "옥산오창 고속도로", "통영대전 고속도로", "중부 고속도로", "통영대전 고속도로",
                          "중부 고속도로", "제2중부 고속도로", "평택제천 고속도로", "중부내륙 고속도로", "영동 고속도로",
                          "광주원주 고속도로", "중앙 고속도로", "중앙 고속도로(부산~대구)", "서울양양 고속도로",
                          "서울양양 고속도로(강일~춘천)", "동해·울산포항 고속도로", "동해 고속도로(부산~울산)",
                          "서울외곽순환 고속도로", "서울외곽순환 고속도로(일산~퇴계원)", "남해 고속도로 제1지선",
                          "남해 고속도로 제2지선", "남해 고속도로 제3지선", "경인 고속도로", "제2경인 고속도로",
                          "인천국제공항 고속도로", "서천공주 고속도로", "평택시흥 고속도로", "용인서울·오산화성 고속도로",
                          "대전남부순환 고속도로", "상주영천 고속도로", "수도권제2순환 고속도로", "중부내륙 고속도로 지선",
                          "중앙 고속도로 지선", "부산외곽순환 고속도로"]

    Highway_combo = ttk.Combobox(Highway_frame, width=30, height=20, values=Highway_stringlist, state='readonly')
    Highway_combo.pack()

    # Highway_List = Listbox(Highway_frame, selectmode=SINGLE, height=1, yscrollcommand=Highway_Listbar.set)
    # Highway_List.insert(1, "경부 고속도로")
    # Highway_List.insert(2, "남해 고속도로")
    '''

    Highway_List.insert(, "무안광주 고속도로")
    Highway_List.insert(, "광주대구 고속도로")
    Highway_List.insert(, "서해안 고속도로")
    Highway_List.insert(, "울산 고속도로")
    Highway_List.insert(, "평택화성 고속도로")
    Highway_List.insert(, "수원광명 고속도로")
    Highway_List.insert(, "익산포항 고속도로")
    Highway_List.insert(, "호남 고속도로")
    Highway_List.insert(, "논산천안 고속도로")
    Highway_List.insert(, "순천완주 고속도로")
    Highway_List.insert(, "세종포천 고속도로")
    Highway_List.insert(, "당진영덕 고속도로")
    Highway_List.insert(, "옥산오창 고속도로")
    Highway_List.insert(, "통영대전 고속도로")
    Highway_List.insert(, "중부 고속도로")
    Highway_List.insert(, "제2중부 고속도로")
    Highway_List.insert(, "평택제천 고속도로")
    Highway_List.insert(, "중부내륙 고속도로")
    Highway_List.insert(, "영동 고속도로")
    Highway_List.insert(, "광주원주 고속도로")
    Highway_List.insert(, "중앙 고속도로")
    Highway_List.insert(, "중앙 고속도로(부산~대구)")
    Highway_List.insert(, "서울양양 고속도로")
    Highway_List.insert(, "서울양양 고속도로(강일~춘천)")
    Highway_List.insert(, "동해·울산포항 고속도로")
    Highway_List.insert(, "동해 고속도로(부산~울산)")
    Highway_List.insert(, "서울외곽순환 고속도로")
    Highway_List.insert(, "서울외곽순환 고속도로(일산~퇴계원)")
    Highway_List.insert(, "남해 고속도로 제1지선")
    Highway_List.insert(, "남해 고속도로 제2지선")
    Highway_List.insert(, "남해 고속도로 제3지선")
    Highway_List.insert(, "경인 고속도로")
    Highway_List.insert(, "제2경인 고속도로")
    Highway_List.insert(, "인천국제공항 고속도로")
    Highway_List.insert(, "서천공주 고속도로")
    Highway_List.insert(, "평택시흥 고속도로")
    Highway_List.insert(, "용인서울·오산화성 고속도로")
    Highway_List.insert(, "대전남부순환 고속도로")
    Highway_List.insert(, "상주영천 고속도로")
    Highway_List.insert(, "수도권제2순환 고속도로")
    Highway_List.insert(, "중부내륙 고속도로 지선")
    Highway_List.insert(, "중앙 고속도로 지선")
    Highway_List.insert(, "부산외곽순환 고속도로")
    '''
    #Highway_List.grid(column=10, row=6)
    # Highway_List.pack(side=LEFT)
    # Highway_Listbar.pack(side=RIGHT)
    #Highway_List.place(x=550, y=75)



def search_location():
    pass

def search_gas_station():
    pass

def meal():
    pass


title()
category()  # 라디오 버튼 함수
highway_list()  # 고속도로 리스트박스


tkinter.mainloop()
