
import paho.mqtt.client as paho
import ssl
global buffer
buffer = bytearray(16)
scalev=409.6
scaleg=2367.13
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
#def on_message(client, userdata, msg):
   # print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))  
def on_connect(client, userdata, flags, rc):
    print('CONNACK received with code %d.' % (rc))
def on_message(client, userdata, message):
    payload = message.payload
    buffer = payload
#   print(buffer) 
    int_sensor_id = buffer[2:3] 
#   print(int_sensor_id)  
    # Data in velocity
    int_velx = buffer[5:7]    #D6 & D7 
#   print(int_velx) 
    int_vely = buffer[7:9]
#   print(int_vely)
    int_velz = buffer[9:11]  
#   print(int_velz) 
    
# Convert the extracted bytes to an integer in velocity
    sensorid_int = int.from_bytes(int_sensor_id, byteorder='big',signed=False)
    print(sensorid_int)  

# Convert the extracted bytes to an integer
    velxconvert_int = int.from_bytes(int_velx, byteorder='big',signed=False)
    print(velxconvert_int/scalev) 

# Convert the extracted bytes to an integer
    velyconvert_int = int.from_bytes(int_vely, byteorder='big',signed=False)
    print(velyconvert_int/scalev)  

# Convert the extracted bytes to an integer
    velzconvert_int = int.from_bytes(int_velz, byteorder='big',signed=False)
    print(velzconvert_int/scalev) 
    
#-----Acceleration-----------------------------

# Data in Acceleration
    int_accx = buffer[11:13] 
#   print(int_accx)  

    int_accy = buffer[13:15]
#   print(int_accy) 

    int_accz = buffer[15:17]  
#   print(int_accz) 

# Convert the extracted bytes to an integer
    accxconvert_int = int.from_bytes(int_accx, byteorder='big',signed=False)
    print(accxconvert_int/scaleg)  

# Convert the extracted bytes to an integer
    accyconvert_int = int.from_bytes(int_accy, byteorder='big',signed=False)
    print(accyconvert_int/scaleg)  

# Convert the extracted bytes to an integer
    acczconvert_int = int.from_bytes(int_accz, byteorder='big',signed=False)
    print(acczconvert_int/scaleg) 

client = paho.Client(paho.CallbackAPIVersion.VERSION1, "123")
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv311)
client.tls_set(certfile=None,keyfile=None,cert_reqs=ssl.CERT_REQUIRED)
client.username_pw_set("test", "12345")
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("3f4b987c21d74a5a87e6bdc7411d5651.s1.eu.hivemq.cloud", 8883)
client.subscribe('#', qos=0)
client.loop_forever()
