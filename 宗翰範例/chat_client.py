# !/usr/bin/python
# coding:utf-8

# chat_client.py

import sys, socket, select, time
 
def chat_client():
    if(len(sys.argv) < 3) :
        print 'Usage : python chat_client.py hostname port'
        sys.exit()

    # 輸入host, port
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2) # 若連接不上，設定嘗試重連到2秒時終止操作
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. You can start sending messages'
    print 'Now time: '+time.asctime( time.localtime(time.time()) )
    sys.stdout.write('[Me] ')
    sys.stdout.flush() # sys.stout螢幕輸出(只接收string類型)
     
    while 1:
        socket_list = [sys.stdin, s] # 輸入s到socket_list
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [], 30)
        # 當省略 timeout 參數時該函數將阻塞直到至少有一個文件描述符準備就绪。 
        # 0: 表示執行輪詢且永不阻塞。
        # 30:等待30秒
        # 若聊天室內都沒有人輸入,則印出當前時間字串
        if not read_sockets:
            print "\n[Server] No one input  "+time.asctime( time.localtime(time.time()) )
        for sock in read_sockets:            
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096) # sock.recv()返回預設值是0
                if not data : # 若server無回傳值
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()     
            
            else : # 若server沒有送資料過來, 也就是可讀socket中沒有s, 那s就可以輸入訊息
                # user entered a message
                msg = sys.stdin.readline() # sys.stdin > 鍵盤輸入
                s.send(msg)
                sys.stdout.write('[Me] '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())

