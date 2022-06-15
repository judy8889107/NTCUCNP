# !/usr/bin/python
# coding:utf-8

# chat_server.py
 
import sys, socket, select, time

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # int setsockopt(level,optname,value)
    # SOL_SOCKET: 基本套介面(level)
    # SO_REUSEADDR: 當socket關閉後，本地端用於該socket的埠號立刻就可以被重用:1(開啟)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10) # 最大連線數
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket) # server socket加入list裡面
 
    print "Chat server started on port " + str(PORT)
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block 輪詢且不會block程式
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        # 可讀 可寫 例外錯誤
        # select.select(輸入, 輸出, 例外錯誤, 超時秒數(可選))若無設定超時秒數則會進入block
        # 這裡設為0, 所以不會block
      
        for sock in ready_to_read:# 讀取ready_to_read的sock
            # a new connection request recieved
            # server socket被連, 狀態可讀，則印出Client
            if sock == server_socket:  # 若為server socket則像tcp一樣先accept
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd) # List加入client
                print "Client (%s, %s) connected" % addr # addr有IP跟port, 所以是兩個字串
                # 廣播訊息(自定義函數)
                # 廣播給不是server_socket和sockfd的socket
                broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr) # 廣播訊息
             
            # a message from a client, not a new connection
            # 若可讀的sokcet不是server_socket 而是client socket
            else:
                 # 處理client傳送過來的資料 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER) # Python2回傳string
                    if data: # 判斷 data!=""
                        # there is something in the socket
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                        # sock.getpeername()返回數組(ipaddr,port) 
                    else: # 若client送來的資料為空
                        # 則將client從list中移除 
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        # 顯示誰已退出聊天室
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception (例外)
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close() # 迴圈外
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # 傳送給除了server和進來的user aaa以外的socket訊息(aaa entered our chatting room)
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 # main執行區塊
if __name__ == "__main__":

    sys.exit(chat_server())


         
