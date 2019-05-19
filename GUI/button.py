import re
        
f=open("/usr/local/etc/yate/ybts.conf")
ybts = f.read()

words = re.split(r'[^\w]',ybts)
for word in words:
     if word == "":
         words.remove(word)
print(words)

bandoperator=words[83]
print (bandoperator)
if bandoperator == '0':
     operator = 'INDOSAT'
elif bandoperator == '50':
     operator = 'TELKOMSEL'
elif bandoperator == '88':
     operator = 'XL'
else:
     operator = 'Unknown'
print(operator)
