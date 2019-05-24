#import dependencies
import os
from flask import Flask, render_template, url_for, request, redirect, send_from_directory
from sarasfunction import gettmsidata, getoperator
from datagps import datagpspets, datagpspetswarning
from petsgetrawdata import read_coordinaterawdata
from datagpsrespack import datagpsrespack
from getsms import getsms

#define flask app
app = Flask(__name__)

#define RESPACK image gallery source directory
app.config['UPLOAD_FOLDER'] = '/usr/local/bin/saras/GUI/remote/camera'

#variabel tambahan untuk fungsi miscellanous
#subscribersSessBut adalah penanda tab yang terakhir dibuka untuk session tersebut pada halaman Subscribers
#configureSessBut adalah penanda tab yang terakhir dibuka untuk session tersebut pada halaman Configure
#Fungsi dari kedua variabel ini adalah penanda agar page kembali terbuka pada tab yang terakhir dibuka.
subscribersSessBut='button1'
configureSessBut='button1'

#render default app page, yang adalah home.html
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

#render default page untuk PETS
#tempat dan tempatwarning adalah variabel yang dapat digunakan pada webpage
#datagpspets() adalah fungsi yang me-retuen daftar koordinat yang telah diterima pada database local
#datagpspetswarning() adalah fungsi yang me-return daftar koordinat dengan nilai warning pada kolom korban (yang berarti adanya perubahan jumlah pelanggan terhubung pada titik tersebut) dari database local
@app.route("/PETS")
def PETS():
    return render_template('PETS.html', tempat=datagpspets(), tempatwarning=datagpspetswarning())
    
#fungsi transfer file, kemudian kembali ke halaman Transfer File
@app.route("/transferfilePETS")
def transferfilePETS():
    #memastikan mesh network aktif dengan mengaktifkan bash script mesh.sh
    os.system("sudo /usr/local/bin/saras/mesh.sh")

    #transfer file data tmsi dan konfigurasi operasi dari PC1
    try:
        #perintah ini berfungsi untuk menyalin isi tmsidata.conf dari MINI PC 1 (172.27.0.4) ke tmsidata1.conf pada penyimpanan lokal melalui SSH. File tersebut berisi daftar pelanggan terhubung.
        os.system("sudo sshpass -p action scp action@172.27.0.4:/usr/local/etc/yate/tmsidata.conf /usr/local/bin/saras/GUI/remote/tmsidata1.conf")
        #perintah ini berfungsi untuk menyalin isi ybts.conf dari MINI PC 1 (172.27.0.4) ke ybts1.conf pada penyimpanan lokal melalui SSH. File ini berisi konfigurasi operator yang berjalan pada MINI PC 1
        os.system("sudo sshpass -p action scp action@172.27.0.4:/usr/local/etc/yate/ybts.conf /usr/local/bin/saras/GUI/remote/ybts1.conf")
        #perintah ini berfungsi untuk menyalin daftar jejak koordinat yang disimpan pada PETS
        os.system("sudo python3 /usr/local/bin/saras/GUI/petsgetdata.py")
    except:
        #Peringatan bahwa transfer file gagal
        print('gagal transfer file 1')

    #transfer file data tmsi dan konfigurasi operasi dari PC2
    try:
        #perintah ini berfungsi untuk menyalin isi tmsidata.conf dari MINI PC 2 (172.27.0.5) ke tmsidata2.conf pada penyimpanan lokal melalui SSH. File tersebut berisi daftar pelanggan terhubung.
        os.system("sudo sshpass -p action scp action@172.27.0.5:/usr/local/etc/yate/tmsidata.conf /usr/local/bin/saras/GUI/remote/tmsidata2.conf")
        #perintah ini berfungsi untuk menyalin isi ybts.conf dari MINI PC 2 (172.27.0.5) ke ybts2.conf pada penyimpanan lokal melalui SSH. File ini berisi konfigurasi operator yang berjalan pada MINI PC 2
        os.system("sudo sshpass -p action scp action@172.27.0.5:/usr/local/etc/yate/ybts.conf /usr/local/bin/saras/GUI/remote/ybts2.conf")
    except:
        #Peringatan bahwa transfer file gagal
        print('gagal transfer file 2')

    #transfer file data tmsi dan konfigurasi operasi dari PC3
    try:
        #perintah ini berfungsi untuk menyalin isi tmsidata.conf dari MINI PC 3 (172.27.0.6) ke tmsidata3.conf pada penyimpanan lokal melalui SSH. File tersebut berisi daftar pelanggan terhubung.
        os.system("sudo sshpass -p action scp action@172.27.0.6:/usr/local/etc/yate/tmsidata.conf /usr/local/bin/saras/GUI/remote/tmsidata3.conf")
        #perintah ini berfungsi untuk menyalin isi ybts.conf dari MINI PC 3 (172.27.0.6) ke ybts1.conf pada penyimpanan lokal melalui SSH. File ini berisi konfigurasi operator yang berjalan pada MINI PC 3
        os.system("sudo sshpass -p action scp action@172.27.0.6:/usr/local/etc/yate/ybts.conf /usr/local/bin/saras/GUI/remote/ybts3.conf")
    except:
        #Peringatan bahwa transfer file gagal
        print('gagal transfer file 3')   
    return redirect(url_for('transferPETS'))

#render page untuk transfer file
@app.route("/transferPETS")
def transferPETS():

    try:
        #read_coordinaterawdata() membaca daftar koordinat yang terdapat pada database di PETS
        temporary = read_coordinaterawdata()
    except:
        #jika pembacaan gagal, maka akan diberi tanda pada koordinat (0,0)
        temporary = {'lat':0, 'lng':0}
    return render_template('transfer.html', title="Transfer", tempat = datagpspets(), tempatpets=temporary)

#render page untuk pesan pesan
@app.route("/messages")
def messages():
    #getsms() adalah fungsi untuk membaca semua sms yang telah diterima
    return render_template('messages.html',title="Messages", pesans = getsms())

#reset isi file tmsi; hapus data subscriber. Fungsi ini menerima dua argumen, yaitu sesbut: tab terakhir yang dibuka, dan pc, yaitu penanda MINI PC yang dimaksud                     
@app.route("/cleartmsi/<pc>/<sesbut>")
def cleartmsi(pc,sesbut):
    #deklarasi dan inisiasi variabel
    filename="a"
    destination="1"
    #fungsi kondisional untuk mengetahui file dan IP address yang dimaksud dari parameter yang didapat dari webpage
    if(pc=='1'): #Untuk MINI PC 1
        filename="tmsidata1.conf"
        destination="172.27.0.4"
    elif(pc=='2'): #Untuk MINI PC 2
        filename="tmsidata2.conf"
        destination="172.27.0.5"
    elif(pc=='3'): #UNTUK MINI PC 3
        filename="tmsidata3.conf"
        destination="172.27.0.6"
    
    #perintah untuk menghapus daftar pelanggan terhubung pada tmsidata(n).conf menurut MINI PC (data local), dengan cara menyalin isi tmsidata.conf pada tmsidata(n).conf
    os.system("sudo cp /usr/local/bin/saras/GUI/tmsidata.conf /usr/local/bin/saras/GUI/remote/"+filename)
    #perintah untuk menghapus daftar pelanggan terhubung pada tmsidata.conf di MINI PC, dengan cara menyalin isi tmsidata.conf local pada tmsidata.conf di MINI PC melalui SSH
    os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/tmsidata.conf action@"+destination+":/usr/local/etc/yate/tmsidata.conf")
    #perintah ini digunakan untuk mengulang kembali layanan BTS melalui SSH
    os.system("sudo sshpass -p action ssh action@"+destination+" sudo systemctl restart yate.service")
    #penanda tab terakhir yang dibuka
    global subscribersSessBut
    subscribersSessBut=sesbut
    return redirect(url_for('subscribers'))

#render page subscriber
@app.route("/subscribers")
def subscribers():
    #pelanggans1, pelanggans2, dan pelanggans3 masing masing adalah variabel yang dapat digunakan pada webpage
    #fungsi gettmsidata(arg) berfungsi untuk mengambil daftar pelanggan terhubung yang telah disimpan secara local, menurut masing-masing MINI PC
    return render_template('subscribers.html', title="Subscribers", pelanggans1=gettmsidata(1), pelanggans2=gettmsidata(2), pelanggans3=gettmsidata(3), sessionbutton=subscribersSessBut)

#reboot RESPACK yang diinginkan. Fungsi ini menerima dua argumen, yaitu sesbut: tab terakhir yang dibuka, dan pc, yaitu penanda MINI PC yang dimaksud                 
@app.route("/reboot/<sesbut>/<pc>")
def reboot(sesbut,pc):
    #deklarasi dan inisiasi variabel
    destination="1"
    #fungsi kondisional untuk mengetahui IP address yang dimaksud dari parameter yang didapat dari webpage
    if (pc=='1'): #Untuk MINI PC 1
        destination="172.27.0.4"
    elif(pc=='2'): #Untuk MINI PC 2
        destination="172.27.0.5"
    elif(pc=='3'): #UNTUK MINI PC 3
        destination="172.27.0.6"
    #memastikan mesh network aktif dengan mengaktifkan bash script mesh.sh
    os.system("sudo sh /usr/local/bin/saras/mesh.sh")
    #menjalankan perintah reboot pada RESPACK melalui SSH
    os.system("sudo sshpass -p action ssh action@"+destination+" sudo reboot")
    #penanda tab terakhir yang dibuka
    global configureSessBut
    configureSessBut=sesbut
    return redirect(url_for('configure'))



#shutdown RESPACK yang diinginkan. Fungsi ini menerima dua argumen, yaitu sesbut: tab terakhir yang dibuka, dan pc, yaitu penanda MINI PC yang dimaksud     
@app.route("/shutdown/<sesbut>/<pc>")
def shutdown(sesbut,pc):
    #deklarasi dan inisiasi variabel
    destination="1"
    #fungsi kondisional untuk mengetahui IP address yang dimaksud dari parameter yang didapat dari webpage
    if (pc=='1'): #Untuk MINI PC 1
        destination="172.27.0.4"
    elif(pc=='2'): #Untuk MINI PC 2
        destination="172.27.0.5"
    elif(pc=='3'): #UNTUK MINI PC 3
        destination="172.27.0.6"
    #memastikan mesh network aktif dengan mengaktifkan bash script mesh.sh   
    os.system("sudo sh /usr/local/bin/saras/mesh.sh")
    #menjalankan perintah poweroff pada RESPACK melalui SSH
    os.system("sudo sshpass -p action ssh action@"+destination+" sudo poweroff")
    #penanda tab terakhir yang dibuka
    global configureSessBut
    configureSessBut=sesbut
    return redirect(url_for('configure'))

#konfigurasi PETS per SDR sesuai operator yang diinginkan. Fungsi ini menerima tiga argumen, yaitu sesbut: tab terakhir yang dibuka, pc: penanda MINI PC yang dimaksud, dan operator: operator yang dimaksud    
@app.route("/changeoperator/<pc>/<operator>/<sesbut>")
def changeoperator(pc,operator,sesbut):
    #deklarasi dan inisiasi variabel
    destination="1"
    filename="a"
    localybts="a"
    #fungsi kondisional untuk mengetahui IP address dan file ybts menurut MINI PC yang dimaksud dari parameter yang didapat dari webpage
    if (pc=='1'): #Untuk MINI PC 1
        destination="172.27.0.4"
        localybts="ybts1.conf"
    elif(pc=='2'): #Untuk MINI PC 2
        destination="172.27.0.5"
        localybts="ybts2.conf"
    elif(pc=='3'): #UNTUK MINI PC 3
        destination="172.27.0.6"
        localybts="ybts3.conf"
    #fungsi kondisional untuk menentukan file konfigurasi operator yang dimaksud dari parameter yang didapat dari webpage
    if (operator=='TSEL'):
        filename="ybts-tsel.conf"
    elif(operator=='XL'):
        filename="ybts-xl.conf"
    elif(operator=='ISAT'):
        filename="ybts-isat.conf"

    #isi perintah untuk menyalin file konfigurasi pada file penanda konfigurasi local untuk ditampilkan pada webpage
    localchgybts="sudo cp /usr/local/bin/saras/GUI/"+filename+" /usr/local/bin/saras/GUI/remote/"+localybts
    #isi perintah untuk mengganti konfigurasi operator pada MINI PC yang dimaksud melalui SSH
    petschgybts="sudo sshpass -p action scp /usr/local/bin/saras/GUI/"+filename+" action@"+destination+":/usr/local/etc/yate/ybts.conf"
    #isi perintah untuk mengulang kembali layanan BTS melalui SSH
    restartsrvcmd="sudo sshpass -p action ssh action@"+destination+" sudo systemctl restart yate.service"
    #menjalankan ketiga perintah
    os.system(localchgybts)
    os.system(petschgybts)
    os.system(restartsrvcmd)
    #penanda tab terakhir yang dibuka
    global configureSessBut
    configureSessBut=sesbut
    return redirect(url_for('configure'))

#render page configure pada PETS. 
@app.route("/configure")
def configure():
    #operatorpc1, operatorpc2, dan operatorpc3 adalah variabel yang dapat digunakan pada webpage
    #fungsi getoperator(arg) membaca konfigurasi terakhir yang dijalankan pada PETS menurut MINI PC        
    return render_template('configure.html',title="Configure", operatorpc1=getoperator(1), operatorpc2=getoperator(2), operatorpc3=getoperator(3), sessionbutton=configureSessBut )

#fungsi reset setting kembali default pada PETS
@app.route("/factoryreset", methods=['GET'])
def factoryreset():
    #import dependencies
    import influxdb
    from influxdb import InfluxDBClient
    from influxdb.client import InfluxDBClientError

    #memastikan mesh network aktif dengan mengaktifkan bash script mesh.sh
    os.system("sudo /usr/local/bin/saras/mesh.sh")

    #Bagian ini menghapus hasil perekaman jejak
    #mengakses database local
    client = InfluxDBClient('localhost', '8086', 'action', 'action', 'PETS1')
    #menghapus tabel coordinate yang berisi hasil pengukuran
    client.drop_measurement('coordinate')
    #mengakses database penyimpanan GPS yang disimpan pada MINI PC 1
    try:
        client = InfluxDBClient('172.27.0.4', '8086', 'action', 'action', 'PETS')
        #menghapus tabel coordinate yang berisi hasil pengukuran
        client.drop_measurement('coordinate')
    except:
        print(' ')
    #Bagian ini me-reset konfigurasi yang berjalan pada PETS, sehingga menghapus semua daftar pelanggan terhubung, dan menjalankan konfigurasi operator default pada masing-masing MINI PC (MINI PC 1- TELKOMSEL, MINI PC 2 - XL, MINI PC 3 - OOREDOO), kemudian mengulang kembali layanan BTS melalui SSH
    try:
        os.system("sudo cp /usr/local/bin/saras/GUI/tmsidata.conf /usr/local/bin/saras/GUI/remote/tmsidata1.conf")
        os.system("sudo cp /usr/local/bin/saras/GUI/ybts-tsel.conf /usr/local/bin/saras/GUI/remote/ybts1.conf")
        os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/ybts-tsel.conf action@172.27.0.4:/usr/local/etc/yate/ybts.conf")
        os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/tmsidata.conf action@172.27.0.4:/usr/local/etc/yate/tmsidata.conf")
        os.system("sudo sshpass -p action ssh action@172.27.0.4 sudo systemctl restart yate.service")
        os.system("sudo cp /usr/local/bin/saras/GUI/tmsidata.conf /usr/local/bin/saras/GUI/remote/tmsidata2.conf")
        os.system("sudo cp /usr/local/bin/saras/GUI/ybts-xl.conf /usr/local/bin/saras/GUI/remote/ybts2.conf")
        os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/ybts-xl.conf action@172.27.0.5:/usr/local/etc/yate/ybts.conf")
        os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/tmsidata.conf action@172.27.0.5:/usr/local/etc/yate/tmsidata.conf")
        os.system("sudo sshpass -p action ssh action@172.27.0.5 sudo systemctl restart yate.service")
        os.system("sudo cp /usr/local/bin/saras/GUI/tmsidata.conf /usr/local/bin/saras/GUI/remote/tmsidata3.conf")
        os.system("sudo cp /usr/local/bin/saras/GUI/ybts-isat.conf /usr/local/bin/saras/GUI/remote/ybts3.conf")
        os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/ybts-isat.conf action@172.27.0.6:/usr/local/etc/yate/ybts.conf")
        os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/tmsidata.conf action@172.27.0.6:/usr/local/etc/yate/tmsidata.conf")
        os.system("sudo sshpass -p action ssh action@172.27.0.6 sudo systemctl restart yate.service")
    except:
        print(' ')
    return redirect(url_for('configure'))

#render page about
@app.route("/about")
def about():
    return render_template('about.html',title="About")

"""Respack"""
#render default page respack
@app.route("/respack")
def respack():
     #tempatrespack1, tempatrespack2, dan tempatrespack3 adalah variabel yang dapat digunakan pada webpage
     #fungsi datagpsrespack berfungsi untuk mengambil data gps yang disimpan pada masing-masing tabel local setelah ditransfer
    return render_template('respack.html', tempatrespack1=datagpsrespack(1),tempatrespack2=datagpsrespack(2),tempatrespack3=datagpsrespack(3))

#fungsi transfer file pada RESPACK
@app.route("/transferfilerespack", methods=['GET'])
def transferfilerespack():

    #memastikan mesh network aktif dengan mengaktifkan bash script mesh.sh
    os.system("sudo /usr/local/bin/saras/mesh.sh")

    #mengambil data jejak gps dari masing-masing RESPACK
    os.system("sudo python3 /usr/local/bin/saras/GUI/respackgetdata.py")

    #mengambil gambar dari RESPACK 1
    try:       
        os.system("sudo sshpass -p raspberry scp -r pi@172.27.0.1:/home/pi/Desktop/camera usr/local/bin/saras/GUI/remote/")
    except:
        print('gagal transfer file 1')

    #mengambil gambar dari RESPACK 2
    try:
        os.system("sudo sshpass -p raspberry scp -r pi@172.27.0.2:/home/pi/Desktop/camera usr/local/bin/saras/GUI/remote/")
    except:
        print('gagal transfer file 2')
    
    #mengambil gambar dari RESPACK 3
    try:
        os.system("sudo sshpass -p raspberry scp -r pi@172.27.0.3:/home/pi/Desktop/camera usr/local/bin/saras/GUI/remote/")
    except:
        print('gagal transfer file 3')   
    return redirect(url_for('transferRESPACK'))

#render page gallery pada RESPACK
@app.route("/gallery")
def gallery():
    #image_names berisi daftar nama file yang terdapat pada folder penyimpan gambar
    image_names=os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html',title="Gallery", image_names=image_names)

#fungsi return file gambar. Fungsi ini menerima satu parameter yaitu nama file, dan me-return file yang dimaksud
@app.route('/<filename>')
def send_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#render page transfer file RESPACK
@app.route("/transferRESPACK")
def transferRESPACK():
    return render_template('config.html',title="Transfer")

#render page about RESPACK
@app.route("/about1")
def about1():
    return render_template('about1.html',title="About")


if __name__ == '__main__':
    app.run(debug=True)  
    while True:
            gettmsidata(1)
            getoperator(1)
            gettmsidata(2)
            getoperator(2)
            gettmsidata(3)
            getoperator(3)
            datagpsrespack(1)
            datagpsrespack(2)
            datagpsrespack(3)
            getsms()

  

