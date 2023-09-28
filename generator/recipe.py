import numpy as np
import random
from ingredient import Ingredient

class Recipe:
    def __init__(self, recipe_strs, emotion):
        self.emotion = emotion
        self.ingredients = {}
        self.base_ingredients = {}
        self.flavor_ingredients = {}
        self.make_ingredient_objects(recipe_strs)
        self.name = self.name_generator()

    def name_generator(self):
        pass
    
    def make_ingredient_objects(self, recipe_strs):
        """Reads recipe_strs and populates self.ingredients with ingredient objects.
           Args:
                recipe_strs (list) : list of the strings corresponding to ingredient/amt in the recipe
        """
        #makes dictionary mapping ingredient name to ingredient object
        for line in recipe_strs: 
            information = line.split(" oz ")
            ingr_amt = float(information[0])
            name = information[1]
            self.ingredients[name] = Ingredient(name, ingr_amt)


    def change_amount(self):
        """An ingredient is selected uniformly at random from the recipe.  
        Its quantity is set to a new value somehow (up to you).
        """
        ingredient = np.random.choice(self.ingredients.values())
        # remove or add up to 100% of original amount 
        new_amt = (random.uniform(-.9,.9) + 1) * ingredient.get_amount()
        ingredient.set_amount(new_amt)

    def add_ingredient(self, all_ingredients):
        """An ingredient is selected uniformly at random from the inspiring set and added to the recipe. 
        The amount of the new ingredient is determined randomly as a random number between 0 and 100 oz.
        Args:
            all_ingredients (set) : A set containing all unique possible ingredients
        """
        new_possible_ingredients = all_ingredients.difference(self.ingredients.keys())

        if len(new_possible_ingredients) == 0: #skip if no new ingredients to add
            return

        new_name = random.choice(tuple(new_possible_ingredients))
        # choose a random amount between 0 and 100 oz 
        new_amt = np.random.choice(range(0,100))

        self.ingredients[new_name] = Ingredient(new_name, new_amt)

    def delete_ingredient(self):
        """An ingredient is selected uniformly at random from the recipe and removed from the recipe.
        """
        selected_ing = random.choice(self.ingredients.keys())
        self.ingredients.remove(selected_ing)

    def swap_ingredient(self, all_ingredients):
        """An ingredient is selected uniformly at random from the recipe. Its name attribute 
        is changed to that of another ingredient that is chosen at random from the ones 
        stored in the inspiring set.
        Args:
            all_ingredients (set) : A set containing all unique possible ingredients
        """
        ingre_name_1 = random.choice(self.ingredients.keys())
        ingredient1_amt = self.ingredients[ingre_name_1].get_amount()

        ingre_name_2 = random.choice(self.ingredients.keys().difference(ingre_name_1))
        ingredient2_amt = self.ingredients[ingre_name_2].get_amount()

        self.ingredients[ingre_name_1] = ingredient2_amt
        self.ingredients[ingre_name_2] = ingredient1_amt
    
    # def combine_duplicate_ingredients(self): 
    #     # loop through all ingredients
    #     checked_ingredients = [self.ingredients[0].copy()]
    #     for ing in self.ingredients: 
    #         for checked_ing in checked_ingredients:
    #             if ing.get_name() == checked_ing.get_name(): 
    #                 checked_ing.set_amount(checked_ing.get_amount() + ing.get_amount())
    #             else: 
    #                 checked_ingredients.append(ing)
    #     self.ingredients = checked_ingredients
    
    def normalize(self):
        """Normalizes all ingredients so amount adds up to 100 oz.
        """
        current_total = 0
        for ingredient in self.ingredients.values(): 
            current_total += ingredient.get_amount() 
        if current_total == 100: #already normalized
            return    
        sizing_factor = 100 / current_total
        for name, ingredient in self.ingredients.items(): 
            new_amt = ingredient.get_amount() * sizing_factor
            if new_amt < .01: #delete ingredient if normalization makes it below .01 oz
                self.ingredients.remove(name)
            else:
                ingredient.set_amount(new_amt)
        
    def get_fitness(self):
        """Returns fitness score
        """
        return len(self.ingredients.keys())
    
    def get_ingredient_strings(self):
        """Returns the ingredients of the recipes as a list of strings
        """
        return [str(ingredient) for ingredient in self.ingredients.values()]
    
    def get_ingredients(self):
        """Returns the ingredient list
        """
        return self.ingredients.values()
    
    def get_name(self):
        """Returns the name of the recipe.
        """
        return self.name

    def mutate(self, all_ingredients):
        """Based on some set probability (40%), returns original recipe 60% of the time. Otherwise, 
        calls some mutation (change_amount, add_ingredient, delete_ingredient, or swap_ingredient) 
        with equal probability. Then calls normalize function.
        Args:
            all_ingredients (set) : A set containing all unique possible ingredients
        """
        mutate = np.random.choice([True, False], p=[0.4,0.6])
        if mutate: 
            mutation = np.random.randint(0,4)
            if mutation == 0: 
                self.change_amount() 
            elif mutation == 1: 
                self.add_ingredient(all_ingredients)
            elif mutation == 2: 
                self.delete_ingredient()
            elif mutation == 3: 
                self.swap_ingredient(all_ingredients)
            # normalize ingredient amounts after mutation 
            self.normalize()
