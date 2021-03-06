import os
import requests
import glob
import time
import json

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True

def callback_function(response):
    if response.code == 200:
        print("Server Side received")
    elif response.code == 400:
        print("Bad Request rejected by Remote Server (probably from Bad Formatting)")
    else:
        print("Server not responding to Message")
        #os.system(reboot)
        #print "reboot pi"

def sendData(data,url,fname):
    try:
        key = {'data': data}
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}

        print('Sending {}'.format(data))

        r = requests.post(url, data=key, headers=headers)
        if r.status_code == 200:
            print("Server Side received")
            os.remove(fname)
            print("Remove " + fname)
        elif r.status_code == 400:
            print("Bad Request rejected by Remote Server (probably from Bad Formatting)")
        else:
            print("Server not responding to Message")

    #except requests.ConnectionError:
    except:
        print("Error Response code" + r.status_code)
        time.sleep(60)

#while True:
#Run to sync file
try:
    files_to_send = glob.glob("/srv/bt_monitor/save/*.log")
    #print(files_to_send)
    if(len(files_to_send) != 0):
        for fname in files_to_send:
            print(fname)
            current_file = open(fname, 'r')
            data = current_file.read()
            if len(data) != 0:
                if is_json(data):
                    sendData(data,'http://api.blusense.co/Bluetooth.php',fname)
                else:
                    print("Json file corrupting")
                    os.rename(fname, fname + '.err')
            else:
                print("No data to sent")
                os.remove(fname)
	        current_file.close()

    sys.exit(0)

except:
    print("Found Error")
    #time.sleep(60)
    sys.exit(1)
finally:
    print("Finish loop")