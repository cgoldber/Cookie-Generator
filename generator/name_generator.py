import numpy as np

EMOTIONAL_REPETOIRE = {
    "Happy" : ["Happy", "Delighted", "Content", "Pleased", "Ecstatic", 
        "Joyful", "Glad", "Jubliant", "Elated", "Merry", "Blissful", 
        "Euphoric"],
    "Sad" : ["Unhappy", "Melancholy", "Depressed", "Sorrowful", 
        "Mournful", "Downcast", "Blue", "Woeful", "Gloomy", 
        "Despondent", "Dejected", "Dismal"],
    "Angry" : ["Furious", "Irritated", "Wrathful", "Enraged", 
        "Indigant", "Irate", "Incensed", "Infuriated", "Agitated", 
        "Outraged", "Fuming", "Vexed"],
    "Excited" : ["Enthusiastic", "Eager", "Thrilled", "Animated", 
        "Jubliant", "Ecstatic", "Elated", "Overjoyed", "Exhilarated", 
        "Pumped", "Fired-up", "Anticipatory", "Exultant"],
    "Tired" : ["Exhausted", "Fatigued", "Weary", "Drained", "Worn-out",
        "Weary", "Burnt-out", "Depleted", "Lethargic", "Run-down", 
        "Beat", "Jet-lagged"],
    "Stressed" : ["Anxious", "Worried", "Tense", "Overwhelmed", 
        "Strained", "Upset", "On-edge", "Frazzeled", "Frantic", 
        "Perturbed", "Exasperated", "Unsettled"]
}

class Name():
    def __init__(self, emotion):
        self.emotion = emotion
        self.name = self.name_generator()

    def name_generator(self):
            """ Generates a name based on the emotion of the recipe
                Args:
                    emotion (str) : recipe's associated emotion
            """
            syn_opts = EMOTIONAL_REPETOIRE[self.emotion]
            syn_choice = np.random.choice(syn_opts)       
            return syn_choice + " " + self.emotion + " Cookies" 
    
    def get_name(self):
        return self.name