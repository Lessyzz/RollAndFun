import socket, threading, time
from Interface import *

class Client():
    def __init__(self):
        host = "127.0.0.1"
        port = 666
        self.client_id = 0

        self.ally_team_champions = []
        self.ally_team_hps = []
        self.ally_team_powers = []
        self.ally_team_roles = []

        self.enemy_team_champions = []
        self.enemy_team_hps = []
        self.enemy_team_powers = []
        self.enemy_team_roles = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((host, port))
        self.run()

    def run(self):
        while True:
            print(self.server_socket.recv(1024).decode()) # Welcome message
            self.client_id = self.server_socket.recv(1024).decode()
            if self.server_socket.recv(1024).decode() == "Game starting":
                print("Oyun başlıyor")
                break
        self.get_data()
    
    def get_data(self):

        # Ally team data
        for _ in range(5): self.ally_team_champions.append(self.server_socket.recv(1024).decode())        
        for _ in range(5): self.ally_team_hps.append(int(self.server_socket.recv(1024).decode()))
        for _ in range(5): self.ally_team_powers.append(int(self.server_socket.recv(1024).decode()))
        for _ in range(5): self.ally_team_roles.append(self.server_socket.recv(1024).decode())

        # Enemy team data
        for _ in range(5): self.enemy_team_champions.append(self.server_socket.recv(1024).decode())        
        for _ in range(5): self.enemy_team_hps.append(int(self.server_socket.recv(1024).decode()))
        for _ in range(5): self.enemy_team_powers.append(int(self.server_socket.recv(1024).decode()))
        for _ in range(5): self.enemy_team_roles.append(self.server_socket.recv(1024).decode())

        self.interface = GameInterface(self.ally_team_champions, self.ally_team_hps, self.ally_team_powers, self.ally_team_roles, self.enemy_team_champions, self.enemy_team_hps, self.enemy_team_powers, self.enemy_team_roles)
        threading.Thread(target = self.interface.game_start).start()
        self.handle_commands()
        
    def handle_commands(self):

        # Stage - 1

        for i in range(5):
            self.stage_command()
        
    def stage_command(self):
        self.turn = self.server_socket.recv(1024).decode()
        if "You turn!" in self.turn:

            self.interface.display_dice_button()
            while self.interface.rolled == False:
                pass
            self.server_socket.sendall("\nrolled".encode())
            number_1 = self.server_socket.recv(1024).decode()
            self.interface.ally_before_rolling_dice()
            time.sleep(2.5)
            threading.Thread(target = self.interface.display_dice_number_ally, args = (number_1, )).start()

            # Enemy play
            number_2 = self.server_socket.recv(1024).decode()
            self.interface.enemy_before_rolling_dice()
            time.sleep(2.5)
            threading.Thread(target = self.interface.display_dice_number_enemy, args = (number_2, )).start()


            # Result damage
            self.result = self.server_socket.recv(1024).decode()
            self.damage = self.server_socket.recv(1024).decode()
            
            if self.result.lower() == "win":
                self.interface.display_result("win")
                edit = self.interface.enemy_team_stats_list[self.interface.stage - 1]
                edit["hp"].config(text = f"Hp: {self.damage}", foreground = "#F8D7FF")

            if self.result.lower() == "draw":
                self.interface.display_result("draw")
                self.damage2 = self.server_socket.recv(1024).decode()
                edit = self.interface.ally_team_stats_list[self.interface.stage - 1]
                edit["hp"].config(text = f"Hp: {self.damage}", foreground = "#F8D7FF")
                edit = self.interface.enemy_team_stats_list[self.interface.stage - 1]
                edit["hp"].config(text = f"Hp: {self.damage2}", foreground = "#F8D7FF")

            if self.result.lower() == "lose":
                self.interface.display_result("lose")
                edit = self.interface.ally_team_stats_list[self.interface.stage - 1]
                edit["hp"].config(text = f"Hp: {self.damage}", foreground = "#F8D7FF")
                

        else:
            # Enemy play
            number_2 = self.server_socket.recv(1024).decode()
            self.interface.enemy_before_rolling_dice()
            time.sleep(2.5)
            threading.Thread(target = self.interface.display_dice_number_enemy, args = (number_2, )).start()

            self.interface.display_dice_button()
            while self.interface.rolled == False:
                pass
            self.server_socket.sendall("rolled".encode())
            number_1 = self.server_socket.recv(1024).decode()
            self.interface.ally_before_rolling_dice()
            time.sleep(2.5)
            threading.Thread(target = self.interface.display_dice_number_ally, args = (number_1, )).start()


            # Result damage
            self.result = self.server_socket.recv(1024).decode()
            self.damage = self.server_socket.recv(1024).decode()

            if self.result.lower() == "win":
                self.interface.display_result("win")
                edit = self.interface.enemy_team_stats_list[self.interface.stage - 1]
                edit["hp"].config(text = f"Hp: {self.damage}", foreground = "#F8D7FF")

            if self.result.lower() == "draw":
                self.interface.display_result("draw")
                self.damage2 = self.server_socket.recv(1024).decode()
                edit = self.interface.ally_team_stats_list[self.interface.stage - 1]
                edit["hp"].config(text = f"Hp: {self.damage}", foreground = "#F8D7FF")
                edit = self.interface.enemy_team_stats_list[self.interface.stage - 1]
                edit["hp"].config(text = f"Hp: {self.damage2}", foreground = "#F8D7FF")

            if self.result.lower() == "lose":
                self.interface.display_result("lose")
                edit = self.interface.ally_team_stats_list[self.interface.stage - 1]
                edit["hp"].config(text = f"Hp: {self.damage}", foreground = "#F8D7FF")


        self.interface.rolled = False
        self.interface.stage += 1

if __name__ == "__main__":
    run = Client()