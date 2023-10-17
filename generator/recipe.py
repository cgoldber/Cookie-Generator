import numpy as np
import pandas as pd
import flavor_pairing
from random import randint
import flavor_pairing
from ingredient import Ingredient
from recipe_instructions import RecipeInstructions
from base_ingredients import BaseIngredients
from flavor_ingredients import FlavorIngredients
from flavor_ingredients import INGREDIENT_TYPES


class Recipe:
    def __init__(self, recipe_strs, emotion="default"):
        self.emotion = emotion
        ing_list = self.make_ingredient_list(recipe_strs)
        self.base_ingredients = BaseIngredients(ing_list)
        self.flavor_ingredients = FlavorIngredients(ing_list)
        self.instructions = RecipeInstructions()
        self.name = self.name_generator(emotion)

    def name_generator(self, emotion: str):
        Happy_syn = ["Happy", "Delgihted", "Content", "Pleased", "Ecstatic", "Joyful", "Glad", "Jubliant", "Elated", "Merry", "Blissful", "Euphoric"]
        Sad_syn = ["Unhappy", "Melancholy", "Depressed", "Sorrowful", "Mournful", "Downcast", "Blue", "Woeful", "Gloomy", "Despondent", "Dejected", "Dismal"]
        Angry_syn = ["Furious", "Irritated", "Wrathful", "Enraged", "Indigant", "Irate", "Incensed", "Infuriated", "Agitated", "Outraged", "Fuming", "Vexed"]
        Excited_syn = ["Enthusiastic", "Eager", "Thrilled", "Animated", "Jubliant", "Ecstatic", "Elated", "Overjoyed", "Exhilarated", "Pumped", "Fired-up", "Anticipatory", "Exultant"]
        Tired_syn = ["Exhausted", "Fatigued", "Weary", "Drained", "Worn-out", "Weary", "Burnt-out", "Depleted", "Lethargic", "Run-down", "Beat", "Jet-lagged"]
        Stressed_syn = ["Anxious", "Worried", "Tense", "Overwhelmed", "Strained", "Upset", "On-edge", "Frazzeled", "Frantic", "Perturbed", "Exasperated", "Unsettled"]
        Emotional_repetoire = {"Happy": Happy_syn, "Sad":Sad_syn, "Angry": Angry_syn, "Excited" : Excited_syn, "Tired" : Tired_syn, "Stressed": Stressed_syn }
        
        for key in Emotional_repetoire:
            if emotion == key:
                words = Emotional_repetoire[emotion]
                words_syn = words[randint(0,11)]
                
        return words_syn + str(emotion).capitalize() + "Cookies"        
        #return str(emotion).capitalize() + " Cookies"
    
    def make_ingredient_list(self, recipe_strs):
        ing_list = []
        for line in recipe_strs: 
            if not line.startswith("-") and line != "":
                if " g " in line: 
                    information = line.split(" g ")
                    unit = "g"
                elif " tsp " in line:
                    information = line.split(" tsp ")
                    unit = "tsp"
                elif " tbsp " in line:
                    information = line.split(" tbsp ")  
                    unit = "tbsp"
                amt = float(information[0])
                name = information[1].strip()
                if "butter" in name and unit == "tbsp":
                    amt *= 14.2
                ing_list.append(Ingredient(name, amt, unit))
        return ing_list

    def flavor_pairing_score(self):
        """ Returns the average similarity score between flavors in the recipe.
        """
        total_ingredients = INGREDIENT_TYPES["spices"] + INGREDIENT_TYPES["mix-ins"] + INGREDIENT_TYPES["oils"]
        all_ingredient_names = self.flavor_ingredients.get_flavor_ing_names()
        if len(all_ingredient_names) == 0: 
            return 0
        elif len(all_ingredient_names) == 1:
            return 0.5
        flavor_scores = []
        for ingredient1 in all_ingredient_names:
            for ingredient2 in all_ingredient_names:
                ingredient1, ingredient2 = ingredient1.strip(), ingredient2.strip()
                if ingredient1 in total_ingredients and ingredient2 in total_ingredients:
                    flavor_score = flavor_pairing.similarity(ingredient1, ingredient2)
                    flavor_scores.append(flavor_score)
        avg_flavor_score = sum(flavor_scores) / len(flavor_scores)
        return avg_flavor_score
    
    def dissimilarity_score(self):
        """ Returns a value indicating how disimilar the recipe is from those in the inspiring set.
        """
        return 0
    
    def emotion_score(self):
        """ Returns a value indicating how much the recipe coincides with the chosen emotion.
        """
        emotion_alignment_df = pd.read_excel("../Ingredient_Matrix.xlsx", header=0, index_col=0)
        ing_list = self.flavor_ingredients.get_flavor_ing_names()
        alignment_sum = sum(emotion_alignment_df.loc[ingr, self.emotion.lower()] for ingr in ing_list)    
        return alignment_sum / len(ing_list)
        
    def get_fitness(self, flavor_pairing_coef=1, dissimilarity_coef=1, emotion_coef=1):
        """Returns fitness score considering how well the flavors are paired, how dissimilar the recipe is from
        recipes in the inspiring set, and how much the recipe coincides with the chosen emotion.
        """
        return self.flavor_pairing_score() * flavor_pairing_coef + \
        self.dissimilarity_score() * dissimilarity_coef + \
        self.emotion_score() * emotion_coef
    
    def get_base_ingredient_strings(self):
        """Returns the ingredients of the recipes as a list of strings
        """
        return [str(ingredient) for ingredient in self.base_ingredients.values()]
    
    def get_base_ing_strings(self): 
        return str(self.base_ingredients).split("\n")
    
    def get_flavor_ing_strings(self): 
        return str(self.flavor_ingredients).split("\n")

    def get_flavor_ingredients(self):
        """Returns the flavor ingredient list
        """
        return self.flavor_ingredients.values()

    def get_name(self):
        """Returns the name of the recipe.
        """
        return self.name

    def mutate(self):
        """Based on some set probability (20%), returns original recipe 80% of 
        the time. Otherwise, calls for the mutation of the base ingredients, 
        flavor ingredients, or recipe instruction with set probability (20%,
        60%, and 20% respectively).
        """
        mutate = np.random.choice([True, False], p=[0.2,0.8])
        if mutate: 
            mutation = np.random.choice(["base", "flavor", "instructions"],p=[0.2,0.7,0.1])
            if mutation == "base": 
                self.base_ingredients.mutate()
            elif mutation == "flavor": 
                self.flavor_ingredients.mutate()
            elif mutation == "instructions": 
                self.instructions.mutate()

    def __str__(self):
        recipe_str = "# " + self.name  + ":\n" + str(self.base_ingredients) + "\n" + str(self.flavor_ingredients)
        return recipe_str
    
    def __repr__(self):
        return self.emotion + ", " + repr(self.flavor_ingredients)