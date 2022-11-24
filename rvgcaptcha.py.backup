#!/usr/bin/python3                                                                                                    
from socket import IP_MULTICAST_LOOP
from time import time
from flask import Flask, request, jsonify, g, redirect, url_for, render_template
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
from email.mime.text import MIMEText
import random
import uuid
import json
import smtplib, ssl
import syslog

app = Flask (__name__)
cors = CORS(app)

class uuid_dictionary(dict):
    def delete(self, captuuid):
            self.pop(captuuid)
        
    def truncate(self):
        dictlen = len(self)
        print("dictlen = ", dictlen)
        dictlist = []

        for c,e in enumerate(self):
            flatlist = []
            flatlist.append(e)

            for d in self[e]:
                flatlist.append(d)
            dictlist.append(flatlist)

        dictlist.sort(reverse = True, key =  lambda i: i[3])

        for c, d in enumerate(dictlist):
            if c > 9:
                self.pop(d[0])
            
    
    def add(self, captuuid, captsum, ipadr, thetimenow):
        data =  [captsum, ipadr, thetimenow]
        self[captuuid] = data
        self.truncate()
        
       
    def chkFreq(self, captuuid):
        iplistTruncate()
        try:
            ipadr = self[captuuid][1]
        except:
            print("key no match")
            return "pass"
        yet = datetime.now()
        comptime = yet
        trigger = 100
        for c, i in enumerate(iplist):
            if c > 0:
                if i[0] == ipadr:
                    diff = datetime.timestamp(comptime) - datetime.timestamp(i[1])
                    trigger = diff
        if trigger < 2:
            print("warning: robotic data entry suspected")
            sipAdd(ipadr)
            return "time"
        if trigger < 4:
            print("failed time difference: ", diff)
            return "time"
        return "pass"
        
    def lookup(self, captuuid, captsum):
        if self.chkFreq(captuuid) == "time":
            return "time"
        if captuuid in self:
            if self[captuuid][0] == captsum:
                result = "pass"
                self.delete(captuuid) # delete, because we want this only for 1 time
            else:
                result = "fail"
                self.delete(captuuid) # delete, because we want this only for 1 time
        else:
             result = "fail"
        self.truncate()
        return result


class genPic():
    def __init__(self):
        pass
    def new(val1, op, val2, captid):
        img = Image.new('RGB', (90, 45), color = 'red')
        d = ImageDraw.Draw(img)
        myFont = ImageFont.truetype('./fonts/NanumPenScript-Regular.ttf', 32)
        d.text((15, 5), val1 + " " + op + " " + val2, font = myFont)
        img.save("task.png")
        fpath = "static/" + captid + ".png"
        url = request.url_root + "static/" + captid + ".png"
        img.save(fpath)
        return url


def sipAdd(ipadr):
    global suspectiplist
    if suspectiplist.count(ipadr) >= 3:
        print("robotic data input identified - blocking ip address")
        global blockediplist
        blockediplist.append(ipadr)
    suspectiplist.append(ipadr)
    print("robotic data input suspected")


def iplistTruncate():
    global iplist
    if len(iplist) < 10:
        print("len iplist: ", len(iplist))
        return

    print("len iplist: ", len(iplist))
    newiplist = iplist[len(iplist)-9:len(iplist)]
    iplist = newiplist
    print(iplist)

def iplistAdd(ipadr, thetimenow):
    iplistTruncate()
    row = []
    row.append(ipadr)
    row.append(thetimenow)
    iplist.append(row)


@app.before_first_request
def before_first_request():
    app.logger.info("before_first_request")
    global captid_dict
    captid_dict = uuid_dictionary()
    global seed
    seed = datetime.time
    global iplist
    iplist = [[]]
    global blockediplist
    blockediplist = []      
    global suspectiplist
    suspectiplist = []                                                                                      
    random.seed(seed)                                                                                                 
                                                                                                                      
                                                                                                                      
@app.route("/")                                                                                                       
def hello():                                                                                                          
    return "RVG Turing Test"                                                                                          
                                                                                                                      
                                                                                                                      
@app.route("/GetCaptYa")                                                                                              
def randomNumber():                                                                                                   
    number1 = str(random.randint(0, 19))                                                                              
    number2 = str(random.randint(0, 19))                                                                              
    ipadr = request.remote_addr
    global blockediplist
    if blockediplist.count(ipadr) > 0:
        return jsonify("blacklisted:", ipadr)
    captformula = number1 + " + " + number2                                                                           
    captsum = str(int(number1) + int(number2))                                                                        
    captuuid = str(uuid.uuid1())
    yet = datetime.now()
    thetimenow = yet
    print("thetimenow: ", thetimenow)
    captid_dict.add(captuuid, captsum, ipadr, thetimenow)
    iplistAdd(ipadr, thetimenow)
    url = genPic.new(number1, "+", number2, captuuid)                                                                 
    return jsonify(                                                                                                   
        uuid = captuuid,                                                                                              
        url = url,
    )                                                                                                                 
                                                                                                                      
@app.route('/legitimize', methods=['GET'])                                                                            
def legitimize():                   
    ipadr = request.remote_addr       
    global blockediplist                                                                           
    if blockediplist.count(ipadr) > 0:
        return jsonify("blacklisted:", ipadr)
    params = request.args.to_dict()                                                                                   
    captsum = params["solution"]                                                                                      
    captuuid = params["uuid"]                                                                                         
    return jsonify(captid_dict.lookup(captuuid, captsum))                                                             

                                                                                                               

def sendmail(data):
    context = ssl.create_default_context()
    port = 465
    sender = 'contactform@ravegroup.cz'
    receiver = ['rvginfo@ravegroup.cz', 'lsnizek@ravegroup.cz']
    smtp_password = 'TmX.921972'
    if data['email'].lower().find('.ru') > 0:
        syslog.syslog(f"RVGCAPTCHA: RU abuse attempt, {data['email']}")
        syslog.syslog("RVGCAPTCHA: Mail not sent")
        return
    if data['email'].lower().find('.cz') > 0 or data['email'].lower().find('.sk') > 0 or data['email'].lower().find('.at') > 0:
        pass
    else:
        syslog.syslog(f"RVGCAPTCHA: abuse attempt, {data['email']}")
        syslog.syslog(f"RVGCAPTCHA: domain not cz, sk or at")
        return
   

    message = "Message Block: \n"
    message = message + " Název obchodního partnera..: " + data['bpname'] + "\n"
    message = message + " IČO........................: " + data['ico'] + "\n"
    message = message + " Jméno......................: " + data['name'] + "\n"
    message = message + " Příjmení...................: " + data['surname'] + "\n"
    message = message + " Adresa.....................: " + data['address'] + "\n"
    message = message + " Email......................: " + data['email'] + "\n"
    message = message + " Telefón....................: " + data['tel'] + "\n\n"
    message = message + " Zpráva: " + "\n"
    message = message + data['message']
    msg = MIMEText(message)
    msg['Subject'] = "Subject: Žádost o informace"
    msg['From'] = 'RVG Contact Form <contactform@ravegroup.cz>'
    msg['To'] = 'RVGInfo <rvginfo@ravegroup.cz>, Lucie Snizek <lsnizek@ravegroup.cz>'

    syslog.syslog("---------------------------------------------------")
    syslog.syslog(message)
    

    with smtplib.SMTP_SSL('smtp.hostinger.com', port, context=context) as server:
        server.login(sender, smtp_password)
        server.sendmail(sender, receiver, msg.as_string().encode(encoding='UTF-8', errors='ignore'))
        server.quit()
        

    receiver = data['email']
    message = message + "\n-----------------------------------------------------\n"
    message = message + "Tohle je kopie zprávy, kterou jsme od vás obdrželi, a potvrzení, že zpráva dorazila k nám."
    msg = MIMEText(message)
    msg['Subject'] = "Subject: Žádost o informace"
    msg['From'] = 'RVG Contact Form <contactform@ravegroup.cz>'
    msg['To'] = data['email']
    

    with smtplib.SMTP_SSL('smtp.hostinger.com', port, context=context) as server:
        server.login(sender, smtp_password)
        server.sendmail(sender, receiver, msg.as_string().encode(encoding='UTF-8', errors='ignore'))
        server.quit()

    return


@app.route('/mailform', methods=['POST', 'GET'])
def mailform():
    if request.method == 'POST':
         data = request.form
         mailsent = sendmail(data)
         # return redirect('https://www.ravegroup.cz/rvg/rvgmain.html', code=307)
         return render_template("return.html")

@app.route('/whitelist', methods=['GET'])                                                                            
def whitelist():                   
    params = request.args.to_dict()
    ipadr = params["ipadr"]
    global blockediplist
    try:
        blockediplist.remove(ipadr)
    except:
        return jsonify("Status: ", "nothing to whitelist")
    return jsonify("Status: ", f"{ipadr} succesfully whitelisted") 


@app.route('/reset')                                                                            
def reset():                   
    before_first_request()
    return jsonify("Status: ", "rvgcaptya succesfully reset")
