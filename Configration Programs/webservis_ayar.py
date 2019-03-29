 # -*- coding: utf-8 -*-

from suds.client import Client
WSDL_URL = "http://authservice.erdogan.edu.tr/AuthenticationService.svc?wsdl"

client = Client(WSDL_URL)


kAdi = 'KullaniciAdi'
kAdiG = 'DersProgrami2017'
kSifre = 'Sifre'
kSifreG = '09998@1@QrZ'
dersKod = 'DersKodu'
dersKodG = 'EEE106'

ust= 'UstBirim'
ustg = '30'  # mühendislik bunu config alicam
derslik = '1493'
birim = 'BirimTipID'
birimG = '90'
sayac = 0
userName  = 'KullaniciAdi'
userPswd = 'DersProgrami2017'
derslikID = '1493'
UUID='EE BE 93 CA'


#result = client.service.GetBirimlerWithCache({"KullaniciAdi":'DersProgrami2017',kSifre:kSifreG,'UstBirim':'90','BirimTipID':"17"})
#derslikler = client.service.GetDerslikler({"KullaniciAdi":userPswd, "Sifre":kSifreG})# üniversite web servisine bağlandım çünkü dersliğin IDsini almam lazım



#for dersliklerdeDolas in derslikler[1][0]:
#    if dersliklerdeDolas[2] == "D-103" and dersliklerdeDolas[5] == "118": # eşleşme sağlanana kadar karşılaştırma yapiyorum
#        derslikID = dersliklerdeDolas[1] # karşılaşma sağlandığında o sinifin derslikIsini aliyorum.
#        break


#print(derslikID)
#result = client.service.GetDersProgrami({"KullaniciAdi":userPswd, "Sifre":kSifreG,'DerslikID':derslikID})


result = client.service.GetKurumKartlari(kullaniciAdi = 'personelcihaz', sifre = 'M5E~zdyV')#, kartNo = UUID)

#result = client.service.GetKurumKartlari(kullaniciAdi = 'personelcihaz',sifre='M5E~zdyV',kartNo = 'EE BE 93 CA')
print(result)

"""


2- )

GetDersiAlanOgrenciler() fonksiyonuna

"KullaniciAdi":'DersProgrami2017'
"Sifre":'09998@1@QrZ'
'DersKodu':'EEE211',
'ProgramID':'772'

olarak gönderildiğinde



DersiAlanOgrencilerResponse){
   Header = None
   dersiAlanOgrencilerDVO =
      (ArrayOfDersiAlanOgrenciDVO){
         DersiAlanOgrenciDVO[] =
            (DersiAlanOgrenciDVO){
               Ad = ""
               GrupNo = ""
               Mufredat = ""
               OgrenciNumarasi = ""
               Soyad = ""
               Sube = ""
            },

            *
            *
            *


    bilgilerini aliyoruz ama bize burada hocanın kartIdsi


(BirimDVO){
               BirimAdi = "MÜHENDİSLİK FAKÜLTESİ"
               BirimId = "30"
               BirimKodu = "95076956"
               BirimTipId = "3"
               BirimTipi = None
               Eposta1 = "foe@erdogan.edu.tr"
               Eposta2 = None
               UstBirimID = "1"





##############################################################################
Hoca mail



1 - )
GetBirimlerWithCache() fonksiyonuna

"KullaniciAdi":'DersProgrami2017'
"Sifre":'09998@1@QrZ'
'UstBirim':'90


bilgileri gönderildiğinde bize

       (BirimDVO){
               BirimAdi = "DEVRELER VE SİSTEMLER ANABİLİM DALI"
               BirimId = "650"
               BirimKodu = None
               BirimTipId = "10"
               BirimTipi = None
               Eposta1 = None
               Eposta2 = None
               UstBirimID = "90"
            },
            (BirimDVO){
               BirimAdi = "Elektrik-Elektronik Mühendisliği"
               BirimId = "772"
               BirimKodu = None
               BirimTipId = "17"
               BirimTipi = None
               Eposta1 = None
               Eposta2 = None
               UstBirimID = "90"
            },
      }

olarak dönüyor şimdi burada anabilim dalı ile normal bölüm birbirinden birimTipID sayesinde ayrılabiliyor ve kullanılabiliyor ama

GetBirimlerWithCache() fonksiyonuna


"KullaniciAdi":'DersProgrami2017'
"Sifre":'09998@1@QrZ'
'UstBirim':'142'

bilgileri gönderildiğinde  bize





2 - )

GetDersiAlanOgrenciler() fonksiyonuna

"KullaniciAdi":'DersProgrami2017'
 "Sifre":'09998@1@QrZ'
 'DersKodu':'EEE211'
 'ProgramID':'772'

bilgileri gönderildiğinde bize

(DersiAlanOgrenciDVO){
               Ad = ""
               GrupNo = ""
               Mufredat = ""
               OgrenciNumarasi = ""
               Soyad = ""
               Sube = ""
            }, ...

olarak dönüyor bize burada bize o öğrencinin kartNo'suda gerekli


Ayrica bize öğretim görevlisi bilgileride gerekli ad soyad , kart numarası ve öğretim görevlisi numarasi olarak kullanabileceğimiz unique birşey lazim

'ProgramID':'772' verildiğinde bize  öğretim görevlisi bilgilerinin döndürmesi lazım

"""

















"""
    veriler servisler

buradan aşağıdaki metod çağrılacak

GetKurumKartlari(string kullaniciAdi, string sifre, string kartNo)

kullaniciAdi == "personelcihaz

sifre == "M5E~zdyV"

kartNo= Hex formatında gönderilecek


---------------------------------------------------

GetDerslikler

 ---------------------------------------------------

GetDersProgrami fonksiyonu eklendi.(parametreler DerslikID, KartNo)

------------------------------------------------------

Program İd değerlerini almak için :

GetBirimlerWithCache fonksiyonu eklendi.

UstBirim: gönderilen birim idsine bağlı alt birimleri getirmek için kullanılır
BirimTipID : Birim tipine göre birimleri döndürür. (Birim tipi 17 programları döndürür)


------------------------------------------------------

    GetDersiAlanOgrenciler

DersKodu :Dersin kodu (Bİl101 gibi)
ProgramID :Hangi program için liste alınacaksa o programın id si




"""


"""



derslik = '1493'

UUID = '55 AD 73 32' # Ercan Sezdi
#UUID = 'EE BE 93 CA' # Burak Tüysüz
#UUID =  '44 DB 4E 21' # Celal Topçu
dersKodu = 'EEE211' # dif def
proID  ='97701903'
BirimTipID= '90'
UstBirim = ' 30'
birim = '9'#'9'#97701903
############


Program İd değerlerini almak için :

GetBirimlerWithCache fonksiyonu eklendi.
UstBirim: gönderilen birim idsine bağlı alt birimleri getirmek için kullanılır
BirimTipID : Birim tipine göre birimleri döndürür. (Birim tipi 17 programları döndürür)



giris = {'KullaniciAdi':'DersProgrami2017', 'Sifre':'09998@1@QrZ','UstBirim':'90'}#,'BirimTipID':'17'}#,'DerslikID':derslik}#,"KartNo":UUID}#,'DerslikID':derslik}
result = client.service.GetBirimlerWithCache(giris)


############
#giris = {"KullaniciAdi":'DersProgrami2017', "Sifre":'09998@1@QrZ','UstBirim':'30'}#,'DerslikID':derslik}#,"KartNo":UUID}#,'DerslikID':derslik}



giris = {"KullaniciAdi":'DersProgrami2017', "Sifre":'09998@1@QrZ','DersKodu':'EEE211','ProgramID':'772'}#,'DerslikID':derslik}#,"KartNo":UUID}#,'DerslikID':derslik}
result = client.service.GetDersiAlanOgrenciler(giris)

print(result)
KullaniciAdi - > DersProgrami2017
Sifre - > 09998@1@QrZ
DersKodu - > EEE211
ProgramID - > 90


result = client.service.GetDersProgrami(giris)
print(result)


for i in result[1][0]:
    if i[2] == 'F-208' and i[5] == '118': # i[1] DerslikID
        print(i)


for i in result[1][0]:
    if  i[5] =="118" :
        if i[2] != None:
            print(i[2])

print('\n\nF-208 Bilgiler\n\n')
for i in result[1][0]:
    if  i[4] =="Muhendislik & Güzel Sanatlar Fak."  and i[0] != None and i[3] != None:#i[2] == 'F-208' and
        print(i)
print('\n\n')
dersprogram = {"KullaniciAdi":'DersProgrami2017', "Sifre":'09998@1@QrZ',"DerslikID":'1493'}#,'DerslikID':derslik}
result2 = client.service.GetDersProgrami(dersprogram)
"""
#print(result2)



"""
DersProgramiByKartNo kaldırıldı

GetDersProgrami fonksiyonu eklendi.(parametreler DerslikID, KartNo)
Ögrenci kart numarası verilirse öğrencinin ders programını DerslikID verilirse o dersliğin ders programını döndürür.

GetDerslikler fonksiyonu eklendi.Parametre almıyor sadece kullanıcı adı ve şifre göndermeniz yeterli. Tüm dersliklerin adını numarasını ve idsini geri döndürüyor.

GetOgrencilerByDersKodu fonksiyonu eklenecek. Henüz tamamlanmadı. Ders Kodu bazında öğrenci listesini almanız için.

İyi Çalışmalar



"""


"""
1- siniflardaki günlük dersler
2- derslerdeki öğrenci listesi
"""
