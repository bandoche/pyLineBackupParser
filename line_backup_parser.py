from datetime import datetime
# import time
import sys
import csv
from copy import copy
#import shlex
import re
if len(sys.argv) > 1:
	filename = sys.argv[1]
	print "filename = ",filename
else:
	filename = 'line.log'

f = open(filename)


csvname = 'line.csv'
fc = open(csvname, 'wb')
cw = csv.writer(fc)

# skip 3 lines
# chats = f.read(1000)
# sh = shlex.shlex(chats)
# ss = shlex.split(chats)
# for item in ss:
# 	print item
# quit()

chats = f.readlines()[3:]
f.close()

# d = datetime.combine(datetime.strptime(chats[0][:12], '%Y. %m. %d'), datetime(0,0,0))
d = datetime.strptime(chats[0][:12], '%Y. %m. %d')
# dt = copy(d)
idx = 0
while(True):
	line = chats[idx]
	chat = line.split("\t")

	l = len(chat)
	if l == 1:
		# 1 tab makes date
		if line != "\n":
			d = datetime.strptime(line[:12], '%Y. %m. %d')
			print d
	elif l == 2:
		# 2 tab makes system command - blah blah blah
		print "SYSTEM: (%s) %s" % (datetime.strptime(chat[0], '%H:%M'), chat[1][:12])
	elif l >= 3:
		# 3 tab makes normal msg
		t = datetime.strptime(chat[0], '%H:%M')
		if chat[2][0] == "\"":
			# long msg start - not sure. if it just double quote in chat... welcome to hell.
			if re.match(r"\d\d:\d\d\t", chats[idx+1][:6]) != None:
				#  lets skip
				msg = chat[2][:-1]
			else:
				j = 1
				allmsg = chat[2]
				flag = True
				while(flag):
					allmsg += chats[idx + j]
					allmsgsp = allmsg.replace("\"\"", "_")
					# print "%d(%s): %s" % (j, allmsgsp[-2], chats[idx + j])
					if allmsgsp[-2] == "\"":
						flag = False
						msg = allmsg[1:-2].replace("\"\"", "\"")
					else:
						j += 1
						# print j
				idx += j
				# print idx

		else:
			msg = chat[2][:-1]


		# j = 0
		# flag = True
		# while(flag):
		# 	try:
		# 		t = datetime.strptime(chats[idx + j][:5], '%H:%M')
		# 		# print "new line"
		# 		flag = False
		# 		pass
		# 	except Exception, e:
		# 		print "idx j = %d, %d" % (idx, j)
		# 		print "err1 - %s" % chats[idx + j] #[:5]
		# 		j += 1
		# 		# flag = True
		# 		pass
		# 	else:
		# 		pass
		# 	finally:
		# 		pass
		# msg = chat[2][:-1]
		# if j > 0:
		# 	for i in range(j):
		# 		msg += "\n" + chats[idx + i][:-1]
		# 	idx += j
		print "%s: %s" % (chat[1], msg)
		# if j > 0:
		# 	msg = chat[2]
		# 	for i in range(j - 1)

		# else:
		# 	msg = chat[2]
		cw.writerow([datetime.combine(d.date(), t.time()), chat[1], msg])
	idx += 1

		
