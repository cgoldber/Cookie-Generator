import numpy as np
import os
import pandas as pd
from random import randint
from ingredient import Ingredient
from recipe_instructions import RecipeInstructions
from base_ingredients import BaseIngredients
from flavor_ingredients import FlavorIngredients
from flavor_ingredients import INGREDIENT_TYPES


class Recipe:
    def __init__(self, recipe_strs, emotion="default", 
                 instructions=RecipeInstructions()):
        self.emotion = emotion
        ing_list = self.make_ingredient_list(recipe_strs)
        self.base_ingredients = BaseIngredients(ing_list)
        self.flavor_ingredients = FlavorIngredients(ing_list)
        self.instructions = instructions
        self.name = self.name_generator(emotion)

    def name_generator(self, emotion):
        """ Generates a name based on the emotion of the recipe
            Args:
                emotion (str) : recipe's associated emotion
        """
        emotional_repetoire = {
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
        
        for key in emotional_repetoire:
            if emotion == key:
                words = emotional_repetoire[emotion]
                words_syn = words[randint(0,11)]
                
        return words_syn + " " + str(emotion).capitalize() + " Cookies"        
    
    def make_ingredient_list(self, recipe_strs):
        ing_list = []
        for line in recipe_strs: 
            if not line.startswith("-") and line != "":
                split_line = line.split(" ")
                amt = float(split_line[0])
                unit = split_line[1]
                ingr_name = " ".join(split_line[2:])
                
                if "butter" in ingr_name and unit == "tbsp":
                    amt *= 14.2
                    
                ing_list.append(Ingredient(ingr_name, amt, unit))
        return ing_list

    def similarity(self, ingr1, ingr2):
        """Returns the similarity between two ingredients based on given data.
        """
        WORD_EMBED_VALS = np.load('flavors/ingred_word_emb.npy', 
        allow_pickle=True).item()
        ingr1_vec = WORD_EMBED_VALS[ingr1]
        ingr2_vec = WORD_EMBED_VALS[ingr2]
        return np.dot(ingr1_vec, ingr2_vec)

    def flavor_pairing_score(self):
        """ Returns the average similarity score between flavors in the recipe.
        """
        total_ingredients = INGREDIENT_TYPES["spices"] + \
        INGREDIENT_TYPES["mix-ins"] + INGREDIENT_TYPES["oils"]
        all_ingredient_names = self.flavor_ingredients.get_flavor_ing_names()
        if len(all_ingredient_names) == 0: 
            return 0
        elif len(all_ingredient_names) == 1:
            return 0.5
        flavor_scores = []
        for ingr1 in all_ingredient_names:
            for ingrt2 in all_ingredient_names:
                ingr1, ingr2 = ingr1.strip(), ingr2.strip()
                if ingr1 in total_ingredients and ingr2 in total_ingredients:
                    flavor_score = self.similarity(ingr1, ingr2)
                    flavor_scores.append(flavor_score)
        avg_flavor_score = sum(flavor_scores) / len(flavor_scores)
        return avg_flavor_score
    
    def get_inpsiring_dic(self, file):
        with open(file, "r") as f:
                lines = f.readlines()
        ingredient_dic = {}
       
        for line in lines:
            if "Ingredients" not in line:
                parts = [line.split(' ')[0], ' '.join(line.split(' ')[2:])]
                ingredient_dic[parts[1]] = parts[0]
        return ingredient_dic

    def dissimilarity_score(self):
        emotion_alignment_df = pd.read_excel("../Ingredient_Matrix.xlsx")
        emotion_alignment_df.set_index('Ingredient', inplace=True)
        ingredients = emotion_alignment_df.index.to_list()

        #get curr recipe vector
        curr_vector = []
        for ingr in ingredients:
            if ingr in self.flavor_ingredients.get_flavor_ing_names():
                amt = self.flavor_ingredients.get_amount_by_name(ingr)
                curr_vector.append(amt)
            else:
                curr_vector.append(0)

        #get vector for each in inspiring set and save scores
        dissimilarities = []
        dir = "../inspiring_set"
        for inspiringRecipe in os.listdir(dir):
            insp_vector = []
            ingr_dic = self.get_inpsiring_dic(dir + "/" + inspiringRecipe)
            for ingr in ingredients:
                if ingr in ingr_dic.keys():
                    insp_vector.append(ingr_dic[ingr])
                else:
                    insp_vector.append(0)
            euc_dist = np.linalg.norm(np.array(curr_vector, dtype=float) \
            - np.array(insp_vector, dtype=float))
            dissimilarities.append(euc_dist)
        dissimilarities = dissimilarities / max(dissimilarities)
        return np.mean(dissimilarities)
    
    def emotion_score(self):
        """ Returns a value indicating how much the recipe coincides with 
        the chosen emotion.
        """
        emotion_df = pd.read_excel("../Ingredient_Matrix.xlsx")
        emotion_df.set_index('Ingredient', inplace=True)
        ing_list = self.flavor_ingredients.get_flavor_ing_names()
        alignment_sum = sum(emotion_df.loc[ingr, self.emotion.lower()] \
        for ingr in ing_list)

        if len(ing_list) == 0:
            return 0
        else:
            return alignment_sum / (len(ing_list))
        
    def get_fitness(self, flavor_pairing_coef=6, dissimilarity_coef=5, 
                    emotion_coef=100, do_print=False):
        """Returns fitness score considering how well the flavors are paired, 
           how dissimilar the recipe is from recipes in the inspiring set, and 
           how much the recipe coincides with the chosen emotion.
        """
        flavor_comp = self.flavor_pairing_score() * flavor_pairing_coef
        dissimilarity_comp = self.dissimilarity_score() * dissimilarity_coef 
        emotion_comp = self.emotion_score() * emotion_coef
        len_comp = len(self.get_flavor_ing_strings()) / 1.5
        if do_print:
            print(f"flavor: {round(flavor_comp, 2)}, dissimilarity: " + \
            f"{round(dissimilarity_comp, 2)}, emotion: " + \
            f"{round(emotion_comp, 2)}, length: {round(len_comp, 2)}")
        return flavor_comp + dissimilarity_comp + emotion_comp + len_comp
        
    def get_base_ing_strings(self): 
        return str(self.base_ingredients).split("\n")
    
    def get_flavor_ing_strings(self): 
        return str(self.flavor_ingredients).split("\n")

    def get_flavor_ingredients(self):
        """Returns the flavor ingredient list
        """
        return self.flavor_ingredients.values()
    
    def get_instructions(self):
        """Returns RecipeInstruction object. 
        """
        return self.instructions

    def get_name(self):
        """Returns the name of the recipe.
        """
        return self.name
    
    def format_instructions(self):
        """ Returns formatted, step-by-step instructions for the recipe with
        elements from the base ingredient, flavor ingredient, and instruction 
        attributes of the Recipe object. 
        """
        instructions = f"Step 1: Preheat the oven to " + \
        f"{str(self.instructions.get_temp())} degrees F.\nStep 2: Mix " + \
        "together dry ingredients, combining flour, " + \
        f"{self.base_ingredients.get_dry()}," + \
        f"{self.flavor_ingredients.get_spice()} in a large bowl. In " + \
        f"another bowl, cream together {self.base_ingredients.get_sugar()}" + \
        f" and {self.base_ingredients.get_fat()}, then add " + \
        f"{self.flavor_ingredients.get_oil()}"

        if self.base_ingredients.get_wet() != "": 
            instructions += f" and {self.base_ingredients.get_wet()}.\n"

        instructions += "\nStep 3: Gradually add the dry ingredients to " + \
        "the wet ingredients, mixing well"
        if self.flavor_ingredients.get_mix_in() != "": 
            instructions += ". Once mixed, add the " + \
            f"{self.flavor_ingredients.get_mix_in()}"
        instructions += ".\nStep 4: "
        if (self.instructions.get_rest_time() > 0):
            instructions += "Let the mixture rest for " + \
            f"{str(self.instructions.get_rest_time())} hours in the " + \
            "refrigerator."
        instructions += " On a baking sheet lined with parchment paper, " + \
        f"add {str(self.instructions.get_size())} grams of dough, rolled " + \
        f"into a sphere. Bake for {str(self.instructions.get_bake_time())}" + \
        " minutes, turning the sheet around halfway through the baking" + \
        " time.\nStep 5: Let the cookies cool."
        return instructions

    def mutate(self):
        """Based on some set probability (20%), returns original recipe 80% of 
        the time. Otherwise, calls for the mutation of the base ingredients, 
        flavor ingredients, or recipe instruction with set probability (20%,
        60%, and 20% respectively).
        """
        # mutate = np.random.choice([True, False], p=[0.8,0.2])
        # if mutate: 
        #     self.flavor_ingredients.mutate()       
        self.flavor_ingredients.mutate()         
        mutate = np.random.choice([True, False], p=[0.3,0.7])
        if mutate: 
            self.base_ingredients.mutate()
        mutate = np.random.choice([True, False], p=[0.3,0.7])
        if mutate: 
            self.instructions.mutate()

    def __str__(self):
        recipe_str = "-" + self.name  + ":\n-Base Ingredients\n" 
        recipe_str += str(self.base_ingredients) + "\n-Flavor Ingredients\n" 
        recipe_str += str(self.flavor_ingredients) + "\n---\nInstructions\n"
        recipe_str += self.format_instructions()
        return recipe_str
    
    def __repr__(self):
        return self.emotion + ", " + repr(self.flavor_ingredients)