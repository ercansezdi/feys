import sqlite3
import os
from datetime import datetime
from time import strftime
import configparser

import webservice
global verbose
global config
global configDosyasiAdres

configDosyasiAdres = 'conf/bilgiler.cfg'
config = configparser.ConfigParser()
verbose = False

class veritabani:
    def __init__(self):
        config.read(configDosyasiAdres) # config dosyasini yani kullanıcı tarafından girilen bilgiler olan dosyayi okudum
        self.derslikAdi = config['veri']['sinif']
    def databaseKayit(self,numara,adSoyad,dBaslama,dBitis,dSaati,dAdi,dHocasi,dGunu,birim,kartID,yil,donem,dKodu,statu):
        if verbose:
            print('< yedekDatabase.veritabani.databaseKayit() fonkisyonuna giriş yapılıyor... >')
        if dGunu == 'Pazartesi':
            engDay ='Monday'
        elif dGunu == 'Salı':
            engDay = 'Tuesday'
        elif dGunu == 'Çarşamba':
            engDay = 'Wednesday'
        elif dGunu == 'Perşembe':
            engDay = 'Thurday'
        elif dGunu == 'Cuma':
            engDay = 'Friday'
        elif dGunu == 'Cumartesi':
            engDay = 'Saturday'
        elif dGunu == 'Pazar':
            engDay = 'Sunday'
        databaseTabloAdi = "'" + dKodu +'_' + str(dAdi) + '_'+  dBaslama + "'"
        baglan = sqlite3.connect( 'kayitlar/' +str(self.derslikAdi) + '/' + yil + '/' + donem +  '/yoklamaKayit/' + engDay + '.db')
        veri = baglan.cursor()
        #databaseTabloAdi =  "'" + dKodu +'_' + str(dAdi) + '_'+  dBaslama + "'"
        kontrol = veri.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name =" + databaseTabloAdi ).fetchone()

        if kontrol == None:
            veri.execute("""CREATE TABLE {} (
            'Numara'	TEXT UNIQUE,
            'Ad_Soyad'	TEXT,
            'Kart_ID'  TEXT,
            'Ders_Baslama_Saati'     TEXT,
            'Ders_Bitis_Saati' TEXT,
            'Ders_Saati' TEXT,
            'Ders_Adi' TEXT,
            'Ders_Kodu' TEXT ,
            'Ders_Hocasi' TEXT,
            'Ders_Gunu'  TEXT,
            'Derslik_Adi' TEXT,
            'Birim' TEXT,
            'Yil' TEXT,
            'Donem' TEXT,
            'Statu' TEXT,
            'Guncelleme_Tarihi' TEXT,
            PRIMARY KEY(Numara));""".format(databaseTabloAdi))
            baglan.commit()
        sayac = 0
        bugunTarih = str(datetime.today().strftime('%d/%m/%Y'))
        for i in numara:

            buKisiEklimi = veri.execute("select exists(select * from " + databaseTabloAdi  +" where numara = "+  str(numara[sayac]) + ")").fetchone()[0]

            if buKisiEklimi == 0: # burada bu kişi ekle
                bugunTarih = datetime.today().strftime('%d/%m/%Y')
                ############### DELETE ###############
                if i == '160711004':                 #
                    kartID[sayac] = '24 93 35 23'    #
                ######################################
                veri.execute("INSERT INTO " + databaseTabloAdi +" (Numara, Ad_Soyad, Kart_ID, Ders_Baslama_Saati, Ders_Bitis_Saati, Ders_Saati, Ders_Adi, Ders_Kodu, Ders_Hocasi, Ders_Gunu, Derslik_Adi, Birim, Yil, Donem, Statu, Guncelleme_Tarihi) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(numara[sayac],adSoyad[sayac],kartID[sayac],dBaslama,dBitis,str(dSaati),dAdi,dKodu,dHocasi,engDay,self.derslikAdi,birim,yil,donem,statu[sayac],bugunTarih))
                if verbose:
                    print(">>> ",dAdi,' !!! New Record !!! ',numara[sayac],'numaralı ' +adSoyad[sayac] +' adlı kişi veritabanına ekleniyor...')
                baglan.commit()

            else:    #sadece çıkış zamanını güncelle
                veri.execute("UPDATE "+ databaseTabloAdi + " SET Guncelleme_Tarihi = '" + str(bugunTarih) + "' WHERE numara = " + str(numara[sayac]))
                baglan.commit()
            sayac += 1

        allDatabase = veri.execute('select * from ' + databaseTabloAdi).fetchall()

        for i in allDatabase:
            if bugunTarih != i[15]:
                veri.execute("Delete from " + databaseTabloAdi + " where numara='" + i[0] + "'")
                if verbose:
                    print(">>> ",dAdi,'!!! Deleting Record !!! ',i[0],'numaralı ' +i[1] +' adlı kişi veritabanından siliniyor...' )
        if verbose:
            print('< yedekDatabase.veritabani.databaseKayit() fonkisyonundan çıkış yapılıyor... >')
        baglan.commit()
        baglan.close()
    def dersBilgilerDatabase(self,yil,donem):
        if verbose:
            print('< yedekDatabase.veritabani.dersBilgilerDatabase() fonksiyonuna giriş yapılıyor... >')
        engDay = datetime.today().strftime('%A')
        baglan = sqlite3.connect( 'kayitlar/' +str(self.derslikAdi) + '/' + yil + '/' + donem + '/' + 'yoklamaKayit/' + engDay + '.db')
        veri = baglan.cursor()
        tableNames = veri.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tabloAdi = []
        dersGunu = []
        dersBaslaZamani = []
        dersBitisZamani = []
        dersAdi = []
        hocaAdi = []
        dKodu = []
        for dolas in tableNames:
            tabloAdi.append(dolas[0])
        uzunluk = len(tabloAdi)
        sayac = 0
        while sayac < uzunluk:
            sonuclar = veri.execute('select * from "' + tabloAdi[sayac] + '"')
            baglan.commit()
            sart = True
            for i in sonuclar:
                if sart == True:
                    dersAdi.append(i[6])
                    hocaAdi.append(i[8])
                    dKodu .append(i[7])
                    dersBaslaZamani.append(i[3])
                    dersBitisZamani.append(i[4])
                    dersGunu.append(i[8])
                    sart = False
            sayac+=1
        if verbose:
            print('< yedekDatabase.veritabani.dersBilgilerDatabase() fonksiyonundan çıkışş yapılıyor... >')
        if tabloAdi != []:
            return tabloAdi,dersGunu,dersBaslaZamani,dersBitisZamani,dersAdi,hocaAdi,dKodu
        else:
            return None,None,None,None,None,None,None
    def kartIDKontrol(self,yil,donem,UUID,dersAdi):
        if verbose:
            print('< yedekDatabase.veritabani.kartIDKontrol() fonksiyonuna giriş yapılıyor... >')
        engDay = datetime.today().strftime('%A')
        baglan = sqlite3.connect( 'kayitlar/' +config['veri']['sinif'] + '/' + yil + '/' + donem + '/' + 'yoklamaKayit/' + engDay + '.db')
        veri = baglan.cursor()

        oku = veri.execute("select * from '"+ dersAdi+ "'").fetchall()


        for okunanKisiler in oku:
            if okunanKisiler[2] == UUID:
                if verbose:
                    print('< yedekDatabase.veritabani.kartIDKontrol() fonksiyonundan çıkış yapılıyor... >')
                return okunanKisiler[0],okunanKisiler[1],okunanKisiler[14],okunanKisiler[5]
        if verbose:
            print('< yedekDatabase.veritabani.kartIDKontrol() fonksiyonundan çıkış yapılıyor... >')
        return None,None,None,None
    def dersGirisCikisKarsilastir(self,dersCikis,yil,donem):
        if verbose:
            print('< yedekDatabase.veritabani.dersGirisCikisKarsilastir() fonksiyonuna giriş yapılıyor... >')
        engDay = datetime.today().strftime('%A')
        baglan = sqlite3.connect( 'kayitlar/' +str(self.derslikAdi) + '/' + yil + '/' + donem + '/' + 'yoklamaKayit/' + engDay + '.db')
        veri = baglan.cursor()
        tableName = veri.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        for dolas in tableName:
            sonuc =veri.execute("SELECT Ders_Baslama_Saati FROM '"+ dolas[0] +"'").fetchall()
            if sonuc[0][0] == dersCikis:
                if verbose:
                    print('< yedekDatabase.veritabani.dersGirisCikisKarsilastir() fonksiyonundan çıkış yapılıyor... >')
                return True
            else:
                pass
        if verbose:
            print('< yedekDatabase.veritabani.dersGirisCikisKarsilastir() fonksiyonundan çıkış yapılıyor... >')
        return False
    def yoklamaKayit(self,yil,donem,dersKodu,numara,adSoyad,statu,hangiKisim):
        if verbose:
            print('< yedekDatabase.veritabani.yoklamaKayit() fonksiyonuna giriş yapılıyor... >')
        bugunTarih = datetime.today().strftime('%d-%m-%Y')
        baglan = sqlite3.connect( 'kayitlar/' +str(self.derslikAdi) + '/' + yil + '/' + donem +'/'+dersKodu+'/'+bugunTarih+'.db')
        veri = baglan.cursor()
        if hangiKisim == 'loginPermit':
            kontrol = veri.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name ='" + dersKodu+"'" ).fetchone()
            if kontrol == None:
                veri.execute("""CREATE TABLE {} (
                'Numara'	 TEXT UNIQUE,
                'Ad_Soyad'	 TEXT,
                'Tarih'      TEXT,
                'Giris_Saat' TEXT,
                'Cikis_Saat' TEXT,
                'Statu'     TEXT,
                'Ders_Metod' TEXT,
                PRIMARY KEY(Numara));""".format(dersKodu))
                baglan.commit()

            buKisiEklimi = veri.execute("select exists(select * from '" + dersKodu  +"' where numara = '"+  str(numara) + "')").fetchone()[0]

            if buKisiEklimi == 0:#bu kişi ekli değil ekle
                Giris_Saat = datetime.today().strftime('%H:%M:%S')
                Cikis_Saat = None
                veri.execute("INSERT INTO '"+ dersKodu + "' (Numara,Ad_Soyad,Tarih,Giris_Saat,Cikis_Saat,Statu,Ders_Metod) VALUES (?,?,?,?,?,?,?)",(numara,adSoyad,bugunTarih,Giris_Saat,Cikis_Saat,statu,None))
                baglan.commit()
                if verbose:
                    print('< yedekDatabase.veritabani.yoklamaKayit() fonksiyonundan çıkış yapılıyor... >')
                return 'girisYapti'
            else:
                if verbose:
                    print('< yedekDatabase.veritabani.yoklamaKayit() fonksiyonundan çıkış yapılıyor... >')
                return 'kisiDahaOnceEklenmis'
        if hangiKisim == 'exitPermit':
            kontrol = veri.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name ='" + dersKodu+"'" ).fetchone()
            if kontrol == None:
                veri.execute("""CREATE TABLE {} (
                'Numara'	 TEXT UNIQUE,
                'Ad_Soyad'	 TEXT,
                'Tarih'      TEXT,
                'Giris_Saat' TEXT,
                'Cikis_Saat' TEXT,
                'Statu'     TEXT,
                'Ders_Metod' TEXT,
                PRIMARY KEY(Numara));""".format(dersKodu))
                baglan.commit()
            buKisiEklimi = veri.execute("select exists(select * from '" + dersKodu  +"' where Numara = '"+  str(numara) + "')").fetchone()[0]
            if buKisiEklimi == 0:
                if verbose:
                    print('< yedekDatabase.veritabani.yoklamaKayit() fonksiyonundan çıkış yapılıyor... >')
                return 'girisKayitYok'
            else:
                cikisKontrol=veri.execute('select exists(select * from '+ dersKodu + ' where Numara= ' + str(numara) + ' and Cikis_Saat)').fetchone()[0]
                if ((cikisKontrol == 0)):
                    dersCikisSaat = datetime.today().strftime('%H:%M:%S')
                    veri.execute("UPDATE '" + dersKodu + "' SET Cikis_Saat = '" + str(dersCikisSaat) + "' WHERE Numara = '" + str(numara)+"'" )
                    baglan.commit()
                    if verbose:
                        print('< yedekDatabase.veritabani.yoklamaKayit() fonksiyonundan çıkış yapılıyor... >')
                    return 'cikisYapti'
                else:
                    if verbose:
                        print('< yedekDatabase.veritabani.yoklamaKayit() fonksiyonundan çıkış yapılıyor... >')
                    return 'cikisYapmıs'
    def verileriYedekle(self,yil,donem,program_id,derslik_id):
        if verbose:
            print('< yedekDatabase.veritabani.verileriYedekle() fonksiyonuna giriş yapılıyor... >')
        guncelleme_tarihi = datetime.today().strftime('%d/%m/%Y')
        baglan = sqlite3.connect( 'kayitlar/' +str(self.derslikAdi) + '/genelKayitlar/' + 'veri_kayit.db')
        veri = baglan.cursor()
        veri.execute("""CREATE TABLE IF NOT EXISTS kayit (
        'yil'	TEXT ,
        'donem'	TEXT,
        'program_id'  TEXT,
        'derslik_id'  TEXT,
        'guncelleme_tarihi' TEXT);""")
        baglan.commit()
        veriler = veri.execute('select * from kayit').fetchone()
        baglan.commit()
        if veriler == None:
            veri.execute("INSERT INTO kayit (yil,donem,program_id,derslik_id,guncelleme_tarihi) VALUES (?,?,?,?,?)",(yil,donem,program_id,derslik_id,guncelleme_tarihi))
            baglan.commit()

        if yil != "empty":
            veri.execute("UPDATE  kayit SET yil = '" + yil + "'")
        if donem != "empty":
            veri.execute("UPDATE  kayit SET donem = '" + donem + "'")
        if program_id != "empty":
            veri.execute("UPDATE  kayit SET program_id = '" + program_id + "'")
        if derslik_id != "empty":
            veri.execute("UPDATE  kayit SET derslik_id = '" + derslik_id + "'")

        veri.execute("UPDATE  kayit SET guncelleme_tarihi = '" + guncelleme_tarihi + "'")
        if verbose:
            print('< yedekDatabase.veritabani.verileriYedekle() fonksiyonundan çıkış yapılıyor... >')
        baglan.commit()
        baglan.close()
