from tkinter import *

''''''''''''''''''''''''''''''''''''''''''''#window (윈도우 옵션)

window = Tk()
window.title("test page")
window.geometry("640x400")
window.resizable(False, False)

''''''''''''''''''''''''''''''''''''''''''''#window (윈도우 옵션)

''''''''''''''''''''''''''''''''''''''''''''#frame 1 (기본 메뉴 제작)

def address_search():
    location_label_x = Label(frame1, text="주소")
    location_label_x.place(x = 10, y = 135)
    location_entry_x = Entry(frame1, width=42)
    location_entry_x.place(x = 40, y = 135)

    push_keyword = Button(frame1, text="검색")
    push_keyword.place(x = 350, y = 130)

def location_search():
    location_label_x = Label(frame1, text="x")
    location_label_x.place(x = 10, y = 135)
    location_entry_x = Entry(frame1, width=20)
    location_entry_x.place(x = 25, y = 135)

    location_label_y = Label(frame1, text="y")
    location_label_y.place(x=180, y=135)
    location_entry_y = Entry(frame1, width=20)
    location_entry_y.place(x=195, y=135)

    push_location = Button(frame1, text="검색")
    push_location.place(x = 350, y = 130)

def keyword_search():
    location_label_x = Label(frame1, text="키워드")
    location_label_x.place(x = 10, y = 135)
    location_entry_x = Entry(frame1, width=40)
    location_entry_x.place(x = 60, y = 135)

    push_keyword = Button(frame1, text="검색")
    push_keyword.place(x = 350, y = 130)

frame1 = Frame(window, width = 400, height = 160)
frame1.place(x=0, y=0)

RadioVariety_1=IntVar()     # 저장된 value값은 변수이름.get()을 통해서 불러올 수 있다.
radio1=Radiobutton(frame1, text="주소 검색", value=3, variable=RadioVariety_1, command=address_search)
radio1.place(x = 50, y = 100)

radio2=Radiobutton(frame1, text="좌표 검색", value=6, variable=RadioVariety_1, command=location_search)
radio2.place(x = 150, y = 100)

radio3=Radiobutton(frame1, text="키워드 검색", value=9, variable=RadioVariety_1, command=keyword_search)
radio3.place(x = 250, y = 100)

photo = PhotoImage(file="test.png")
imageLabel = Label(frame1, width=400, height=90, image=photo)
imageLabel.place(x = 0, y = 0)


''''''''''''''''''''''''''''''''''''''''''''#frame 1 (기본 메뉴 제작)

''''''''''''''''''''''''''''''''''''''''''''#frame 2 (지도 및 기타 추가 메뉴 제작)
text_button_width, text_button_height = 15, 1

frame2 = Frame(window, width = 240, height = 400)       # 가로 크기: 160, 세로 크기: 400
frame2.place(x=400, y=0)                                # 시작 좌표 x: 480, y: 0

button1 = Button(frame2, text="Help", width = text_button_width, height = text_button_height)
button1.place(x = 0, y = 5)                           # 윈도우 내 좌표 x: 480 + 0, y: 5

button2 = Button(frame2, text="Mail", width = text_button_width, height = text_button_height)
button2.place(x = 120, y = 5)                          # 윈도우 내 좌표 x: 480 + 120, y: 5

button3 = Button(frame2, text="Telegram", width = text_button_width, height = text_button_height)
button3.place(x = 0, y = 30)                           # 윈도우 내 좌표 x: 480 + 0, y: 30

button4 = Button(frame2, text="Exit", width = text_button_width, height = text_button_height)
button4.place(x = 120, y = 30)                         # 윈도우 내 좌표 x: 480 + 120, y: 30

map_canvas = Canvas(frame2, width=230, height=240, bg="white")
map_canvas.place(x = 0, y = 60)                            # 윈도우 내 좌표 x: 480 + 0, y: 60

label = Label(frame2, text="이미지가 표시된 주소", width=30, height=4, bg="white")
label.place(x = 10, y = 320)                            # 윈도우 내 좌표 x: 480 + 0, y: 320
''''''''''''''''''''''''''''''''''''''''''''#frame 2 (지도 및 기타 추가 메뉴 제작)
''''''''''''''''''''''''''''''''''''''''''''#frame 3 (검색결과 창)
frame3 = Frame(window, width = 380, height = 280)

listbox = Listbox(frame3, width = 53, height = 14)
text = "(우)15073 경기도 시흥시 산기대학로 237 (정왕동) "
for i in range(10):
   listbox.insert(i, text)
listbox.pack(side="left", fill="y")

scrollbar = Scrollbar(frame3)
scrollbar.pack(side="right", fill="y")
scrollbar.config(command=listbox.yview)

listbox.config(yscrollcommand=scrollbar.set)

frame3.place(x=10, y=160)
''''''''''''''''''''''''''''''''''''''''''''#frame 3 (검색결과 창)

''''''''''''''''''''''''''''''''''''''''''''# (입력, 명령 실행)
''''''''''''''''''''''''''''''''''''''''''''# (입력, 명령 실행)

window.mainloop()