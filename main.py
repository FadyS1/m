# This is a sample Python script.
import selectors
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import socket
import threading
lock = threading.Lock()

video_time_serv1 = 0
video_time_serv2 = 0
video_time_serv3 = 0

picture_time_serv1 = 0
picture_time_serv2 = 0
picture_time_serv3 = 0

music_time_serv1 = 0
music_time_serv2 = 0
music_time_serv3 = 0



def serveClient(client, address, serv1, serv2, serv3):
    data = client.recv(2)
    request_kind = chr(data[0])
    duration = chr(data[1]) - '0'
    #chosen server number
    chosen = 0
    global video_time_serv1, video_time_serv2, video_time_serv3, picture_time_serv1, picture_time_serv2, picture_time_serv3, music_time_serv1, music_time_serv2, music_time_serv3
    lock.acquire()
    # if request is Video.
    if request_kind == 'V':
        if video_time_serv1 <= video_time_serv2:
            chosen = 1
            video_time_serv1 += duration
        else:
            chosen = 2
            video_time_serv2 += duration

    # if request is Music.
    if request_kind == 'M':
        if (music_time_serv1+1) / (music_time_serv3 +1) < 0.1:
            if music_time_serv1 <= music_time_serv2:
                chosen = 1
                music_time_serv1 += 2 * duration
            else:
                chosen = 2
                music_time_serv2 += 2 * duration
        else:
            chosen = 3
            music_time_serv3 += duration

    # if request is Picture.
    if request_kind == 'P':
        if (1+picture_time_serv3) / (picture_time_serv1+1) < 0.1 and duration <=5:
            chosen = 3
            music_time_serv3 += 2 * duration
        elif picture_time_serv1 <= picture_time_serv2:
            chosen = 1
            picture_time_serv1 += duration
        else:
            chosen = 2
            picture_time_serv2 += duration
    lock.release()

    if chosen == 1:
        serv1.sendAll(data)
        response = serv1.recv(1024)
        client.sendAll(response)
        client.close()
        return
    if chosen == 2:
        serv2.sendAll(data)
        response = serv2.recv(1024)
        client.sendAll(response)
        client.close()
        return
    if chosen == 3:
        serv3.sendAll(data)
        response = serv3.recv(1024)
        client.sendAll(response)
        client.close()
        return







def LB():

    # connecting to serv1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv1:
        serv1.connect(("192.168.0.101", 80))
    # connecting to serv2
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv2:
        serv2.connect(("192.168.0.102", 80))
    # connecting to serv2
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv3:
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
