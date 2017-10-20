import sys
import os
import cv2
def Handler(filename):
	medianame = filename.split('/');
	directoryname = medianame[len(medianame)-1].split('.')[0]
	directoryname = "/arts/www/pages/media/" + directoryname
	os.system('mkdir -p ' + directoryname)	#create media direatory of the mp4 file same name
	
	commond = "ffmpeg -i "+ filename +"  -c copy -map 0 -f segment -segment_list   "+ directoryname +"/playlist.m3u8 -segment_time 1 " + directoryname + "/stream_%03d.mp4 >/dev/null "
	os.system(commond);
	metalist = GetSlice(directoryname + "/playlist.m3u8");
	for name in metalist:
		KeyFrameExtration(directoryname + "/" + name)

def KeyFrameExtration(filename):
	vc = cv2.VideoCapture(filename) 
	rval,frame = vc.read()
	picname = filename.split('.')[0] + ".jpg"; 
	cv2.imwrite(picname, frame)
	vc.release()
def GetSlice(m3u8file):
	metalist = []
	fp = open(m3u8file,"r");
	while True:
		line = fp.readline();
		if not line:
			break;
		if 'EXTINF' in line:
			line = fp.readline();
			metalist.append(line[0:len(line)-1]);
	return metalist;
		
if __name__ == "__main__":
	filename = sys.argv[1];
	Handler(filename)
