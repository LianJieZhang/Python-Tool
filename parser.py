# coding=utf-8
import time
import MySQLdb as mysql
import sys

def getMem(filename):
	db = mysql.connect(user="root",passwd="199211",db="memory",host="localhost")
	db.autocommit(True)
	cur = db.cursor()
	
	alltotal = 0;
	alllost = 0;
	videotemp = 0;
	typelist = [];
	membertotal = {};
	memberseq = {};
	memberlost = {};
		
	file_object = open(filename,"rb");                                                                                                                              
	for line in file_object:
	#stats all type
		seqtype = int( (line.split('-')[8][:-1]) )
		if (seqtype != 0):
			typelist.append(seqtype)
			typelist = list(set(typelist)); #去掉重复的

#member stats
#统计各个ssrc的总数
		if (not(membertotal.has_key(seqtype))):
			membertotal[seqtype] = 0;
		membertotal[seqtype] += 1;
#将seq 放入字典
		if (not(memberseq.has_key(seqtype))):	
			memberseq[seqtype] = [];
		seq = int(line.split('-')[2])
		memberseq[seqtype].append(seq)
		alltotal += 1;
#seq排序并判断丢包
	for key in memberseq:
		memberseq[key].sort();
		videotemp = 0;
		for seq in memberseq[key]:
			if (not(memberlost.has_key(key))):
				memberlost[key] = 0;
			if (videotemp == 0):
				videotemp = seq;
			if ((seq - videotemp) > 1):
				print("--",key,seq)
				memberlost[key] += (seq - videotemp) -1;
			videotemp = seq;

	print("all type:",typelist)
	for ssrc in typelist:
		alllost += memberlost[ssrc];
		print("ssrc:%d	packettotal:%d	packetloss:%d	 packetlossrate:%f%%" %(ssrc ,(membertotal[ssrc]) ,(memberlost[ssrc]) ,((memberlost[ssrc] / float(membertotal[ssrc])) * 100) ))
	print("lost number:%d,total:%d, total lost rate:%f%%" %(alllost, alltotal,(float(alllost) / alltotal) * 100))
		
	
	#return videolist,audiolist		

		#seq = int(line.split('-')[1]);
		#t = int(line.split('-')[5]);
		#sql = 'insert into webrtc (seq,time) value (%s,%s)'%(seq,t)
		#cur.execute(sql)
getMem(sys.argv[1])
