import MFRC522
import signal
import sqlite3
from datetime import datetime
from time import strftime
import RPi.GPIO as GPIO
import sys

def toHex(dec):
	x = (dec %16)
	digits = "0123456789ABCDEF"
	rest = dec /16

	return digits[int(rest)] + digits[int(x)]
def end_read(signal,frame):
	print('End')
	sys.exit()


signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()
last_UUID = 0
UUID = 0
engDay = datetime.today().strftime('%A')
print(engDay)
baglan = sqlite3.connect('../kayitlar/D-103/2017-2018/Bahar/yoklamaKayit/' + engDay + '.db')
veri = baglan.cursor()
dersler = veri.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
dersSayisi = len(dersler)
print('-------',dersler[0])
sayac=0
giris=True
islem = input("""
1 --- >  kart ID okumak
2 --- > karşılaştırma
diğerleri çıkış
islem giriniz :""")
print('\nKart Okutun\n')
if islem == '1':
	while True:
		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
		(status,uid) = MIFAREReader.MFRC522_Anticoll()
		if status == MIFAREReader.MI_OK:
	      		UUID= toHex(uid[int(0)]) + " " +toHex(uid[int(1)])+ " " +toHex(uid[int(2)]) + " " +toHex(uid[int(3)])
		if last_UUID != UUID:
			print('Okunan kart :',UUID)
			last_UUID = UUID
elif islem == '2':
	while True:
		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
		(status,uid) = MIFAREReader.MFRC522_Anticoll()
		if status == MIFAREReader.MI_OK:
				UUID= toHex(uid[int(0)]) + " " +toHex(uid[int(1)])+ " " +toHex(uid[int(2)]) + " " +toHex(uid[int(3)])
		if last_UUID != UUID:
			last_UUID = UUID


			okundu = False
			if giris == True:
				print('-'*150)
				giris = False
			while sayac != dersSayisi:
				oku = veri.execute("select * from '"+ dersler[sayac][0]+ "'").fetchall()
				for okunanKisiler in oku:

					if okunanKisiler[2] == last_UUID:
						print("""
						Okunan kart hakkında bilgiler

						Adı soyadı = {}
						Numarası   = {}
						Ders adı   = {}
						Kart ID    = {}
						""".format(okunanKisiler[1],okunanKisiler[0],okunanKisiler[6],okunanKisiler[2]))
						print('-'*150)
						okundu = True

				if okundu == False:
					print('\t\t\t\t\t\tTanınmayan Kart')
					print('-'*150)
				sayac+=1

			if dersSayisi == sayac:
				sayac = 0
