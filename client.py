import socket
import Message_UDP
import threading
import msvcrt
import time

TeamName = "Leaders\n"
Buffer_Size = 1024


def start_client(port):
    print("Client started, listening for offer requests...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind(('', port))
    while True:
        data, address = client_socket.recvfrom(Buffer_Size)
        server_port = Message_UDP.unpack_message(data)
        if server_port == None: continue
        host_ip = address[0]
        print("Received offer from " + str(host_ip) + ",attempting to connect...")
        connect_client(host_ip, server_port)
        # clear previuos invites
        clear_invites(client_socket)
        print("Server disconnected, listening for offer requests...")


def clear_invites(client_socket):
    client_socket.setblocking(False)
    while True:
        try:
            client_socket.recv(Buffer_Size)
        except socket.error:
            client_socket.setblocking(True)
            return


def connect_client(host_ip, server_port):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(10)
    try:
        tcp_socket.connect((host_ip, server_port))
    except socket.error as error:
        print("Fail in connecting to server: " + str(error))
        return

    try:
        tcp_socket.sendall(TeamName.encode())
    except socket.error as error:
        print("error occured while sending team names: " + str(error))
        tcp_socket.close()
        return
    tcp_socket.settimeout(10)
    client_game(tcp_socket)


def client_game(tcp_socket):
    terminate_keyboard_handler = threading.Event()
    keyboard_thread = threading.Thread(target=client_pressing, args=(tcp_socket, terminate_keyboard_handler))
    try:
        server_message = tcp_socket.recv(Buffer_Size).decode()
        print(server_message)
        # we should clear the buffer
        while msvcrt.kbhit():
            msvcrt.getch().decode('utf-8')
        keyboard_thread.start()
        while True:
            server_final_message = tcp_socket.recv(Buffer_Size).decode()
            if not server_final_message:
                break
            print(server_final_message)
        terminate_keyboard_handler.set()
        tcp_socket.close()
    except socket.error as error:
        print("an error occured in the game: " + str(error))
        terminate_keyboard_handler.set()
        tcp_socket.close()
        return


def client_pressing(client_socket, terminate_keyboard_handler):
    while not terminate_keyboard_handler:
        time.sleep(1)
        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8')
            try:
                client_socket.sendall(str(char).encode)
            except socket.error as error:
                print("error occured while sending the chars :" + str(error))


if __name__ == '__main__':
    start_client(13117)







