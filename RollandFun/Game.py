import random

class Game():
    def __init__(self):
        self.dice_numbers = [1, 2, 3, 4, 5, 6]

        self.features = ["Increase the high roll rate of the dice", 
                         "Win 1 round straight", 
                         "Reduce the number of opponent dice"]
        
        self.characters = [
            ("Brofa", 100, 45, "Figther"),          
            ("Berneta", 120, 35, "Figther"), 
            ("Torun", 130, 30, "Tank"),
            ("Terra", 120, 35, "Tank"), 
            ("Merny", 85, 50, "Mage"), 
            ("Serna", 95, 45, "Mage"), 
            ("Perr", 90, 45, "Assasin"), 
            ("Asfer", 105, 40, "Assasin"), 
            ("Karre", 80, 40, "Marksman"), 
            ("Herry", 75, 45, "Marksman")] 

        self.round_start_remaining = 0

    def game_start(self):
        team_characters = []
        team_hps = []
        team_powers = []
        team_roles = []

        for i in range(5):
            random_number = random.randint(0, 9)
            team_characters.append(self.characters[random_number][0])
            team_hps.append(self.characters[random_number][1])
            team_powers.append(self.characters[random_number][2])
            team_roles.append(self.characters[random_number][3])
        return team_characters, team_hps, team_powers, team_roles

    def roll_the_dice(self):
        return random.choice(self.dice_numbers)
