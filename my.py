from facepp import *
import threading
import time
from qr import *
import os
from pymongo import *
import redis
import re
import cPickle as pickle
import logging


logging.basicConfig(filename='log',level=logging.INFO)

IMAGE_PATH = '/home/ramin/insta-crawler/insta_crawler/media/selfie/'
RESULT_PATH = os.getcwd() + '/result/'
LANDMARK_PATH = os.getcwd() + '/landmark/'

client = MongoClient()
db = client['selfie']

media_list = [  media['_id'] for media  in db.media_model.find()]

accounts = list()


def init():
	global accounts
	q = Queue('facepp')
	if not len(q):
		f = open('facepp.cfg', 'r')
		for line in f:
			q.push('(' + line.strip() + ')')
		f.close()


def get_access_token():
	r = redis.StrictRedis()
	return pickle.loads(r.rpoplpush('facepp', 'facepp'))


def request_data(media_id):
	global IMAGE_PATH, RESULT_PATH
	token = re.search('\((.*)\)', get_access_token()).group(1).split(',')
	api = API(token[0], token[1], srv=token[2])
	res = api.detection.detect(img=File(IMAGE_PATH + media_id + '.jpg'))
	if res:
		faces = list()
		for face in res['face']:
			faces.append(api.detection.landmark(img=File(IMAGE_PATH + media_id + '.jpg'), face_id=face['face_id']))
		pickle.dump(res , open(RESULT_PATH + media_id , 'w'))
		pickle.dump(faces , open(LANDMARK_PATH + media_id , 'w'))
		logging.info(media_id + ',stored.')
	logging.info(media_id + ',failed.')



init()
th_list = list()
counter = 0
for media in media_list:
	try:
		counter+=1
		if counter<40:
			continue
		if len(th_list) == 8:
			for th in th_list:
				th.join()
			th_list = list()
		th = threading.Thread(target=request_data , args=[media])
		th.start()
		if counter %20 == 0:
			time.sleep(1)
		print counter
	except APIError,x:
		f = open('error' , 'a')
		f.write(media,x.code)
		
	





