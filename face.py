import cv2
import requests
import base64
import json
import time
import ctypes
import shutil

def face_score():
    #拍照
    cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
    ret,frame = cap.read()
    cv2.imwrite('cache.jpg',frame,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
    cap.release()
    cv2.destroyAllWindows()

    #获取access_token
    file_1=open("./api.json",encoding='utf-8')
    file_2=json.load(file_1)
    c_id=file_2["api_key"]
    c_se=file_2["secret_key"]
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+c_id+'&client_secret='+c_se
    response = requests.get(host)
    if response:
        s=response.json()

    #转换base64
    with open("./cache.jpg", 'rb') as f:
        base64_data1 = base64.b64encode(f.read())
        pic1 = base64_data1.decode()

    with open("./face.jpg", 'rb') as ff:
        base64_data2 = base64.b64encode(ff.read())
        pic2 = base64_data2.decode()

    #对比
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
    dict1={"image":pic1 , "image_type":"BASE64"}
    dict2={"image":pic2 , "image_type":"BASE64"}
    params="["+json.dumps(dict1)+","+json.dumps(dict2)+"]"
    access_token = s["access_token"]
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    ss=response.json()
    if ss["error_code"]==0:
        ans=int(ss["result"]["score"])
    elif ss["error_code"]==222202:
        ans=0
    else:
        ans=-1
    return ans;

def lock_win():#锁屏
    user32.LockWorkStation()

def if_locked():#是否进入锁屏界面
    if user32.GetForegroundWindow()==0:
        time.sleep(2)
        if user32.GetForegroundWindow()==0:
            return True
        else:
            return False
    else:
        return False

user32=ctypes.windll.LoadLibrary("user32.dll")
if_lock=False
while True:
    time.sleep(0.3)
    if if_locked()==True:
        if_lock=True
    elif if_lock==True:
        fc=face_score()
        if fc<80:
            shutil.copyfile("./cache.jpg","./error_photos/"+str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))+".jpg")
            lock_win()
        else:
            if_lock=False