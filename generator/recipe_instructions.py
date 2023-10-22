import numpy as np

class RecipeInstructions: 
    def __init__(self, temp=350, bake_time=10, rest_time=2, size=50):
        self.temp = temp
        self.bake_time = bake_time
        self.rest_time = rest_time
        self.size = size

    def adjust_temp(self):
        """ Randomly sets temperature to a multiple of 25 degrees F between 325
            and 425 inclusive
        """
        self.temp = np.random.randint(13, 18) * 25

    def adjust_bake_time(self):
        """ Randomly sets bake time to a time between 8 and 12 minutes
        """
        self.bake_time = np.random.randint(8,13) 

    def adjust_rest_time(self):
        """ Randomly sets rest time to a time between 0 and 12 hours
        """
        self.rest_time = np.random.randint(0,13) 

    def adjust_size(self):
        """ Randomly sets size to a multiple of 5 between 40 and 60 grams per 
            cookie.
        """
        self.size = np.random.randint(8, 13) * 5

    def mutate(self):
        """ Calls an above mutation
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
        elements from the base ingredient, flavor ingredient, and instruction 
        attributes of the Recipe object. 
        """
        instructions = f"Step 1: Preheat the oven to " + \
        f"{str(recipe.instructions.get_temp())} degrees F.\nStep 2: Mix " + \
        "together dry ingredients, combining flour, " + \
        f"{recipe.base_ingredients.get_dry()}," + \
        f"{recipe.flavor_ingredients.get_spice()} in a large bowl. In " + \
        f"another bowl, cream together {recipe.base_ingredients.get_sugar()}" + \
        f" and {recipe.base_ingredients.get_fat()}, then add " + \
        f"{recipe.flavor_ingredients.get_oil()}"

        if recipe.base_ingredients.get_wet() != "": 
            instructions += f" and {recipe.base_ingredients.get_wet()}.\n"

        instructions += "\nStep 3: Gradually add the dry ingredients to " + \
        "the wet ingredients, mixing well"
        if recipe.flavor_ingredients.get_mix_in() != "": 
            instructions += ". Once mixed, add the " + \
            f"{recipe.flavor_ingredients.get_mix_in()}"
        instructions += ".\nStep 4: "
        if (recipe.instructions.get_rest_time() > 0):
            instructions += "Let the mixture rest for " + \
            f"{str(recipe.instructions.get_rest_time())} hours in the " + \
            "refrigerator."
        instructions += " On a baking sheet lined with parchment paper, " + \
        f"add {str(recipe.instructions.get_size())} grams of dough, rolled " + \
        f"into a sphere. Bake for {str(recipe.instructions.get_bake_time())}" + \
        " minutes, turning the sheet around halfway through the baking" + \
        " time.\nStep 5: Let the cookies cool."
        return instructions

    def get_temp(self):
        return self.temp
    
    def get_bake_time(self):
        return self.bake_time
    
    def get_rest_time(self):
        return self.rest_time
    
    def get_size(self):
        return self.size

    def get_temp_times_size(self):
        return list(self.temp, self.bake_time, self.rest_time, self.size)