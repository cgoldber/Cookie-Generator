import numpy as np
import random
from ingredient import Ingredient

class BaseIngredients: 
    def __init__(self, ing_list): 
        self.wet = {}
        self.flour = {}
        self.dry = {}
        self.sugars = {}
        self.fats = {}
        self.volume = 0
        self.sort_ingredients(ing_list)
    
    def sort_ingredients(self, ing_list):
        pass

    def adjust_base_ratios(self):
        """Change ratio of sugar to flour to fat"""
        pass 

    def adjust_sugar_ratios(self):
        """Adjust types and ratios of sugars (white, brown, honey, molasses)"""
        pass

    def adjust_fat_ratios(self):
        """Adjust types and ratios of fats (butter, vegetable oil, olive oil, margarine)"""
        pass

    def adjust_eggs(self): 
        """Adjust ratios and composition of eggs (whole, white, yolks)"""
        # 1 large egg = 50 g (30 g whites, 20 g yolk)
        # should be between 1-2 eggs per recipe, or 0 for shortbread
        pass

    def mutate(self):
        """Calls an above mutation with equal probability."""
        mutation = np.random.randint(0,4)
        if mutation == 0: 
            self.adjust_base_ratios() 
        elif mutation == 1: 
            self.adjust_sugar_ratios()
        elif mutation == 2: 
            self.adjust_fat_ratios()
        elif mutation == 3: 
            self.adjust_eggs()


