from tkinter import *
from tkinter import ttk
from tkinter import font
import kakao_parsing
import RestArea_parsing
import tkinter.messagebox
import map

root = Tk()
root.title("휴게소 검색")
root.geometry('800x500')
root.resizable(False, False)

Frame_pos = {                   #"~~Frame" : (x, y)로 추가
    "TitleFrame" : (30, 10), "HighwayFrame" : (30, 50), "RestareaFrame" : (30, 130), "RestareaMapFrame" : (400, 60),
    "InfoFrame" : (400, 310)
}

RESTAREA = {
    "0010" : "경부선", "0100" : "남해선", "0101" : "남해선(영암-순천)", "0120" : "88올림픽선",
    "0121" : "무안광주선", "0140" : "고창담양선", "0150" : "서해안선" , "0153" : "평택시흥선",
    "0160" : "울산선", "0170" : "평택화성선", "0200" : "대구포항선", "0201" : "익산장수선",
    "0251" : "호남선", "0252" : "천안논산선", "0270" : "순천완주선", "0300" : "청원상주선" ,
    "0301" : "당진대전선", "0351" : "중부선(대전통영)", "0352" : "중부선", "0370" : "제2중부선",
    "0400" : "평택제천선", "0500" : "중부내륙선", "0550" : "영동선"
}



def title():                    #로고
    Title_frame = Frame(root, width=30, height=25)     #로고 프레임
    Title_frame.place(x = Frame_pos["TitleFrame"][0], y = Frame_pos["TitleFrame"][1])
    title = Label(Title_frame, text='로고')
    title.pack()


def highway_list():                                #고속도로 콤보박스
    Highway_frame = LabelFrame(root, text='고속도로 선택', width=300, height=10, padx=25, pady=15)
    Highway_frame.place(x = Frame_pos["HighwayFrame"][0], y = Frame_pos["HighwayFrame"][1])

    global RESTAREA
    Highway_stringlist = [
        RESTAREA["0010"], RESTAREA["0100"], RESTAREA["0101"], RESTAREA["0120"],
        RESTAREA["0121"], RESTAREA["0140"], RESTAREA["0150"], RESTAREA["0153"],
        RESTAREA["0160"], RESTAREA["0170"], RESTAREA["0200"], RESTAREA["0201"],
        RESTAREA["0251"], RESTAREA["0252"], RESTAREA["0270"], RESTAREA["0300"],
        RESTAREA["0301"], RESTAREA["0351"], RESTAREA["0352"], RESTAREA["0370"],
        RESTAREA["0400"], RESTAREA["0500"], RESTAREA["0550"]
    ]
    global Highway_combo
    Highway_combo = ttk.Combobox(Highway_frame, width=25, height=20, values=Highway_stringlist, state='readonly')
    Highway_combo.pack(side=LEFT)

    Search_Button = Button(Highway_frame, text="검색", command=add_restarea_list)
    Search_Button.pack(side=RIGHT)

def restarea_list():                                #해당 고속도로에 대한 휴게소 리스트박스
    global restarea_Listbox
    restarea_frame = LabelFrame(root, text='휴게소 목록', width=400, height=500, padx=23, pady=15)
    restarea_frame.place(x = Frame_pos["RestareaFrame"][0], y = Frame_pos["RestareaFrame"][1])

    restarea_scrollbar = Scrollbar(restarea_frame)
    restarea_scrollbar.pack(side = RIGHT, fill="y")


    restarea_Listbox = Listbox(restarea_frame, width = 30, yscrollcommand = restarea_scrollbar.set)
    restarea_Listbox["activestyle"] = "none"
    restarea_Listbox.pack()
    restarea_scrollbar["command"]=restarea_Listbox.yview

    Search_Button = Button(restarea_frame, text="검색", command=select_result, width=30)
    Search_Button.pack(side=BOTTOM)

def add_restarea_list():                            #고속도로 검색에 대한 휴게소 목록 추가 함수
    global restarea_Listbox, Highway_combo, RESTAREA, route_list
    restarea_Listbox.delete(0,restarea_Listbox.size())
    route_list = []
    for route_num, route_name in RESTAREA.items():
        if(route_name == Highway_combo.get()):
            route_list = RestArea_parsing.Parsing_PublicData_Find_Find_route(route_num)
            break
    for i in range(len(route_list)):
        text = route_list[i][0]
        restarea_Listbox.insert(i, text)


def select_result():                                #휴게소 선택에 대한 결과 출력
    global restarea_Listbox, Highway_combo, RESTAREA, route_list, RestAreaInfo_label
    add_RestAreaMap(float(route_list[restarea_Listbox.curselection()[0]][1]),
                    float(route_list[restarea_Listbox.curselection()[0]][2]))
    result = add_RestAreaInfo(route_list[restarea_Listbox.curselection()[0]][0])
    RestAreaInfo_label.config(text = result)

def draw_RestAreaMap():                     #맵 프레임 구성 함수
    restareamap_frame = LabelFrame(root, text='휴게소 지도', width=300, height=200, padx=25, pady=15)
    restareamap_frame.place(x=Frame_pos["RestareaMapFrame"][0], y=Frame_pos["RestareaMapFrame"][1])
    global RestAreaMap_Canvas, Image_RestArea
    RestAreaMap_Canvas = Canvas(restareamap_frame, width=300, height=180)
    RestAreaMap_Canvas.pack()

def add_RestAreaMap(x,y):                   #휴게소 검색시 좌표값이 존재한다면 구글 맵 띄워주는 함수
    global RestAreaMap_Canvas, Image_RestArea
    if(x == 0):             #해당 휴게소의 좌표가 없는 경우
        RestAreaMap_Canvas.delete(RestAreaMap_Canvas.find_all())            #캔버스 이미지 클리어
    else:
        Image_RestArea = map.Draw_MapImage(x, y)
        RestAreaMap_Canvas.create_image(155,100,image = Image_RestArea)     #155, 100만큼 이동해줘야 찍어낸다..


def Facility_Information():             #휴게소 정보 프레임
    Info_Frame = LabelFrame(root, text="휴게소 정보", width=300, height=200, padx=25, pady=15)
    Info_Frame.place(x=Frame_pos["InfoFrame"][0], y=Frame_pos["InfoFrame"][1])
    global RestAreaInfo_label, Image_RestArea
    RestAreaInfo_label = Label(Info_Frame, width=39, height=8)
    RestAreaInfo_label.pack()

def add_RestAreaInfo(RestAreaName):                 #휴게소 정보 출력 함수
    return RestArea_parsing.Parsing_PublicData_Find_Facilities(RestAreaName)


def search_location():
    pass



title()            #로고
highway_list()  # 고속도로 콤보박스
restarea_list() # 휴게소 리스트 박스
Facility_Information()  #휴게소 정보
draw_RestAreaMap()      #휴게소 맵

tkinter.mainloop()
