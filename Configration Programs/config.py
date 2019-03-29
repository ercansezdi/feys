import configparser
from tkinter import *
from time import strptime,strftime,sleep
import sqlite3
from datetime import datetime
import os


class tkinterGui(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.cfg_address = '../conf/bilgiler.cfg'
        self.parent = parent
        self.config = configparser.ConfigParser()
        self.config.read(self.cfg_address)
        self.parent.bind('<Escape>',quit)
        #self.parent.attributes("-fullscreen", True)
        self.parent.geometry('725x425')
        self.parent.title('Configuration Program')
        self.arkaPlanRenk = "#E0FFFF"
        self.backGround = "#E0FFFF"
        self.yaziTipi = "Helvetica 12 bold italic"
        self.parent.config(background="#E0FFFF")
        self.updateWrite1 = StringVar()
        self.updateWrite2 = StringVar()
        self.updateWrite3 = StringVar()
        self.updateWrite4 = StringVar()
        self.updateWrite5 = StringVar()
        self.updateWrite6 = StringVar()
        self.updateWrite7 = StringVar()
        self.updateWrite8 = StringVar()
        self.updateWrite9 = StringVar()
        self.updateWrite10 = StringVar()
        self.updateWrite11 = StringVar()
        self.updateWrite12 = StringVar()
        self.updateWrite13 = StringVar()
        self.updateWrite14 = StringVar()
        self.updateWrite15 = StringVar()
        self.updateWrite16 = StringVar()
        self.updateWrite17 = StringVar()
        self.updateWrite18 = StringVar()
        self.updateWrite19 = StringVar()
        self.updateWrite20 = StringVar()
        self.updateWrite21 = StringVar()
        self.updateWrite22 = StringVar()
        self.updateWrite23 = StringVar()
        self.updateWrite24 = StringVar()
        self.updateWrite25 = StringVar()
        self.updateWrite26 = StringVar()
        self.updateWrite27 = StringVar()
        self.updateWrite28 = StringVar()
        self.a1 = PhotoImage(file = '../icons/onay.png')
        self.a2 = PhotoImage(file = '../icons/renksiz.png')
        self.a3 = PhotoImage(file = '../icons/ret.png')
        self.screen()
        self.update_page()

    def screen(self):
        self.veri_cevap = []
        for i in self.config['veri']:
            self.veri_cevap.append(self.config['veri'][str(i)])



        #**********************************************************************************************
        #*******************************************  label* ******************************************
        #**********************************************************************************************
        if True:
            self.textbox = Label(self.parent,text='Sistem saati & veritabanı saati güncelle',font =self.yaziTipi,bg = self.backGround,fg ="red",wraplength=790) # saat)
            self.textbox.grid(row=11,column=1,sticky=W, padx=200 ,  pady = 5,columnspan=2,rowspan=1)
            ###############################################################################################
            self.clock = Label(textvariable=self.updateWrite22,font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.clock.grid(row=12,column=1,sticky=W, padx=20 ,  pady = 5,columnspan=2,rowspan=1)
            ###############################################################################################
            self.update1Update = Label(text="Günlük güncelleme saati",font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update1Update.grid(row=1,column=1,sticky=W, padx=20 ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update2Update = Label(text="Fakülte ID",font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update2Update.grid(row=2,column=1,sticky=W, padx=20 ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update3Update = Label(text="Bölüm ID",font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update3Update.grid(row=3,column=1,sticky=W, padx=20 ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update4Update = Label(text="Fakülteye ait bina ID",font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update4Update.grid(row=4,column=1,sticky=W, padx=20 ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update5Update = Label(text="Binaya ait sınıf adı",font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update5Update.grid(row=5,column=1,sticky=W, padx=20 ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update6Update = Label(text="Öğr. Gör. onay süresi",font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update6Update.grid(row=6,column=1,sticky=W, padx=20 ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update7Update = Label(text="Popup pencere süresi",font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update7Update.grid(row=7,column=1,sticky=W, padx=20 ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update8Update = Label(text="Giriş izin  süresi",font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update8Update.grid(row=8,column=1,sticky=W, padx=20 ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update9Update = Label(text="Erken giriş başlama süresi",font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update9Update.grid(row=9,column=1,sticky=W, padx=20 ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update10Update = Label(text="Erken çıkış başlama süresi",font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update10Update.grid(row=10,column=1,sticky=W, padx=20 ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update1Update = Label(textvariable=self.updateWrite1,font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update1Update.grid(row=1,column=2,sticky=W, padx=40  ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update2Update = Label(textvariable=self.updateWrite2,font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update2Update.grid(row=2,column=2,sticky=W, padx=40  ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update3Update = Label(textvariable=self.updateWrite3,font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update3Update.grid(row=3,column=2,sticky=W, padx=40  ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update4Update = Label(textvariable=self.updateWrite4,font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update4Update.grid(row=4,column=2,sticky=W, padx=40  ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update5Update = Label(textvariable=self.updateWrite5,font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update5Update.grid(row=5,column=2,sticky=W, padx=40  ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update6Update = Label(textvariable=self.updateWrite6,font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update6Update.grid(row=6,column=2,sticky=W, padx=40  ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update7Update = Label(textvariable=self.updateWrite7,font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update7Update.grid(row=7,column=2,sticky=W, padx=40  ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update8Update = Label(textvariable=self.updateWrite8,font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update8Update.grid(row=8,column=2,sticky=W, padx=40  ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update9Update = Label(textvariable=self.updateWrite9,font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update9Update.grid(row=9,column=2,sticky=W, padx=40  ,  pady = 5,columnspan=1,rowspan=1)
            ###############################################################################################
            self.update10Update = Label(textvariable=self.updateWrite10,font =self.yaziTipi,bg = self.backGround,wraplength=790) # saat
            self.update10Update.grid(row=10,column=2,sticky=W, padx=40  ,  pady = 5,columnspan=1,rowspan=1)
        #**********************************************************************************************
        #*******************************************  button ******************************************
        #**********************************************************************************************
        if True:
            #self.button = Button(self.parent,font = "Helvetica 15 bold italic",padx = 20,text = 'X',command = self.parent.destroy)
            #self.button.grid(row = 1, column = 4,padx = 230,pady=0,rowspan=1,columnspan=1)#,columnspan = 2,rowspan = 2)
            ###############################################################################################
            self.buton1 = Button(text= "Değiştir", width=4,height=1,command= lambda: self.change_information('buton1'))
            self.buton1.grid(row=1,column=2, sticky=W,padx= 120, pady = 1,columnspan=1,rowspan=1)
            ###############################################################################################
            self.buton2 = Button(text= "Değiştir", width=4,height=1,command= lambda: self.change_information('buton2'))
            self.buton2.grid(row=2,column=2, sticky=W,padx= 120, pady = 1,columnspan=1,rowspan=1)
            ###############################################################################################
            self.buton3 = Button(text= "Değiştir", width=4,height=1,command= lambda: self.change_information('buton3'))
            self.buton3.grid(row=3,column=2, sticky=W,padx= 120, pady = 1,columnspan=1,rowspan=1)
            ###############################################################################################
            self.buton4 = Button(text= "Değiştir", width=4,height=1,command= lambda: self.change_information('buton4'))
            self.buton4.grid(row=4,column=2, sticky=W,padx= 120, pady = 1,columnspan=1,rowspan=1)
            ###############################################################################################
            self.buton5 = Button(text= "Değiştir", width=4,height=1,command= lambda: self.change_information('buton5'))
            self.buton5.grid(row=5,column=2, sticky=W,padx= 120, pady = 1,columnspan=1,rowspan=1)
            ###############################################################################################
            self.buton6 = Button(text= "Değiştir", width=4,height=1,command= lambda: self.change_information('buton6'))
            self.buton6.grid(row=6,column=2, sticky=W,padx= 120, pady = 1,columnspan=1,rowspan=1)
            ###############################################################################################
            self.buton7 = Button(text= "Değiştir", width=4,height=1,command= lambda: self.change_information('buton7'))
            self.buton7.grid(row=7,column=2, sticky=W,padx= 120, pady = 1,columnspan=1,rowspan=1)
            ###############################################################################################
            self.buton8 = Button(text= "Değiştir", width=4,height=1,command= lambda: self.change_information('buton8'))
            self.buton8.grid(row=8,column=2, sticky=W,padx= 120, pady = 1,columnspan=1,rowspan=1)
            ###############################################################################################
            self.buton9 = Button(text= "Değiştir", width=4,height=1,command= lambda: self.change_information('buton9'))
            self.buton9.grid(row=9,column=2, sticky=W,padx= 120, pady = 1,columnspan=1,rowspan=1)
            ###############################################################################################
            self.buton10 = Button(text= "Değiştir", width=4,height=1,command= lambda: self.change_information('buton10'))
            self.buton10.grid(row=10,column=2, sticky=W,padx= 120, pady = 1,columnspan=1,rowspan=1)
            ###############################################################################################
            self.buton11 = Button(text= "Sistem tarihini güncelle", width=40,height=2,command= lambda: self.change_information('buton11'))
            self.buton11.grid(row=13,column=0, sticky=W,padx= 20, pady = 1,columnspan=3,rowspan=1)
            ###############################################################################################
            self.buton11 = Button(text= "Database  tarihini güncelle", width=40,height=2,command= lambda: self.change_information('buton12'))
            self.buton11.grid(row=13,column=2, sticky=W,padx= 120, pady = 1,columnspan=3,rowspan=1)
        #**********************************************************************************************
        #*******************************************  entry ******************************************
        #**********************************************************************************************
        if True:
            self.entry1 = Entry(textvariable=self.updateWrite11,width=9,justify=CENTER)
            self.entry1.grid(row=1,column=2, sticky=W,padx= 190, pady = 1,columnspan=1,rowspan=1)
            self.entry1.insert(0,self.updateWrite11)
            self.entry1.bind("<Button>",self.entry_hint_1)
            #----------------------------------------------------------------------------------------------
            self.entry11 = Entry(textvariable=self.updateWrite21,width=9,justify=CENTER)
            self.entry11.grid(row=1,column=2, sticky=W,padx= 280, pady = 1,columnspan=1,rowspan=1)
            self.entry11.insert(0,self.updateWrite21)
            self.entry11.bind("<Button>",self.entry_hint_11)
            ###############################################################################################
            self.entry2 = Entry(textvariable=self.updateWrite12,width=20,justify=CENTER)
            self.entry2.grid(row=2,column=2, sticky=W,padx= 190, pady = 1,columnspan=1,rowspan=1)
            self.entry2.insert(0,self.updateWrite12)
            self.entry2.bind("<Button>",self.entry_hint_2)
            ###############################################################################################
            self.entry3 = Entry(textvariable=self.updateWrite13,width=20,justify=CENTER)
            self.entry3.grid(row=3,column=2, sticky=W,padx= 190, pady = 1,columnspan=1,rowspan=1)
            self.entry3.insert(0,self.updateWrite13)
            self.entry3.bind("<Button>",self.entry_hint_3)
            ###############################################################################################
            self.entry4 = Entry(textvariable=self.updateWrite14,width=20,justify=CENTER)
            self.entry4.grid(row=4,column=2, sticky=W,padx= 190, pady = 1,columnspan=1,rowspan=1)
            self.entry4.insert(0,self.updateWrite14)
            self.entry4.bind("<Button>",self.entry_hint_4)
            ###############################################################################################
            self.entry5 = Entry(textvariable=self.updateWrite15,width=20,justify=CENTER)
            self.entry5.grid(row=5,column=2, sticky=W,padx= 190, pady = 1,columnspan=1,rowspan=1)
            self.entry5.insert(0,self.updateWrite15)
            self.entry5.bind("<Button>",self.entry_hint_5)
            ###############################################################################################
            self.entry6 = Entry(textvariable=self.updateWrite16,width=20,justify=CENTER)
            self.entry6.grid(row=6,column=2, sticky=W,padx= 190, pady = 1,columnspan=1,rowspan=1)
            self.entry6.insert(0,self.updateWrite16)
            self.entry6.bind("<Button>",self.entry_hint_6)
            ###############################################################################################
            self.entry7 = Entry(textvariable=self.updateWrite17,width=20,justify=CENTER)
            self.entry7.grid(row=7,column=2, sticky=W,padx= 190, pady = 1,columnspan=1,rowspan=1)
            self.entry7.insert(0,self.updateWrite17)
            self.entry7.bind("<Button>",self.entry_hint_7)
            ###############################################################################################
            self.entry8 = Entry(textvariable=self.updateWrite18,width=20,justify=CENTER)
            self.entry8.grid(row=8,column=2, sticky=W,padx= 190, pady = 1,columnspan=1,rowspan=1)
            self.entry8.insert(0,self.updateWrite18)
            self.entry8.bind("<Button>",self.entry_hint_8)
            ###############################################################################################
            self.entry9 = Entry(textvariable=self.updateWrite19,width=20,justify=CENTER)
            self.entry9.grid(row=9,column=2, sticky=W,padx= 190, pady = 1,columnspan=1,rowspan=1)
            self.entry9.insert(0,self.updateWrite19)
            self.entry9.bind("<Button>",self.entry_hint_9)
            ###############################################################################################
            self.entry10 = Entry(textvariable=self.updateWrite20,width=20,justify=CENTER)
            self.entry10.grid(row=10,column=2, sticky=W,padx= 190, pady = 1,columnspan=1,rowspan=1)
            self.entry10.insert(0,self.updateWrite20)
            self.entry10.bind("<Button>",self.entry_hint_10)
            ###############################################################################################
            ###############################################################################################
            self.entry12 = Entry(textvariable=self.updateWrite23,width=6,justify=CENTER)
            self.entry12.grid(row=12,column=2, sticky=W,padx= 40, pady = 1,columnspan=3,rowspan=1) #saat
            self.entry12.insert(0,self.updateWrite23)
            self.entry12.bind("<Button>",self.entry_hint_12)
            ###############################################################################################
            self.entry13 = Entry(textvariable=self.updateWrite24,width=6,justify=CENTER)
            self.entry13.grid(row=12,column=2, sticky=W,padx= 100, pady = 1,columnspan=3,rowspan=1) #dakika
            self.entry13.insert(0,self.updateWrite24)
            self.entry13.bind("<Button>",self.entry_hint_13)
            ###############################################################################################
            self.entry14 = Entry(textvariable=self.updateWrite25,width=6,justify=CENTER)
            self.entry14.grid(row=12,column=2, sticky=W,padx= 160, pady = 1,columnspan=3,rowspan=1)#saniye
            self.entry14.insert(0,self.updateWrite25)
            self.entry14.bind("<Button>",self.entry_hint_14)
            ###############################################################################################
            self.entry15 = Entry(textvariable=self.updateWrite26,width=6,justify=CENTER)
            self.entry15.grid(row=12,column=2, sticky=W,padx= 230, pady = 1,columnspan=3,rowspan=1)     # gün
            self.entry15.insert(0,self.updateWrite26)
            self.entry15.bind("<Button>",self.entry_hint_15)
            ###############################################################################################
            self.entry16 = Entry(textvariable=self.updateWrite27,width=6,justify=CENTER)
            self.entry16.grid(row=12,column=2, sticky=W,padx= 290, pady = 1,columnspan=3,rowspan=1)#        ay
            self.entry16.insert(0,self.updateWrite27)
            self.entry16.bind("<Button>",self.entry_hint_16)
            ###############################################################################################
            self.entry17 = Entry(textvariable=self.updateWrite28,width=6,justify=CENTER)
            self.entry17.grid(row=12,column=2, sticky=W,padx= 350, pady = 1,columnspan=3,rowspan=1)#    yil
            self.entry17.insert(0,self.updateWrite28)
            self.entry17.bind("<Button>",self.entry_hint_17)
        #**********************************************************************************************
        #*******************************************  image *******************************************
        #**********************************************************************************************
        self.resim_ok = Label(self.parent,image=self.a1,borderwidth=0)
        self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        self.resim_ok.grid_remove()
        ###############################################################################################
        self.resim_o = Label(self.parent,image=self.a2,borderwidth=0)
        self.resim_o.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        ###############################################################################################
        self.resim_no = Label(self.parent,image=self.a3,borderwidth=0)
        self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        self.resim_no.grid_remove()
        #**********************************************************************************************
        #*******************************************  start *******************************************
        #**********************************************************************************************

        if True:

            self.update_page()
            self.entry_hint_update('all')

    def entry_hint_1(self,event):
        self.entry1.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_1')
    def entry_hint_2(self,event):
        self.entry2.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_2')
    def entry_hint_3(self,event):
        self.entry3.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_3')
    def entry_hint_4(self,event):
        self.entry4.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_4')
    def entry_hint_5(self,event):
        self.entry5.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_5')
    def entry_hint_6(self,event):
        self.entry6.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_6')
    def entry_hint_7(self,event):
        self.entry7.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_7')
    def entry_hint_8(self,event):
        self.entry8.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_8')
    def entry_hint_9(self,event):
        self.entry9.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_9')
    def entry_hint_10(self,event):
        self.entry10.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_10')
    def entry_hint_11(self,event):
        self.entry11.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_11')
    def entry_hint_12(self,event):
        self.entry12.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_12')
    def entry_hint_13(self,event):
        self.entry13.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_13')
    def entry_hint_14(self,event):
        self.entry14.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_14')
    def entry_hint_15(self,event):
        self.entry15.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_15')
    def entry_hint_16(self,event):
        self.entry16.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_16')
    def entry_hint_17(self,event):
        self.entry17.delete(0,END)
        usercheck=True
        self.entry_hint_update('entry_hint_17')

    def update_date(self,bugunTarih,yil="2017-2018",donem="Bahar"):
        gunler = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

        for i in range(0,len(gunler)):
            day = gunler[i]
            baglan = sqlite3.connect( '../kayitlar/' +str(self.derslikAdi) + '/' + yil + '/' + donem +  '/yoklamaKayit/' + day + '.db')
            veri = baglan.cursor()
            kontrol = veri.execute("SELECT name FROM sqlite_master").fetchall()
            for i in range(0,len(kontrol)):
                if kontrol[i][0][0] != "s" and kontrol[i][0][0] != "q":
                    dersAdi = kontrol[i][0]
                    allDatabase = veri.execute('select * from "' +  str(kontrol[i][0]) + '"' ).fetchall()
                    for i in allDatabase:
                        if bugunTarih != i[15]:
                            veri.execute("UPDATE '"+ str(dersAdi) + "' SET Guncelleme_Tarihi = '" + str(bugunTarih)+"'")
            baglan.commit()

        baglan = sqlite3.connect( './kayitlar/' +str(self.derslikAdi) + '/genelKayitlar/veri_kayit.db')
        veri = baglan.cursor()
        kontrol = veri.execute("SELECT name FROM sqlite_master").fetchall()

        veri.execute("UPDATE '"+ str(kontrol[0][0]) + "' SET Guncelleme_Tarihi = '" + str(bugunTarih)+"'")
        baglan.commit()

        baglan = sqlite3.connect( '../kayitlar/' +str(self.derslikAdi) + '/' + yil + '/' + donem +  '/elektrikKayit/sonGuncellemeTarihi.db')
        veri = baglan.cursor()
        kontrol = veri.execute("SELECT name FROM sqlite_master").fetchall()
        veri.execute("UPDATE '"+ str(kontrol[0][0]) + "' SET database_son_guncelleme_tarihi = '" + str(bugunTarih)+"'")
        baglan.commit()

    def change_information(self,value='?'):

        if value == "buton1":
            if self.entry1.get() == '' or self.entry1.get() == 'Saat'  or not(str(self.entry1.get()).isnumeric()):
                 self.resim_o.grid_remove()
                 self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            else:
                if  self.entry11.get() == 'Dakika' or str(self.entry11.get()).isnumeric() or self.entry11.get() == '':
                    if int(self.entry1.get()) > 24:
                        self.resim_o.grid_remove()
                        self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                    else:
                        if int(self.entry1.get()) == 24:
                            if str(self.entry11.get()) == 'Dakika':
                                veri = '00:00'
                            else:
                                if len(str(self.entry11.get())) == 2:
                                    veri = '00:' + str(self.entry11.get())
                                else:
                                    veri = '00:0' + str(self.entry11.get())
                        elif int(self.entry1.get()) == 0:
                            if str(self.entry11.get()) == 'Dakika':
                                veri = '00:00'
                            else:
                                if len(str(self.entry11.get())) == 2:
                                    veri = '00:' + str(self.entry11.get())
                                else:
                                    veri = '00:0' + str(self.entry11.get())
                        else:
                                if len(str(self.entry1.get())) == 2:
                                    if str(self.entry11.get()) == 'Dakika':
                                        veri = str(self.entry1.get()) + ':00'
                                    else:
                                        if len(str(self.entry11.get())) == 2:
                                            veri = str(self.entry1.get()) + ':' + str(self.entry11.get())
                                        else:
                                            veri = str(self.entry1.get()) + ':0' + str(self.entry11.get())

                                else:
                                    if str(self.entry11.get()) == 'Dakika' or  str(self.entry11.get()) == '':
                                        veri = '0' + str(self.entry1.get()) + ':00'
                                    else:
                                        if len(str(self.entry11.get())) == 2:
                                            veri = '0' + str(self.entry1.get()) + ':' + str(self.entry11.get())
                                        else:
                                            veri = '0' + str(self.entry1.get()) + ':0' + str(self.entry11.get())

                        self.config.set('veri',str(self.veri[7]),veri)
                        self.set_information()
                        self.entry_hint_update('entry_hint_1')
                        self.resim_o.grid_remove()
                        self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                else:
                    self.resim_o.grid_remove()
                    self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        elif value == "buton2":
            if self.entry2.get() == '' or self.entry2.get() == ('Örn. ' + self.veri_cevap[8]):
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            else:
                self.config.set('veri',str(self.veri[8]),self.entry2.get())
                self.set_information()
                self.entry_hint_update('entry_hint_2')
                self.resim_o.grid_remove()
                self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        elif value == "buton3":
            if self.entry3.get() == '' or self.entry3.get() == ('Örn. ' + self.veri_cevap[9]):
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            else:
                self.config.set('veri',str(self.veri[9]),self.entry3.get())
                self.set_information()
                self.entry_hint_update('entry_hint_3')
                self.resim_o.grid_remove()
                self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        elif value == "buton4":
            if self.entry4.get() == '' or self.entry4.get() == ('Örn. ' + self.veri_cevap[11]):
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            else:
                self.config.set('veri',str(self.veri[11]),self.entry4.get())
                self.set_information()
                self.entry_hint_update('entry_hint_4')
                self.resim_o.grid_remove()
                self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        elif value == "buton5":
            if self.entry5.get() == '' or self.entry5.get() == ('Örn. ' + self.veri_cevap[10]):
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            else:
                self.config.set('veri',str(self.veri[10]),self.entry5.get())
                self.set_information()
                self.entry_hint_update('entry_hint_5')
                self.resim_o.grid_remove()
                self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        elif value == "buton6":
            if not(str(self.entry6.get()).isnumeric()) or self.entry6.get() == ('Örn. ' + self.veri_cevap[12]) or str(self.entry6.get()) == '0':
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            else:
                if int(self.entry6.get()) >10 or int(self.entry6.get()) < 2:
                    self.resim_o.grid_remove()
                    self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                else:
                    self.config.set('veri',str(self.veri[12]),self.entry6.get())
                    self.set_information()
                    self.entry_hint_update('entry_hint_6')
                    self.resim_o.grid_remove()
                    self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        elif value == "buton7" :
            if not(str(self.entry7.get()).isnumeric()) or self.entry7.get() == ('Örn. ' + self.veri_cevap[13]) or str(self.entry7.get()) == '0':
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            else:
                if int(self.entry7.get()) >3 or int(self.entry7.get()) < 1:
                    self.resim_o.grid_remove()
                    self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                else:
                    self.config.set('veri',str(self.veri[13]),self.entry7.get())
                    self.set_information()
                    self.entry_hint_update('entry_hint_7')
                    self.resim_o.grid_remove()
                    self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        elif value == "buton8":
            if not(str(self.entry8.get()).isnumeric()) or self.entry8.get() == ('Örn. ' + self.veri_cevap[14]) or str(self.entry8.get()) == '0':
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            else:
                if int(self.entry8.get()) >20 or int(self.entry8.get()) < 1:
                    self.resim_o.grid_remove()
                    self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                else:
                    self.config.set('veri',str(self.veri[14]),self.entry8.get())
                    self.set_information()
                    self.entry_hint_update('entry_hint_8')
                    self.resim_o.grid_remove()
                    self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        elif value == "buton9":
            if not(str(self.entry9.get()).isnumeric()) or self.entry9.get() == ('Örn. ' + self.veri_cevap[15]) or str(self.entry9.get()) == '0':
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            else:
                if int(self.entry9.get()) >20 or int(self.entry9.get()) < 10:
                    self.resim_o.grid_remove()
                    self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                else:
                    self.config.set('veri',str(self.veri[15]),self.entry9.get())
                    self.set_information()
                    self.entry_hint_update('entry_hint_9')
                    self.resim_o.grid_remove()
                    self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        elif value == "buton10":
            if not(str(self.entry10.get()).isnumeric()) or self.entry10.get() == ('Örn. ' + self.veri_cevap[16]) or str(self.entry10.get()) == '0':
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            else:
                if int(self.entry10.get()) >20 or int(self.entry10.get()) < 5:
                    self.resim_o.grid_remove()
                    self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                else:
                    self.config.set('veri',str(self.veri[16]),self.entry10.get())
                    self.set_information()
                    self.entry_hint_update('entry_hint_10')
                    self.resim_o.grid_remove()
                    self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        elif value == "buton11":
            if not(str(self.entry12.get()).isnumeric()) and not(str(self.entry15.get()).isnumeric()): # tarih saat girilmemiş
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            elif str(self.entry12.get()).isnumeric() and str(self.entry13.get()).isnumeric() and str(self.entry14.get()).isnumeric() and str(self.entry15.get()).isnumeric() and str(self.entry16.get()).isnumeric() and str(self.entry17.get()).isnumeric():# tarih saat girilmiş
                if int(self.entry12.get()) > 23 or int(self.entry13.get()) > 59 or int(self.entry14.get()) > 59 or  int(self.entry16.get()) > 12 or int(self.entry17.get()) < 2017:
                    self.resim_o.grid_remove()
                    self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                else:
                    if int(self.entry17.get()) > 2019 :
                        self.resim_o.grid_remove()
                        self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                    else:
                        if ((int(self.entry16.get()) < 8 and int(self.entry16.get()) % 2 == 1 ) or (int(self.entry16.get()) > 7 and int(self.entry16.get()) % 2 == 0 )) and int(self.entry16.get()) != 2:
                            if int(self.entry15.get()) > 31:
                                self.resim_o.grid_remove()
                                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                            else:
                                if str(self.entry14.get()).isnumeric():
                                    saat_yil = str(self.entry12.get()) + ':' + self.entry13.get() + ':'+ self.entry14.get()  + " " + self.entry15.get() + '/' + self.entry16.get() + '/' + self.entry17.get()
                                    saat_yil = datetime.strptime(saat_yil,'%H:%M:%S %d/%m/%Y')
                                    saat_yil = saat_yil.strftime("%d %b %Y %H:%M:%S")
                                else:
                                    saat_yil = str(self.entry12.get()) + ':' + self.entry13.get() + ':00'  + " " + self.entry15.get() + '/' + self.entry16.get() + '/' + self.entry17.get()
                                    saat_yil = datetime.strptime(saat_yil,'%H:%M:%S %d/%m/%Y')
                                    saat_yil = saat_yil.strftime("%d %b %Y %H:%M:%S")
                                print(saat_yil + '_1')
                                os.system('sudo date -s "' + saat_yil + '"')
                                self.resim_o.grid_remove()
                                self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                        elif ((int(self.entry16.get()) > 7 and int(self.entry16.get()) % 2 == 1 ) or (int(self.entry16.get()) < 7 and int(self.entry16.get()) % 2 == 0 )) and int(self.entry16.get()) != 2:
                            if int(self.entry15.get()) > 30:
                                self.resim_o.grid_remove()
                                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                            else:
                                if str(self.entry14.get()).isnumeric():
                                    saat_yil = str(self.entry12.get()) + ':' + self.entry13.get() + ':'+ self.entry14.get()  + " " + self.entry15.get() + '/' + self.entry16.get() + '/' + self.entry17.get()
                                    saat_yil = datetime.strptime(saat_yil,'%H:%M:%S %d/%m/%Y')
                                    saat_yil = saat_yil.strftime("%d %b %Y %H:%M:%S")
                                else:
                                    saat_yil = str(self.entry12.get()) + ':' + self.entry13.get() + ':00'  + " " + self.entry15.get() + '/' + self.entry16.get() + '/' + self.entry17.get()
                                    saat_yil = datetime.strptime(saat_yil,'%H:%M:%S %d/%m/%Y')
                                    saat_yil = saat_yil.strftime("%d %b %Y %H:%M:%S")
                                print(saat_yil+ '_2')
                                os.system('sudo date -s "' + saat_yil + '"')
                                self.resim_o.grid_remove()
                                self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                        elif int(self.entry16.get())  == 2:
                            if int(self.entry15.get()) > 28:
                                self.resim_o.grid_remove()
                                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
                            else:
                                if str(self.entry14.get()).isnumeric():
                                    saat_yil = str(self.entry12.get()) + ':' + self.entry13.get() + ':'+ self.entry13.get()  + " " + self.entry15.get() + '/' + self.entry16.get() + '/' + self.entry17.get()
                                    saat_yil = datetime.strptime(saat_yil,'%H:%M:%S %d/%m/%Y')
                                    saat_yil = saat_yil.strftime("%d %b %Y %H:%M:%S")
                                else:
                                    saat_yil = str(self.entry12.get()) + ':' + self.entry13.get() + ':00'  + " " + self.entry15.get() + '/' + self.entry16.get() + '/' + self.entry17.get()
                                    saat_yil = datetime.strptime(saat_yil,'%H:%M:%S %d/%m/%Y')
                                    saat_yil = saat_yil.strftime("%d %b %Y %H:%M:%S")
                                os.system('sudo date -s "' + saat_yil + '"')
                                self.resim_o.grid_remove()
                                self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)

                        else:
                            pass
            else:
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)



        elif value == "buton12":
            if not(str(self.entry15.get()).isnumeric()) or not(str(self.entry16.get()).isnumeric()) or not(str(self.entry17.get()).isnumeric()):
                self.resim_o.grid_remove()
                self.resim_no.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
            else:
                bugunTarih = self.entry15.get() + '/' + self.entry16.get() + '/' + self.entry17.get()
                self.update_date(bugunTarih)
                self.resim_o.grid_remove()
                self.resim_ok.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        else:
            pass
    def update_page(self):
        self.veri_cevap = []
        self.veri = []
        for i in self.config['veri']:
            self.veri.append(i)
            self.veri_cevap.append(self.config['veri'][str(i)])

        self.derslikAdi = self.veri_cevap[10]
        self.updateWrite1.set( self.veri_cevap[7])
        self.updateWrite2.set(self.veri_cevap[8])
        self.updateWrite3.set(self.veri_cevap[9])
        self.updateWrite4.set(self.veri_cevap[11])
        self.updateWrite5.set(self.veri_cevap[10])
        self.updateWrite6.set(self.veri_cevap[12] + " sn.")
        self.updateWrite7.set(self.veri_cevap[13] + " sn.")
        self.updateWrite8.set(self.veri_cevap[14] + " dk.")
        self.updateWrite9.set(self.veri_cevap[15] + " dk.")
        self.updateWrite10.set(self.veri_cevap[16] + " dk.")
    def entry_hint_update(self,answer):
        self.veri_cevap = []
        for i in self.config['veri']:
            self.veri_cevap.append(self.config['veri'][i])

        if answer != 'entry_hint_1' and answer != 'entry_hint_11':
            self.updateWrite11.set('Saat')
            self.updateWrite21.set('Dakika')
        if answer != 'entry_hint_2':
            self.updateWrite12.set('Örn. ' + self.veri_cevap[8])
        if answer != 'entry_hint_3':
            self.updateWrite13.set('Örn. ' + self.veri_cevap[9])
        if answer != 'entry_hint_4':
            self.updateWrite14.set('Örn. ' + self.veri_cevap[11])
        if answer != 'entry_hint_5':
            self.updateWrite15.set('Örn. ' + self.veri_cevap[10])
        if answer != 'entry_hint_6':
            self.updateWrite16.set('min: 2 & max: 10')
        if answer != 'entry_hint_7':
            self.updateWrite17.set('min: 1 & max: 3')
        if answer != 'entry_hint_8':
            self.updateWrite18.set('min: 1 & max: 20')
        if answer != 'entry_hint_9':
            self.updateWrite19.set('min: 10 & max 20')
        if answer != 'entry_hint_10':
            self.updateWrite20.set('min: 5 & max: 20')
        if answer != 'entry_hint_12' and answer != 'entry_hint_13' and answer != 'entry_hint_14' and answer != 'entry_hint_15' and answer != 'entry_hint_16' and answer != 'entry_hint_17':
            self.updateWrite23.set('Saat')
            self.updateWrite24.set('Dakika')
            self.updateWrite25.set('Saniye')
            self.updateWrite26.set('Gün')
            self.updateWrite27.set('Ay')
            self.updateWrite28.set('Yıl')
    def set_information(self):
        with open(self.cfg_address, 'w') as configfile:
                self.config.write(configfile)
        self.update_page()
    def hata_ver(self):
        pass

    def saatGuncelle(self):
        self.updateWrite22.set(datetime.today().strftime('Saat / Tarih   ' + '%H:%M:%S   %d/%m/%Y'))
        if int(datetime.today().strftime('%S')) % 3 == 0:
            self.resim_ok.grid_remove()
            self.resim_no.grid_remove()
            self.resim_o.grid(row=6,column=2,padx= 400, pady = 1,columnspan=1,rowspan=1)
        self.tekrarBasla = root.after(1000,run.saatGuncelle)

if __name__ == "__main__":
    root = Tk()
    root.call('tk', 'scaling', 1.0)
    run = tkinterGui(root)
    root.after(1000,run.saatGuncelle)
    root.mainloop()
