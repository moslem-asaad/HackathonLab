import socket
import threading
import ConnectionHandler
import Message_UDP
import time
import Game


def initial_server_and_broadcast(server_port,broadcast_port):
    print("Server started, listening on IP address: "+ socket.gethostbyname(socket.gethostname()))
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
    udp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    udp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    message = Message_UDP.pack_message(server_port)
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind("",server_port)
    server_socket.setblocking(False)
    server_socket.listen()
    num_client = 1
    while True:
        game = Game.Game()
        while(num_client<3):
            udp_socket.sendto(message,broadcast_port)
            try:
                connection_socket,address = server_socket.accept()
                connection_socket.setblocking(True)
                num_client+=1
                team_name = get_team_name(connection_socket)
                game.assign_client_name(team_name,num_client)
                if team_name == None:
                    connection_socket.close()
                else:
                    client_handler = ConnectionHandler.ConnectinHandler(connection_socket,game,team_name)
                    client_thread = threading.Thread(target=client_handler.start_the_game)
                    game.assign_clien_thread(client_thread,num_client)
            except socket.error as error:
                print(str(error))
        time.sleep(10)
        game.start_clients_threads()
        threading.current_thread()
        game.join_clients_threads()
        print("Game over, sending out offer requests...\n")

def get_team_name(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            team_name = str(message,'utf-8')
            if team_name[len(team_name)-1]!='\n':
                print("wrong team names format\n" + team_name)
                client_socket.close()
                return None
            else:
                client_socket.setblocking(False)
                while True:
                    try:
                        client_socket.recv(1024)
                    except socket.error:
                        client_socket.setblocking(True)
                        break
                    break
        except socket.error as error:
            print(str(error))
            return None
        return team_name[:len(team_name)-1]

if __name__ == '__main__':
    initial_server_and_broadcast(3001,13117)

    
            





