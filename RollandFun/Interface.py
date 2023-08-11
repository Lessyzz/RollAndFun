from tkinter import * 
import sys, os, threading, time
from PIL import ImageTk, Image
from Client import *


class GameInterface:
    def __init__(self, ally_team_champions, ally_team_hps, ally_team_powers, ally_team_roles, enemy_team_champions, enemy_team_hps, enemy_team_powers, enemy_team_roles):
        if getattr(sys, "frozen", False):
            path = os.path.dirname(sys.executable)
        elif __file__:
            path = os.path.dirname(__file__)

        self.character_images = {
            "Brofa" : path + "/Brofa.png",
            "Asfer" : path + "/Asfer.png",
            "Berneta" : path + "/Berneta.png",
            "Herry" : path + "/Herry.png",
            "Karre" : path + "/Karre.png",
            "Merny" : path + "/Merny.png",
            "Perr" : path + "/Perr.png",
            "Serna" : path + "/Serna.png",
            "Terra" : path + "/Terra.png",
            "Torun" : path + "/Torun.png"}
        
        self.stage_rolling_ally_coordinates = {
            1 : (52, 660),
            2 : (452, 660),
            3 : (852, 660),
            4 : (1252, 660),
            5 : (1652, 660)}
        
        self.dice_number_ally_coordinates = {
            1 : (107, 720),
            2 : (507, 720),
            3 : (907, 720),
            4 : (1307, 720),
            5 : (1707, 720)}

        self.dice_image = path + "/Dice.png"
        self.dice_rolling_image = path + "/Rolling.gif"
        self.win_gif = path + "/Win.gif"
        self.lose_gif = path + "/Lose.gif"

        
        self.ally_team_champions = ally_team_champions
        self.ally_team_hps = ally_team_hps
        self.ally_team_powers = ally_team_powers
        self.ally_team_roles = ally_team_roles

        self.ally_team_champions_list = []
        self.ally_team_stats_list = []



        self.enemy_team_champions = enemy_team_champions
        self.enemy_team_hps = enemy_team_hps
        self.enemy_team_powers = enemy_team_powers
        self.enemy_team_roles = enemy_team_roles

        self.enemy_team_champions_list = []
        self.enemy_team_stats_list = []

        self.stage = 1

        self.rolled = False

    def set_images(self, counter, label, list):
        image = Image.open(self.character_images[list[counter]])
        photo = ImageTk.PhotoImage(image)
        label.config(image = photo)
        label.image = photo

    def set_labels(self, counter, label, list, text):
        label.config(text = f"{text}{list[counter]}", font = "Courier 12")
    
    def game_start(self):
        self.root = Tk()
        self.root.title("Roll and Fun")
        self.root.config(background = "black")
        self.root.state("zoomed")

        roll_and_fun_label = Label(self.root, background = "black", foreground = "#F8D7FF", text = "Roll and Fun!", font = "Times 14")
        roll_and_fun_label.pack(), roll_and_fun_label.place(x = 920, y = 10)

        # Ally team images
        counter = 45
        for i in range(5):
            label = Label(self.root, background = "#F8D7FF")
            label.pack(), label.place(x = counter, y = 800)
            threading.Thread(target = self.set_images, args = (i, label,self.ally_team_champions, )).start()
            counter += 400

        # Enemy team images
        counter = 45
        for i in range(5):
            label = Label(self.root, background = "#F8D7FF")
            label.pack(), label.place(x = counter, y = 87)
            threading.Thread(target = self.set_images, args = (i, label, self.enemy_team_champions, )).start()
            counter += 400

        # Ally team stats
        counter = 200
        for i in range(5):

            champion_name_L = Label(self.root, background = "black", foreground = "red")
            champion_name_L.pack(), champion_name_L.place(x = counter, y = 800)

            label__ = Label(self.root, background = "black", foreground = "#F8D7FF", text = "---------", font = "Courier 15")
            label__.pack(), label__.place(x = counter, y = 820)

            champion_hp_L = Label(self.root, background = "black", foreground = "red")
            champion_hp_L.pack(), champion_hp_L.place(x = counter, y = 850)

            champion_power_L = Label(self.root, background = "black", foreground = "red")
            champion_power_L.pack(), champion_power_L.place(x = counter, y = 880)

            champion_role_L = Label(self.root, background = "black", foreground = "red")
            champion_role_L.pack(), champion_role_L.place(x = counter, y = 910)

            self.ally_team_stats_list.append({
                "name": champion_name_L,
                "hp": champion_hp_L,
                "power": champion_power_L,
                "role": champion_role_L})

            threading.Thread(target = self.set_labels, args = (i, champion_name_L, self.ally_team_champions, "", )).start()
            threading.Thread(target = self.set_labels, args = (i, champion_hp_L, self.ally_team_hps, "Hp: ")).start()
            threading.Thread(target = self.set_labels, args = (i, champion_power_L, self.ally_team_powers, "Power: ")).start()
            threading.Thread(target = self.set_labels, args = (i, champion_role_L, self.ally_team_roles, "")).start()
        
            counter += 400

        # Enemy team stats
        counter = 200
        for i in range(5):

            champion_name_L = Label(self.root, background = "black", foreground = "red")
            champion_name_L.pack(), champion_name_L.place(x = counter, y = 87)

            label__ = Label(self.root, background = "black", foreground = "#F8D7FF", text = "---------", font = "Courier 15")
            label__.pack(), label__.place(x = counter, y = 107)

            champion_hp_L = Label(self.root, background = "black", foreground = "red")
            champion_hp_L.pack(), champion_hp_L.place(x = counter, y = 137)

            champion_power_L = Label(self.root, background = "black", foreground = "red")
            champion_power_L.pack(), champion_power_L.place(x = counter, y = 167)

            champion_role_L = Label(self.root, background = "black", foreground = "red")
            champion_role_L.pack(), champion_role_L.place(x = counter, y = 197)

            self.enemy_team_stats_list.append({
                "name": champion_name_L,
                "hp": champion_hp_L,
                "power": champion_power_L,
                "role": champion_role_L})

            threading.Thread(target = self.set_labels, args = (i, champion_name_L, self.enemy_team_champions, "", )).start()
            threading.Thread(target = self.set_labels, args = (i, champion_hp_L, self.enemy_team_hps, "Hp: ")).start()
            threading.Thread(target = self.set_labels, args = (i, champion_power_L, self.enemy_team_powers, "Power: ")).start()
            threading.Thread(target = self.set_labels, args = (i, champion_role_L, self.enemy_team_roles, "")).start()
        
            counter += 400

        self.root.mainloop()

    # region Dice button and Rolling frame

    def display_dice_button(self):
        self.image = Image.open(self.dice_image)
        self.photo = ImageTk.PhotoImage(self.image)
        self.diceButton = Button(self.root, background = "#F8D7FF", image = self.photo, borderwidth = 0, highlightthickness = 0, command = self.dice_rolled)
        self.diceButton.pack(), self.diceButton.place(x = 850, y = 450)

    def dice_rolled(self):
        self.rolled = True
        self.diceButton.destroy()

    def ally_before_rolling_dice(self):
        self.canvas = Canvas(self.root, width = 130, height = 120, background = "black", highlightthickness = 0)
        self.canvas.pack(), self.canvas.place(x = self.stage_rolling_ally_coordinates[self.stage][0], y = self.stage_rolling_ally_coordinates[self.stage][1])
        self.gif = Image.open(self.dice_rolling_image)
        self.gif_frames = [ImageTk.PhotoImage(frame) for frame in self.get_frames()]
        self.current_frame = 0
        self.repeat_index = 0
        threading.Thread(target = self.rolling_dice).start()

    def enemy_before_rolling_dice(self):
        self.canvas = Canvas(self.root, width = 130, height = 120, background = "black", highlightthickness = 0)
        self.canvas.pack(), self.canvas.place(x = self.stage_rolling_ally_coordinates[self.stage][0], y = self.stage_rolling_ally_coordinates[self.stage][1] - 360)
        self.gif = Image.open(self.dice_rolling_image)
        self.gif_frames = [ImageTk.PhotoImage(frame) for frame in self.get_frames()]
        self.current_frame = 0
        self.repeat_index = 0
        threading.Thread(target = self.rolling_dice).start()

    def rolling_dice(self):
        if self.repeat_index < 3:
            if self.current_frame < len(self.gif_frames):
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, anchor = NW, image = self.gif_frames[self.current_frame])
                self.current_frame += 1
                self.root.after(100, self.rolling_dice)
            else:
                self.current_frame = 0
                self.repeat_index += 1
                self.rolling_dice()
        else:
            self.canvas.destroy()

    def get_frames(self):
        frames = []
        try:
            while True:
                frames.append(self.gif.copy())
                self.gif.seek(len(frames))
        except EOFError:
            pass
        return frames

# endregion

    def display_dice_number_ally(self, number):
        label = Label(self.root, foreground = "#F8D7FF", background = "black", text = number, font = "Courier 20")
        label.pack(), label.place(x = self.dice_number_ally_coordinates[self.stage][0], y = self.dice_number_ally_coordinates[self.stage][1])
    
    def display_dice_number_enemy(self, number):
        label = Label(self.root, foreground = "#F8D7FF", background = "black", text = number, font = "Courier 20")
        label.pack(), label.place(x = self.dice_number_ally_coordinates[self.stage][0], y = self.dice_number_ally_coordinates[self.stage][1] - 410)
    
    def canvas_create_animation(self):
        w = 100
        h = 75
        while w != 1200:
            self.canvas.config(width = w, height = h)
            time.sleep(0.02)
            w += 50
            h += 35

    def canvas_destroy_animation(self):
        w = 1200
        h = 845
        while w != 100:
            self.canvas.config(width = w, height = h)
            self.root.update()
            time.sleep(0.02)
            w -= 50
            h -= 35
        self.canvas.destroy()

    def display_result(self, result):
        self.canvas = Canvas(self.root, width = 100, height = 75, background = "black", highlightthickness = 0)
        self.canvas.pack(), self.canvas.place(x = 300, y = 100)
        self.canvas_create_animation()
        self.before_result_screen(result)

    def before_result_screen(self, result):
        if result == "win":
            self.gif = Image.open(self.win_gif)
        elif result == "draw":
            self.gif = Image.open(self.win_gif)
        elif result == "lose":
            self.gif = Image.open(self.lose_gif)
        self.result = result
        self.gif_frames = [ImageTk.PhotoImage(frame) for frame in self.get_frames()]
        self.current_frame = 0
        self.repeat_index = 0
        threading.Thread(target = self.display_result_screen).start()

    def display_result_screen(self):
        repeat = 1 if self.result == "win" or self.result == "draw" else 2
        if self.repeat_index < repeat:
            if self.current_frame < len(self.gif_frames):
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, anchor = NW, image = self.gif_frames[self.current_frame])
                self.current_frame += 1
                self.root.after(50, self.display_result_screen)
            else:
                self.current_frame = 0
                self.repeat_index += 1
                self.display_result_screen()
        else:
            self.canvas_destroy_animation()
