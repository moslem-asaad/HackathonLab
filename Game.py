from _typeshed import Self
import threading


class Game:

    def __init__(self):
        self.client1_name = None
        self.client1_thread = None
        self.client2_name = None
        self.client2_thread = None
        self.client1_res = False
        self.client2_res = False
        self.game_result = -1  
        


    def assign_client_name(self,team_name,number):
        if number == 1:
            self.client1_name = team_name
        else:
            self.client2_name = team_name    

    def assign_clien_thread(self,thread,number):
        if number == 1:
            self.client1_name = thread
        else:
            self.client2_name = thread    

     

    def start_clients_threads(self):
        self.client1_thread.start()
        self.client2_thread.start()

    def join_clients_threads(self):
        self.client1_thread.join()
        self.client2_thread.join()

    def final_message(self):
        msg = "Game over!\nThe correct answer was " + str(self.game_result) + "!\n\n"
        if self.client1_res == False and self.client2_res == False:
            return msg + " the game finished with draw\n"
        elif self.client1_res == True:
            return msg + "Congratulations to the winner: " + self.client1_name
        else:
            return msg + "Congratulations to the winner: " + self.client2_name

        