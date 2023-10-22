from flavor_ingredients import INGREDIENT_TYPES
import pandas as pd
import os
import numpy as np

class Fitness():

    def __init__(self, flavor_ingredients, emotion):
        self.fitness_val = 0
        self.emotion = emotion
        self.flavor_ingredients = flavor_ingredients
        self.flavor_names = flavor_ingredients.get_flavor_ing_names()

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

        if len(self.flavor_names) == 0: 
            return 0
        elif len(self.flavor_names) == 1:
            return 0.5

        flavor_scores = []
        for ingr1 in self.flavor_names:
            for ingr2 in self.flavor_names:
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
            if ingr in self.flavor_names:
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
  
        alignment_sum = sum(emotion_df.loc[ingr, self.emotion.lower()] \
        for ingr in self.flavor_names)

        if len(self.flavor_names) == 0:
            return 0
        else:
            return alignment_sum / (len(self.flavor_names))
    
    def set_fitness_val(self, flavor_pairing_coef=6, dissimilarity_coef=5, 
                    emotion_coef=100, do_print=False):
        """Sets fitness score considering how well the flavors are paired, 
           how dissimilar the recipe is from recipes in the inspiring set, and 
           how much the recipe coincides with the chosen emotion.
        """
        flavor_comp = self.flavor_pairing_score() * flavor_pairing_coef
        dissimilarity_comp = self.dissimilarity_score() * dissimilarity_coef 
        emotion_comp = self.emotion_score() * emotion_coef
        len_comp = len(self.flavor_names) / 1.5

        if do_print:
            print(f"flavor: {round(flavor_comp, 2)}, dissimilarity: " + \
            f"{round(dissimilarity_comp, 2)}, emotion: " + \
            f"{round(emotion_comp, 2)}, length: {round(len_comp, 2)}")
    
        self.fitness_val =  flavor_comp + dissimilarity_comp + emotion_comp + len_comp

    def get_fitness_val(self):
        return self.fitness_val
    
