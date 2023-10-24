import numpy as np
import random

EMOTIONAL_SONGS = {
    "Happy" : ["Walking on Sunshine", "Dancing Queen", 
        "Here Comes the Sun", "What a wonderful world", 
        "Beautiful Day", "Happy", "Rhythm and Blues", "Happy", "8TEEN", 
        "Good Life", "Mona Lisa", "Castle on the Hill", "Confident"],
    "Sad" : ["My heart will go on", "Candle in the wind", 
        "Marvin's room", "Redemption", "Driver's lisence", 
        "Heartbreak Anniversery", "Coaster", "Cold Blooded", "Ivy",
        "Find you", "Blue", "Bahamas Promises", "Alone"],
    "Angry" : ["Nonstop", "Rolling in the Deep", "Break Stuff", 
        "I'm Upset", "Worst behavior", "99 problems", 
        "I heard it through the grapevine", "Ex-factor", 
        "Irreplacable", "The Final Countdown", "IDGAF", 
        "Commitment Issues", "Shot for me"], 
    "Excited" : ["Can't stop the feeling", "Dynamite", 
        "Walking on Sunshine", "All Star", "I gotta Feeling", 
        "Twist and shout", "Superstar Sh*t", "Watermelon Sugar", 
        "Intentions", "One Thing", "Sugar", "Cool Kids", 
        "Can't Feel my Face" ],
    "Tired" : ["Socks", "babydoll", "Tired of Running", "Jaded", 
        "Furthest Thing", "Tried Our Best", "Apocolypse", 
        "never find u", "Are You Bored Yet?", "Blessed", "Streetcar", 
        "I'm tired", "Apocalypse"],
    "Stressed" : ["Changes", "Don't give up on me", "Stay", 
        "This City", "Do not Distrub", "One Man can change the world", 
        "Emotion", "Chanel", "Japanesse Denim", "Goodbyes", "Lie", 
        "White Ferrari", "Come Back to Earth"]
}  


class RecipeInstructions: 
    """ A class to represent instructions in a recipe.

    ...

    Attributes
    ----------
    temp : int
        baking temperature, in Fahrenheit. 
    bake_time : int
        baking time, in minutes.
    rest_time : int
        resting time, in hours.
    size : int 
        size of each cookie, in grams.
    emotion : strng
        user's current emotion.

    Methods
    -------
    adjust_temp():
        Randomly adjusts temperature between 325-425 degrees F.
    adjust_bake_time():
        Randomly adjusts bake time between 8-12 minutes.
    adjust_rest_time():
        Randomly adjusts rest time between 0-12 hours.
    adjust_size():
        Randomly adjust size between 40-60 grams.
    select_song():
        Chooses random song associated with user's emotion.
    mutate():
        Chooses and executes one of the mutations above with equal probability.
    fill_in_quantities(recipe):
        Returns formatted, step-by-step instructions for the recipe.
    """

    def __init__(self, emotion, temp=350, bake_time=10, rest_time=2, size=50):
        """ Initializes cooking instruction parameters to default settings.
            Args:
                temp (int) : temperature to preheat oven in F
                bake_time (int) : how long to bake cookies in mins
                rest_time (int) : how long to leave cookies out after baking
                size (int) : size of cookie dough on sheet
                emotion (string) : the user's current emotion
        """
        self.temp = temp
        self.bake_time = bake_time
        self.rest_time = rest_time
        self.size = size
        self.emotion = emotion

    def adjust_temp(self):
        """ Randomly sets temperature to a multiple of 25 degrees F between 325
            and 425 inclusive.
        """
        self.temp = np.random.randint(13, 18) * 25

    def adjust_bake_time(self):
        """ Randomly sets bake time to a time between 8 and 12 minutes.
        """
        self.bake_time = np.random.randint(8,13) 

    def adjust_rest_time(self):
        """ Randomly sets rest time to a time between 0 and 12 hours.
        """
        self.rest_time = np.random.randint(0,13) 

    def adjust_size(self):
        """ Randomly sets size to a multiple of 5 between 40 and 60 grams per 
            cookie.
        """
        self.size = np.random.randint(8, 13) * 5
    
    def select_song(self):
        """ Selects a song associated with the user's emotion.
        """
        song_opts = EMOTIONAL_SONGS[self.emotion]  
        return random.choice(song_opts)

    def mutate(self):
        """ Calls an above mutation.
        """
        mutation = np.random.randint(0,4)
        if mutation == 0: 
            self.adjust_temp() 
        elif mutation == 1: 
            self.adjust_bake_time()
        elif mutation == 2: 
            self.adjust_rest_time()
        elif mutation == 3:
            self.adjust_size()
    
    def fill_in_quantities(self, recipe):
        """ Returns formatted, step-by-step instructions for the recipe with
            elements from the base ingredient, flavor ingredient, and 
            instruction attributes of the Recipe object. 
            Args:
                recipe (Recipe) : The recipe whose instructions are written for
        """
        instructions = (f"Put on the {self.emotion.lower()} song, " +
        f"{self.select_song()}, so that you can get in the mood while baking" +
        f"!\nStep 1: Preheat the oven to {str(self.temp)} degrees F.\nStep 2" + 
        ": Mix together dry ingredients, combining the following in a large " + 
        "bowl: flour")
        if recipe.base_ingredients.get_dry() != "":
            instructions += f", {recipe.base_ingredients.get_dry()}"
        if recipe.flavor_ingredients.get_spice() != "":
            instructions += f", {recipe.flavor_ingredients.get_spice()}"
        instructions += (". In another bowl, cream together the following: " + 
        f"{recipe.base_ingredients.get_sugar()}")
        if recipe.base_ingredients.get_fat() != "":
            instructions += f", {recipe.base_ingredients.get_fat()}"
        if recipe.flavor_ingredients.get_spice() != "":
            instructions += f", {recipe.flavor_ingredients.get_oil()}"
        if recipe.base_ingredients.get_wet() != "": 
            instructions += f", {recipe.base_ingredients.get_wet()}"

        instructions += (".\nStep 3: Gradually add the dry ingredients to " + 
        "the wet ingredients, mixing well")
        if recipe.flavor_ingredients.get_mix_in() != "": 
            instructions += (". Once mixed, add the " + 
            f"{recipe.flavor_ingredients.get_mix_in()}")
        instructions += ".\nStep 4: "
        if (self.rest_time > 0):
            instructions += ("Let the mixture rest for " + 
            f"{str(self.rest_time)} hours in the " + 
            "refrigerator.")
        instructions += (" On a baking sheet lined with parchment paper, " +
        f"add {str(self.size)} grams of dough, rolled" + 
        f" into a sphere. Bake for " + \
        f" {str(self.bake_time)} minutes, turning the" + 
        " sheet around halfway through the baking time.\nStep 5: Let the " + 
        "cookies cool.")
        return instructions