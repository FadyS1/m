# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import socket
import threading
lock = threading.Lock()
lock2 = threading.Lock()
lock3 = threading.Lock()


# video_time_serv1 = 0
# video_time_serv2 = 0
# video_time_serv3 = 0
#
# picture_time_serv1 = 0
# picture_time_serv2 = 0
# picture_time_serv3 = 0
#
# music_time_serv1 = 0
# music_time_serv2 = 0
# music_time_serv3 = 0

aomes_serv1 = 0
aomes_serv2 = 0
aomes_serv3 = 0


def serveClient(client, address, serv1, serv2, serv3):
    data = client.recv(2)
    data_str = data.decode('ascii')
    request_kind = data_str[0]
    duration = ord(data_str[1]) - ord('0')
    #chosen server number
    chosen = 0
    global aomes_serv1, aomes_serv2, aomes_serv3
    lock.acquire()
    # if request is Video.
    if request_kind == 'V':
        if aomes_serv3 - ((aomes_serv1 + aomes_serv2)/2) < -30:
            chosen = 3
            aomes_serv3 += 3 * duration
        elif aomes_serv1 <= aomes_serv2:
            chosen = 1
            aomes_serv1 += duration
        else:
            chosen = 2
            aomes_serv2 += duration

    # if request is Music.
    if request_kind == 'M':
        if aomes_serv1 - aomes_serv3 < -15 or aomes_serv2 - aomes_serv3 < -15:
            if aomes_serv1 <= aomes_serv2:
                chosen = 1
                aomes_serv1 += 2 * duration
            else:
                chosen = 2
                aomes_serv2 += 2 * duration
        else:
            chosen = 3
            aomes_serv3 += duration

    # if request is Picture.
    if request_kind == 'P':
        if aomes_serv3 - aomes_serv1 < -20 or aomes_serv3 - aomes_serv1 < -20:
            chosen = 3
            aomes_serv3 += 2 * duration
        elif aomes_serv1 <= aomes_serv2:
            chosen = 1
            aomes_serv1 += duration
        else:
            chosen = 2
            aomes_serv2 += duration
    lock.release()

    if chosen == 1:
        lock2.acquire()
        serv1.sendall(data)
        lock2.release()
        response = serv1.recv(1024)
        client.sendall(response)
        client.close()
        return
    if chosen == 2:
        lock2.acquire()
        serv2.sendall(data)
        lock2.release()
        response = serv2.recv(1024)
        client.sendall(response)
        client.close()
        return
    if chosen == 3:
        lock2.acquire()
        serv3.sendall(data)
        lock2.release()
        response = serv3.recv(1024)
        client.sendall(response)
        client.close()
        return







def LB():

    # connecting to serv1
    serv1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv1.connect(("192.168.0.101", 80))
    # connecting to serv2
    serv2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv2.connect(("192.168.0.102", 80))
    # connecting to serv3
    serv3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv3.connect(("192.168.0.103", 80))


    # listening to hosts requests
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind(("10.0.0.1", 80))
    lsock.listen(20)
    while True:
        client, address = lsock.accept()
        #
        threading.Thread(target=serveClient, args=(client, address, serv1, serv2, serv3)).start()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    LB()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
