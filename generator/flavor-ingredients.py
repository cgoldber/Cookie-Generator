import numpy as np
import random
from ingredient import Ingredient

class FlavorIngredients: 
    def __init__(self, ing_list): 
        self.spices = {}
        self.mix_ins = {}
        self.volume = 0
        self.sort_ingredients(ing_list)
    
    def sort_ingredients(self, ing_list):
        """From a list of flavors in the recipe, sort into either spices (including cinnamon, chili powder, almond extract, 
        basil, etc.) or mix-ins (including chocolate chips, nuts, dried fruit, etc.). Note that spices will have a much
        smaller volume compared to mix-ins."""
        pass

    def add_ingredient(self):
        """With equal probability, add a new spice or a new mix-in"""
        pass 

    def delete_ingredient(self):
        """With equal probability, add a spice or mix-in"""
        pass

    def swap_ingredient(self):
        """With equal probability, swap a spice or mix-in with a new spice or mix-in"""
        pass

    def mutate(self):
        """Calls an above mutation with equal probability."""
        mutation = np.random.randint(0,3)
        if mutation == 0: 
            self.add_ingredient() 
        elif mutation == 1: 
            self.delete_ingredient()
        elif mutation == 2: 
            self.swap_ingredient()