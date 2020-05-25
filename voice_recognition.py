import wave                        #音频文件处理
import urllib.request, pycurl
#import base64  
import json
# get access token by api key & secret key  
import time
import re

def get_token():  
    apiKey = "oZncYte95yCKRlQ8LIwW4lV3"            #这两行是登录用的密码
    secretKey = "xwpDXHke8fh4v3F00RfQstguqAn1osgg"  
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey  
    res = urllib.request.urlopen(auth_url)  
    json_data = res.read() 
    json_data = str(json_data,encoding = 'utf-8')
    return json.loads(json_data)['access_token']

def dump_res(buf):
    global cmd
    buf = str(buf, encoding = 'utf-8')
    buf = eval(buf)
    cmd = buf["result"][0]
    #print(cmd)  
    #print(type(buf["result"]))
  
## post audio to server  
def use_cloud(token,filename):  
    #  fp = wave.open('test.pcm', 'rb')  

    fp = wave.open(filename, 'rb') 
    #  fp = wave.open('vad_1.wav', 'rb')  
    nf = fp.getnframes()
    f_len = nf * 2  
    audio_data = fp.readframes(nf)
    cuid = "123456"  
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token  +'&dev_pid=1737'
    http_header = [  
        'Content-Type: audio/pcm; rate=16000',  
        #  'Content-Type: audio/pcm; rate=8000',  
        'Content-Length: %d' % f_len]
  
    c = pycurl.Curl() 
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode  
    #c.setopt(c.RETURNTRANSFER, 1)  
    c.setopt(c.HTTPHEADER, http_header)   #http头字段，must be list, not dict  
    c.setopt(c.POST, 1) 
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30) 
    c.setopt(c.WRITEFUNCTION, dump_res)     #把输出定向到dump_res
    c.setopt(c.POSTFIELDS,audio_data)     #设置发送的数据
    c.setopt(c.POSTFIELDSIZE, f_len)  
    c.perform() #pycurl.perform() has no return val
    
def recognition(filename):
    token =get_token()
    use_cloud(token,filename)
    return cmd

#cmd=recognition('D:/Spyder/dataset/TIMIT/train/dr1/fcjf0/sa1.wav')
#print(cmd)
##对所有语音进行标注
if __name__ == "__main__":
#   import index
   for i in range(2):
       data=[]
       with open('D:\\Spyder\\dataset\\TIMIT\\dr'+str(i)+'.txt','r') as f:
           for line in f.readlines():
               line=re.split('\n',line)
               line.remove('')
               data.append(line)
#       data=index.txtread('D:\\Spyder\\dataset\\TIMIT\\dr'+str(i)+'.txt')

       for j in range(len(data)):
           label=recognition(''.join(data[j]))
           f=open('D:\\Spyder\\dataset\\TIMIT\\'+str(i)+'.txt','a')
           print(label,file=f)
           f.close()
#           index.txtwrite(label,'D:\\Spyder\\dataset\\TIMIT\\'+str(k)+'.txt')
       print('alright')
       
          