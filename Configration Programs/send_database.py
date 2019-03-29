
import os
import configparser


class send_information:
    def __init__(self,yil,donem):

        config = configparser.ConfigParser()
        yil = '2017-2018'
        donem = 'Bahar'
        config.read('../conf/bilgiler.cfg')
        address = "../kayitlar/" + config['veri']['sinif'] + "/" + yil + "/" + donem
        for i in os.listdir(address):
            if i != "yoklamaKayit" and i != "elektrikKayit":
                real_address = address + "/" + i
                os.system("rsync -avz --delete "+ real_address + " trforever@95.183.170.191:/home/trforever/Desktop/gonder")


if __name__ == "__main__":
    curser = send_information('2017-2018','Bahar')
