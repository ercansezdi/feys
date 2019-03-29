

import configparser
from suds.client import Client # okulun veritabanina bağlanmak için kütüphane
import yedekDatabase
import sqlite3
from datetime import datetime
from time import strftime
import os
global configDosyasiAdres
global config
global verbose

verbose = False
configDosyasiAdres = 'conf/bilgiler.cfg'  # config dosyasinin olduğu adres
config = configparser.ConfigParser() # config dosyasini okumak için config parser tanitim

class webserviceClass:

    def __init__(self):
        self.database = yedekDatabase.veritabani()
        config.read(configDosyasiAdres) # config dosyasini yani kullanıcı tarafından girilen bilgiler olan dosyayi okudum
        self.webServiceAdres = config['veri']['databaseAdres']
        self.userName = config['veri']['webServiceUserName']  # config dosyasindan web servis kullanıcı adi aldım
        self.userPswd = config['veri']['webServiceUserPaswd'] # config dosyasından web sevis kullanıcı şifre aldım
        self.sinifAdi = config['veri']['sinif'] # config dosyasından sinif adini okudum
        self.binaId =  config['veri']['binaId'] # config dosyasından bina idisini okudum
        self.dersSaatiKacdakika = config['veri']['dersSaatiKacdakika']
        self.birimID = config['veri']['birimID']
        self.birimTipID = config['veri']['birimTipID']
        self.sinif = config['veri']['sinif']
        #self.derslik = self.derslikIDOgren()
    def basla(self):
        if verbose:
            print('< webservice.webserviceClass.basla() fonksiyonuna giriş yapılıyor... >')
        self.derslikIDOgren()
        self.programIDOgren()
        self.donemYilOgren()
        if verbose:
            print('< webservice.webserviceClass.basla() fonksiyonundan çıkış yapılıyor... >')
    def derslikIDOgren(self): #New
        if verbose:
            print('< webservice.webserviceClass.derslikIDOgren() fonksiyonuna giriş yapılıyor...>')
        baglanti = Client(self.webServiceAdres)
        derslikler = baglanti.service.GetDerslikler({"KullaniciAdi":self.userName, "Sifre":self.userPswd})# üniversite web servisine bağlandım çünkü dersliğin IDsini almam lazım
        for dersliklerdeDolas in derslikler[1][0]:

            if dersliklerdeDolas[2] == self.sinifAdi and dersliklerdeDolas[5] == self.binaId: # eşleşme sağlanana kadar karşılaştırma yapiyorum
                derslikID = dersliklerdeDolas[1] # karşılaşma sağlandığında o sinifin derslikIsini aliyorum.
                break
        if verbose:
            print('< webservice.webserviceClass.derslikIDOgren() fonksiyonundan çıkış yapılıyor... >')
        self.database.verileriYedekle(yil='empty',donem='empty',program_id='empty',derslik_id=derslikID)
    def programIDOgren(self): #New
        if verbose:
            print('< webservice.webserviceClass.programIDOgren() fonksiyonuna giriş yapılıyor... >')
        baglanti = Client(self.webServiceAdres)
        baglan = sqlite3.connect( 'kayitlar/' +str(self.sinif) + '/genelKayitlar/' + 'veri_kayit.db')
        veri = baglan.cursor()
        veriler = veri.execute('select * from kayit').fetchone()
        derslikid = veriler[3]
        birimID = baglanti.service.GetDersProgrami({"KullaniciAdi":self.userName,"Sifre":self.userPswd,"DerslikID":derslikid})
        for i in birimID[1][0]:
            if i[3] == self.birimTipID :
                UstBirim = i[3]
        ############################### DELETE #####################################3
        UstBirim = '90' # Burasi webservise eklenecek burada ders hangi bolumun ise o bolumun idsi alınıyor # 90 EEM  # 99 Mac Muh # 95 Ins Muh
        #########################################################################

        altBolumler = baglanti.service.GetBirimlerWithCache({'KullaniciAdi':self.userName,"Sifre":self.userPswd,'UstBirim':UstBirim})
        for i in altBolumler[1][0]:
            if i[3] == self.birimTipID:
                programID = i[1]
        if verbose:
            print('< webservice.webserviceClass.programIDOgren() fonksiyonundan çıkış yapılıyor... >')
        self.database.verileriYedekle(yil='empty',donem='empty',program_id=programID,derslik_id='empty')
    def derseGoreOgrenciGetir(self,dersKodu): # New
        baglanti = Client(self.webServiceAdres)
        if verbose:
            print('< webservice.webserviceClass.derseGoreOgrenciGetir() fonksiyonuna giriş yapılıyor...')
        baglan = sqlite3.connect( 'kayitlar/' +str(self.sinif) + '/genelKayitlar/' + 'veri_kayit.db')
        veri = baglan.cursor()
        veriler = veri.execute('select * from kayit').fetchone()
        programıd = veriler[2]
        ogrenciler = baglanti.service.GetDersiAlanOgrenciler({"KullaniciAdi":self.userName, "Sifre":self.userPswd,'DersKodu':dersKodu,'ProgramID':str(programıd)})
        numara = []
        adSoyad = []
        kartNo = []
        statu  =[]
        sayac = 0
        if ogrenciler[1] != None:
            for i in ogrenciler[1][0]:
                numara.append(i[3])
                adSoyad.append(str(i[0]) + ' ' + str(i[4]))
                kartNo.append(sayac)
                statu.append('ST')
                sayac+=1
            if verbose:
                print('< webservice.webserviceClass.derseGoreOgrenciGetir() fonksiyonundan çıkış yapılıyor...')
            return numara,adSoyad,kartNo,statu
        else:
            if verbose:
                print('< webservice.webserviceClass.derseGoreOgrenciGetir() fonksiyonundan çıkış yapılıyor...')
            return 'Ogrenci Listesine Ulasılamadı','Ogrenci Listesine Ulasılamadı','Ogrenci Listesine Ulasılamadı','Ogrenci Listesine Ulasılamadı'
    def tablolariGuncelle(self,yil,donem): #New
        if verbose:
            print('< webservice.webserviceClass.tablolariGuncelle fonksiyonuna giriş yapılıyor...>')
        baglanti = Client(self.webServiceAdres)
        baglan = sqlite3.connect( 'kayitlar/' +str(self.sinif) + '/genelKayitlar/' + 'veri_kayit.db')
        veri = baglan.cursor()
        veriler = veri.execute('select * from kayit').fetchone()
        derslikID = veriler[3]
        baglanti =Client(self.webServiceAdres)
        derslikler = baglanti.service.GetDersProgrami({"KullaniciAdi":self.userName, "Sifre":self.userPswd,'DerslikID':derslikID})# üniversite web servisine bağlandım çünkü dersliğin IDsini almam lazım
        for i in derslikler[1][0]:

                if int(i[1]) < 10:
                    dersBaslamaSaati = '0'+ i[1] # ders başlama saatini ab:cd şekline getirdim
                else:
                    dersBaslamaSaati = i[1]
                if int(i[0]) < 10:
                    dersBaslamaSaati = dersBaslamaSaati + ':0' + i[0]
                else:
                    dersBaslamaSaati = dersBaslamaSaati + ':' + i[0]

                if int(i[4]) < 10:
                    dersBitisSaati = '0' + i[4]
                else:
                    dersBitisSaati = i[4]
                if int(i[3]) < 10:
                    dersBitisSaati = dersBitisSaati + ':0' + i[3]
                else:
                    dersBitisSaati = dersBitisSaati + ':' + i[3]
                dersID = i[6]
                dersAdi = i[5]
                dersHocasi = i[14]
                dersGunu = i[12]
                dakika = abs(int(i[1]) - int(i[4])) * 60

                if int(i[0]) > int(i[3]):
                    dakika =  (int(i[4]) - int(i[1]))*60 - abs(int(i[3]) - int(i[0]))
                elif (int(i[0]) < int(i[3])):
                    dakika = ( int(i[4]) - int(i[1]) ) * 60 + abs(int(i[3]) - int(i[0]))

                dersSaati = int(dakika) // int (self.dersSaatiKacdakika)

                if dersSaati == 0:
                    dersSaati = 1
                dersID = i[6]
                derslikAdi = i[8]
                birim = i[2]
                numara , adSoyad ,kartNo, statu=  self.derseGoreOgrenciGetir(dersID)
                if verbose:
                    print(">> ",str(dersGunu),' Günü saat ',dersBaslamaSaati,' daki ',dersAdi,' dersi için veritabani güncelleniyor...')
                if numara != 'Ogrenci Listesine Ulasılamadı' and adSoyad != 'Ogrenci Listesine Ulasılamadı':
                    ##############################################
                    #               DELETE                       #
                    ##############################################
                    numara.append('123456789')                   #
                    adSoyad.append(dersHocasi)                   #
                    kartNo.append('B7 82 00 35')                 #
                    statu.append('TE')                           #
                    ##############################################
                    numara.append('150703002')                   #
                    kartNo.append('0B 27 1F B3')                 #
                    statu.append('ST')                           #
                    adSoyad.append('Doğan Başaran')              #
                    ##############################################
                    numara.append('159357123')                   #
                    kartNo.append('56 47 F1 C5')                 #
                    statu.append('ST')                           #
                    adSoyad.append('Student_Card_5')             #
                    ##############################################
                    numara.append('150000001')                   #
                    kartNo.append('F5 A1 AE A5')                 #
                    statu.append('ST')                           #
                    adSoyad.append('Student_Card_1')             #
                    ##############################################
                    numara.append('150000002')                   #
                    kartNo.append('80 3D 00 35')                 #
                    statu.append('ST')                           #
                    adSoyad.append('Student_Card_2')             #
                    ##############################################
                    numara.append('150000003')                   #
                    kartNo.append('25 2B B2 A5')                 #
                    statu.append('ST')                           #
                    adSoyad.append('Student_Card_3')             #
                    ##############################################
                    numara.append('150000004')                   #
                    kartNo.append('94 B2 9B EB')                 #
                    statu.append('ST')                           #
                    adSoyad.append('Student_Card_4')             #
                    ##############################################

                    self.database.databaseKayit(numara,adSoyad,dersBaslamaSaati,dersBitisSaati,dersSaati,dersAdi,dersHocasi,dersGunu,birim,kartNo,yil,donem,dersID,statu)

        baglan = sqlite3.connect('kayitlar/'+ self.sinif + '/' + yil + '/' + donem + '/' + 'elektrikKayit/sonGuncellemeTarihi.db')
        bugunTarih = str(datetime.today().strftime('%d/%m/%Y'))
        veri = baglan.cursor()
        veriler = veri.execute("select * from guncelleme_tarihi").fetchall()
        for i in veriler:
            if (i[0] != str(bugunTarih)):
                veri.execute('''INSERT INTO guncelleme_tarihi (database_son_guncelleme_tarihi) VALUES ("''' + str(bugunTarih) + '''")''')
                break
        else:
            veri.execute('''INSERT INTO guncelleme_tarihi (database_son_guncelleme_tarihi) VALUES ("''' + str(bugunTarih) + '''")''')
        if verbose:
            print('< webservice.webserviceClass.tablolariGuncelle fonksiyonundan çıkış yapılıyor...>')
        baglan.commit()
    def donemYilOgren(self): #New

        if verbose:
            print('< webservice.webserviceClass.donemYilOgren() fonksiyonuna giriş yapılıyor... >')
        baglanti =Client(self.webServiceAdres)
        derslikler = baglanti.service.GetDerslikler({"KullaniciAdi":self.userName, "Sifre":self.userPswd})# üniversite web servisine bağlandım çünkü dersliğin IDsini almam lazım
        derslikID = 'HATA' # Eğerki eşlemeş bulamaz ise hata vermesi için
        for dersliklerdeDolas in derslikler[1][0]:
            if dersliklerdeDolas[2] == self.sinifAdi and dersliklerdeDolas[5] == self.binaId: # eşleşme sağlanana kadar karşılaştırma yapiyorum
                derslikID = dersliklerdeDolas[1] # karşılaşma sağlandığında o sinifin derslikIsini aliyorum.
                break
        if derslikID != 'HATA':
            sinifProgram = baglanti.service.GetDersProgrami({"KullaniciAdi":self.userName, "Sifre":self.userPswd,'DerslikID':derslikID})
            for i in sinifProgram[1][0]:
                yil = i[17]
                donem = i[9]
                if verbose:
                    print('< webservice.webserviceClass.donemYilOgren() fonksiyonundan çıkış yapılıyor... >')
                self.database.verileriYedekle(yil=yil,donem=donem,program_id='empty',derslik_id='empty')
