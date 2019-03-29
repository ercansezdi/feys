from tkinter import Frame, Tk,ttk,N,S,W,E,SUNKEN,Canvas,Scrollbar
import tkinter.ttk as ttk
import os
import sqlite3
from time import strftime
from datetime import datetime
class tkinterGui(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        #self.parent.attributes("-fullscreen", True)
        self.parent.geometry('810x750')
        self.backGround = "white"
        self.foreGround = 'white'
        self.foreGround_2 = 'black'
        self.parent.title('FEYS')
        self.parent.bind('<Escape>',quit)
        self.parent.configure(background=self.backGround)
        self.classes = []
        self.boyut=25
        self.interface()

    def interface(self):
        self.tree =  ttk.Treeview(self.parent, height=36)
        self.tree.place(x=30, y=95)
        vsb = ttk.Scrollbar(self.parent, orient="vertical", command=self.tree.yview)
        vsb.place(x=30+760+6, y=24, height=707+20)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree['columns'] = ('starttime', 'endtime', 'status','status_1')
        #-------------------------------------------------------
        self.tree.heading("#0", text='Giriş Sırası', anchor='center')
        self.tree.column("#0", anchor="center",width=90,minwidth= 35)#W,N,S,
        #-------------------------------------------------------
        self.tree.heading('starttime', text='Numarası', anchor='center')
        self.tree.column('starttime', anchor='center', width=107,minwidth= 130)
        #-------------------------------------------------------
        self.tree.heading('endtime', text='Adı - Soyadı', anchor='center')
        self.tree.column('endtime', anchor='center', width=320,minwidth= 125)
        #-------------------------------------------------------
        self.tree.heading('status', text='Giriş Saati', anchor='center')
        self.tree.column('status', anchor='center', width=130,minwidth=0)
        #-------------------------------------------------------
        self.tree.heading('status_1', text='Çıkış Saati', anchor='center')
        self.tree.column('status_1', anchor='center', width=150,minwidth=0)
        #-------------------------------------------------------
        self.tree.grid(sticky = (N,S,W,E),row = 1, column = 0,padx = 0,pady=0,columnspan = 12 ,rowspan = 4)

        self.canvas = Canvas(self.tree, relief=SUNKEN, borderwidth=2)#,
                         #scrollregion=('-11c', '-11c', '50c', '20c'))
        self.vscroll = Scrollbar(self.tree, command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.vscroll.set)

        ttk.Style().configure("Treeview",background=self.backGround,fieldbackground = self.backGround,font=(None,12),foreground=self.foreGround_2)

        self.tree.grid_rowconfigure(0, weight = 1)
        self.tree.grid_columnconfigure(0, weight = 1)
    def start(self):
        self.donem = 'Bahar'
        self.yil =  '2017-2018'
        adres =  '../kayitlar/' + 'D-103'+ '/' + self.yil + '/' + self.donem
        array = []
        dizinler = os.listdir(adres)
        for i in dizinler:
            if i != 'yoklamaKayit' and i != "elektrikKayit":
                array.append(i)
            else:
                pass
        for a in array:
            ok = True
            for b in self.classes:
                if a == b :
                    ok = False
                else:
                    pass
            if ok:
                self.classes.append(a)

        if self.boyut != len(self.classes):
            cb = ttk.Combobox(self.parent, values=self.classes,background=self.backGround,state="readonly")
            cb.grid(row = 0, column = 0,padx = 0,pady=0,columnspan=12)
            cb.bind('<<ComboboxSelected>>', self.hazirla)
            self.boyut = len(self.classes)
        self.tekrarBasla = root.after(1000,run.start)

    def hazirla(self,eventObject):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.classes = []
        self.sayac = 1
        self.control_array = []
        self.ders_adi = eventObject.widget.get()
        self.baslat()

    def baslat(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.classes = []
        self.sayac = 1
        self.control_array = []


        self.donem = 'Bahar'
        self.yil =  '2017-2018'
        adres =  '../kayitlar/' + 'D-103'+ '/' + self.yil + '/' + self.donem
        array = []
        dizinler = os.listdir(adres)
        dizinler = os.listdir(adres+ '/' + self.ders_adi)
        dizi = []
        for t in dizinler:
            baglan = sqlite3.connect(adres+ '/' + self.ders_adi + '/' + t)
            veri = baglan.cursor()
            res = veri.execute("SELECT name FROM sqlite_master WHERE type='table';")
            for name in res:
                veriler = veri.execute('select * from '+ name[0]).fetchall()
                baglan.commit()

                if self.control_array == []:
                    if veriler[0][4] == None:
                        self.control_array.append(veriler[0][0])
                        self.tree.insert('', 'end', text= "1", values=(str(veriler[0][0]),str(veriler[0][1]),str(veriler[0][3]),'Çıkış Yapmamış'))
                    else:
                        self.control_array.append(veriler[0][0])
                        self.tree.insert('', 'end', text= "1", values=(veriler[0][0],veriler[0][1],veriler[0][3],veriler[0][4]))
                    self.sayac = self.sayac + 1
                if self.control_array != []:
                    for k in veriler:
                        empty = True
                        for num in self.control_array:
                            if k[0] == num:
                                empty = False
                            else:
                                pass
                        if k[4] == None and empty:
                            self.control_array.append(k[0])
                            self.tree.insert('', 'end', text= self.sayac, values=(k[0],k[1],k[3],'Çıkış Yapmamış'))
                            self.sayac = self.sayac + 1

                        elif k[4] != None and empty:
                            self.control_array.append(k[0])
                            self.tree.insert('', 'end', text= self.sayac, values=(k[0],k[1],k[3],k[4]))
                            self.sayac = self.sayac + 1
                        else:
                            pass
        self.tekrarBasla = root.after(1000,run.baslat)

###########################################################################################  MAIN FUNCTION ###############################################################################
##########################################################################################################################################################################################

if __name__ == "__main__":
    root = Tk()
    root.call('tk', 'scaling', 1.0)
    run = tkinterGui(root)
    root.after(1000,run.start)
    root.mainloop()
