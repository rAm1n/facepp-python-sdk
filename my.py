from facepp import *
import threading
import time
from qr import *

IMAGE_PATH = '/home/ramin/'
RESULT_PATH = '/home/ramin/'

accounts = list()

def init():
	global accounts
	q = Queue('facepp')
	if not len(q):
		f = open('facepp.cfg' , 'r')
		for line in f:
			accounts.append(tuple(line.strip().split(',')))
			q.push(tuple(line.strip().split(',')))
		f.close()



def get_access_token():
	q = Queue('facepp')
	return q.rpoplpush('facepp' , 'facepp')

def request_data(media_id):
	global IMAGE_PATH,RESULT_PATH		
	FILE = File(IMAGE_PATH + media_id + '.jpg')
	token = get_access_token()
	api = API(token[0],token[1],srv=token[2])
	print api.detection.detect(img=FILE)
	print '--------------------'
	print api.detection.landmark(img=FILE)
	
	
	
	
	
	
	
