##Python codes to do server-side part of chat room.
import _thread
import socket
import threading
import sys
"""AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The 2nd context of the code is the type of socket. """
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# piece of code to allow IP address & Port

# 預設host為127.0.0.1(方便測試)
host = "127.0.0.1"
# 若有輸入參數則為預設參數
if len(sys.argv)==2:
    host = sys.argv[1]
port=5000
s.bind((host,port))
s.listen(5)
clients=[]
#code to allow users to send messages

def connectNewClient(c):

     while True:
        global clients
        msg = c.recv(2048) # server收到訊息
        if len(msg) != 0: # 若長度不為0則傳送出去給其他User
            msg ='User('+str(clients.index(c)+1)+'):'+msg.decode('UTF-8')
            sendToAll(msg,c)

        else: # 若收到訊息為空則移除User
            print('server closed connection.')
            clients.remove(c)

def sendToAll(msg,con):
    for client in clients:
        client.send(msg.encode('UTF-8')) 
        

while True:
    c,ad=s.accept()
    # Display message when user connects
    print('*Server Connected ')
    print (host) # 測試用
    clients.append(c)
    c.send(('User('+str(clients.index(c)+1)+')').encode('UTF-8'))
    _thread.start_new_thread(connectNewClient,(c,))

c.close()
s.close()