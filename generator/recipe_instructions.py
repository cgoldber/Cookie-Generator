import numpy as np


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
    mutate():
        Chooses and executes one of the mutations above with equal probability.
    fill_in_quantities(recipe):
        Returns formatted, step-by-step instructions for the recipe.
    """
    
    def __init__(self, temp=350, bake_time=10, rest_time=2, size=50):
        self.temp = temp
        self.bake_time = bake_time
        self.rest_time = rest_time
        self.size = size

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
        instructions = (f"Step 1: Preheat the oven to " + 
        f"{str(self.temp)} degrees F.\nStep 2: Mix " + 
        "together dry ingredients, combining the following in a large bowl" + 
        ": flour")
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