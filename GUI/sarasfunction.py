def gettmsidata(pc):
        if (pc==1):
                filename="tmsidata1.conf"
        elif (pc==2):
                filename="tmsidata2.conf"
        elif (pc==3):
                filename="tmsidata3.conf"
        f=open("/etc/saras/GUI/remote/"+filename)
        tmsi = f.read()
        import re
        words = re.split(r'[^\w]',tmsi)
        for word in words:
                if word == "":
                        words.remove(word)
        imsi_get = []
        imei_get = []
        localMSISDN_get = []
        tmsi_get = []
        pelanggans = []
        #print(range(len(words)))
        #print(len(words))
        #print(words)
        for i in range(len(words)):
                if words[i] == 'ues':
                        k=0
                        leng=len(words)		
                        while k<(int((leng-4)//7)):
                                imsi_get.append(words[(i+1)+(k*7)])
                                imei_get.append(words[i+3+(k*7)])
                                localMSISDN_get.append(words[i+4+(k*7)])
                                tmsi_get.append(words[i+5+(k*7)])
                                k = k+1
        for j in range(len(imsi_get)):
                pelanggans.append(
                        {
                        'IMSI' : imsi_get[j],
                        'IMEI' : imei_get[j],
                        'MSISDN' : localMSISDN_get[j],
                        'tmsi' : tmsi_get[j]
                        })
        return pelanggans

def getoperator(pc):
    import re
    if (pc==1):
        filename="ybts1.conf"
    elif (pc==2):
        filename="ybts2.conf"
    elif (pc==3):
        filename="ybts3.conf"      
    f=open("/etc/saras/GUI/remote/"+filename)
    ybts = f.read()

    words = re.split(r'[^\w]',ybts)
    for word in words:
         if word == "":
             words.remove(word)
    #print(words)
    bandoperator = words[83]
    if bandoperator == '0':
         operator = 'INDOSAT'
    elif bandoperator == '50':
         operator = 'TELKOMSEL'
    elif bandoperator == '88':
         operator = 'XL'
    else:
         operator = 'Unknown'
    #print(operator)

    return operator
# def gettmsidata2():
#         f=open("/etc/saras/GUI/remote/tmsidata2.conf")
#         tmsi = f.read()
#         import re
#         words = re.split(r'[^\w]',tmsi)
#         for word in words:
#                 if word == "":
#                         words.remove(word)
#         imsi_get = []
#         imei_get = []
#         localMSISDN_get = []
#         tmsi_get = []
#         pelanggans = []
#         #print(range(len(words)))
#         #print(len(words))
#         #print(words)
#         for i in range(len(words)):
#                 if words[i] == 'ues':
#                         k=0
#                         leng=len(words)		
#                         while k<(int((leng-4)//7)):
#                                 imsi_get.append(words[(i+1)+(k*7)])
#                                 imei_get.append(words[i+3+(k*7)])
#                                 localMSISDN_get.append(words[i+4+(k*7)])
#                                 tmsi_get.append(words[i+5+(k*7)])
#                                 k = k+1
#         for j in range(len(imsi_get)):
#                 pelanggans.append(
#                         {
#                         'IMSI' : imsi_get[j],
#                         'IMEI' : imei_get[j],
#                         'MSISDN' : localMSISDN_get[j],
#                         'tmsi' : tmsi_get[j]
#                         })
#         return pelanggans

# def gettmsidata3():
#         f=open("/etc/saras/GUI/remote/tmsidata3.conf")
#         tmsi = f.read()
#         import re
#         words = re.split(r'[^\w]',tmsi)
#         for word in words:
#                 if word == "":
#                         words.remove(word)
#         imsi_get = []
#         imei_get = []
#         localMSISDN_get = []
#         tmsi_get = []
#         pelanggans = []
#         #print(range(len(words)))
#         #print(len(words))
#         #print(words)
#         for i in range(len(words)):
#                 if words[i] == 'ues':
#                         k=0
#                         leng=len(words)		
#                         while k<(int((leng-4)//7)):
#                                 imsi_get.append(words[(i+1)+(k*7)])
#                                 imei_get.append(words[i+3+(k*7)])
#                                 localMSISDN_get.append(words[i+4+(k*7)])
#                                 tmsi_get.append(words[i+5+(k*7)])
#                                 k = k+1
#         for j in range(len(imsi_get)):
#                 pelanggans.append(
#                         {
#                         'IMSI' : imsi_get[j],
#                         'IMEI' : imei_get[j],
#                         'MSISDN' : localMSISDN_get[j],
#                         'tmsi' : tmsi_get[j]
#                         })
#         return pelanggans

def getoperator1(pc):
    import re
    if (pc==1):
        file="ybts1.conf"
    elif (pc==2):
        file="ybts2.conf"
    elif (pc==3):
        file="ybts3.conf"      
    f=open("/etc/saras/GUI/remote/"+file)
    ybts = f.read()

    words = re.split(r'[^\w]',ybts)
    for word in words:
         if word == "":
             words.remove(word)
    #print(words)
    bandoperator = words[83]
    if bandoperator == '0':
         operator = 'INDOSAT'
    elif bandoperator == '50':
         operator = 'TELKOMSEL'
    elif bandoperator == '88':
         operator = 'XL'
    else:
         operator = 'Unknown'
    #print(operator)

    return operator

# def getoperator2():
#     import re
        
#     f=open("/etc/saras/GUI/remote/ybts2.conf")
#     ybts = f.read()

#     words = re.split(r'[^\w]',ybts)
#     for word in words:
#          if word == "":
#              words.remove(word)
#     #print(words)
#     bandoperator = words[83]
#     if bandoperator == '0':
#          operator = 'INDOSAT'
#     elif bandoperator == '50':
#          operator = 'TELKOMSEL'
#     elif bandoperator == '88':
#          operator = 'XL'
#     else:
#          operator = 'Unknown'
#     #print(operator)

#     return operator

# def getoperator3():
#     import re
        
#     f=open("/etc/saras/GUI/remote/ybts3.conf")
#     ybts = f.read()

#     words = re.split(r'[^\w]',ybts)
#     for word in words:
#          if word == "":
#              words.remove(word)
#     #print(words)
#     bandoperator = words[83]
#     if bandoperator == '0':
#          operator = 'INDOSAT'
#     elif bandoperator == '50':
#          operator = 'TELKOMSEL'
#     elif bandoperator == '88':
#          operator = 'XL'
#     else:
#          operator = 'Unknown'
#     #print(operator)

#     return operator
