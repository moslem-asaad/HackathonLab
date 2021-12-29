from os import times
import socket
import threading
import time
import EquationHandler


class ConnectinHandler:

    def __init__(self, soket, game, name):
        self.connection_socket = soket
        self.game = game
        self.team_name = name

    def start_the_game(self):
        self.connection_socket.settimeout(10)
        terminate_time = time.time() + 10
        try:

            msg = "Welcome to Quick Maths.\n"
            msg = msg + "Player 1: " + self.game.client1_name + "\n"
            msg = msg + "Player 2: " + self.game.client2_name + "\n"
            msg = msg + "==\nPlease answer the following question as fast as you can:\n"
            equation = EquationHandler.generate_equation()
            msg = msg + "How much is " + EquationHandler.equation_to_str(equation) + "?"
            result = EquationHandler.equation_result(equation)
            self.game.game_result = result
            self.connection_socket.sendall(str(msg).encode())
        except socket.error as error:
            print(str(error))
            self.connection_socket.close()
            return
        while terminate_time > time.time():
            if (terminate_time - time.time() < 0):
                self.connection_socket.settimeout(0)
            else:
                self.connection_socket.settimeout(terminate_time - time.time())
            data = self.connection_socket.recv(1024).decode()
            if not data: break
            if (threading.current_thread is self.game.client1_thread):
                if data is result:
                    self.game.client1_res = True
                else:
                    self.game.client2_res = False
            else:
                if data is result:
                    self.game.client1_res = True
                else:
                    self.game.client2_res = False
        final_message = self.game.final_message()
        try:
            self.connection_socket.sendall(final_message.encode())
        except socket.error as error:
            print(str(error))
        self.connection_socket.close()
        return


