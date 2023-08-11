import socket, time
from Game import *
from Interface import *
from Client import *

class Server():
    def __init__(self):
        host = "127.0.0.1"
        port = 666

        self.clients = {}

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)

        self.team_1_characters = []
        self.team_2_characters = []

        self.team_1_character_hps = []
        self.team_2_character_hps = []

        self.team_1_character_powers = []
        self.team_2_character_powers = []

        self.team_1_character_roles = []
        self.team_2_character_roles = []

        self.remaining_time = 9
        self.stage = 1

        self.wait_for_players()

    def wait_for_players(self):
        while True:
            connection, address = self.server_socket.accept()
            print(f"Bağlantı kuruldu: {address}")

            self.clients[address] = connection
            

            message_to_client = "Welcome to game!"
            connection.send(message_to_client.encode())

            if len(self.clients) == 2:
                connection.send("2".encode())
                time.sleep(0.01)
                for connection in self.clients.values():
                    connection.sendall("Game starting".encode())
                break
            
            connection.send("1".encode())

        self.first_client = list(self.clients.values())[0]
        self.second_client = list(self.clients.values())[1]

        self.game_start()
        
    def game_start(self):
        self.game_database = Game()

        self.team_1_characters, self.team_1_character_hps, self.team_1_character_powers, self.team_1_character_roles = self.game_database.game_start()
        self.team_2_characters, self.team_2_character_hps, self.team_2_character_powers, self.team_2_character_roles = self.game_database.game_start()
        
        
        # Send to first client
        self.send_data_to_client(self.first_client, self.team_1_characters)
        self.send_data_to_client(self.first_client, self.team_1_character_hps)
        self.send_data_to_client(self.first_client, self.team_1_character_powers)
        self.send_data_to_client(self.first_client, self.team_1_character_roles)

        self.send_data_to_client(self.first_client, self.team_2_characters)
        self.send_data_to_client(self.first_client, self.team_2_character_hps)
        self.send_data_to_client(self.first_client, self.team_2_character_powers)
        self.send_data_to_client(self.first_client, self.team_2_character_roles)

        # Send to second client
        self.send_data_to_client(self.second_client, self.team_2_characters)
        self.send_data_to_client(self.second_client, self.team_2_character_hps)
        self.send_data_to_client(self.second_client, self.team_2_character_powers)
        self.send_data_to_client(self.second_client, self.team_2_character_roles)

        self.send_data_to_client(self.second_client, self.team_1_characters)
        self.send_data_to_client(self.second_client, self.team_1_character_hps)
        self.send_data_to_client(self.second_client, self.team_1_character_powers)
        self.send_data_to_client(self.second_client, self.team_1_character_roles)
    
        self.game()
    
    def send_data_to_client(self, client, list):
        for i in list:
            client.send(str(i).encode())
            time.sleep(.01)
    
    def game(self):
        self.fp_hps = self.team_1_character_hps
        self.fp_powers = self.team_1_character_powers

        self.sp_hps = self.team_2_character_hps
        self.sp_powers = self.team_2_character_powers
        
        # Stage - 1

        for i in range(5):
            self.stage_command()
        
    def stage_command(self):
        #random_player = random.randint(1, 2)
        #self.fp = self.first_client if random_player == 1 else self.second_client
        #self.sp = self.first_client if random_player == 2 else self.second_client
        
        self.first_client.sendall("You turn!".encode())
        self.second_client.sendall("Opponent's turn!".encode())

        self.fp = self.first_client
        self.sp = self.second_client

        # Player_1 play
        self.fp.recv(1024).decode()
        number_1 = self.game_database.roll_the_dice()
        self.fp.sendall(str(number_1).encode())
        self.sp.sendall(str(number_1).encode())

        # Player_2 play
        self.sp.recv(1024).decode()
        number_2 = self.game_database.roll_the_dice()
        self.fp.sendall(str(number_2).encode())
        self.sp.sendall(str(number_2).encode())
        time.sleep(3)
        
        if number_1 > number_2:
            self.fp.sendall("Win".encode())
            self.sp.sendall("Lose".encode())
            self.fp.sendall(str(self.sp_hps[self.stage - 1] - self.fp_powers[self.stage - 1]).encode())
            self.sp.sendall(str(self.sp_hps[self.stage - 1] - self.fp_powers[self.stage - 1]).encode())
            self.sp_hps[self.stage - 1] -= self.fp_powers[self.stage - 1]
        if number_1 == number_2:
            self.fp.sendall("Draw".encode())
            self.sp.sendall("Draw".encode())
            self.fp.sendall(str(self.fp_hps[self.stage - 1] - 10).encode())
            self.fp.sendall(str(self.sp_hps[self.stage - 1] - 10).encode())
            self.sp.sendall(str(self.sp_hps[self.stage - 1] - 10).encode())
            self.sp.sendall(str(self.fp_hps[self.stage - 1] - 10).encode())
            self.fp_hps[self.stage - 1] -= 10
            self.sp_hps[self.stage - 1] -= 10


        if number_1 < number_2:
            self.fp.sendall("Lose".encode())
            self.sp.sendall("Win".encode())
            self.fp.sendall(str(self.fp_hps[self.stage - 1] - self.sp_powers[self.stage - 1]).encode())
            self.sp.sendall(str(self.fp_hps[self.stage - 1] - self.sp_powers[self.stage - 1]).encode())
            self.fp_hps[self.stage - 1] -= self.sp_powers[self.stage - 1]
        self.stage += 1

        time.sleep(10)

run = Server()