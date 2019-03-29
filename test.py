from threading import Thread
import random
import os # sistem komutlarini kontrol etmek için
import configparser # bilgilerin verildiği dosyayı okumak için
import sqlite3 # veritabani oluşturmak için
from time import strftime,ctime,sleep,strptime # zamanı almak için
from datetime import datetime ,timedelta
from tkinter import Tk,Label,Button,PhotoImage,ttk,Frame,StringVar,Menu,Toplevel,Canvas,ALL,W,N,S,E,SUNKEN,Scrollbar
from PIL import Image, ImageFont, ImageDraw,ImageTk
import textwrap
import tkinter.ttk
from functools import partial
###################
global configDosyasiAdres
global config
global verbose
global guncel


                        #Değişiklik yapilmayacaklar
configDosyasiAdres = 'conf/bilgiler.cfg'
config = configparser.ConfigParser() # config dosyasini okumak için config parser tanitim

                        #Değişiklik yapılabilecekler

guncel = False
verbose = False
continue_reading = True


class tkinterGui(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        #self.parent.attributes("-fullscreen", True)
        self.parent.geometry('500x500')
        self.parent.bind('<Escape>',quit)


        self.backGround = "#008000"
        self.foreGround = 'white'
        self.foreGround_2 = 'black'
        #self.yaziRengi = 'blue'
        #self.yaziTipi = "Helvetica 20 bold italic"
        self.parent.title('FEYS')

        self.font = ImageFont.truetype("conf/Colored_Crayons.ttf", 25)
        self.font_button = ImageFont.truetype("conf/Colored_Crayons.ttf", 21)
        self.parent.configure(background=self.backGround,cursor = 'none')

        ####### StringVars #######################

        self.updateWrite1 = StringVar()
        self.updateWrite2 = StringVar()
        self.updateWrite3 = StringVar()
        self.updateWrite4 = StringVar()
        self.st= StringVar()
        self.geriSayim = StringVar()

        ####### pictures #######################

        resimAdres =   'icons/'
        #self.board = PhotoImage(file = resimAdres+'board.png')
        self.amblem = PhotoImage(file = resimAdres + 'logo.png')
        self.undefinedCard = PhotoImage(file = resimAdres + "tanımsız_kart.png")
        self.no_wifi = PhotoImage(file = resimAdres + "no_wifi.png")
        self.earlyExit  = PhotoImage(file = resimAdres + "early_exit.png")
        self.noLogin = PhotoImage(file = resimAdres + "no_login.png")
        self.hata_ret = PhotoImage(file = resimAdres + "hata_resmi.png")
        self.welcome = PhotoImage(file = resimAdres + "welcome.png")
        self.byebye = PhotoImage(file = resimAdres + "byebye.png")
        self.red = PhotoImage(file = resimAdres + "rd.png")
        self.green = PhotoImage(file = resimAdres + "gr.png")
        self.giris_ret = PhotoImage(file = resimAdres + "giris.png")
        self.cikis_ret = PhotoImage(file = resimAdres + "cikis.png")
        self.aboutPhoto = PhotoImage(file = resimAdres + "hakkinda.png")
        #Tanimlamalar

        config.read(configDosyasiAdres)
        sleep(int(config['veri']['popupSuresi']))

        ########################################
        self.dummy = None
        self.araDegisken = 1
        self.araDegisken2 = 1
        self.izinAraDegisken = 1
        self.yoklamayaIzinVerme = False # ana fonksiyonda yok izni açıp kapamada kullanılıyor
        self.deger = '' # numara girmek için kullanılıyor
        self.last_uuid = False
        self.pencere = Toplevel()
        self.pencere.destroy()
        self.kalanSaat = None
        self.ErkenCikis = False
        self.ErkenCikisDersBitmeSaati = False
        self.dakikaAyar = 61
        self.dersAyar = 'giris_cikis_ara'
        self.ders_kismi = 'empty'
        self.mainScreen()


    def add_text_1(self,text):
        width, height = self.font.getsize(text)
        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=self.font, fill=self.foreGround)
        self._photoimage_1 =  ImageTk.PhotoImage(image)
    def add_text_2(self,text):
        width, height = self.font.getsize(text)
        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=self.font, fill=self.foreGround)
        self._photoimage_2 = ImageTk.PhotoImage(image)
    def add_text_3(self,text):
        width, height = self.font.getsize(text)
        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=self.font, fill=self.foreGround)
        self._photoimage_3  =ImageTk.PhotoImage(image)
    def add_text_4(self,text):
        width, height = self.font.getsize(text)
        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=self.font, fill=self.foreGround)
        self._photoimage_4 =  ImageTk.PhotoImage(image)
    def add_text_button(self,text):

        width, height = self.font_button.getsize(text)
        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=self.font_button, fill=self.foreGround)
        self._photoimage_button =  ImageTk.PhotoImage(image)
    def add_button(self,text):
        width, height = self.font_button.getsize(text)
        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=self.font_button, fill=self.foreGround)
        self._photoimage_button =  ImageTk.PhotoImage(image)

    def onayKutusu(self):
        self.onayKutusu = Toplevel()
        self.onayKutusu.configure(background=self.backGround,cursor = 'none')
        self.onayKutusu.attributes("-fullscreen", True)
        onay = Label(self.onayKutusu,text=" ONAYLIYOR MUSUNUZ ? ",font ="Helvetica 40 bold italic",bg = self.backGround,wraplength=780)
        onay.grid(row=2,column=1,columnspan=7,rowspan =3, sticky=W,padx= 75, pady=90)

        button1 = Button(self.onayKutusu,text= ' EVET ', width=15,height=5,font = "Helvetica 18 bold italic",command=self.araKisim,bg=self.backGround,anchor="center",highlightbackground="black")
        button1.grid(row=5,column=1,columnspan=1,rowspan =1, sticky=W,padx= 100, pady=25)

        button2 = Button(self.onayKutusu,text= ' HAYIR ', width=15,height=5,font = "Helvetica 18 bold italic",command=self.onayKutusu.destroy,bg=self.backGround,anchor="center",highlightbackground="black")
        button2.grid(row=5,column=2,columnspan=1,rowspan =1, sticky=W,padx= 0, pady=25)
    def admin_panel(self):
        self.ek_screen = Toplevel()
        self.ek_screen.attributes("-fullscreen", True)
        self.ek_screen.title('FEYS')
        self.ek_screen.bind('<Escape>',quit)
        self.ek_screen.configure(background=self.backGround,cursor = 'none')
        self.adminButton0 = Button(self.ek_screen,text = 'Veritabanı güncellemesi',bg=self.backGround,wraplength=750,anchor="center",height=6,width=44,highlightbackground="black",command=self.menuGuncellemesi,font ="Helvetica 11 bold italic",fg='white')
        self.adminButton0.grid(row=0,column=0, sticky=W,padx= 18, pady = 0,columnspan=1,rowspan=1)
        self.adminButton1 = Button(self.ek_screen,text = 'Değişken güncellemesi',bg=self.backGround,wraplength=750,anchor="center",height=6,width=44,highlightbackground="black",command=self.menuGuncellemesi,font ="Helvetica 11 bold italic",fg='white')
        self.adminButton1.grid(row=0,column=0, sticky=W,padx= 404, pady = 0,columnspan=1,rowspan=1)
        self.adminButton2 = Button(self.ek_screen,text = 'Kayıt ekle / sil',bg=self.backGround,wraplength=750,anchor="center",height=6,width=92,highlightbackground="black",command=self.girisYapanlar,font ="Helvetica 11 bold italic",fg='white')
        self.adminButton2.grid(row=1,column=0, sticky=W,padx= 18, pady = 8,columnspan=1,rowspan=1)
        self.adminButton3 = Button(self.ek_screen,text = 'Hakkında',bg=self.backGround,wraplength=750,anchor="center",height=6,width=92,highlightbackground="black",command=self.hakkinda,font ="Helvetica 11 bold italic",fg='white')
        self.adminButton3.grid(row=2,column=0, sticky=W,padx= 18, pady = 5,columnspan=1,rowspan=1)
        self.adminButton4 = Button(self.ek_screen,text = 'Çıkış',bg=self.backGround,wraplength=750,anchor="center",height=5,width=92,highlightbackground="black",command=self.admin_panel_cikis,font ="Helvetica 11 bold italic",fg='white')
        self.adminButton4.grid(row=3,column=0, sticky=W,padx= 18, pady = 5,columnspan=1,rowspan=1)
    def mainScreen(self):
        if verbose:
            print("< read_card.tkinterGui.mainScreen() fonksiyonuna giriş yapılıyor.")
        ######################################################################
        self.rd = Label(self.parent,image=self.red,borderwidth=0,bg=self.backGround)
        self.rd.grid(row=0,column=0,padx=0 ,  pady = 0,rowspan=5,columnspan=7)
        self.rd.grid_remove()
        self.gr = Label(self.parent,image=self.green,borderwidth=0,bg=self.backGround)
        self.gr.grid(row=0,column=0,padx=0 ,  pady = 0,rowspan=5,columnspan=7)
        self.gr.grid_remove()
        self.amblo = Label(self.parent,image=self.amblem,borderwidth=0,bg=self.backGround)
        self.amblo.grid(row=0,column=0,padx=0 ,  pady = 0,rowspan=5,columnspan=7)
        self.amblo.grid_remove()

        self.update1Update = Label(bg = self.backGround,wraplength=790) # saat
        self.update1Update.grid(row=0,column=0,sticky=W, padx=40 ,  pady = 25,columnspan=4,rowspan=1)
        self.update1Update.grid_remove()


        self.adminButton = Button(self.parent,text = 'Yönetici Paneli',font ="Helvetica 10 bold italic",bg=self.backGround,fg='white',anchor="center",height=2,width=17,highlightbackground="black",command=self.admin_panel)
        self.adminButton.grid(row=0,column=4,padx= 0, pady = 25,columnspan=2,rowspan=1)# sticky=W
        self.adminButton.grid_remove()

        self.update2Update = Label(bg = self.backGround,wraplength=800) # ok
        self.update2Update.grid(row=1,column=0,sticky=W, padx=40 ,  pady = 0,columnspan=7,rowspan=1)
        self.update2Update.grid_remove()

        self.update3Update = Label(bg = self.backGround,wraplength=750) # ok
        self.update3Update.grid(row=2,column=0, sticky=W,padx= 40, pady = 0,columnspan=7,rowspan=1)
        self.update3Update.grid_remove()

        self.update4Update= Label(bg = self.backGround,wraplength=750) #ok
        self.update4Update.grid(row=3,column=0, sticky=W,padx= 40, pady = 0,columnspan=7,rowspan=1)#123
        self.update4Update.grid_remove()

        self.add_text_button(text=config['veri']['butonYazisi'])
        self.buton = Button(self.parent,bg=self.backGround, image=self._photoimage_button,wraplength=750,anchor="center",height=50,width=360,highlightbackground="black",command=self.onayKutusu)
        self.buton.grid(row=3,column=0, sticky=W,padx= 32, pady = 0,columnspan=7,rowspan=1)
        self.buton.grid_remove()
        if verbose:
            print("< read_card.tkinterGui.mainScreen() fonksiyonundan çıkış yapılıyor.")
        self.ekranAyarla()
    def ekranAyarla(self):
        if verbose:
            print('< read_card.tkinterGui.ekranAyarla() fonksiyonuna giriş yapılıyor... >')
        self.hangiKisim = 'loginPermit'
        self.dersAdi ='MATH'
        hocaAdi = 'asf'
        self.dersBasla = '18:30:00'
        self.dersBitis = '19:40:00'
        self.dersKodu = '4665'

        if self.ErkenCikis == True:
            self.hangiKisim = 'exitPermit'
        try:
            self.tabloAdi = self.dersKodu+'_'+self.dersAdi+'_'+self.dersBasla.strftime('%H:%M')
        except:
            self.tabloAdi='Bos'
        self.yil = '2017-2018'
        self.donem = 'Bahar'
        if self.hangiKisim == 'loginPermit' or self.hangiKisim == "exitPermit" or self.hangiKisim ==  "between" :
            if self.dersAyar != self.hangiKisim:
                self.adminButton.grid(row=0,column=4,padx= 0, pady = 25,columnspan=2,rowspan=1)# sticky=W
                self.add_text_2(text='Ders adı : ' + self.dersKodu + ' - '+self.dersAdi)
                self.update3Update.grid_remove()
                self.update3Update=Label(self.parent,bg=self.backGround, image= self._photoimage_2,wraplength=750,anchor="center")
                self.update3Update.grid(row=2,column=0, sticky=W,padx= 40, pady = 0,columnspan=7,rowspan=1)
            guncelSaat = datetime.strptime(datetime.today().strftime("%H:%M:%S"),"%H:%M:%S")  # şimdiki güncel saat
            #kayitlar/D-103/2017-2018/Bahar
            if self.hangiKisim == 'loginPermit' or self.hangiKisim == "exitPermit":
                if not(os.path.exists('kayitlar/'+config['veri']['sinif']+'/'+self.yil+'/'+self.donem+'/'+self.dersKodu)):
                    os.mkdir('kayitlar/'+config['veri']['sinif']+'/'+self.yil+'/'+self.donem+'/'+self.dersKodu)
                if self.hangiKisim == "loginPermit":
                    if verbose:
                            print(">> ekranAyarla-loginPermit")
                    if self.dersAyar != self.hangiKisim:
                        self.adminButton.grid(row=0,column=4,padx= 0, pady = 25,columnspan=2,rowspan=1)# sticky=W
                        self.add_text_4(text='Öğr. Gör. Adı : ' + hocaAdi)
                        self.update4Update = Label(self.parent,bg=self.backGround, image=self._photoimage_4,wraplength=750,anchor="center")

                        self.update4Update.grid(row=3,column=0, sticky=W,padx= 40, pady = 0,columnspan=7,rowspan=1)#123
                    print('*****',self.dersBasla)
                    dersBaslamaSaati = datetime.strptime(self.dersBasla,"%H:%M:%S")  # dersin başlama saati
                    yoklamaSuresi = timedelta(minutes = int(config['veri']['dersGirisIzinSuresi']))
                    zamanSaniye = (dersBaslamaSaati + yoklamaSuresi - guncelSaat).seconds
                else: # exitPermit
                    if verbose:
                            print(">> ekranAyarla-exitPermit ")
                    dersBitisSaati = datetime.strptime(self.dersBitis.strftime("%H:%M:%S"),"%H:%M:%S")  # dersin başlama saati
                    yoklamaSuresi = timedelta(minutes = int(config['veri']['dersCikisIzinSuresi']))
                    cevap = self.yedekVeritabani.dersGirisCikisKarsilastir(self.dersBitis.strftime('%H:%M'),self.yil,self.donem)
                    if cevap == True:
                        zamanSaniye = (dersBitisSaati - guncelSaat -timedelta(minutes = 15)).seconds
                    else:
                        zamanSaniye = (dersBitisSaati - guncelSaat).seconds
                    if self.ErkenCikis == True:
                        guncelSaat = datetime.strptime(datetime.today().strftime("%H:%M:%S"),"%H:%M:%S")
                        zamanSaniye = (self.ErkenCikisDersBitmeSaati - guncelSaat).seconds
                        self.yoklamayaIzinVerme = False
                        sleep(2)
                        if verbose:
                            print(' >>> Erken çkış kalan zaman :' , zamanSaniye)
                self.kalanSaat = zamanSaniye
                self.buton.grid_remove()
                #self.update4Update.grid(row=6,column=0, sticky=W,padx= 20, pady = 35,columnspan=7,rowspan=2)
                #self.updateWrite4.set('Öğr. Gör. Adı : ' + hocaAdi)
                if self.dersAyar != self.hangiKisim:
                    self.adminButton.grid(row=0,column=4,padx= 0, pady = 25,columnspan=2,rowspan=1)# sticky=W
                    self.add_text_4(text='Öğr. Gör. Adı : ' + hocaAdi)
                    self.update4Update = Label(self.parent,bg=self.backGround, image=self._photoimage_4,wraplength=750,anchor="center")
                    self.update4Update.grid(row=3,column=0, sticky=W,padx= 40, pady = 0,columnspan=7,rowspan=1)#123


            elif self.hangiKisim == "between":
                if not(os.path.exists('kayitlar/'+config['veri']['sinif']+'/'+self.yil+'/'+self.donem+'/'+self.dersKodu)):
                    os.mkdir('kayitlar/'+config['veri']['sinif']+'/'+self.yil+'/'+self.donem+'/'+self.dersKodu)

                if verbose:
                    print(">> ekranAyarla -between ")

                dersBitisSaati = datetime.strptime(self.dersBitis.strftime("%H:%M:%S"),"%H:%M:%S")  # dersin başlama saati
                yoklamaSuresi = timedelta(minutes = int(config['veri']['dersCikisIzinSuresi']))
                zamanSaniye = (dersBitisSaati  - yoklamaSuresi - guncelSaat).seconds
                self.update4Update.grid_remove()
                if self.dersAyar != self.hangiKisim:
                    self.adminButton.grid(row=0,column=4,padx= 0, pady = 25,columnspan=2,rowspan=1)# sticky=W
                    self.add_text_button(text=config['veri']['butonYazisi'])
                    self.buton = Button(self.parent,bg=self.backGround, image=self._photoimage_button,wraplength=750,anchor="center",height=30,width=738,highlightbackground="black",command=self.onayKutusu)
                    self.buton.grid(row=3,column=0, sticky=W,padx= 32, pady = 0,columnspan=7,rowspan=1)


                self.kalanSaat = zamanSaniye
            if self.dersAyar != self.hangiKisim:
                self.dersAyar = self.hangiKisim
        elif self.hangiKisim == 'erkenCikis' :
            if verbose:
                print(">> ekranAyarla -erkenCikis ")
                print('>> Time : {}'.format(datetime.today().strftime('%H:%M:%S')))
            self.rd.grid(row=0,column=0,padx=0 ,  pady = 0,rowspan=5,columnspan=7)
            self.amblo.grid_remove()
            self.gr.grid_remove()
            self.buton.grid_remove()
            self.update2Update.grid_remove()
            if self.dersAyar != self.hangiKisim:
                self.adminButton.grid(row=0,column=4,padx= 0, pady = 25,columnspan=2,rowspan=1)# sticky=W
                self.add_text_4(text='Öğr. Gör. Adı : ' + hocaAdi)
                self.update4Update = Label(self.parent,bg=self.backGround, image=self._photoimage_4,wraplength=750,anchor="center")
                self.dersAyar = self.hangiKisim
                self.update4Update.grid(row=3,column=0, sticky=W,padx= 40, pady = 0,columnspan=7,rowspan=1)#123


        elif self.hangiKisim == None:

            if verbose:
                    print(">> ekranAyarla-None")
            if self.dersAyar != self.hangiKisim:
                self.adminButton.grid_remove()
                self.update4Update.grid_remove()
                self.update3Update.grid_remove()
                self.update2Update.grid_remove()
                self.buton.grid_remove()
                self.kalanSaat = None
                self.rd.grid_remove()
                self.gr.grid_remove()
                self.amblo.grid(row=0,column=0,padx=0 ,  pady = 0,rowspan=5,columnspan=7)
                self.add_text_3(text=config['veri']['dersBaslamadiYazisi'])
                self.update3Update = Label(self.parent,bg=self.backGround, image=self._photoimage_3,wraplength=750,anchor="center")
                self.update3Update.grid(row=2,column=0, sticky=W,padx= 40, pady = 0,columnspan=7,rowspan=1)
                self.dersAyar = self.hangiKisim
        else:
            pass
        if verbose:
            print(">>> Kalan Saniye :",self.kalanSaat)
            print('>>> Time : {}'.format(datetime.today().strftime('%H:%M:%S')))
        if verbose:
            print("< read_card.tkinterGui.ekranAyarla() fonksiyonundan çıkış yapılıyor... >")

if __name__ == "__main__":

    root = Tk()
    root.call('tk', 'scaling', 1.0)
    run = tkinterGui(root)
    #root.after(1000,run.loading_start)
    root.mainloop()
