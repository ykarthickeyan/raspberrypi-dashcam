import time
import os
import json
import picamera

MAX_FILES = 120
videos_folder = "/home/pi/videos/"

def start_action():
    global MAX_FILES
    file_number = 0
    create_video_folder()
    while(file_number <=MAX_FILES):
        file_path = "video%05d.h264" % file_number
        file_number = file_number + 1
        roll_camera(file_path)
        if file_number == MAX_FILES:
            file_number = 0


def roll_camera(file_name):
    with picamera.PiCamera() as camera:
        # print(f'Starting to record {time.ctime()}, with file name {file_name}')
        camera.resolution = '720p'
        camera.framerate = 30
        camera.rotation = 270
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = time.ctime()
        camera.start_recording(videos_folder+file_name)
        time.sleep(60)
        camera.stop_recording()


def create_video_folder():
    if not os.path.exists(videos_folder):
	    os.makedirs(videos_folder)
	    print ('Created videos folder.')


def write_last_stored_file(file_number):
    last_file = {}
    last_file['file'] = file_number
    with open('last_stored.json', 'w') as f:
        json.dump(last_file, f)


def get_last_stored_file_number():
    last_log = 0
    if os.path.isfile('last_stored.json'):
        with open('last_stored.json', 'r') as f:
            last_json_log = json.load(f)
            last_log = last_json_log.get('file')
    return last_log


def check_if_video_file_exists(file_number):
    file_name = "video%05d.h264" % file_number
    return os.path.isfile(file_name)    



start_action()