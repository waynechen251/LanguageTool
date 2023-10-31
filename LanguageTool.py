import time, os, sys, subprocess
from ftplib import FTP
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
#by waynechen251 email:waynechen251@digiwin.com

###
# -*- coding: utf-8 -*-
def select_path():
    path = filedialog.askdirectory()
    Field_path.delete("1.0", "end")
    Field_path.insert("end", path)

def logger(msg):
    nowtime = time.strftime("%H:%M:%S", time.localtime())
    Field_log.configure(state='normal')
    Field_log.insert("end", nowtime+" "+msg+"\n")
    Field_log.configure(state='disabled')
    Field_log.see("end")
    print(nowtime+" "+msg)

def add():
    id_text = Field_id.get("1.0", "end")
    tw_text = Field_tw.get("1.0", "end")
    cn_text = Field_cn.get("1.0", "end")
    vi_text = Field_vi.get("1.0", "end")
    en_text = Field_en.get("1.0", "end")
    th_text = Field_th.get("1.0", "end")

    readyList_id = []
    readyList_tw = []
    readyList_cn = []
    readyList_vi = []
    readyList_en = []
    readyList_th = []

    ids = id_text.split("\n")
    tws = tw_text.split("\n")
    cns = cn_text.split("\n")
    vis = vi_text.split("\n")
    ens = en_text.split("\n")
    ths = th_text.split("\n")

    del ids[-1]
    del tws[-1]
    del cns[-1]
    del vis[-1]
    del ens[-1]
    del ths[-1]

    for id in ids:
        readyList_id.append(id)
    for tw in tws:
        readyList_tw.append(tw)
    for cn in cns:
        readyList_cn.append(cn)
    for vi in vis:
        readyList_vi.append(vi)
    for en in ens:
        readyList_en.append(en)
    for th in ths:
        readyList_th.append(th)

    len_id = len(readyList_id)
    len_tw = len(readyList_tw)
    len_cn = len(readyList_cn)
    len_vi = len(readyList_vi)
    len_en = len(readyList_en)
    if(check_containTH.get()==True):
        len_th = len(readyList_th)
    else:
        len_th = len(readyList_id)

    if(len_id==len_tw==len_cn==len_vi==len_en==len_th):
        idIsnull = False
        twIsnull = False
        cnIsnull = False
        viIsnull = False
        enIsnull = False
        thIsnull = False

        path=Field_path.get("1.0", "end-1c")+'/'
        filename=Field_filename.get("1.0", "end-1c")+".txt"

        for i in range(0, len_id):
            if(readyList_id[i]=="" or readyList_id[i]=="\n"):
                idIsnull = True
            if(readyList_tw[i]=="" or readyList_tw[i]=="\n"):
                twIsnull = True
            if(readyList_cn[i]=="" or readyList_cn[i]=="\n"):
                cnIsnull = True
            if(readyList_vi[i]=="" or readyList_vi[i]=="\n"):
                viIsnull = True
            if(readyList_en[i]=="" or readyList_en[i]=="\n"):
                enIsnull = True
            if(check_containTH.get()==True):
                if(readyList_th[i]=="" or readyList_th[i]=="\n"):
                    thIsnull = True
        if(idIsnull==True or twIsnull==True or cnIsnull==True or viIsnull==True or enIsnull==True or thIsnull==True):
            logger("Error: 偵測到空值")
        elif(Field_path.get("1.0","end-1c")==""):
            logger("Error: 請指定輸出路徑")
        elif(Field_filename.get("1.0","end-1c")==""):
            logger("Error: 請輸入檔案名稱")
        elif(not os.path.isdir(path)):
            logger("Error: 此目錄不存在 "+path)
        elif(readyList_id[0]!="" and readyList_tw[0]!="" and readyList_cn[0]!="" and readyList_vi[0]!="" and readyList_en[0]!="" and readyList_th[0]!=""):
            logger("Info: 語系數量相等，開始產生SQL語句")
            start_create_lang(readyList_id, readyList_tw, readyList_cn, readyList_vi, readyList_en, readyList_th)
        else:
            logger("Error: 未輸入語系資料")
    else:
        logger("Error: 語系數量不相等")

def start_create_lang(readyList_id, readyList_tw, readyList_cn, readyList_vi, readyList_en, readyList_th):
    do_i = 0
    do=True
    path=Field_path.get("1.0", "end-1c")+'/'
    filename=Field_filename.get("1.0", "end-1c")+".txt"

    if(check_killexistFile.get()==True):
        try:
            if(os.path.isfile(path+filename)):
                os.remove(path+filename)
                logger("Info: 已刪除檔案 "+path+filename)
            else:
                logger("Info: 未發現檔案 "+path+filename)
        except:
            logger("Info: 刪除檔案 "+path+filename+" 失敗")

    while do==True:

        id=readyList_id[do_i]
        text_tw=readyList_tw[do_i]
        text_cn=readyList_cn[do_i]
        text_vi=readyList_vi[do_i]
        text_en=readyList_en[do_i]
        text_th=readyList_th[do_i]

        if(check_containTH.get()==True):
            output=f"IF NOT EXISTS ( SELECT TOP 1 1 FROM dbo.[LANGUAGE]  WHERE ID = N'{id}')\n\t"
            output+=f"INSERT dbo.[LANGUAGE] (ID, ZH_TW, ZH_CN, VI_VN, EN_US, TH_TH) VALUES (N'{id}', N'{text_tw}', N'{text_cn}', N'{text_vi}', N'{text_en}', N'{text_th}')\nELSE\n\t"
            output+=f"UPDATE dbo.[LANGUAGE] SET ZH_TW = N'{text_tw}', ZH_CN = N'{text_cn}', VI_VN = N'{text_vi}', EN_US = N'{text_en}', TH_TH = N'{text_th}'  WHERE ID = N'{id}'\n\n"
        else:
            output=f"IF NOT EXISTS ( SELECT TOP 1 1 FROM dbo.[LANGUAGE]  WHERE ID = N'{id}')\n\t"
            output+=f"INSERT dbo.[LANGUAGE] (ID, ZH_TW, ZH_CN, VI_VN, EN_US) VALUES (N'{id}', N'{text_tw}', N'{text_cn}', N'{text_vi}', N'{text_en}')\nELSE\n\t"
            output+=f"UPDATE dbo.[LANGUAGE] SET ZH_TW = N'{text_tw}', ZH_CN = N'{text_cn}', VI_VN = N'{text_vi}', EN_US = N'{text_en}'  WHERE ID = N'{id}'\n\n"

        with open(path+filename, "a+", encoding="utf-8") as f:
            f.write(output)

        Field_log.configure(state='normal')
        Field_log.insert("end", output)
        Field_log.configure(state='disabled')
        Field_log.see("end")
        print(output)

        if(do_i==len(readyList_id)-1):
            do=False
            logger("Info: 已輸出檔案 "+filename+" 到路徑 "+path)
        else:
            do_i+=1

    openOpfilemsg = messagebox.askquestion("提示", "是否打開輸出檔案?")
    if(openOpfilemsg=="yes"):
        subprocess.Popen(path+filename,shell = True)
###
def creat_new_label(_text, _row, _column): #文字,行,列
    temp = ttk.Label(root, text=_text)
    temp.grid(row=_row, column=_column)

    return temp

def creat_new_button(_text, _command, _row, _column): #文字,事件,行,列
    temp = ttk.Button(root, command=_command, text=_text)
    temp.grid(row=_row, column=_column)

    return temp

def creat_new_text(_height, _width, _row, _column):
    temp = tk.Text(root, height=_height, width=_width)
    temp.grid(row=_row, column=_column)

    return temp

def clearAll():
    clearAllmsg = messagebox.askquestion("提示", "是否清除所有內容?")
    if(clearAllmsg=="yes"):
        Field_id.delete("1.0","end")
        Field_tw.delete("1.0","end")
        Field_cn.delete("1.0","end")
        Field_vi.delete("1.0","end")
        Field_en.delete("1.0","end")
        Field_th.delete("1.0","end")

        logger("Info: 清除所有內容")

def menu_exit():
    exitBoxmsg = messagebox.askquestion("提示", "是否離開本程式?")
    if(exitBoxmsg=="yes"):
        root.destroy()

def menu_help_exit(helpwin):
    helpwin.destroy()

def loadExample():
    loadExamplemsg = messagebox.askquestion("提示", "是否載入範例?")
    if(loadExamplemsg=="yes"):
        Field_id.insert("end", "JS_0012_00012\n")
        Field_tw.insert("end", "己啟動\n")
        Field_cn.insert("end", "己启动\n")
        Field_vi.insert("end", "Đã khởi động\n")
        Field_en.insert("end", "Activated\n")
        Field_th.insert("end", "เปิดใช้แล้ว\n")

        Field_id.insert("end", "JS_0012_00013\n")
        Field_tw.insert("end", "注意\n")
        Field_cn.insert("end", "注意\n")
        Field_vi.insert("end", "Chú ý\n")
        Field_en.insert("end", "Note\n")
        Field_th.insert("end", "Note\n")

        Field_id.insert("end", "JS_0012_00014")
        Field_tw.insert("end", "請選擇公司別資料")
        Field_cn.insert("end", "请选择公司别数据")
        Field_vi.insert("end", "Xin chọn dữ liệu mục công ty")
        Field_en.insert("end", "Select Company")
        Field_th.insert("end", "กรุณาเลือกข้อมูลบริษัท")
        logger("Info: 載入範例")
    else:
        pass

def menu_help():
    helpwin = tk.Toplevel(root)
    helpwin.title("使用說明")
    helpwin.geometry("600x400")
    helpwin.resizable(False, False)

    help_menubar = tk.Menu(helpwin)
    help_menu = tk.Menu(help_menubar)
    help_menu.add_command(label="關閉使用說明", command=lambda:menu_help_exit(helpwin))
    helpwin.config(menu=help_menu)

    help_text = tk.Text(helpwin, height=30, width=82)
    help_text.insert("end", "刪除已存在檔案:\n")
    help_text.insert("end", "\t打勾會刪除原有檔案\n")
    help_text.insert("end", "\t未打勾則會在原有檔案最後新增語系\n")
    help_text.insert("end", "檔案輸出路徑:\n")
    help_text.insert("end", "\t選取語系檔生成後輸出的路徑，注意寫入權限，目標在C槽有可能無法寫入\n\n")
    help_text.insert("end", "檔案輸出名稱:\n")
    help_text.insert("end", "\t請輸入檔名，附檔名預設為.txt\n\n")
    help_text.insert("end", "語系ID:\n")
    help_text.insert("end", "\t填入要新增的語系ID-繁中-簡中-越南文-英文-泰文必須以一組為單位做新增\n")
    help_text.insert("end", "\t注意，每組之間以Enter為分隔判斷\n\n")
    help_text.insert("end", "執行:\n")
    help_text.insert("end", "\t開始執行SQL語系產生，若有訊息會在事件紀錄窗口出現\n\n")
    help_text.insert("end", "您也可以透過選單>載入範例進行測試\n\n")
    help_text.insert("end", "本程式使用 Python 3.8 編寫，透過 Pyinstaller 打包執行檔，可在未安裝 Python 環境裝置上執行。\n")
    help_text.insert("end", "Source Code為壓縮檔內 LanguageTool.py\n")
    help_text.insert("end", "日後若要進行功能調整皆可修改\n\n")
    help_text.insert("end", "LanguageTool2exe.bat 可自動進行檔案打包與生成rar壓縮檔，使用方式為:\n")
    help_text.insert("end", "\t1.需安裝 Python 3 並安裝 pyinstaller 套件\n")
    help_text.insert("end", "\t2.需安裝 WinRAR\n")
    help_text.insert("end", "\t3.將 LanguageTool.py 與 LanguageTool2exe.bat 檔案放置在同一目錄下，並以系統管理員執行批次檔即可\n")
    help_text.configure(state='disabled')
    help_text.grid(row=0, column=0, sticky=tk.S + tk.W + tk.E + tk.N)
    help_text_scroll = ttk.Scrollbar(helpwin, orient="vertical",command=help_text.yview)
    help_text.config(yscrollcommand = help_text_scroll.set)
    help_text_scroll.grid(row=0, column=1, sticky=tk.S + tk.W + tk.E + tk.N)

def keyevent(event):
    if(event.keysym=="F1"):
        menu_help()
    elif(event.keysym=="F2"):
        loadExample()
    elif(event.keysym=="F3"):
        clearAll()
    elif(event.keysym=="F4"):
        menu_exit()
def onlineUpdate():
    testMode=0
    exitBoxmsg = messagebox.askquestion("提示", "是否更新本程式?")
    if(testMode==0):
        if(exitBoxmsg=="yes"):
            #root.destroy()
            logger("更新功能還沒做好，想不到吧")
            logger(sys.executable)
    elif(testMode==1):
        if(exitBoxmsg=="yes"):
            path=sys.executable.split('\\LanguageTool.exe')[0]
            ftpInfo ="open 10.40.140.172\n"
            ftpInfo+="user dci\n"
            ftpInfo+="70614749\n"
            ftpInfo+="prompt off\n"
            ftpInfo+="cd /SFT_code/LanguageTool\n"
            ftpInfo+=f"lcd {path}\n"
            ftpInfo+=f"get LanguageTool.exe\n"
            ftpInfo+=f"bye"

            with open(path+"\\ftp.txt", "a+", encoding="utf-8") as f:
                f.write(ftpInfo)
            f.close()

            updateBat ="@echo off\n"
            updateBat+="timeout /t 1\n"
            updateBat+=f"del {path}\\LanguageTool.exe\n"
            updateBat+=f"ftp -n -s:{path}\\ftp.txt\n"
            updateBat+="timeout /t 3\n"
            updateBat+=f"start {path}\\LanguageTool.exe\n"
            updateBat+=f"del {path}\\ftp.txt\n"
            updateBat+=f"del {path}\\update.bat\n"
            updateBat+=f"pause"

            with open(path+"\\update.bat", "a+", encoding="utf-8") as f:
                f.write(updateBat)
            f.close()

            root.destroy()
            subprocess.Popen(f'start {path}\\update.bat',shell = True)
    else:
        if(exitBoxmsg=="yes"):
            path=sys.executable.split('\\LanguageTool.exe')[0]
            print(path)
            ip="10.40.140.172"
            port=21
            timeout=30

            ftp = FTP()
            ftp.set_pasv(True)
            ftp.connect(ip,port,timeout) # 連線FTP伺服器
            ftp.login("dci","70614749") # 登入
            ftp.cwd("/SFT_code/LanguageTool")    # 設定FTP路徑
            filename=""
            files=ftp.nlst()
            for file in files:
                if('.exe' in file):
                    filename = file
                    break
            f = open(path+"\\_LanguageTool.exe",'wb')
            ftp.retrbinary(f'RETR {filename}',f.write)
            f.close()
            ftp.quit()

            updateBat ="@echo off\n"
            updateBat+=f"del {path}\\LanguageTool.exe\n"
            updateBat+=f"move {path}\\_LanguageTool.exe {path}\\LanguageTool.exe\n"
            updateBat+=f"start {path}\\LanguageTool.exe\n"
            updateBat+=f"del {path}\\update.bat"
            with open(path+"\\updateBat.bat", "a+", encoding="utf-8") as u:
                u.write(updateBat)
            u.close()

            root.destroy()
            subprocess.Popen(f'start {path}\\update.bat',shell = True)

###
root=tk.Tk()
root.resizable(False, False)
root.title("語系小幫手 Ver1.1")
root.geometry("960x600")

_height=25
_width=22

root.bind_all('<KeyPress>', keyevent)

menubar = tk.Menu(root)
menubar.add_command(label="使用說明(F1)", command=menu_help)
menubar.add_command(label="載入範例(F2)", command=loadExample)
menubar.add_command(label="清除資料(F3)", command=clearAll)
menubar.add_command(label="結束程式(F4)", command=menu_exit)
menubar.add_command(label="更新程式", command=onlineUpdate)
root.config(menu=menubar)

check_killexistFile = tk.BooleanVar()
check_killexistFile.set(False)
checkbox_killexistFile = tk.Checkbutton(root, text='刪除已存在檔案', var=check_killexistFile)
checkbox_killexistFile.grid(row=0, column=0)

check_containTH = tk.BooleanVar()
check_containTH.set(False)
checkbox_containTH = tk.Checkbutton(root, text='是否產生泰文欄位', var=check_containTH)
checkbox_containTH.grid(row=0, column=1)

Label_ver = creat_new_label("程式最後更新日期: 2021/4/13",0,4)

Label_path = creat_new_label("檔案輸出路徑:",1, 0)
Field_path = tk.Text(root, height=1, width=65)
Field_path.grid(row=1, column=1, columnspan=3)
path_btn = creat_new_button("選擇路徑", select_path, 1, 4)

Label_filename = creat_new_label("檔案輸出名稱:", 2, 0)
Field_filename = tk.Text(root, height=1, width=65)
Field_filename.grid(row=2, column=1, columnspan=3)

Label_id = creat_new_label("語系ID",3,0)
Field_id = creat_new_text(_height, _width, 4, 0)

Label_tw = creat_new_label("繁體中文",3,1)
Field_tw = creat_new_text(_height, _width, 4, 1)

Label_cn = creat_new_label("簡體中文",3,2)
Field_cn = creat_new_text(_height, _width, 4, 2)

Label_ci = creat_new_label("越南文",3,3)
Field_vi = creat_new_text(_height, _width, 4, 3)

Label_en = creat_new_label("英文",3,4)
Field_en = creat_new_text(_height, _width, 4, 4)

Label_th = creat_new_label("泰文",3,5)
Field_th = creat_new_text(_height, _width, 4, 5)

creat_new_label("事件記錄窗口:",8,0)
Field_log = tk.Text(root, height=10, width=110)
Field_log.configure(state='disabled')
Field_log.grid(row=9, column=0, columnspan=6, sticky=tk.S + tk.W + tk.E + tk.N)
scroll = ttk.Scrollbar(orient="vertical",command=Field_log.yview)
Field_log.config(yscrollcommand = scroll.set)
scroll.grid(row=9,column=6, sticky=tk.S + tk.W + tk.E + tk.N)

start_btn = creat_new_button("執行", add, 10, 2)

root.mainloop()

print("Sys: end.")