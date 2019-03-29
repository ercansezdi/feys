#!/usr/bin/env python
# -*- coding: utf8 -*-

__auther__ = 'Ercan Sezdi'
__version__ = '0.2'

##########################################################################################################################################################################################
########################################################################### LIBRARY ######################################################################################################
##########################################################################################################################################################################################
from threading import Thread
import random
import os # sistem komutlarini kontrol etmek için
import socket # internet kontrol için kütüphane
from suds.client import Client # okulun veritabanina bağlanmak için kütüphane
import configparser # bilgilerin verildiği dosyayı okumak için
import sqlite3 # veritabani oluşturmak için
from time import strftime,ctime,sleep,strptime # zamanı almak için
from datetime import datetime ,timedelta
#import ntplib # zaman kontrolu yapmak için
from tkinter import Tk,Label,Button,PhotoImage,ttk,Frame,StringVar,Menu,Toplevel,Canvas,ALL,W,N,S,E,SUNKEN,Scrollbar
from PIL import Image, ImageFont, ImageDraw,ImageTk
import textwrap
import tkinter.ttk
import RPi.GPIO as GPIO
import MFRC522
from functools import partial
import signal
##########################################################################################################################################################################################
############################################################################ MODÜLLER ####################################################################################################
##########################################################################################################################################################################################

#import runChapter
import yedekDatabase #verileri database yazmak için sqlite3 'den yararlanaılarak oluşturulan modul
import webservice

##########################################################################################################################################################################################
####################################################################### AÇIKLAMA #########################################################################################################


                        # Global değişkenler

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


##########################################################################################################################################################################################
################################################################ ANA PROGRAM  ############################################################################################################
##########################################################################################################################################################################################
############################################################################# CLASS BOLUMU  ##############################################################################################
##########################################################################################################################################################################################
########################################################################################### BUZZER  CLASS ################################################################################
##########################################################################################################################################################################################
class buzzerClass():
    def __init__(self):

        GPIO.setmode(GPIO.BOARD)
        self.buzzer_pin = 37
        #GPIO.setup(self.buzzer_pin, GPIO.IN)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
    def buzz(self,pitch, duration):   #create the function “buzz” and feed it the pitch and duration)

        if(pitch==0):
            sleep(duration)
            return
        period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
        delay = period / 2     #calcuate the time for half of the wave
        cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency

        for i in range(cycles):    #start a loop from 0 to the variable “cycles” calculated above
            GPIO.output(self.buzzer_pin, True)   #set pin 18 to high
            sleep(delay)    #wait with pin 18 high
            GPIO.output(self.buzzer_pin, False)    #set pin 18 to low
            sleep(delay)    #wait with pin 18 low
    def play(self,tune):
        x=0
        if(tune==1): #st
            pitches=[10, 20]
            duration=[0.2,0.2]
            for p in pitches:
                self.buzz(p, duration[x])  #feed the pitch and duration to the func$
                sleep(duration[x] *0.5)
                x+=1

        elif(tune==2):
            pitches=[90]
            duration=[0.4]
            for p in pitches:
                self.buzz(p, duration[x])  #feed the pitch and duration to the func$
                sleep(duration[x] *0.5)
                x+=1

        elif(tune==3): # te
            pitches=[10, 20]
            duration=[0.1,0.2]
            for p in pitches:
                self.buzz(p, duration[x])  #feed the pitch and duration to the func$
                sleep(duration[x] *0.5)
                x+=1
##########################################################################################################################################################################################
########################################################################################### RGB CLASS ####################################################################################
##########################################################################################################################################################################################
class RedGreenBlueLed: # Ledler için class
    def __init__(self): # ledler için gerekli pinler tanımlanıyor ### ortak katotlu
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.kirmizi=29
        self.yesil=31
        self.mavi =33
        GPIO.setup(self.kirmizi,GPIO.OUT)
        GPIO.setup(self.yesil  ,GPIO.OUT)
        GPIO.setup(self.mavi  ,GPIO.OUT)
        config.read(configDosyasiAdres)
    def redOn(self):
        GPIO.output(self.kirmizi,GPIO.LOW)
        GPIO.output(self.yesil  ,GPIO.HIGH)
        GPIO.output(self.mavi   ,GPIO.HIGH)
        sleep(int(config['veri']['popupSuresi']))
        GPIO.output(self.kirmizi,GPIO.HIGH)
        GPIO.output(self.yesil  ,GPIO.HIGH)
        GPIO.output(self.mavi  ,GPIO.HIGH)
    def greenOn(self):
        GPIO.output(self.kirmizi,GPIO.HIGH)
        GPIO.output(self.yesil,GPIO.LOW)
        GPIO.output(self.mavi ,GPIO.HIGH)
        sleep(int(config['veri']['popupSuresi']))
        GPIO.output(self.kirmizi,GPIO.HIGH)
        GPIO.output(self.yesil,GPIO.HIGH)
        GPIO.output(self.mavi,GPIO.HIGH)
    def blueOn(self):
        GPIO.output(self.kirmizi,GPIO.HIGH)
        GPIO.output(self.yesil,GPIO.HIGH)
        GPIO.output(self.mavi ,GPIO.LOW)
        sleep(int(config['veri']['popupSuresi']))
        GPIO.output(self.kirmizi,GPIO.HIGH)
        GPIO.output(self.yesil,GPIO.HIGH)
        GPIO.output(self.mavi,GPIO.HIGH)
##########################################################################################################################################################################################
########################################################################################### INTERNET KONTROL  CLASS ######################################################################
##########################################################################################################################################################################################
class internetSaatKontrol :
    def __init__(self):
        config.read(configDosyasiAdres)
        self.portNo  = config['veri']['port'] # bilgiler dosyasindaki veri isminde adindaki değişken içine atanmış olan port değişkenini aldım
        self.pingGonderAdres = config['veri']['dnsAdres'] # bilgiler dosyasindaki veri isminde adindaki değişken içine atanmış dnsAdres port değişkenini aldım
        self.sinif_adi = config['veri']['sinif']
    def internet(self): # internet bağlantisini kontrol edecek olan fonksiyonu tanımladım
        if verbose:
            print('< internetSaatKontrol.internet() fonksiyonuna giriş yapılıyor... >')
        i=0
        sayac=0
        while i<3: # 3 döngünün 3 defa dönmesini sağladım bu sayede 3 False olursa internet olmadığını anlayacağız
            try:
                socket.setdefaulttimeout(3)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.pingGonderAdres, int(self.portNo))) #aldiği dnsAdres ve portNo değişkenlerini yerine yazdim
            except Exception:
                sayac=sayac+1 # eğerki verilen dnsAdresindeki porta bağlanamaz ise sayac değişkenini bir arttıracak bu sayede 3 defa false olduğunu anlayacağız
            i=i+1

        if sayac == 3 : # eğer ki 3 adet False döndü ise geriye internetYok olarak döndürecek.
            if verbose:
                print('< internetSaatKontrol.internet() fonksiyonundan çıkış yapılıyor... >')
            veri_yaz = open("kayitlar/"+ str(self.sinif_adi) + "/genelKayitlar/internetKontrol/internet.txt",'a')
            veri_yaz.write("Saat {} 'de-da internet bağlantısı yoktur.\n".format(datetime.today().strftime('%H:%M:%S')))
            veri_yaz.close()
            return False
        else: # 3 'den daha az defa False döndü ise cevap olarak internetVar olarak dönücek ve internetin olduğunu anlayacağız.
            if verbose:
                print('< internetSaatKontrol.internet() fonksiyonundan çıkış yapılıyor... >')
            veri_yaz = open("kayitlar/"+ str(self.sinif_adi) + "/genelKayitlar/internetKontrol/internet.txt",'a')
            veri_yaz.write("Saat {} 'de-da internet bağlantısı vardır.\n".format(datetime.today().strftime('%H:%M:%S')))
            veri_yaz.close()
            return True
##########################################################################################################################################################################################
########################################################################################### ELEKTRIK KONTROL  CLASS ######################################################################
##########################################################################################################################################################################################
class elektrikKontrol:#New
    def __init__(self):
        config.read(configDosyasiAdres)
    def kontrol(self,yil,donem,tarih):
        if verbose:
            print('< read_card.elektrikKontrol.kontrol() fonksiyonuna giriş yapılıyor... >')

        if not(os.path.isfile( 'kayitlar/' + config['veri']['sinif'] + '/' + yil + '/' + donem + '/elektrikKayit/'  + 'sonGuncellemeTarihi.db')):
            print('**   ','kayitlar/' + config['veri']['sinif'] + '/' +  yil + '/' + donem + '/elektrikKayit/sonGuncellemeTarihi.db')
            print('kayitlar/' + config['veri']['sinif'] + '/' +  yil + '/' + donem + '/elektrikKayit/sonGuncellemeTarihi.db')
            baglan = sqlite3.connect( 'kayitlar/' + config['veri']['sinif'] + '/' +  yil + '/' + donem + '/elektrikKayit/sonGuncellemeTarihi.db')
            veri = baglan.cursor()
            veri.execute("CREATE TABLE guncelleme_tarihi (database_son_guncelleme_tarihi)")
            baglan.commit()

        baglan = sqlite3.connect( 'kayitlar/' + config['veri']['sinif'] + '/' + yil + '/' + donem + '/elektrikKayit/sonGuncellemeTarihi.db')
        veri = baglan.cursor()
        sonuc  = veri.execute('select * from guncelleme_tarihi').fetchall()
        baglan.commit()

        sart = False
        for i in sonuc :
            if str(i[0]) == str(tarih) :
                sart = True

        if sart != True:
            if verbose:
                print('<> Gün içersinde güncellenmiş database Mevcut değildir, Güncelleme yapılacaktır... >')
                print('< read_card.elektrikKontrol.kontrol() fonksiyonuna çıkış yapılıyor... >')
            return False
        else:
            if verbose:
                print('<> Gün içersinde güncellenmiş database mevcuttur, Güncelleme yapılmayacaktır...>')
                print('< read_card.elektrikKontrol.kontrol() fonksiyonuna çıkış yapılıyor... >')
            return True
##########################################################################################################################################################################################
########################################################################################### GEREKLI KLASORLER CLASS ######################################################################
##########################################################################################################################################################################################
class klasorKontrolClass: #### NeW
    def __init__(self):
        config.read(configDosyasiAdres)
    def klasorKontrol(self,yil,donem):
        if verbose:
            print('< read_card.klasorKontrol.klasorKontrol() fonksiyonu giriş yapılıyor...>')
            print('>> kontrol -> Gerekli klasörler oluşturuluyor...')
        adres=''
        if not(os.path.exists('kayitlar/')):
            os.mkdir(adres +'kayitlar/')
        adres = adres +'kayitlar/'
        if not(os.path.exists(adres + config['veri']['sinif'] + '/')):
            os.mkdir(adres + config['veri']['sinif'] + '/')
        adres = adres + config['veri']['sinif'] + '/'
        if not(os.path.exists(adres + '/' + yil + '/')):
            os.mkdir(adres + '/' + yil + '/')
        adres = adres + '/' + yil + '/'
        if not(os.path.exists(adres + '/' + donem + '/')):
            os.mkdir(adres + '/' + donem + '/')
        adres = adres + '/' + donem + '/'
        if not(os.path.exists(adres + 'yoklamaKayit/')):
            os.mkdir(adres + '/yoklamaKayit/')
        if not(os.path.exists(adres + '/' + 'elektrikKayit' + '/')):
            os.mkdir(adres + '/elektrikKayit/')

        if verbose:
            print('< read_card.klasorKontrol.klasorKontrol() fonksiyonundan çıkış yapılıyor...>')
    def klasorNoNetwork(self):
        if verbose:
            print('< read_card.klasorKontrol.klasornoNetwork() fonksiyonuna giriş yapılıyor...>')
            print('>> klasorNoNetwork -> Gerekli klasörler oluşturuluyor...')
        adres = ''
        if not(os.path.exists(adres +'kayitlar/')):
            os.mkdir(adres +'kayitlar/')
        adres = adres +'kayitlar/'
        if not(os.path.exists(adres + config['veri']['sinif'] + '/')):
            os.mkdir(adres + config['veri']['sinif'] + '/')
        adres = adres + config['veri']['sinif'] + '/'
        if not(os.path.exists(adres + 'genelKayitlar/')):
            os.mkdir(adres + 'genelKayitlar/')
        adres = adres + 'genelKayitlar/'
        if not(os.path.exists(adres + 'internetKontrol/')):
            os.mkdir(adres + 'internetKontrol/')

        if verbose:
            print('< read_card.klasorKontrol.klasornoNetwork() fonksiyonundan çıkış yapılıyor... >')

    #######################################################################################################################################################
##########################################################################################################################################################################################
###########################################################################################  GUI CLASS ###################################################################################
##########################################################################################################################################################################################
class tkinterGui(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.parent.attributes("-fullscreen", True)
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
        self.internetClass =  internetSaatKontrol() # internet'in olup olmadiğini kontrol ettiğim modülü çağirdim
        self.yedekVeritabani = yedekDatabase.veritabani() # veritabani olup olmadığını kontrol etmek için veritabani classını çağirdim.
        self.baglanWebservice = webservice.webserviceClass() # webservis classını çağırdım
        self.elektControl = elektrikKontrol() #class
        self.klasorler = klasorKontrolClass() # class
        #GPIO.cleanup()
        self.rgb = RedGreenBlueLed() # redOn, blueOn ve green0n vardır.
        self.buzzer = buzzerClass() # self.buzzer.play(x) x= olumlu veya x = olumsuz
        signal.signal(signal.SIGINT, self.end_read)
        self.MIFAREReader = MFRC522.MFRC522()

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
        #######################################
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
    def admin_panel_giris(self):
        self.yoklamayaIzinVerme = True
        self.admin_panel()
    def admin_panel_cikis(self):
        self.ek_screen.destroy()
        self.yoklamayaIzinVerme = False
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


        self.adminButton = Button(self.parent,text = 'Yönetici Paneli',font ="Helvetica 10 bold italic",bg=self.backGround,fg='white',anchor="center",height=2,width=17,highlightbackground="black",command=self.admin_panel_giris)
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


        saat = Thread(target=self.saatGuncelle)
        ekran = Thread(target=self.ekranAyarla)

        if verbose:
            print("< read_card.tkinterGui.mainScreen() fonksiyonundan çıkış yapılıyor.")
        saat.start()
        ekran.start()
    def addPeople(self):
        if self.hangiKisim != None:
            if len(self.deger) == 9:
                if self.araDegisken2 == 1 and self.izinAraDegisken == 1 :
                    self.izinAraDegisken = 0
                    self.geriSayimSuresi  = config['veri']['geriSayim']
                    self.sayim = int(datetime.today().strftime('%S') ) + int(self.geriSayimSuresi)
                    self.popupPencere_Two = Toplevel()
                    self.popupPencere_Two.configure(background=self.backGround,cursor = 'none')
                    self.popupPencere_Two.attributes("-fullscreen", True)
                    yazi = Label(self.popupPencere_Two,textvariable=self.geriSayim,font ="Helvetica 200 bold italic",bg = self.backGround,wraplength=475)
                    yazi.grid(row=4,column=3,columnspan=7,rowspan = 7,padx=0,pady=0)#, sticky=W)#,padx= 310, pady=100)

                    button = Button(self.popupPencere_Two,font = "Helvetica 15 bold italic",padx = 20,text = 'X',command = self.popupPencere_Two.destroy,bg=self.backGround)
                    button.grid(row = 0, column = 7,padx = 720,pady=0,rowspan=1,columnspan=7)#,columnspan = 2,rowspan = 2)
                    self.geriSayimFunk()
                if self.araDegisken2 == 'kartOkundu':
                    bugun = datetime.today().strftime('%A')
                    baglan = sqlite3.connect( 'kayitlar/' + config['veri']['sinif'] + '/' + self.yil + '/' + self.donem + '/yoklamaKayit/' + bugun + '.db')
                    veri = baglan.cursor()
                    dersBaslamaSaati = self.dersBasla.strftime('%H:%M')
                    dersAdi = str(self.dersKodu) + '_' + str(self.dersAdi)+ '_' + str(dersBaslamaSaati)
                    kisiBilgisi = veri.execute("SELECT * FROM '" + dersAdi +"' WHERE Numara=?", (self.deger,)).fetchone()
                    baglan.commit()

                    if kisiBilgisi != None:
                        bugunTarih = datetime.today().strftime('%d-%m-%Y')
                        simdiSaat = datetime.today().strftime('%H-%M-%S')
                        baglan = sqlite3.connect( 'kayitlar/' + config['veri']['sinif'] + '/' + self.yil + '/' + self.donem + '/' + self.dersKodu + '/'+ bugunTarih +'.db')
                        veri = baglan.cursor()
                        kontrol = veri.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name ='" + self.dersKodu+"'" ).fetchone()
                        if kontrol == None:
                            veri.execute("""CREATE TABLE {} (
                            'Numara'	 TEXT UNIQUE,
                            'Ad_Soyad'	 TEXT,
                            'Tarih'      TEXT,
                            'Giris_Saat' TEXT,
                            'Cikis_Saat' TEXT,
                            'Statu'     TEXT,
                            'Ders_Metod' TEXT,
                            PRIMARY KEY(Numara));""".format(self.dersKodu))
                            baglan.commit()
                        buKisiEklimi = veri.execute("select exists(select * from '" + self.dersKodu  +"' where numara = '"+  str(self.deger) + "')").fetchone()[0]
                        if buKisiEklimi == 0:
                            veri.execute("INSERT INTO '" + self.dersKodu +"' (Numara,Ad_Soyad,Tarih,Giris_Saat,Cikis_Saat,Statu,Ders_Metod) VALUES (?,?,?,?,?,?,?)",(self.deger,kisiBilgisi[1],bugunTarih,'E-'+ simdiSaat,None,kisiBilgisi[14],None))
                        else:
                            self.hata_ver()
                        baglan.commit()
                        self.deger = ''
                        self.st.set(self.deger)
                        self.araDegisken2 = 0
                        #self.tree.delete()
                        self.CreateUI()
                        self.LoadTable()

                    else:
                        self.hata_ver()
                        self.deger = ''
                        self.st.set(self.deger)
                        self.araDegisken2 = 1
                    #işlemler
                if self.geriSayimSuresi > 1:
                    root.after(1000,run.addPeople)
            else:
                self.hata_ver()
                self.araDegisken2 = 1
                self.deger = ''
                self.st.set(self.deger)
        else:
            self.hata_ver()
            self.araDegisken2 = 1
            self.deger = ''
            self.st.set(self.deger)
    def deletePeople(self):
        if self.hangiKisim != None:
            if len(self.deger) == 9:
                if self.araDegisken2 == 1 and self.izinAraDegisken == 1 :# self.yoklamayaIzinVerme == True and
                    #self.yoklamayaIzinVerme = True
                    self.izinAraDegisken = 0
                    self.geriSayimSuresi  = config['veri']['geriSayim']
                    self.sayim = int(datetime.today().strftime('%S') ) + int(self.geriSayimSuresi)
                    self.popupPencere_Two = Toplevel()
                    self.popupPencere_Two.configure(background=self.backGround,cursor = 'none')
                    self.popupPencere_Two.attributes("-fullscreen", True)

                    yazi = Label(self.popupPencere_Two,textvariable=self.geriSayim,font ="Helvetica 200 bold italic",bg = self.backGround,wraplength=475)
                    yazi.grid(row=4,column=3,columnspan=7,rowspan = 7,padx=0,pady=0)#, sticky=W)#,padx= 310, pady=100)

                    button = Button(self.popupPencere_Two,font = "Helvetica 15 bold italic",padx = 20,text = 'X',command = self.popupPencere_Two.destroy,bg=self.backGround)
                    button.grid(row = 0, column = 7,padx = 720,pady=0,rowspan=1,columnspan=7)#,columnspan = 2,rowspan = 2)
                    self.geriSayimFunk()
                if self.araDegisken2 == 'kartOkundu':
                    bugun = datetime.today().strftime('%A')
                    baglan = sqlite3.connect( 'kayitlar/' + config['veri']['sinif'] + '/' + self.yil + '/' + self.donem + '/yoklamaKayit/' + bugun + '.db')
                    veri = baglan.cursor()
                    dersBaslamaSaati = self.dersBasla.strftime('%H:%M')
                    dersAdi = str(self.dersKodu) + '_' + str(self.dersAdi)+ '_' + str(dersBaslamaSaati)
                    kisiBilgisi = veri.execute("SELECT * FROM '" + dersAdi +"' WHERE Numara=?", (self.deger,)).fetchone()
                    baglan.commit()

                    if kisiBilgisi != None:
                        bugunTarih = datetime.today().strftime('%d-%m-%Y')
                        simdiSaat = datetime.today().strftime('%H-%M-%S')
                        baglan = sqlite3.connect( 'kayitlar/' + config['veri']['sinif'] + '/' + self.yil + '/' + self.donem + '/' + self.dersKodu + '/'+ bugunTarih +'.db')
                        veri = baglan.cursor()
                        kontrol = veri.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name ='" + self.dersKodu+"'" ).fetchone()
                        if kontrol == None:
                            veri.execute("""CREATE TABLE {} (
                            'Numara'	 TEXT UNIQUE,
                            'Ad_Soyad'	 TEXT,
                            'Tarih'      TEXT,
                            'Giris_Saat' TEXT,
                            'Cikis_Saat' TEXT,
                            'Statu'     TEXT,
                            'Ders_Metod' TEXT,
                            PRIMARY KEY(Numara));""".format(self.dersKodu))
                            baglan.commit()
                        buKisiEklimi = veri.execute("select exists(select * from '" + self.dersKodu  +"' where numara = '"+  str(self.deger) + "')").fetchone()[0]
                        if buKisiEklimi == 0:
                            self.hata_ver()
                            self.deger = ''
                            self.st.set(self.deger)
                            self.araDegisken2 = 0
                        else:
                            veri.execute("Delete from " + self.dersKodu + " where numara='" + self.deger + "'")
                        baglan.commit()
                        self.deger = ''
                        self.st.set(self.deger)
                        self.araDegisken2 = 1
                        #self.tree.delete()
                        self.CreateUI()
                        self.LoadTable()

                    else:
                        self.hata_ver()
                        self.deger = ''
                        self.araDegisken2 = 1
                        self.st.set(self.deger)
                    #işlemler
                if self.geriSayimSuresi > 1:
                    self.yoklamayaIzinVerme = True
                    root.after(1000,run.deletePeople)
            else:
                self.hata_ver()
                self.deger = ''
                self.araDegisken2 = 1
                self.st.set(self.deger)
        else:
            self.hata_ver()
            self.deger = ''
            self.araDegisken2 = 1
            self.st.set(self.deger)
    def girisYapanlar(self):
        #-------------------------------------------------------------------------------------------------------------------------------------------- veri.execute("Delete from " + databaseTabloAdi + " where numara='" + i[0] + "'")
        if verbose:
            print('< read_card.tkinterGui.girisYapanlar() fonksiyonuna giriş yapılıyor... >')
        self.araPencere = Toplevel()
        self.yoklamayaIzinVerme = True
        self.araPencere.configure(background=self.backGround,borderwidth=0,cursor = 'none')
        self.araPencere.attributes("-fullscreen", True)
        self.CreateUI()
        self.LoadTable()
        self.grid(sticky = (N,S,W,E))
        self.araPencere.grid_rowconfigure(0, weight = 0)
        self.araPencere.grid_columnconfigure(0, weight = 0)

        if verbose:
            print('< read_card.tkinterGui.girisYapanlar() fonksiyonundan çıkış yapılıyor... >')
    def geriSayimFunk(self):
        self.geriSayim.set(self.sayim - int(datetime.today().strftime('%S')))
        self.geriSayimSuresi = self.sayim - int(datetime.today().strftime('%S'))
        #--------------------------------------
        #--------------------------------------
        if (self.sayim - int(datetime.today().strftime('%S'))) < 0  or  self.sayim - int(datetime.today().strftime('%S')) > int(config['veri']['geriSayim']):
            self.yoklamayaIzinVerme = True
            self.popupPencere_Two.destroy()
            self.izinAraDegisken = 1
        else:

            kartIdOgren = self.kart_okuma()
            if kartIdOgren != False :
                numara,adSoyad,statu,dersSaati = self.yedekVeritabani.kartIDKontrol(self.yil,self.donem,kartIdOgren,self.tabloAdi)
                if statu == 'TE':

                    self.popupPencere_Two.destroy()
                    self.geriSayimSuresi = -1
                    self.araDegisken2 = 'kartOkundu'
                    self.izinAraDegisken=1
                    self.yoklamayaIzinVerme = True
                else:
                    self.popupPencere_Two.destroy()
                    self.araDegisken2 = 1
                    self.geriSayimSuresi = -1
                    self.izinAraDegisken = 1
                    self.yoklamayaIzinVerme = True

            else:
                root.after(1000,run.geriSayimFunk)
    def LoadTable(self):
        self.yoklamayaIzinVerme = True
        if self.hangiKisim != None:
            if self.araDegisken2 == 0:
                self.araDegisken2 = 1
            bugunTarih = datetime.today().strftime('%d-%m-%Y')
            baglan = sqlite3.connect( 'kayitlar/' + config['veri']['sinif'] + '/' + self.yil + '/' + self.donem + '/' + self.dersKodu + '/' +bugunTarih +'.db')
            veri = baglan.cursor()
            try:
                veriler = veri.execute('select * from '+self.dersKodu)
                baglan.commit()
            except:
                veriler = None
            sayac = 1
            for i in veriler:
                self.tree.insert('', 'end', text= sayac, values=(i[0],i[1],i[3]))
                sayac = sayac + 1
        else:
            pass
    def CreateUI(self):
        self.yoklamayaIzinVerme = True
        self.tree =  tkinter.ttk.Treeview(self.araPencere, height=11)

        self.tree.place(x=30, y=95)
        #self.tree.configure(bg = self.backGround)
        vsb = tkinter.ttk.Scrollbar(self.araPencere, orient="vertical", command=self.tree.yview)
        vsb.place(x=30+750+2, y=0, height=217+20)
        self.tree.configure(yscrollcommand=vsb.set)
        buttons = [['1','2','3'],
                  ['4','5','6'],
                  ['7','8','9'],
                  ['x','0','<']]
        for r in range(4):
            for c in range(3):
                button = Button(self.araPencere,
                                font = "Helvetica 30 bold italic",
                                padx = 20,anchor="center",highlightbackground="black",bg=self.backGround,
                                text = buttons[r][c],
                                command = partial(self.buttonClicked, buttons[r][c]))
                button.grid(row = r+5, column = c,padx = 0,pady=0)#,columnspan = 0,rowspan = 0)

        buton1 = Button(self.araPencere,text= ' Kapat ', width=0,height=0,font = "Helvetica 30 bold italic",command=self.araPencere.destroy,anchor="center",highlightbackground="black",bg=self.backGround)
        buton1.grid(row=8,column=3,sticky=W,padx=0, pady=0,rowspan = 2,columnspan = 3 )

        buton2 = Button(self.araPencere,text= ' Kayıt Sil ', width=0,height=0,font = "Helvetica 30 bold italic",command=self.deletePeople,anchor="center",highlightbackground="black",bg=self.backGround)
        buton2.grid(row=8,column=6,sticky=W,padx=0, pady=0,rowspan = 2,columnspan = 3 )

        buton3 = Button(self.araPencere,text= ' Kayıt Ekle ', width=0,height=0,font = "Helvetica 30 bold italic",command=self.addPeople,anchor="center",highlightbackground="black",bg=self.backGround)
        buton3.grid(row=8,column=9,sticky=W,padx=0, pady=0,rowspan = 2,columnspan = 3 )

        numaraGiris = Label(self.araPencere,textvariable =self.st,width = 0,font = "Helvetica 75 bold italic",anchor="center",highlightbackground="black",bg=self.backGround)#,bd = 25)
        numaraGiris.grid(row =4 , column =3,padx = 0,pady=0,columnspan = 9,rowspan =3)

        self.tree['columns'] = ('starttime', 'endtime', 'status')
        #-------------------------------------------------------
        self.tree.heading("#0", text='Giriş Sırası', anchor='center')
        self.tree.column("#0", anchor="center",width=100,minwidth= 35)#W,N,S,
        #-------------------------------------------------------
        self.tree.heading('starttime', text='Numarası', anchor='center')
        self.tree.column('starttime', anchor='center', width=150,minwidth= 130)
        #-------------------------------------------------------
        self.tree.heading('endtime', text='Adı - Soyadı', anchor='center')
        self.tree.column('endtime', anchor='center', width=350,minwidth= 125)
        #-------------------------------------------------------
        self.tree.heading('status', text='Giriş Saati', anchor='center')
        self.tree.column('status', anchor='center', width=130,minwidth=0)
        #-------------------------------------------------------
        self.tree.grid(sticky = (N,S,W,E),row = 0, column = 0,padx = 0,pady=0,columnspan = 12 ,rowspan = 4)

        self.canvas = Canvas(self.tree, relief=SUNKEN, borderwidth=2)#,
                         #scrollregion=('-11c', '-11c', '50c', '20c'))
        self.vscroll = Scrollbar(self.tree, command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.vscroll.set)

        tkinter.ttk.Style().configure("Treeview",background=self.backGround,fieldbackground = self.backGround,font=(None,12),foreground=self.foreGround_2)

        self.tree.grid_rowconfigure(0, weight = 1)
        self.tree.grid_columnconfigure(0, weight = 1)
        #--------------------------------------------------------------------------------------------------------------------------------------------
    def buttonClicked(self,buttonVal):
        self.yoklamayaIzinVerme = True
        sayi = int(len(self.deger))
        if buttonVal == '<':

            self.deger = ".".join(self.deger)
            self.deger = self.deger.split(".")
            sonuc =  ''
            for i in range(sayi-1):
                sonuc = sonuc + self.deger[i]
            self.deger = sonuc
            self.st.set(self.deger)

        elif buttonVal == 'x':
            self.deger= ''
            self.st.set(self.deger)
        elif sayi < 9:
            self.deger = self.deger + buttonVal
            self.st.set(self.deger)
        else:
            pass
    def hakkinda(self):
        if self.araDegisken == 1:
            self.pencere_hakkinda = Toplevel()
            self.pencere_hakkinda.configure(background=self.backGround,borderwidth=0,cursor = 'none')
            self.pencere_hakkinda.attributes("-fullscreen", True)
            hakkinda=Label(self.pencere_hakkinda,image=self.aboutPhoto).grid(rowspan = 3,row=2)
            self.kapanmaZamani = datetime.strptime(datetime.today().strftime('%H:%M:%S'),'%H:%M:%S')
            sure = timedelta(seconds = int(config['veri']['popupSuresi']))
            self.kapanmaZamani = self.kapanmaZamani + sure
            self.kapanmaZamani = self.kapanmaZamani.strftime('%H:%M:%S')
            self.kapanmaZamani = datetime.strptime(self.kapanmaZamani,'%H:%M:%S')
            self.araDegisken = 0
        guncelSure = datetime.strptime(datetime.today().strftime('%H:%M:%S'),'%H:%M:%S')
        if guncelSure > self.kapanmaZamani:
            self.pencere_hakkinda.destroy()
            self.araDegisken = 1
        else:
            self.tekrarBasla = root.after(1000,run.hakkinda)
    def menuGuncellemesi(self):
        self.windows = Toplevel()
        self.windows.attributes("-fullscreen", True)
        self.windows.bind('<Escape>',quit)
        self.windows.configure(background=self.backGround,cursor = 'none')
        self.loadingGerekliTanimlamalar()
        self.yoklamayaIzinVerme = True
        target3 = Thread(target = self.start_loading)
        target4 = Thread(target = self.dailyUpdate)
        target3.start()
        target4.start()
    def menuTamGuncelleme(self):
        self.yoklamayaIzinVerme = True
        self.internetVarmi = self.internetClass.internet()
        if self.internetVarmi == True:
            self.araDegisken = 0
            self.windows = Toplevel()
            self.windows.attributes("-fullscreen", True)
            self.windows.bind('<Escape>',quit)
            self.windows.configure(background=self.backGround,cursor = 'none')
            self.loadingGerekliTanimlamalar()
            target3 = Thread(target = self.start_loading)
            target4 = Thread(target = self.dailyUpdate)
            target3.start()
            target4.start()
        else:
            noWifi = Thread(target=self.popup,args=('no_wifi',))
            noWifi.start()
        self.yoklamayaIzinVerme = False
    def menu_uyari(self):
        if verbose:
            print('< read_card.tkinterGui.popup() fonksiyonuna giriş yapılıyor... >')
        self.yoklamayaIzinVerme = True
        self.pencere_menu_uyari = Toplevel()
        self.pencere_menu_uyari.configure(background=self.backGround,cursor = 'none')
        self.pencere_menu_uyari.attributes("-fullscreen", True)
        eight = Label(self.pencere_menu_uyari,image=self.hata_ret,borderwidth=0)
        eight.grid(row = 0, column = 0,padx = 0,pady=0,columnspan = 8,rowspan = 8)

        button = Button(self.pencere_menu_uyari,font = "Helvetica 15 bold italic",padx = 20,text = 'X',command = self.pencere_menu_uyari.destroy,bg=self.backGround)
        button.grid(row = 0, column = 7,padx = 0,pady=0)#,columnspan = 2,rowspan = 2)
        sleep(int(config['veri']['popupSuresi']))
        self.pencere_menu_uyari.destroy()
    def iki(self,numara):
        self.yoklamayaIzinVerme = True
        self.butonGecici = Button(self.dersSecim,text= '1 + 1 ', width=52,height=8,font = "Helvetica 20 bold italic",command=lambda: self.islemler("1+1",numara))
        self.butonGecici.grid(row=0,column=0, sticky=W,padx= 0, pady = 0,columnspan=2,rowspan=2)
        self.butonGecici = Button(self.dersSecim,text= '2 + 0', width=52,height=8,font = "Helvetica 20 bold italic",command=lambda: self.islemler("2+0",numara))
        self.butonGecici.grid(row=2,column=0, sticky=W,padx= 0, pady = 0,columnspan=2,rowspan=2)
    def uc(self,numara):
        self.yoklamayaIzinVerme = True
        self.butonGecici = Button(self.dersSecim,text= '1 + 1 + 1', width=44,height=3,font = "Helvetica 24 bold italic",command=lambda: self.islemler("1+1+1",numara))
        self.butonGecici.grid(row=0,column=0, sticky=W,padx= 0, pady = 0,columnspan=2,rowspan=2)
        self.butonGecici = Button(self.dersSecim,text= '3 + 0 ', width=44,height=3,font = "Helvetica 24 bold italic",command=lambda: self.islemler("3+0",numara))
        self.butonGecici.grid(row=2,column=0, sticky=W,padx= 0, pady = 0,columnspan=2,rowspan=2)
        self.butonGecici = Button(self.dersSecim,text= '2 + 1', width=44,height=3,font = "Helvetica 24 bold italic",command=lambda: self.islemler("2+1",numara))
        self.butonGecici.grid(row=4,column=0, sticky=W,padx= 0, pady = 0,columnspan=2,rowspan=2)
        self.butonGecici = Button(self.dersSecim,text= '1 + 2 ', width=44,height=3,font = "Helvetica 24 bold italic",command=lambda: self.islemler("1+2",numara))
        self.butonGecici.grid(row=6,column=0, sticky=W,padx= 0, pady = 0,columnspan=2,rowspan=2)
    def dort(self,numara):
        self.yoklamayaIzinVerme = True
        self.butonGecici = Button(self.dersSecim,text= '1 + 1 + 1 + 1', width=56,height=3,font = "Helvetica 19 bold italic",command=lambda: self.islemler("1+1+1+1",numara))
        self.butonGecici.grid(row=0,column=0, sticky=W,padx= 0, pady = 0,columnspan=2,rowspan=2)
        self.butonGecici = Button(self.dersSecim,text= '2 + 2 ', width=56,height=3,font = "Helvetica 19 bold italic",command=lambda: self.islemler("2+2",numara))
        self.butonGecici.grid(row=2,column=0, sticky=W,padx= 0, pady = 0,columnspan=2,rowspan=2)
        self.butonGecici = Button(self.dersSecim,text= '3 + 1', width=56,height=3,font = "Helvetica 19 bold italic",command=lambda: self.islemler("3+1",numara))
        self.butonGecici.grid(row=4,column=0, sticky=W,padx= 0, pady = 0,columnspan=2,rowspan=2)
        self.butonGecici = Button(self.dersSecim,text= '1 + 3 ', width=56,height=3,font = "Helvetica 19 bold italic",command=lambda: self.islemler("1+3",numara))
        self.butonGecici.grid(row=6,column=0, sticky=W,padx= 0, pady = 0,columnspan=2,rowspan=2)
        self.butonGecici = Button(self.dersSecim,text= '4 + 0 ', width=56,height=3,font = "Helvetica 19 bold italic",command=lambda: self.islemler("4+0",numara))
        self.butonGecici.grid(row=8,column=0, sticky=W,padx= 0, pady = 0,columnspan=2,rowspan=2)
    def islemler(self,Value,numara):
        bugunTarih = datetime.today().strftime('%d-%m-%Y')
        baglan = sqlite3.connect( 'kayitlar/' + 'D-103' + '/' + self.yil + '/' + self.donem + '/' + self.dersKodu + '/'+ bugunTarih +'.db')
        veri = baglan.cursor()
        veri.execute("UPDATE '" + self.dersKodu + "' SET Ders_Metod = '" + Value + "' WHERE Numara = '" + str(numara)+"'" )
        baglan.commit()
        self.dersSecim.destroy()
    def toHex(self,dec):
        x = (dec %16)
        digits = "0123456789ABCDEF"
        rest = dec /16

        return digits[int(rest)] + digits[int(x)]
    def end_read(self,signal,frame):
        global continue_reading
        continue_reading = False
        GPIO.cleanup()
    def kart_okuma(self):
        (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        (status,uid) = self.MIFAREReader.MFRC522_Anticoll()
        if status == self.MIFAREReader.MI_OK:
            self.UUID = self.toHex(uid[int(0)]) + " " +self.toHex(uid[int(1)])+ " " +self.toHex(uid[int(2)]) + " " +self.toHex(uid[int(3)])
            kartOkumaSuresi = datetime.today()
            if self.UUID == self.last_uuid:
                if self.kartOkumaIzinSuresi < kartOkumaSuresi:
                    return self.UUID
                else:
                    return False
            else:
                return self.UUID
        else:
            return False
    def guncelleme(self):
        sleep(2) # program çok hızlı çalıştığından dolayı beklemesi gerekli
        if verbose:
            print('< read_card.tkinterGui.guncelleme() fonksiyonuna giriş yapılıyor... >')
        self.yoklamayaIzinVerme = True
        ##################################################
        # Burasi beklememesi için konuldu daha sonra sil #
        if guncel:
            self.stop_loading()                              #
            self.mainScreen()                                #
        ##################################################

        #--------------------------------------------------------------- BURADAN SONRA GUİ ÇALIAŞACAK
        self.klasorler.klasorNoNetwork() # gerekli klasörleri yoksa oluşturan klasör
        baglan = sqlite3.connect( 'kayitlar/' +str(config['veri']['sinif']) + '/genelKayitlar/' + 'veri_kayit.db')
        veri = baglan.cursor()
        try:
            veriler = veri.execute('select * from kayit').fetchone()
            self.yil = veriler[0]
            self.donem = veriler[1]
        except:
            self.baglanWebservice.basla()
            veriler = veri.execute('select * from kayit').fetchone()
            self.yil = veriler[0]
            self.donem = veriler[1]
        self.klasorler.klasorKontrol(self.yil,self.donem)

        self.bugun = datetime.today().strftime('%d/%m/%Y') # Bugünün tarihini gun/ay/yil şeklinde alıyor
        if veriler[4] != self.bugun:
            self.baglanWebservice.basla()
        #----------------------------------------------------------------  Gerekli yapılar alındı --------------------------------------------------

         # gerekli klasörleri kontrol ediyor yok ise oluşturuyor.
        self.hangiGun = datetime.today().strftime('%A')  # Bugünün adini aliyor
        self.databaseGuncelMi = self.elektControl.kontrol(self.yil,self.donem,self.bugun)  # True yada False döndürür // False --- > elektrik gitmedi //  True --- > elektrik gitti
        if verbose:
            print('>>> self.databaseGuncelMi :',self.databaseGuncelMi)
        if self.databaseGuncelMi == False:
            self.baglanWebservice.tablolariGuncelle(self.yil,self.donem)
        if verbose:
            print('< read_card.tkinterGui.guncelleme() fonksiyonundan çıkış yapılıyor... >')
        self.stop_loading()
        self.yoklamayaIzinVerme = False
        self.mainScreen()
    def dailyUpdate(self):
        if verbose:
            print('< read_card.tkinterGui.dailyUpdate() fonksiyonuna  giriş yapılıyor... >')
        sleep(2)
        self.yoklamayaIzinVerme = True
        self.klasorler.klasorNoNetwork() # gerekli klasörleri yoksa oluşturan klasör
        baglan = sqlite3.connect( 'kayitlar/' +str(config['veri']['sinif']) + '/genelKayitlar/veri_kayit.db')
        veri = baglan.cursor()
        veriler = veri.execute('select * from kayit').fetchone()
        guncelleme_tarihi = veriler[4]
        self.bugun = datetime.today().strftime('%d/%m/%Y') # Bugünün tarihini gun/ay/yil şeklinde alıyor
        if guncelleme_tarihi != self.bugun or self.araDegisken == 0:
            self.internetVarmi = self.internetClass.internet()
            if self.internetVarmi == True:
                try:
                    self.baglanWebservice.basla()
                    self.yil = veriler[0]
                    self.donem = veriler[1]
                    self.baglanWebservice.tablolariGuncelle(self.yil,self.donem)
                except:
                    pass
                self.araDegisken = 1
                self.yoklamayaIzinVerme = False
            else:
                self.stop_loading()
                self.bekle = Toplevel()
                self.bekle.attributes("-fullscreen", True)
                self.bekle.bind('<Escape>',quit)
                self.bekle.configure(background=self.backGround,cursor = 'none')
                noWifi = Thread(target=self.popup,args=('no_wifi',))
                noWifi.start()
                if verbose:
                    print('< read_card.tkinterGui.loading_start() fonksiyonundan çıkış yapılıyor... >')
                if verbose:
                    print('< read_card.tkinterGui.bekle_no_network() fonksiyonuna giriş yapılıyor... >')
                self.bekle_no_network()
        #----------------------------------------------------------------  Gerekli yapılar alındı --------------------------------------------------
        baglan = sqlite3.connect( 'kayitlar/' +str(config['veri']['sinif']) + '/genelKayitlar/' + 'veri_kayit.db')
        veri = baglan.cursor()
        veriler = veri.execute('select * from kayit').fetchone()
        self.yil = veriler[0]
        self.donem = veriler[1]
        self.klasorler.klasorKontrol(self.yil,self.donem) # gerekli klasörleri kontrol ediyor yok ise oluşturuyor
        self.hangiGun = datetime.today().strftime('%A')  # Bugünün adini aliyor
        self.databaseGuncelMi = self.elektControl.kontrol(self.yil,self.donem,self.bugun)  # True yada False döndürür // False --- > elektrik gitmedi //  True --- > elektrik gitti
        self.stop_loading()
        self.yoklamayaIzinVerme = False


        if verbose:
            print('>> Ara Günceleme Sona Erdi.')
            print('< read_card.tkinterGui.dailyUpdate() fonksiyonundan çıkış yapılıyor...')
    def neredeyim(self):
        if verbose:
            print('< read_card.tkinterGui.neredeyim() fonksiyonuna giriş yapılıyor... >')
        erkenBasla = timedelta(minutes = int(config['veri']['dersErkenBaslamaSaati']))  # config dosyasından dersin ne kadar erken başlaması gerektiğini aldım
        girisIzin = timedelta(minutes = int(config['veri']['dersGirisIzinSuresi']))
        cikisIzin = timedelta(minutes = int(config['veri']['dersCikisIzinSuresi']))

        #-----------------------------------# GUNCEL DATABASE ELIMIZDE  #-----------------------------------------#
        baglan = sqlite3.connect( 'kayitlar/' +str(config['veri']['sinif']) + '/genelKayitlar/' + 'veri_kayit.db')
        veri = baglan.cursor()
        veriler = veri.execute('select * from kayit').fetchone()
        self.yil = veriler[0]
        self.donem = veriler[1]
        tablolar,gunler,self.dersVakitler,dersBitisVakitler,dersAdi,hocaAdi,dKodu = self.yedekVeritabani.dersBilgilerDatabase(self.yil,self.donem)
        sayac = 0
        try:
            self.sifirlama = len(tablolar)

        except:
            self.sifirlama = 0
        while sayac < self.sifirlama:
            guncelHocaAdi = hocaAdi[sayac]
            guncelDersKodu = dKodu[sayac]
            guncelDersAdi = dersAdi[sayac]
            guncelSaat = datetime.today().strftime('%H:%M:%S')
            guncelSaniye = (datetime.today().strftime('%S')) # Güncel saniyeyi aldım
            dersBaslamaSaati = datetime.strptime(self.dersVakitler[sayac],'%H:%M')
            dersBitisSaati = datetime.strptime(dersBitisVakitler[sayac],'%H:%M')
            guncelSaat = datetime.strptime(guncelSaat,'%H:%M:%S')
            erkenBaslaTime = (dersBaslamaSaati - erkenBasla)
            girmeIzinTime = (dersBaslamaSaati + girisIzin)
            dersCikisBasla = dersBitisSaati - cikisIzin
            if guncelSaat >= erkenBaslaTime and guncelSaat < girmeIzinTime: # 08:45 ile 09:15 arasinda ise
                if verbose:
                    print(">> login-permit")
                    print('< read_card.tkinterGui.neredeyim() fonksiyonundan çıkış yapılıyor... >')
                return 'loginPermit',guncelDersAdi,guncelHocaAdi,dersBaslamaSaati,dersBitisSaati,guncelDersKodu
            else:
                if guncelSaat >= girmeIzinTime and guncelSaat <= dersCikisBasla: # 09:15 ile 09:44 arasinda ise
                    if self.ErkenCikisDersBitmeSaati == True:
                        if verbose:
                            print('>> early-permit')
                            print('< read_card.tkinterGui.neredeyim() fonksiyonundan çıkış yapılıyor... >')
                        return 'erkenCikis',guncelDersAdi,guncelHocaAdi,dersBaslamaSaati,dersBitisSaati,guncelDersKodu
                    if verbose:
                        print(">> between-permit")
                        print('< read_card.tkinterGui.neredeyim() fonksiyonundan çıkış yapılıyor... >')
                    return 'between',guncelDersAdi,guncelHocaAdi,dersBaslamaSaati,dersBitisSaati,guncelDersKodu

                elif dersCikisBasla < guncelSaat and guncelSaat <= (dersBitisSaati ):
                    if self.ErkenCikisDersBitmeSaati == True:
                        if verbose:
                            print('>> early-permit')
                            print('< read_card.tkinterGui.neredeyim() fonksiyonundan çıkış yapılıyor... >')
                        return 'erkenCikis',guncelDersAdi,guncelHocaAdi,dersBaslamaSaati,dersBitisSaati,guncelDersKodu
                    if verbose:
                        print(">> exit-permit")
                        print('< read_card.tkinterGui.neredeyim() fonksiyonundan çıkış yapılıyor... >')
                    return 'exitPermit',guncelDersAdi,guncelHocaAdi,dersBaslamaSaati,dersBitisSaati,guncelDersKodu
            #if int(guncelDakika) > int(dersErkenBasla):
            sayac += 1
        if (self.ErkenCikisDersBitmeSaati == True):
            if verbose:
                print('>> erkenCikis Sona Erdi.')
            self.ErkenCikisDersBitmeSaati = False
        if verbose:
            print('< read_card.tkinterGui.neredeyim() fonksiyonundan çıkış yapılıyor... >')
        return None,None,None,None,None,None
    def popup(self,sart):
        if verbose:
            print('< read_card.tkinterGui.popup() fonksiyonuna giriş yapılıyor... >')
        self.yoklamayaIzinVerme = True
        self.pencere_popup = Toplevel()
        self.pencere_popup.configure(background=self.backGround,cursor = 'none')
        self.pencere_popup.attributes("-fullscreen", True)


        if sart == 'girisKayitYok':
            seven = Label(self.pencere_popup,image=self.noLogin,borderwidth=0)
            seven.grid(row = 0, column = 0,padx = 0,pady=0,columnspan = 8,rowspan = 8)
        elif sart == 'undefined':
            #Label(self.pencere, text = 'YABANCI KART   ', font ="Helvetica 30 bold italic",bg = 'grey',wraplength=440).grid(row = 1, column = 0 ,sticky = 'W',columnspan = 2 ,rowspan = 2,padx=85, pady=130)
            one = Label(self.pencere_popup,image=self.undefinedCard,borderwidth=0)
            one.grid(row = 0, column = 0,padx = 0,pady=0,columnspan = 8,rowspan = 8)
        elif sart == 'earlyExit':
            two = Label(self.pencere_popup,image=self.earlyExit,borderwidth=0)
            two.grid(row = 1, column = 0,padx = 0,pady=0,columnspan = 8,rowspan = 8)
        elif sart == 'no_wifi':
            theere = Label(self.pencere_popup,image=self.no_wifi,borderwidth=0)
            theere.grid(row = 1, column = 0,padx = 0,pady=0,columnspan = 8,rowspan = 8)
        elif sart == 'giris_ret':
            four = Label(self.pencere_popup,image=self.giris_ret,borderwidth=0)
            four.grid(row = 1, column = 0,padx = 0,pady=0,columnspan = 8,rowspan = 8)
        elif sart == 'cikis_ret':
            five = Label(self.pencere_popup,image=self.cikis_ret,borderwidth=0)
            five.grid(row = 1, column = 0,padx = 0,pady=0,columnspan = 8,rowspan = 8)
        elif sart == 'cikis':
            six = Label(self.pencere_popup,image=self.byebye,borderwidth=0)
            six.grid(row = 1, column = 0,padx = 0,pady=0,columnspan = 8,rowspan = 8)

        elif sart == 'hatali_giris':
            eight = Label(self.pencere_popup,image=self.hata_ret,borderwidth=0)
            eight.grid(row = 0, column = 0,padx = 0,pady=0,columnspan = 8,rowspan = 8)
        else:
            pass

        button = Button(self.pencere_popup,font = "Helvetica 15 bold italic",padx = 20,text = 'X',command = self.pencere_popup.destroy,bg=self.backGround)
        button.grid(row = 0, column = 7,padx = 0,pady=0)#,columnspan = 2,rowspan = 2)

        if verbose:
            print('< read_card.tkinterGui.popup() fonksiyonundan çıkış yapılıyor... >')
        sleep(int(config['veri']['popupSuresi']))
        self.pencere_popup.destroy()
        self.yoklamayaIzinVerme = False
    def loginAndExitPopup(self,adSoyad,sart):
        if verbose:
            print('< read_card.tkinterGui.loginAndExitPopup() fonksiyonuna giriş yapılıyor... >')
        self.yoklamayaIzinVerme = True
        self.pencere_loginAndExitPopup = Toplevel()
        self.pencere_loginAndExitPopup.configure(background=self.backGround,cursor = 'none')
        self.pencere_loginAndExitPopup.attributes("-fullscreen", True)
        button = Button(self.pencere_loginAndExitPopup,font = "Helvetica 15 bold italic",padx = 20,text = 'X',command = self.pencere_loginAndExitPopup.destroy,bg=self.backGround)
        button.grid(row = 0, column = 4,padx = 0,pady=0)#,columnspan = 2,rowspan = 2)
        if sart == 'login':
            Label(self.pencere_loginAndExitPopup, text = adSoyad, font ="Helvetica 30 bold italic",bg = self.backGround,wraplength=750).grid(column=2,row= 1,sticky = 'W',pady = 0,padx = 0)#,
            Label(self.pencere_loginAndExitPopup,image=self.welcome,borderwidth=0).grid(row=2,column= 0,rowspan =8,columnspan = 5)


        elif sart == 'exit':
            exit=Label(self.pencere_loginAndExitPopup,image=self.byebye,borderwidth=0).grid(row=1,column= 0,rowspan =8,columnspan = 5)
            exit=Label(self.pencere_loginAndExitPopup, text = adSoyad, font ="Helvetica 30 bold italic",bg = self.backGround,wraplength=750).grid(column=2,row= 1,sticky = 'W',pady = 0,padx = 0)#,

        else:
            pass

        if verbose:
            print('< read_card.tkinterGui.loginAndExitPopup() fonksiyonundan çıkış yapılıyor... >')
        sleep(int(config['veri']['popupSuresi']))
        self.pencere_loginAndExitPopup.destroy()
        self.yoklamayaIzinVerme = False
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
    def araKisim(self):

        if verbose:
            print("< read_card.tkinterGui.araKisim() fonksiyonuna giriş yapılıyor...")
        config.read(configDosyasiAdres)
        self.geriSayimSuresi  = config['veri']['geriSayim']
        self.onayKutusu.destroy()
        self.yoklamayaIzinVerme = True
        self.sayim = int(datetime.today().strftime('%S') ) + int(self.geriSayimSuresi)
        self.popupPencere_araKisim = Toplevel()
        self.popupPencere_araKisim.configure(background=self.backGround,cursor = 'none')
        self.popupPencere_araKisim.attributes("-fullscreen", True)
        #Label(self.popupPencere_araKisim,textvariable=self.geriSayim,font ="Helvetica 200 bold italic",bg = self.foreground,wraplength=475).grid(row=0,column=0,columnspan=2, sticky=W,padx= 310, pady=100)
        yazi = Label(self.popupPencere_araKisim,textvariable=self.geriSayim,font ="Helvetica 200 bold italic",bg = self.backGround,wraplength=475)
        yazi.grid(row=4,column=3,columnspan=7,rowspan = 7,padx=0,pady=0)#, sticky=W)#,padx= 310, pady=100)

        button = Button(self.popupPencere_araKisim,font = "Helvetica 15 bold italic",padx = 20,text = 'X',command = self.popupPencere_araKisim.destroy,bg=self.backGround)
        button.grid(row = 0, column = 7,padx = 720,pady=0,rowspan=1,columnspan=7)#,columnspan = 2,rowspan = 2)
        if verbose:
            print("< read_card.tkinterGui.araKisim() fonksiyonundan çıkış yapılıyor...")
        self.onayKutusuGeriSayim()
    def onayKutusuGeriSayim(self):
        self.geriSayim.set(self.sayim - int(datetime.today().strftime('%S')))
        #--------------------------------------
        #--------------------------------------
        if (self.sayim - int(datetime.today().strftime('%S'))) < 0  or self.ErkenCikis == True or self.sayim - int(datetime.today().strftime('%S')) > int(config['veri']['geriSayim']):

            self.popupPencere_araKisim.destroy()
            sleep(int(config['veri']['popupSuresi']))
            self.yoklamayaIzinVerme = False
        else:
            kartIdOgren = self.kart_okuma()
            if kartIdOgren != False :
                numara,adSoyad,statu,dersSaati = self.yedekVeritabani.kartIDKontrol(self.yil,self.donem,kartIdOgren,self.tabloAdi)
                if statu == 'TE':
                    kontrol = self.yedekVeritabani.yoklamaKayit(self.yil,self.donem,self.dersKodu,numara,adSoyad,statu,'exitPermit')
                    if True: # kontrol == 'cikisYapti' or kontrol == 'girisKayitYok':
                        #self.teacher(adSoyad,'cikis')
                        self.onay_ver()
                        sleep(int(config['veri']['popupSuresi'])/2)
                        self.ErkenCikis = True
                        guncelSaat = datetime.strptime(datetime.today().strftime("%H:%M:%S"),"%H:%M:%S")
                        yoklamaSuresi = timedelta(minutes = int(config['veri']['ogretiGorevlisiKartBastiktanSonraIzinSuresi']))
                        self.ErkenCikisDersBitmeSaati = guncelSaat + yoklamaSuresi
                        ekran = Thread(target=self.ekranAyarla)
                        ekran.start()
                    else:
                        pass

            root.after(1000,run.onayKutusuGeriSayim)
    def ekranAyarla(self):
        if verbose:
            print('< read_card.tkinterGui.ekranAyarla() fonksiyonuna giriş yapılıyor... >')
        self.hangiKisim,self.dersAdi,hocaAdi,self.dersBasla,self.dersBitis,self.dersKodu =  self.neredeyim()
        if self.ErkenCikis == True:
            self.hangiKisim = 'exitPermit'
        try:
            self.tabloAdi = self.dersKodu+'_'+self.dersAdi+'_'+self.dersBasla.strftime('%H:%M')
        except:
            self.tabloAdi='Bos'
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
                    dersBaslamaSaati = datetime.strptime(self.dersBasla.strftime("%H:%M:%S"),"%H:%M:%S")  # dersin başlama saati
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
        self.loop()
    def student(self,adSoyad,sart):
        if verbose:
            print('< read_card.tkinterGui.student() fonksiyonuna giriş yapılıyor... >')
        buzzer = Thread(target=self.buzzer.play,args=(3,))
        rgb = Thread(target=self.rgb.greenOn)
        if sart == 'giris':
            popup = Thread(target=self.loginAndExitPopup,args=(adSoyad,'login',))
        elif sart == 'cikis':
            popup = Thread(target=self.loginAndExitPopup,args=(adSoyad,'exit',))
        """
        #                   Delete
        yil = '2017-2018'
        donem = 'Bahar'
        config.read('conf/bilgiler.cfg')
        address = "kayitlar/" + config['veri']['sinif'] + "/" + yil + "/" + donem
        for i in os.listdir(address):
            if i != "yoklamaKayit" and i != "elektrikKayit":
                real_address = address + "/" + i
                os.system("rsync -avz --delete "+ real_address + " trforever@95.183.170.191:/home/trforever/Desktop/feys/kayitlar/D-103/2017-2018/Bahar")
        #####################
        """
        if verbose:
            print('< read_card.tkinterGui.student() fonksiyonundan çıkış yapılıyor... >')
        rgb.start()
        popup.start()
        buzzer.start()
    def hata_ver(self):
        if verbose:
            print('< read_card.tkinterGui.hata_ver() fonksiyonuna giriş yapılıyor... >')

        popup = Thread(target=self.menu_uyari)
        if verbose:
            print('< read_card.hata_ver.hata_ver() fonksiyonundan çıkış yapılıyor... >')
        popup.start()
    def onay_ver(self):
        if verbose:
            print('< read_card.tkinterGui.onay_ver() fonksiyonuna giriş yapılıyor... >')

        popup = Thread(target=self.popup,args=('earlyExit',))
        if verbose:
            print('< read_card.hata_ver.onay_ver() fonksiyonundan çıkış yapılıyor... >')
        popup.start()
    def teacher(self,adSoyad,sart,numara,dersSaati):
        if verbose:
            print('< read_card.tkinterGui.teacher() fonksiyonuna giriş yapılıyor... >')
        buzzer = Thread(target=self.buzzer.play,args=(1,))
        rgb = Thread(target=self.rgb.blueOn)
        if sart == 'giris':
            popup = Thread(target=self.loginAndExitPopup,args=(adSoyad,'login',))
            yolla = Thread(target=self.dersSaatiSecim,args=(numara,dersSaati,))
        elif sart == 'cikis':
            popup = Thread(target=self.loginAndExitPopup,args=(adSoyad,'exit',))
        """
        #                   Delete
        yil = '2017-2018'
        donem = 'Bahar'
        config.read('conf/bilgiler.cfg')
        address = "kayitlar/" + config['veri']['sinif'] + "/" + yil + "/" + donem
        for i in os.listdir(address):
            if i != "yoklamaKayit" and i != "elektrikKayit":
                real_address = address + "/" + i
                #alias yolla="rsync -avz --delete /home/pi/Desktop/gonder trforever@192.168.43.131:/home/trforever/Desktop/gonder"
                os.system("rsync -avz --delete "+ real_address + " trforever@95.183.170.191:/home/trforever/Desktop/feys/kayitlar/D-103/2017-2018/Bahar")
        #####################
        """
        if verbose:
            print('read_card.tkinterGui.teacher() fonksiyonundan çıkış yapılıyor...>')
        rgb.start()
        popup.start()
        buzzer.start()
        if sart == 'giris':
            yolla.start()
    def foreign(self):
        if verbose:
            print('< read_card.tkinterGui.foreign() fonksiyonuna giriş yapılyor... >')
        buzzer = Thread(target=self.buzzer.play,args=(2,))
        rgb = Thread(target=self.rgb.redOn)
        popup = Thread(target=self.popup,args=('undefined',))
        if verbose:
            print('read_card.tkinterGui.foreign() fonksiyonundan çıkış yapılıyor...>')
        rgb.start()
        buzzer.start()
        popup.start()
    def giris_kayit_reddedildi(self):
        if verbose:
            print('< read_card.tkinterGui.giris_kayit_reddedildi() fonksiyonuna giriş yapılıyor... >')
        buzzer = Thread(target=self.buzzer.play,args=(2,))
        rgb = Thread(target=self.rgb.redOn)
        popup = Thread(target=self.popup,args=('giris_ret',))
        if verbose:
            print('< read_card.tkinterGui.giris_kayit_reddedildi() fonksiyonundan çıkış yapılıyor... >')
        rgb.start()
        buzzer.start()
        popup.start()
    def cikis_kayit_reddedildi(self):
        if verbose:
            print('< read_card.tkinterGui.cikis_kayit_reddedildi() fonksiyonuna giriş yapılıyor... >')
        buzzer = Thread(target=self.buzzer.play,args=(2,))
        rgb = Thread(target=self.rgb.redOn)
        popup = Thread(target=self.popup,args=('cikis_ret',))
        if verbose:
            print('< read_card.tkinterGui.cikis_kayit_reddedildi() fonksiyonundan çıkış yapılıyor... >')
        rgb.start()
        buzzer.start()
        popup.start()
    def girisKayitYok(self):
        if verbose:
            print('< read_card.tkinterGui.cikis_kayit_reddedildi() fonksiyonuna giriş yapılıyor... >')
        buzzer = Thread(target=self.buzzer.play,args=(2,))
        rgb = Thread(target=self.rgb.redOn)
        popup = Thread(target=self.popup,args=('girisKayitYok',))
        if verbose:
            print('< read_card.tkinterGui.cikis_kayit_reddedildi() fonksiyonundan çıkış yapılıyor... >')
        rgb.start()
        buzzer.start()
        popup.start()
    def saatGuncelle(self):
        if self.dummy != datetime.today().strftime('%M'):
            self.add_text_1(text=datetime.today().strftime('Tarih / Saat : ' + '%d/%m/%Y   %H:%M'))
            self.update1update = Label(self.parent,bg=self.backGround, image= self._photoimage_1,wraplength=750,anchor="center")
            self.update1update.grid(row=0,column=0,sticky="w",padx=40,pady=25)
            self.dummy = datetime.today().strftime('%M')
        else:
            pass
        if self.kalanSaat != None:
            self.kalanSaat = self.kalanSaat-1
            #########################
            saniye = self.kalanSaat      #
            gun = saniye // 86400
            saat = (saniye- ( 86400 * gun) ) // 3600
            dakika = (saniye - ((saat*3600)+(86400*gun))) // 60
            saniye = (saniye - ((saat*3600)+(86400*gun)+(60*dakika)))%60
            if saat < 10:              #
                saat = "0"  + str(saat)   #
            if dakika < 10:              #
                dakika = "0"  + str(dakika)   #
            if saniye < 10:              #
                saniye = "0"  + str(saniye)   #
            #########################
            yazi = "{} sa.  {} dk. ".format(saat,dakika)
            if (self.hangiKisim == "loginPermit") and dakika != self.dakikaAyar:
                self.update2Update .grid_remove()
                self.dakikaAyar = dakika
                self.add_text_3(text='Giriş yoklamasının bitimine kalan süre : ' + yazi)
                self.update2Update = Label(self.parent,bg=self.backGround, image= self._photoimage_3,wraplength=750,anchor="center")

            elif (self.hangiKisim == "between") and dakika != self.dakikaAyar:
                self.update2Update .grid_remove()
                self.dakikaAyar = dakika
                self.add_text_3(text='Çıkış yoklamasının başlamasına kalan süre : ' + yazi)
                self.update2Update = Label(self.parent,bg=self.backGround, image= self._photoimage_3,wraplength=750,anchor="center")

            elif (self.hangiKisim == "exitPermit") and dakika != self.dakikaAyar:
                self.update2Update .grid_remove()
                self.dakikaAyar = dakika
                self.add_text_3(text='Çıkış yoklamasının bitimine kalan süre : ' + yazi)
                self.update2Update = Label(self.parent,bg=self.backGround, image= self._photoimage_3,wraplength=750,anchor="center")
            else:
                pass


            if self.hangiKisim == "loginPermit":
                self.amblo.grid_remove()
                self.gr.grid(row=0,column=0,padx=0 ,  pady = 0,rowspan=5,columnspan=7)
                self.rd.grid_remove()
                self.update2Update.grid(row=1,column=0,sticky=W, padx=40 ,  pady = 0,columnspan=7,rowspan=1)

                #self.update2Update.grid(row=2,column=0,sticky=W, padx=20 ,  pady = 35,columnspan=7,rowspan=2)
                #self.updateWrite2.set('Giriş yoklamasının bitimine kalan süre : ' + yazi)
            elif self.hangiKisim == "between":
                self.amblo.grid_remove()
                self.gr.grid_remove()
                self.rd.grid(row=0,column=0,padx=0 ,  pady = 0,rowspan=5,columnspan=7)
                self.update4Update.grid_remove()
                self.update2Update.grid(row=1,column=0,sticky=W, padx=40 ,  pady = 0,columnspan=7,rowspan=1)

                #self.update2Update.grid(row=2,column=0,sticky=W, padx=20 ,  pady = 35,columnspan=7,rowspan=2)
                #self.updateWrite2.set('Çıkış yoklamasının başlamasına kalan süre : ' + yazi)
            elif self.hangiKisim == "exitPermit":
                self.amblo.grid_remove()
                self.gr.grid(row=0,column=0,padx=0 ,  pady = 0,rowspan=5,columnspan=7)
                self.rd.grid_remove()
                self.update2Update.grid(row=1,column=0,sticky=W, padx=40 ,  pady = 0,columnspan=7,rowspan=1)

                #self.update2Update.grid(row=2,column=0,sticky=W, padx=20 ,  pady = 35,columnspan=7,rowspan=2)
                #self.updateWrite2.set('Çıkış yoklamasının bitimine kalan süre : ' + yazi)
            if (int(saat) == 0 and int(dakika) == 0 and int(saniye) < 30) and self.ErkenCikis == True:
                self.ErkenCikis = False
                self.ErkenCikisDersBitmeSaati = True

            else:
                pass
        else:
            pass
        #if int(datetime.today().strftime('%M')) % 5 == 0 and (int(datetime.today().strftime('%S')) == 0 or int(datetime.today().strftime('%S')) == 30):
        #    self.internetClass.internet()

        guncellemeSaatDakika = config['veri']['guncellemeSaati'].strip().split(":")
        if False:
            if datetime.today().strftime("%H") == guncellemeSaatDakika[0] and datetime.today().strftime("%M") == guncellemeSaatDakika[1] and (datetime.today().strftime("%S") == '02' or datetime.today().strftime("%S") == '00' or datetime.today().strftime("%S") == '01' ) :
                self.windows = Toplevel()
                self.windows.attributes("-fullscreen", True)
                self.windows.bind('<Escape>',quit)
                self.windows.configure(background=self.backGround,cursor = 'none')
                self.loadingGerekliTanimlamalar()
                target3 = Thread(target = self.start_loading)
                target4 = Thread(target = self.dailyUpdate)
                target3.start()
                target4.start()
        self.tekrarBasla = root.after(1000,run.saatGuncelle)
    def dersSaatiSecim(self,numara,dersSaati):
        self.dersSecim = Toplevel()
        self.dersSecim.attributes("-fullscreen", True)
        self.dersSecim.bind('<Escape>',quit)
        self.dersSecim.configure(background=self.backGround,cursor = 'none')
        if dersSaati == '1':
            self.dersSecim.destroy()
            bugunTarih = datetime.today().strftime('%d-%m-%Y')
            baglan = sqlite3.connect( 'kayitlar/' + 'D-103' + '/' + self.yil + '/' + self.donem + '/' + self.dersKodu + '/'+ bugunTarih +'.db')
            veri = baglan.cursor()
            veri.execute("UPDATE '" + self.dersKodu + "' SET Ders_Metod = '" + Value + "' WHERE Numara = '" + str(numara)+"'" )
            baglan.commit()
        elif dersSaati == '2':
            self.iki(numara)
        elif dersSaati == '3':
            self.uc(numara)
        elif dersSaati == '4':
            self.dort(numara)
        else:
            pass
    def loop(self):
        #-------------------------------------------------
        if self.yoklamayaIzinVerme == False:
            kartIdOgren = self.kart_okuma()
        else:
            kartIdOgren = False

        if kartIdOgren != False and self.hangiKisim != None:
            self.last_uuid = self.UUID
            self.kartOkumaIzinSuresi = datetime.today() + timedelta(seconds = 10)
            numara,adSoyad,statu,dersSaati = self.yedekVeritabani.kartIDKontrol(self.yil,self.donem,kartIdOgren,self.tabloAdi)
            if self.hangiKisim == "loginPermit":
                if statu == None :
                    self.foreign()
                elif statu == "TE":
                    kontrol = self.yedekVeritabani.yoklamaKayit(self.yil,self.donem,self.dersKodu,numara,adSoyad,statu,self.hangiKisim)
                    if kontrol == 'girisYapti':
                        self.teacher(adSoyad,'giris',numara,dersSaati)

                    else:
                        self.giris_kayit_reddedildi()

                elif statu == "ST":
                    kontrol = self.yedekVeritabani.yoklamaKayit(self.yil,self.donem,self.dersKodu,numara,adSoyad,statu,self.hangiKisim)
                    if kontrol == 'girisYapti':
                        self.student(adSoyad,'giris')

                    else:
                        self.giris_kayit_reddedildi()

                    #####
                else:
                    pass

            elif self.hangiKisim == 'exitPermit':
                if statu == None :
                    self.foreign()
                elif statu == "TE":
                    kontrol = self.yedekVeritabani.yoklamaKayit(self.yil,self.donem,self.dersKodu,numara,adSoyad,statu,self.hangiKisim)
                    if kontrol == 'cikisYapti':
                        self.teacher(adSoyad,'cikis',numara,dersSaati)


                    elif kontrol == 'girisKayitYok':
                        self.girisKayitYok()
                    else:
                        self.cikis_kayit_reddedildi()
                elif statu == "ST":
                    kontrol = self.yedekVeritabani.yoklamaKayit(self.yil,self.donem,self.dersKodu,numara,adSoyad,statu,self.hangiKisim)
                    if kontrol == 'cikisYapti':
                        self.student(adSoyad,'cikis')


                    elif kontrol == 'girisKayitYok':
                        self.girisKayitYok()
                    else:
                        self.cikis_kayit_reddedildi()
                else:
                    pass

            elif self.hangiKisim == 'between':
                    pass
            else:
                pass

        if self.kalanSaat == 0 or datetime.today().strftime("%S") == '00' or datetime.today().strftime("%S") == '01':
            self.kalanSaat = None
            sleep(0.75)
            ekranAyarlaFunk = Thread(target = self.ekranAyarla)
            ekranAyarlaFunk.start()

        else:

            self.tekrarBasla = root.after(1000,run.loop)
    def loadingGerekliTanimlamalar(self):
        if verbose:
            print('< read_card.tkinterGui.loadingGerekliTanimlamalar() fonksiyonuna giriş yapılıyor...> ')
        input_file_say = 74 #int(input("dosya sayisi :"))
        imagelist = []
        for i in range(0,input_file_say+1):
            imagelist.append('icons/loading/'+ str(i)+".gif")
        # extract width and height info
        photo = PhotoImage(file=imagelist[0])
        width = photo.width()
        height = photo.height()
        self.canvas = Canvas(self.windows,width=width, height=height)
        self.canvas.grid()
        self.timer_id = None

        # create a list of image objects

        self.giflist = []
        for imagefile in imagelist:
            photo = PhotoImage(file=imagefile)
            self.giflist.append(photo)

        if verbose:
            print('< read_card.tkinterGui.loadingGerekliTanimlamalar() fonksiyonundan çıkış yapılıyor...>')
        # loop through the gif image objects for a while
    def start_loading(self,n=0):
        gif = self.giflist[n%len(self.giflist)]
        self.canvas.create_image(gif.width()//2, gif.height()//2, image=gif)
        self.timer_id = self.windows.after(100, self.start_loading, n+1) # call this function every 100ms
    def stop_loading(self):
        if verbose:
            print('< read_card.tkinterGui.stop_loading() fonksiyonuna giriş yapılıyor... >')
        if self.timer_id:
            self.windows.after_cancel(self.timer_id)
            self.canvas.delete(ALL)
            if verbose:
                print('< read_card.tkinterGui.stop_loading() fonksiyonundan çıkış yapılıyor... >')
            self.windows.destroy()
    def loading_start(self):
        if verbose:
            print('< read_card.tkinterGui.loading_start() fonksiyonuna giriş yapılıyor... >')

        if guncel:
            self.mainScreen()
        else:
            self.internetVarmi = self.internetClass.internet()

            self.databaseGuncelMi = True


            if self.internetVarmi == False:

                ##########################################################################
                ################## DATABASE'DEN CEKILECEK SEKILDE AYARLA #################

                """  ---------  ACIKLAMA -----------  """
                # Bu kısımda bulunduğu yılı ve donemi intenet olmadığından sanal olarak oluşturur
                # bulunduğu yıl A ise ve bulunduğu ay eylül - ekim . . . - ocak herhangi birisi ise eğitim-öğretim yılı A - A+1 dönemi Güz
                # bulunduğu yıl A ise ve bulunduğu ay şubat - mart . . . - temmuz herhangi birisi ise eğitim-öğretim yılı A-1 - A dönemi Bahar olarak alır
                """ --------------------------------  """
                self.yil = strftime('%Y') # hangi yilda olduğumuzu aldım
                ay = strftime('%m'); # hangi ayda olduğumu aldım
                if (int(ay) > 8 ) or int(ay) == 1:
                    yilArtiBir = int(self.yil) + 1 # bir sonraki yili aldım
                    self.yil = str(self.yil) + '-' +str(yilArtiBir) # ikisini birleştirdim örneğin yil 2017 bir fazlasi 2018 olur birleişimide 2017-2018
                    self.donem = 'Güz'
    
                    #### delete
                    """
                    self.yil = '2017-2018'
                    self.donem = 'Bahar'
                    """
                else:
                    yilEksiBir = int(self.yil) - 1# bir önceki yili aldim
                    self.yil = str(yilEksiBir) + '-' +str(self.yil)
                    """
                    #  delete
                    self.yil = '2017-2018'
                    self.donem = 'Bahar'
                    """
                    
                self.bugun = datetime.today().strftime('%d/%m/%Y') # Bugünün tarihini gun/ay/yil şeklinde alıyor
                # delete
                #self.bugun = '08/10/2018'

                
                self.databaseGuncelMi = self.elektControl.kontrol(self.yil,self.donem,self.bugun)  # True yada False döndürür // False --- > elektrik gitmedi //  True --- > elektrik gitti

            if verbose:
                print('>> self.internetVarmi :',self.internetVarmi)

            if (self.internetVarmi == True):
                self.windows = Toplevel()
                self.windows.attributes("-fullscreen", True)
                self.windows.bind('<Escape>',quit)
                self.windows.configure(background=self.backGround,cursor = 'none')

                self.loadingGerekliTanimlamalar()


                target1 = Thread(target = self.start_loading)
                target2 = Thread(target = self.guncelleme)
                if verbose:
                    print('< read_card.tkinterGui.loading_start() fonksiyonundan çıkış yapılıyor... >')
                target1.start()
                target2.start()

            elif self.internetVarmi == False and  self.databaseGuncelMi == True:

                target2 = Thread(target = self.mainScreen)


                ####################################

                target2.start()


                #self.mainScreen()

            elif self.internetVarmi == False and self.databaseGuncelMi == False:
                self.bekle = Toplevel()
                self.bekle.attributes("-fullscreen", True)
                self.bekle.bind('<Escape>',quit)
                self.bekle.configure(background=self.backGround,cursor = 'none')
                login=Label(self.bekle,image=self.no_wifi,borderwidth=0).grid(rowspan = 3,row=2)
                if verbose:
                    print('< read_card.tkinterGui.loading_start() fonksiyonundan çıkış yapılıyor... >')
                if verbose:
                    print('< read_card.tkinterGui.bekle_no_network() fonksiyonuna giriş yapılıyor... >')
                self.bekle_no_network()
    def bekle_no_network(self):
        self.internetVarmi = self.internetClass.internet()
        if self.internetVarmi == False:
            self.tekrarBasla = root.after(1000,run.bekle_no_network)

        elif self.internetVarmi == True:
            self.bekle.destroy()
            if verbose:
                print('< read_card.tkinterGui.bekle_no_network() fonksiyonundan çıkış yapılıyor... >')
            self.loading_start()
        else:
            pass



def random_feys():
    sozluk = {"1":"""
    .....................................................................
    .. __________...____________...___.............___..._____________...
    ../**********\.|************\./***\.........../***\.|*************\..
    ..|****_*__*_/.|****_*_*_*_*/.|***|...........|***|.|***_*_*_*_*_*/..
    ..|***|........|***|...........\**|...........|**/..|***|............
    ..|***|........|***|............\**\_._._._._/**/...|***|............
    ..|***\_:_:_:..|***\_:_:_:_......\*************/....|***\_:_:_:_:_...
    ..|**********\.|************\.....\_*_*****_*_/.....|*************\..
    ..|***_*_*_*_/.|****_*_*_*_*/.........|***|.........\*_*_*_*_*.***|..
    ..|***|........|****\_____............|***|...................|***|..
    ..|***|........|****|.................|***|...................|***|..
    ..|***|........|****|_______..........|***|.........._._._._._|***|..
    ..|***|........|************\.........|***|........./*************|..
    ..|*_*|........|_*_*_*_*_*_*/.........\_*_/.........\_*_*_*_*_*_*_/..
    .....................................................................
    """,
    "2":"""
        _////////_////////_//      _//  _// //
        _//      _//       _//    _// _//    _//
        _//      _//        _// _//    _//
        _//////  _//////      _//        _//
        _//      _//          _//           _//
        _//      _//          _//     _//    _//
        _//      _////////    _//       _// //

    """,
    "3":"""
    :::::::::: :::::::::: :::   :::  ::::::::
    :+:        :+:        :+:   :+: :+:    :+:
    +:+        +:+         +:+ +:+  +:+
    :#::+::#   +#++:++#     +#++:   +#++:++#++
    +#+        +#+           +#+           +#+
    #+#        #+#           #+#    #+#    #+#
    ###        ##########    ###     ########
    """,
    "4":"""
    >=======> >=======> >=>      >=>   >=>>=>
    >=>       >=>        >=>    >=>  >=>    >=>
    >=>       >=>         >=> >=>     >=>
    >=====>   >=====>       >=>         >=>
    >=>       >=>           >=>            >=>
    >=>       >=>           >=>      >=>    >=>
    >=>       >=======>     >=>        >=>>=>
    """,
    "5":"""
    ..........................................
    ..'########:'########:'##:::'##::'######::
    .. ##.....:: ##.....::. ##:'##::'##... ##:
    .. ##::::::: ##::::::::. ####::: ##:::..::
    .. ######::: ######:::::. ##::::. ######::
    .. ##...:::: ##...::::::: ##:::::..... ##:
    .. ##::::::: ##:::::::::: ##::::'##::: ##:
    .. ##::::::: ########:::: ##::::. ######::
    ..::::::::........:::::..::::::......:::::
    """,
    "6":"""
    8 8888888888   8 8888888888 `8.`8888.      ,8' d888888o.
    8 8888         8 8888        `8.`8888.    ,8'.`8888:' `88.
    8 8888         8 8888         `8.`8888.  ,8' 8.`8888.   Y8
    8 8888         8 8888          `8.`8888.,8'  `8.`8888.
    8 888888888888 8 888888888888   `8.`88888'    `8.`8888.
    8 8888         8 8888            `8. 8888      `8.`8888.
    8 8888         8 8888             `8 8888       `8.`8888.
    8 8888         8 8888              8 8888   8b   `8.`8888.
    8 8888         8 8888              8 8888   `8b.  ;8.`8888
    8 8888         8 888888888888      8 8888    `Y8888P ,88P'
    """,
    "7":"""
     ÛÛÛÛÛÛÛÛÛÛÛ ÛÛÛÛÛÛÛÛÛÛ ÛÛÛÛÛ ÛÛÛÛÛ  ÛÛÛÛÛÛÛÛÛ
     °°ÛÛÛ°°°°°°Û°°ÛÛÛ°°°°°Û°°ÛÛÛ °°ÛÛÛ  ÛÛÛ°°°°°ÛÛÛ
     °ÛÛÛ   Û °  °ÛÛÛ  Û °  °°ÛÛÛ ÛÛÛ  °ÛÛÛ    °°°
     °ÛÛÛÛÛÛÛ    °ÛÛÛÛÛÛ     °°ÛÛÛÛÛ   °°ÛÛÛÛÛÛÛÛÛ
     °ÛÛÛ°°°Û    °ÛÛÛ°°Û      °°ÛÛÛ     °°°°°°°°ÛÛÛ
     °ÛÛÛ  °     °ÛÛÛ °   Û    °ÛÛÛ     ÛÛÛ    °ÛÛÛ
     ÛÛÛÛÛ       ÛÛÛÛÛÛÛÛÛÛ    ÛÛÛÛÛ   °°ÛÛÛÛÛÛÛÛÛ
     °°°°°       °°°°°°°°°°    °°°°°     °°°°°°°°°
"""}
    print(sozluk[str(random.randint(1,7))])

##########################################################################################################################################################################################
###########################################################################################  MAIN FUNCTION ###############################################################################
##########################################################################################################################################################################################

if __name__ == "__main__":
    random_feys()
    root = Tk()
    root.call('tk', 'scaling', 1.0)
    run = tkinterGui(root)
    root.after(1000,run.loading_start)
    root.mainloop()
