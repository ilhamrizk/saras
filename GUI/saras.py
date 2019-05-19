#import dependencies
import os
from flask import Flask, render_template, url_for, request, redirect, send_from_directory
from sarasfunction import gettmsidata, getoperator
from datagps import datagpspets, datagpspetswarning
from petsgetrawdata import read_coordinaterawdata
from datagpsrespack import datagpsrespack1, datagpsrespack2, datagpsrespack3
from getsms import getsms

#define flask app
app = Flask(__name__)

#define RESPACK image gallery source directory
app.config['UPLOAD_FOLDER'] = '/usr/local/bin/saras/GUI/remote/camera'

#variabel tambahan untuk fungsi miscellanous
subscribersSessBut='button1'
configureSessBut='button1'

#render default app page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

#render default page untuk PETS
@app.route("/PETS")
def PETS():
    return render_template('PETS.html', tempat=datagpspets(), tempatwarning=datagpspetswarning())
    
#fungsi transfer file
@app.route("/transferfile", methods=['GET'])
def transferfile():
    #memastikan mesh network aktif
    os.system("sudo /usr/local/bin/saras/mesh.sh")

    #transfer file data tmsi dan konfigurasi operasi dari PC1
    try:
        os.system("sudo sshpass -p action scp action@172.27.0.4:/usr/local/etc/yate/tmsidata.conf /usr/local/bin/saras/GUI/remote/tmsidata1.conf")
        os.system("sudo sshpass -p action scp action@172.27.0.4:/usr/local/etc/yate/ybts.conf /usr/local/bin/saras/GUI/remote/ybts1.conf")
        os.system("sudo python3 /usr/local/bin/saras/GUI/petsgetdata1.py")
    except:
        print('gagal transfer file 1')

    #transfer file data tmsi dan konfigurasi operasi dari PC2
    try:
        os.system("sudo sshpass -p action scp action@172.27.0.5:/usr/local/etc/yate/tmsidata.conf /usr/local/bin/saras/GUI/remote/tmsidata2.conf")
        os.system("sudo sshpass -p action scp action@172.27.0.5:/usr/local/etc/yate/ybts.conf /usr/local/bin/saras/GUI/remote/ybts2.conf")
        #os.system("sudo python3 /usr/local/bin/saras/GUI/petsgetdata2.py")
    except:
        print('gagal transfer file 2')

    #transfer file data tmsi dan konfigurasi operasi dari PC3
    try:
        os.system("sudo sshpass -p action scp action@172.27.0.6:/usr/local/etc/yate/tmsidata.conf /usr/local/bin/saras/GUI/remote/tmsidata3.conf")
        os.system("sudo sshpass -p action scp action@172.27.0.6:/usr/local/etc/yate/ybts.conf /usr/local/bin/saras/GUI/remote/ybts3.conf")
        #dos.system("sudo python3 /usr/local/bin/saras/GUI/petsgetdata2.py")
    except:
        print('gagal transfer file 3')   
    return redirect(url_for('transfer'))

#render page untuk transfer file
@app.route("/transfer")
def transfer():

    try:
        temporary = read_coordinaterawdata()
        # os.system("sudo sshpass -p action ssh action@172.27.0.4 systemctl restart yate.service")
        # os.system("sudo sshpass -p action ssh action@172.27.0.5 systemctl restart yate.service")
        # os.system("sudo sshpass -p action ssh action@172.27.0.6 systemctl restart yate.service")
    except:
        temporary = {'lat':0, 'lng':0}
    return render_template('transfer.html', title="Transfer", tempat = datagpspets(), tempatpets=temporary)

#render page untuk pesan pesan
@app.route("/messages")
def messages():
    return render_template('messages.html',title="Messages", pesans = getsms())

#reset isi file tmsi; hapus data subscriber                
@app.route("/cleartmsi/<pc>/<sesbut>")
def cleartmsi(pc,sesbut):
    filename="a"
    destination="1"
    if(pc==1):
        filename="tmsidata1.conf"
        destination="172.27.0.4"
    elif(pc==2):
        filename="tmsidata2.conf"
        destination="172.27.0.5"
    elif(pc==3):
        filename="tmsidata3.conf"
        destination="172.27.0.6"
    os.system("sudo cp /usr/local/bin/saras/GUI/tmsidata.conf /usr/local/bin/saras/GUI/remote/"+filename)
    os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/tmsidata.conf action@"+destination+":/usr/local/etc/yate/tmsidata.conf")
    os.system("sudo sshpass -p action ssh action@"+destination+" sudo systemctl restart yate.service")
    global subscribersSessBut
    subscribersSessBut=sesbut
    return redirect(url_for('subscribers'))

# @app.route("/cleartmsi2/<sesbut>")
# def cleartmsi2(sesbut):
#     os.system("sudo cp /usr/local/bin/saras/GUI/tmsidata.conf /usr/local/bin/saras/GUI/remote/tmsidata2.conf")
#     os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/tmsidata.conf action@172.27.0.5:/usr/local/etc/yate/tmsidata.conf")
#     os.system("sudo sshpass -p action ssh action@172.27.0.5 sudo systemctl restart yate.service")
#     global subscribersSessBut
#     subscribersSessBut=sesbut
#     return redirect(url_for('subscribers'))

# @app.route("/cleartmsi3/<sesbut>")
# def cleartmsi3(sesbut):
#     os.system("sudo cp /usr/local/bin/saras/GUI/tmsidata.conf /usr/local/bin/saras/GUI/remote/tmsidata3.conf")
#     os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/tmsidata.conf action@172.27.0.6:/usr/local/etc/yate/tmsidata.conf")
#     os.system("sudo sshpass -p action ssh action@172.27.0.6 sudo systemctl restart yate.service")
#     global subscribersSessBut
#     subscribersSessBut=sesbut
#     return redirect(url_for('subscribers'))

#render page subscriber
@app.route("/subscribers")
def subscribers():
    return render_template('subscribers.html', title="Subscribers", pelanggans1=gettmsidata(1), pelanggans2=gettmsidata(2), pelanggans3=gettmsidata(3), sessionbutton=subscribersSessBut)

#reboot RESPACK yang diinginkan                
@app.route("/reboot/<sesbut>/<pc>")
def reboot(sesbut,pc):
    destination="1"
    if (pc==1):
        destination="172.27.0.4"
    elif(pc==2):
        destination="172.27.0.5"
    elif(pc==2):
        destination="172.27.0.6"
    os.system("sudo sh /usr/local/bin/saras/mesh.sh")
    os.system("sudo sshpass -p action ssh action@"+destination+" sudo reboot")
    global configureSessBut
    configureSessBut=sesbut
    return redirect(url_for('configure'))

# @app.route("/reboot2/<sesbut>")
# def reboot2(sesbut):
#     os.system("sudo sh /usr/local/bin/saras/mesh.sh")
#     os.system("sudo sshpass -p action ssh action@172.27.0.5 sudo reboot")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

# @app.route("/reboot3/<sesbut>")
# def reboot3(sesbut):
#     os.system("sudo sh /usr/local/bin/saras/mesh.sh")
#     os.system("sudo sshpass -p action ssh action@172.27.0.6 sudo reboot")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

#shutdown RESPACK yang diinginkan
@app.route("/shutdown/<sesbut>/<pc>")
def shutdown(sesbut,pc):
    destination="1"
    if (pc==1):
        destination="172.27.0.4"
    elif(pc==2):
        destination="172.27.0.5"
    elif(pc==2):
        destination="172.27.0.6"
    os.system("sudo sh /usr/local/bin/saras/mesh.sh")
    os.system("sudo sshpass -p action ssh action@"+destination+" sudo poweroff")
    global configureSessBut
    configureSessBut=sesbut
    return redirect(url_for('configure'))

# @app.route("/shutdown2/<sesbut>")
# def shutdown2(sesbut):
#     os.system("sudo sh /usr/local/bin/saras/mesh.sh")
#     os.system("sudo sshpass -p action ssh action@172.27.0.5 sudo poweroff")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

# @app.route("/shutdown3/<sesbut>")
# def shutdown3(sesbut):
#     os.system("sudo sh /usr/local/bin/saras/mesh.sh")
#     os.system("sudo sshpass -p action ssh action@172.27.0.6 sudo poweroff")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

#konfigurasi PETS per SDR sesuai operator yang diinginkan
@app.route("/changeoperator/<pc>/<operator>/<sesbut>")
def changeoperator(pc,operator,sesbut):
    destination="1"
    filename="a"
    localybts="a"
    if (pc==1):
        destination="172.27.0.4"
        localybts="ybts1.conf"
    elif(pc==2):
        destination="172.27.0.5"
        localybts="ybts2.conf"
    elif(pc==2):
        destination="172.27.0.6"
        localybts="ybts3.conf"

    if (operator=='TSEL'):
        filename="ybts-tsel.conf"
    elif(operator=='XL'):
        filename="ybts-xl.conf"
    elif(operator=='ISAT'):
        filename="ybts-isat.conf"

    os.system("sudo cp /usr/local/bin/saras/GUI/"+filename+" /usr/local/bin/saras/GUI/remote/"+localybts)
    os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/"+filename+" action@"+destination+":/usr/local/etc/yate/ybts.conf")
    os.system("sudo sshpass -p action ssh action@"+destination+" sudo systemctl restart yate.service")
    global configureSessBut
    configureSessBut=sesbut
    return redirect(url_for('configure'))

# @app.route("/xl1/<sesbut>")
# def xl1(sesbut):
#     os.system("sudo cp /usr/local/bin/saras/GUI/ybts-xl.conf /usr/local/bin/saras/GUI/remote/ybts1.conf")
#     os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/ybts-xl.conf action@172.27.0.4:/usr/local/etc/yate/ybts.conf")
#     os.system("sudo sshpass -p action ssh action@172.27.0.4 sudo systemctl restart yate.service")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

# @app.route("/indosat1/<sesbut>")
# def indosat1(sesbut):
#     os.system("sudo cp /usr/local/bin/saras/GUI/ybts-isat.conf /usr/local/bin/saras/GUI/remote/ybts1.conf")
#     os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/ybts-isat.conf action@172.27.0.4:/usr/local/etc/yate/ybts.conf")
#     os.system("sudo sshpass -p action ssh action@172.27.0.4 sudo systemctl restart yate.service")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

# @app.route("/telkomsel2/<sesbut>")
# def telkomsel2(sesbut):
#     os.system("sudo cp /usr/local/bin/saras/GUI/ybts-tsel.conf /usr/local/bin/saras/GUI/remote/ybts2.conf")
#     os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/ybts-tsel.conf action@172.27.0.5:/usr/local/etc/yate/ybts.conf")
#     os.system("sudo sshpass -p action ssh action@172.27.0.5 sudo systemctl restart yate.service")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

# @app.route("/xl2/<sesbut>")
# def xl2(sesbut):
#     os.system("sudo cp /usr/local/bin/saras/GUI/ybts-xl.conf /usr/local/bin/saras/GUI/remote/ybts2.conf")
#     os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/ybts-xl.conf action@172.27.0.5:/usr/local/etc/yate/ybts.conf")
#     os.system("sudo sshpass -p action ssh action@172.27.0.5 sudo systemctl restart yate.service")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

# @app.route("/indosat2/<sesbut>")
# def indosat2(sesbut):
#     os.system("sudo cp /usr/local/bin/saras/GUI/ybts-isat.conf /usr/local/bin/saras/GUI/remote/ybts2.conf")
#     os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/ybts-isat.conf action@172.27.0.5:/usr/local/etc/yate/ybts.conf")
#     os.system("sudo sshpass -p action ssh action@172.27.0.5 sudo systemctl restart yate.service")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

# @app.route("/telkomsel3/<sesbut>")
# def telkomsel3(sesbut):
#     os.system("sudo cp /usr/local/bin/saras/GUI/ybts-tsel.conf /usr/local/bin/saras/GUI/remote/ybts3.conf")
#     os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/ybts-tsel.conf action@172.27.0.6:/usr/local/etc/yate/ybts.conf")
#     os.system("sudo sshpass -p action ssh action@172.27.0.6 sudo systemctl restart yate.service")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

# @app.route("/xl3/<sesbut>")
# def xl3(sesbut):
#     os.system("sudo cp /usr/local/bin/saras/GUI/ybts-xl.conf /usr/local/bin/saras/GUI/remote/ybts3.conf")
#     os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/ybts-xl.conf action@172.27.0.6:/usr/local/etc/yate/ybts.conf")
#     os.system("sudo sshpass -p action ssh action@172.27.0.6 sudo systemctl restart yate.service")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

# @app.route("/indosat3/<sesbut>")
# def indosat3(sesbut):
#     os.system("sudo cp /usr/local/bin/saras/GUI/ybts-isat.conf /usr/local/bin/saras/GUI/remote/ybts3.conf")
#     os.system("sudo sshpass -p action scp /usr/local/bin/saras/GUI/ybts-isat.conf action@172.27.0.6:/usr/local/etc/yate/ybts.conf")
#     os.system("sudo sshpass -p action ssh action@172.27.0.6 sudo systemctl restart yate.service")
#     global configureSessBut
#     configureSessBut=sesbut
#     return redirect(url_for('configure'))

#render page configure pada PETS
@app.route("/configure")
def configure():        
    return render_template('configure.html',title="Configure", operatorpc1=getoperator(1), operatorpc2=getoperator(2), operatorpc3=getoperator(3), sessionbutton=configureSessBut )

#fungsi reset setting kembali default pada PETS
@app.route("/factoryreset", methods=['GET'])
def factoryreset():
    import influxdb
    from influxdb import InfluxDBClient
    from influxdb.client import InfluxDBClientError
    os.system("sudo /usr/local/bin/saras/mesh.sh")
    client = InfluxDBClient('localhost', '8086', 'action', 'action', 'PETS1')
    client.drop_measurement('coordinate')
    client = InfluxDBClient('172.27.0.4', '8086', 'action', 'action', 'PETS')
    client.drop_measurement('coordinate')
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
    return redirect(url_for('configure'))

#render page about
@app.route("/about")
def about():
    return render_template('about.html',title="About")

"""Respack"""
#render default page respack
@app.route("/respack")
def respack():
    return render_template('respack.html', tempatrespack1=datagpsrespack1(),tempatrespack2=datagpsrespack2(),tempatrespack3=datagpsrespack3())

#fungsi transfer file pada RESPACK
@app.route("/transferfilerespack", methods=['GET'])
def transferfilerespack():
    os.system("sudo /usr/local/bin/saras/mesh.sh")
    try:       
        os.system("sudo python3 /usr/local/bin/saras/GUI/respack1getdata.py")
        os.system("sudo sshpass -p raspberry scp -r pi@172.27.0.1:/home/pi/Desktop/camera /usr/local/bin/saras/GUI/remote/")
    except:
        print('gagal transfer file 1')
    try:
        os.system("sudo python3 /usr/local/bin/saras/GUI/respack2getdata.py")
        os.system("sudo sshpass -p raspberry scp -r pi@172.27.0.2:/home/pi/Desktop/camera /usr/local/bin/saras/GUI/remote/")
    except:
        print('gagal transfer file 2')
    try:
        os.system("sudo python3 /usr/local/bin/saras/GUI/respack3getdata.py")
        os.system("sudo sshpass -p raspberry scp -r pi@172.27.0.3:/home/pi/Desktop/camera /usr/local/bin/saras/GUI/remote/")
    except:
        print('gagal transfer file 3')   
    return redirect(url_for('config'))

#render page location pada RESPACK?????
@app.route("/location")
def location():
    return render_template('location.html',title="Location")

#render page gallery pada RESPACK
@app.route("/gallery")
def gallery():
    image_names=os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html',title="Gallery", image_names=image_names)

#fungsi return file gambar
@app.route('/<filename>')
def send_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#render page config RESPACK
@app.route("/config")
def config():
    return render_template('config.html',title="Transfer")

#render page about RESPACK
@app.route("/about1")
def about1():
    return render_template('about1.html',title="About")


if __name__ == '__main__':
    app.run(debug=True)  
    while True:
            gettmsidata1()
            getoperator1()
            gettmsidata2()
            getoperator2()
            gettmsidata3()
            getoperator3()
            datagpsrespack1()
            datagpsrespack2()
            datagpsrespack3()
            getsms()

  

