from tkinter import *
from tkinter import ttk
from tkinter import Text
import telegram_run
import kakao_parsing
import RestArea_parsing
import tkinter.messagebox
import map
import sp

route_list = []
bookmark_route_list = [(),(),(),()]
now_RestArea = ()
root = Tk()
root.title("휴게소 검색")
root.geometry('800x600')
root.resizable(False, False)

Frame_pos = {                   #"~~Frame" : (x, y)로 추가
    "TitleFrame" : (30, 10), "HighwayFrame" : (30, 230), "RestareaFrame" : (30, 330),
    "RestareaMapFrame" : (400, 70), "InfoFrame" : (400, 320), "ButtonFrame" : (400, 10),
    "BookmarkFrame" : (400, 520)
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
    Title_frame = Frame(root, width=300, height=100)     #로고 프레임
    Title_frame.place(x = Frame_pos["TitleFrame"][0], y = Frame_pos["TitleFrame"][1])

    title_Canvas = Canvas(Title_frame, width=290, height=200)
    global logo_picture
    logo_picture = PhotoImage(file="logo.png")
    title_Canvas.create_image(150, 100, image=logo_picture)
    title_Canvas.pack()


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
    if (route_name == RESTAREA["0120"]):
        route_list.pop(0)
        route_list.pop(4)
        route_list.pop(5)
    elif (route_name == RESTAREA["0201"]):
        route_list.pop(2)
        route_list.pop(2)
    elif (route_name == RESTAREA["0252"]):
        route_list.pop(0)
        route_list.pop(0)
        route_list.pop(0)
        route_list.pop(0)
    elif (route_name == RESTAREA["0270"]):
        route_list.pop(0)
        route_list.pop(0)
    elif (route_name == RESTAREA["0301"]):
        route_list.pop(0)
        route_list.pop(2)
        route_list.pop(2)
    elif (route_name == RESTAREA["0352"]):
        route_list.pop(7)
        route_list.pop(7)
    elif (route_name == RESTAREA["0400"]):
        route_list.pop(3)
        route_list.append(("천등산휴게소(평택)",0,0))
    elif (route_name == RESTAREA["0500"]):
        route_list.pop(12)
        route_list.pop(12)
    for i in range(len(route_list)):
        text = route_list[i][0]
        restarea_Listbox.insert(i, text)


def select_result():                                #휴게소 선택에 대한 결과 출력
    global restarea_Listbox, Highway_combo, RESTAREA, route_list, RestAreaInfo_label, now_RestArea

    if(len(route_list) == 0):           #최초에 검색, 또는 휴게소가 없는 경우 새창을 띄워 그래프를 보여준다.
        Draw_Graph()

    else:
        result, x, y, flag = add_RestAreaInfo(route_list[restarea_Listbox.curselection()[0]][0],
                                  float(route_list[restarea_Listbox.curselection()[0]][1]),
                                  float(route_list[restarea_Listbox.curselection()[0]][2]))
        add_RestAreaMap(x,y)
        new_text = '특색 메뉴 : {0}\n입점 브랜드 : {1}\n편의시설 : {2}\n전화번호 : {3}\n주소 : {4}'.format(result[0],result[1],result[2],result[3],result[4])
        now_RestArea = (route_list[restarea_Listbox.curselection()[0]][0],
                                 x, y, new_text)
        RestAreaInfo_label.config(text = new_text)

def draw_RestAreaMap():                     #맵 프레임 구성 함수
    restareamap_frame = LabelFrame(root, text='휴게소 지도', width=310, height=200, padx=25, pady=15)
    restareamap_frame.place(x=Frame_pos["RestareaMapFrame"][0], y=Frame_pos["RestareaMapFrame"][1])
    global RestAreaMap_Canvas, Image_RestArea
    RestAreaMap_Canvas = Canvas(restareamap_frame, width=310, height=180)
    RestAreaMap_Canvas.pack()

def Draw_Graph():
    Graph_toplevel = tkinter.Toplevel(root)
    Graph_toplevel.title("휴게소 현황")
    Graph_toplevel.geometry("960x500")
    Graph_toplevel.resizable(False, False)

    graph_frame = Frame(Graph_toplevel)
    graph_frame.pack()
    canvas = Canvas(graph_frame, width = 900, height = 340, bg = 'white')
    canvas.pack()


    Highway_stringlist = [
        RESTAREA["0010"], RESTAREA["0100"], RESTAREA["0101"], RESTAREA["0120"],
        RESTAREA["0121"], RESTAREA["0140"], RESTAREA["0150"], RESTAREA["0153"],
        RESTAREA["0160"], RESTAREA["0170"], RESTAREA["0200"], RESTAREA["0201"],
        RESTAREA["0251"], RESTAREA["0252"], RESTAREA["0270"], RESTAREA["0300"],
        RESTAREA["0301"], RESTAREA["0351"], RESTAREA["0352"], RESTAREA["0370"],
        RESTAREA["0400"], RESTAREA["0500"], RESTAREA["0550"]
    ]
    barW = int((900 - 10 - 10) / len(RESTAREA))
    RESTAREA_count = [34,11,2,8,2,0,20,0,0,0,4,2,13,0,4,6,4,10,9,0,6,12,14]
    maxCount = max(RESTAREA_count)
    for i in range(len(RESTAREA)):
        canvas.create_rectangle(10 + barW * i + 5, 350 - 10, 10 + barW * (i + 1) - 5,
                                350 - 10 - 300 * (RESTAREA_count[i] / maxCount), fill="red")
        canvas.create_text(10 + barW * i + 5+15, 350 - 10 - 300 * (RESTAREA_count[i] / maxCount) - 10, text =RESTAREA_count[i])

        t = Label(Graph_toplevel, text=Highway_stringlist[i], wraplength='1')
        t.place(x = 10 + barW * i + 40, y =350)
    '''
    34 11 2 8 2 0 20 0 0 0 4 2 13 0 4 6 4 10 9 0 6 12 14
    '''

def add_RestAreaMap(x,y):                   #휴게소 검색시 좌표값이 존재한다면 구글 맵 띄워주는 함수
    global RestAreaMap_Canvas, Image_RestArea
    if(x == 0 or x == 0.0):             #해당 휴게소의 좌표가 없는 경우
        RestAreaMap_Canvas.delete(RestAreaMap_Canvas.find_all())            #캔버스 이미지 클리어
    else:
        Image_RestArea = map.Draw_MapImage(x, y)
        RestAreaMap_Canvas.create_image(160,100,image = Image_RestArea)     #155, 100만큼 이동해줘야 찍어낸다..


def Facility_Information():             #휴게소 정보 프레임
    Info_Frame = LabelFrame(root, text="휴게소 정보", width=330, height=200, padx=25, pady=15)
    Info_Frame.place(x=Frame_pos["InfoFrame"][0], y=Frame_pos["InfoFrame"][1])
    global RestAreaInfo_label, Image_RestArea
    RestAreaInfo_label = Label(Info_Frame, width=44, height=8)
    RestAreaInfo_label.pack()

def add_RestAreaInfo(RestAreaName,X,Y):                 #휴게소 정보 출력 함수
    return RestArea_parsing.Parsing_PublicData_Find_Facilities(RestAreaName,X,Y)

def Gather_Button():             #버튼 프레임
    Button_Frame = LabelFrame(root, width=360, height=50, padx=25, pady=15)
    Button_Frame.place(x=Frame_pos["ButtonFrame"][0], y=Frame_pos["ButtonFrame"][1])

    help_button = Button(Button_Frame, text='help', width=10, height=1, command=help_program)
    help_button.pack(side="left")

    telegram_button = Button(Button_Frame, text='telegram', width=10, height=1, command=turnon_telegram)
    telegram_button.pack(side = "left")

    mail_button = Button(Button_Frame, text='mail', width=10, height=1, command=send_mail)
    mail_button.pack(side="left")

    exit_button = Button(Button_Frame, text = 'exit', width=10, height = 1, command = program_end)
    exit_button.pack(side = "left")

def Bookmark_Button():      #북마크 프레임
    Bookmark_Frame = LabelFrame(root, text='북마크', width=370, height=50, padx=25, pady=15)
    Bookmark_Frame.place(x=Frame_pos["BookmarkFrame"][0], y=Frame_pos["BookmarkFrame"][1])

    Bookmark_Button1 = Button(Bookmark_Frame, text=1, width=10, height=1, command=Bookmark_Input1)
    Bookmark_Button1.pack(side="left")
    Bookmark_Button2 = Button(Bookmark_Frame, text=2, width=10, height=1, command=Bookmark_Input2)
    Bookmark_Button2.pack(side="left")
    Bookmark_Button3 = Button(Bookmark_Frame, text=3, width=10, height=1, command=Bookmark_Input3)
    Bookmark_Button3.pack(side="left")
    Bookmark_Button4 = Button(Bookmark_Frame, text=4, width=10, height=1, command=Bookmark_Input4)
    Bookmark_Button4.pack(side="left")
    #for i in range(4):
        #bookmark_bbutton[i] = Button(Bookmark_Frame, text=i, width=10, height=1, command=Bookmark_Input(i))

def Bookmark_Input1():
    global bookmark_route_list, now_RestArea
    bookmark_route_list[0] =now_RestArea
    tkinter.messagebox.showinfo("북마크 1번", "내용 추가")

def Bookmark_Input2():
    global bookmark_route_list, route_list
    bookmark_route_list[1] =now_RestArea
    tkinter.messagebox.showinfo("북마크 2번", "내용 추가")

def Bookmark_Input3():
    global bookmark_route_list, route_list
    bookmark_route_list[2] =now_RestArea
    tkinter.messagebox.showinfo("북마크 3번", "내용 추가")

def Bookmark_Input4():
    global bookmark_route_list, route_list
    bookmark_route_list[3] =now_RestArea
    tkinter.messagebox.showinfo("북마크 4번", "내용 추가")

def help_program():
    Help_toplevel = tkinter.Toplevel(root)
    Help_toplevel.title("도움말")
    Help_toplevel.geometry("300x75")
    Help_toplevel.resizable(False, False)


    search_frame = Frame(Help_toplevel)
    search_frame.pack()
    search_Label = Label(search_frame, text="입력[ Highway , Restarea , Button,  RInfo , Bookmark ]", )
    search_Label.pack()
    search_Button = Button(search_frame, text="검색", command = search_help)
    search_Button.pack(side='bottom')
    global search_Input
    search_Input = Entry(search_frame, width = 20)
    search_Input.pack(side='bottom')

def search_help():
    global search_Input
    ntype = sp.strcmp(search_Input.get())
    if (ntype == 0):
        tkinter.messagebox.showerror("검색어 없음", "해당하는 검색어가 없습니다.")
    elif (ntype == 2): #Highway
        msg = '박스를 누르면 전국의 고속도로 목록이 나옵니다.\n원하는 고속도로를 선택하고 "검색"버튼을 눌러주세요.'
        tkinter.messagebox.showinfo(search_Input.get(), msg)
    elif (ntype == 3): #Restarea
        msg = '앞서 검색한 고속도로에 위치한 모든 휴게소가 표시됩니다.\n정보를 보고 싶은 휴게소를 선택하고 "검색"버튼을 눌러주세요.\n빈 목록 상태에서 검색 시 해당 고속도로에서 검색가능한 휴게소 현황 그래프가 보여집니다.'
        tkinter.messagebox.showinfo(search_Input.get(), msg)
    elif (ntype == 4): #Button
        msg = 'help : 이 도움말을 표시합니다.\ntelegram : 텔레그램 봇을 작동시킵니다.\nmail : 메일을 보내기 위한 양식을 표시합니다.\nexit : 프로그램을 종료합니다.'
        tkinter.messagebox.showinfo(search_Input.get(), msg)
    elif (ntype == 5): #RInfo
        msg = '검색한 휴게소의 정보가 표시됩니다.\n1. 특색메뉴\n2. 입점 브랜드\n3. 편의시설\n4. 전화번호\n5. 주소'
        tkinter.messagebox.showinfo(search_Input.get(), msg)
    elif (ntype == 6):  #Bookmark
        msg = '현재 휴게소를 즐겨찾기에 추가합니다.\n메일을 보낼 때 첨부됩니다.'
        tkinter.messagebox.showinfo(search_Input.get(), msg)

def turnon_telegram():
    telegram_run.work_telegram()

def send_mail():

    Mail_toplevel = tkinter.Toplevel(root)
    Mail_toplevel.title("메일 발송")
    Mail_toplevel.geometry("400x400")
    Mail_toplevel.resizable(False, False)

    Send_Frame = Frame(Mail_toplevel, width=380, height=450, padx=25, pady=15)
    Send_Frame.pack(side=TOP)

    mail_Label = Label(Send_Frame, text ="사용자(보내는 사람)의 이메일 주소를 입력해주세요", anchor = 'center', justify='center')
    mail_Label.place(x=0,y=0)

    global mail_Input
    mail_Input = Entry(Send_Frame, width = 46)
    mail_Input.place(x=0, y= 25)

    add_Label = Label(Send_Frame, text="내용 입력 ", anchor = 'center', justify=CENTER)
    add_Label.place(x=0, y= 50)

    global add_Post
    add_Post = Text(Send_Frame, width = 46, height=20)
    add_Post.place(x=0, y= 75)

    Send_Button = Button(Send_Frame, text = "메일 전송", command = Send_mail)
    Send_Button.place(x=140, y= 350)

def Send_mail():
    global mail_Input, add_Post
    import mimetypes
    import mysmtplib
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText

    # global value
    host = "smtp.naver.com"  # Gmail STMP 서버 주소.
    port = "587"

    senderAddr = "min_linea@naver.com"
    recipientAddr = mail_Input.get()  # 받는 사람 email 주소.

    msg = MIMEBase("multipart", "비밀번호는 조큼..")
    msg['Subject'] = "휴게소 검색 프로그램"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    text = add_Post.get(1.0, END) + '\n'
    for i in range(4):
        text += '\n'
        for j in range (len(bookmark_route_list[i])):
            text += str(bookmark_route_list[i][j]) + ' '
            if j == 2:
                text += '\n'
        text += '\n'
    comment = MIMEText(text, _charset='utf-8')
    msg.attach(comment)

    # 메일을 발송한다.
    s = mysmtplib.MySMTP(host, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("min_linea@naver.com","storyline1!")
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()


def program_end():
    exit()

def search_location():
    pass


title()            #로고
highway_list()  # 고속도로 콤보박스
restarea_list() # 휴게소 리스트 박스
Facility_Information()  #휴게소 정보
draw_RestAreaMap()      #휴게소 맵
Gather_Button()         #도움, 텔레그램, 메일, 나가기 버튼
Bookmark_Button()       #북마크 버튼
tkinter.mainloop()
