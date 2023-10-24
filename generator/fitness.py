import pandas as pd
import os
import numpy as np


class Fitness():
    """ Computes and keeps track of the fitness score

    ...

    Attributes
    ----------
    fitness_val : float
        The overall fitness score.
    emotion : string
        The emotion inspiration of the associated recipe.
    flavor_ingredient : list
        The flavor ingredients of the associated recipe.
    flavor_names : list
        The flavor names of the associated recipe.
    
    Methods
    -------
    similarity():
        Returns the flavor pairing score between two ingredients.
    flavor_pairing_score():
        Returns the average similarity score between flavors in the recipe.
    get_inpsiring_dic():
        Reads inspiring recipes and stores them as dictionaries.
    calc_euc_dist():
        Computed Euclidean Distance between current and inspiring set recipes.
    dissimilarity_score():
        Calculates dissimilarity between current/inspiring set recipes.
    emotion_score():
        Returns how much flavor ingredients align with associated emotion.
    set_fitness_val():
        Computes and sets fitness values attribute.
    get_fitness_val():
        Returns fitness value.
    """

    def __init__(self, flavor_ingredients, emotion):
        """ Initializes the fitness score to 0
            Args:
                flavor_ingredients (list) : FlavorIngredients of associated
                                            recipe
                emotion (string) : emotion inspiration for associated recipe
        """
        self.fitness_val = 0
        self.emotion = emotion
        self.flavor_ingredients = flavor_ingredients
        self.flavor_names = flavor_ingredients.get_flavor_ing_names()

    def similarity(self, ingr1, ingr2):
        """ Returns the similarity between two ingredients based on given data
            where the output indicates how good the ingredients taste together
            (low is 0 and high is 1).
            Args:
                ingr1 (str) : first ingredient name
                ingr2 (str) : second ingredient name
        """
        WORD_EMBED_VALS = np.load('flavors/ingred_word_emb.npy', 
        allow_pickle=True).item()
        ingr1_vec = WORD_EMBED_VALS[ingr1]
        ingr2_vec = WORD_EMBED_VALS[ingr2]
        return np.dot(ingr1_vec, ingr2_vec)
    
    def flavor_pairing_score(self):
        """ Returns the average similarity score between flavors in the 
            associated recipe.
        """
        if len(self.flavor_names) == 0: 
            return 0
        elif len(self.flavor_names) == 1:
            return 0.2

        flavor_scores = []
        for i in range(len(self.flavor_names) - 1):
            for j in range(i + 1, len(self.flavor_names)):
                ingr1 = self.flavor_names[i].strip()
                ingr2 = self.flavor_names[j].strip()
                flavor_score = self.similarity(ingr1, ingr2)
                flavor_scores.append(flavor_score)

        return np.mean(flavor_scores)
    
    def get_inpsiring_dic(self, file):
        """ Reads the inspiring recipes and stores them as a dictionary where
            the keys represent the ingredient and the values represented the
            associated amount.
            Args:
                file (str) : name of the inspiring recipe file
        """
        with open(file, "r") as f:
                lines = f.readlines()
        ingredient_dic = {}
       
        for line in lines:
            if "Ingredients" not in line:
                parts = [line.split(' ')[0], ' '.join(line.split(' ')[2:])]
                ingredient_dic[parts[1]] = parts[0]
        return ingredient_dic

    def calc_euc_dist(self, insp_dic):
        """ Calculates how different the recipe associated with the given
            inspring recipe dictionary is from the current recipe that this
            fitness object belongs to. To compute this value, the current and
            inpsiring recipe are converted into vectors, where each index 
            corresponds to an ingredient that at least one of the two recipes
            have, and the values are the amount of that ingredient. Then,
            the euclidean distance is computed
            Args:
                insp_dic (dic) : dict corresponding to an inspiring recipe
        """
        all_ingrs = set(self.flavor_names + list(insp_dic.keys()))
        curr_vector, insp_vector = [], []
        for ingr in all_ingrs:
            curr_vector.append(
                            self.flavor_ingredients.get_amount_by_name(ingr))
            if ingr in insp_dic.keys():
                insp_vector.append(insp_dic[ingr])
            else:
                insp_vector.append(0)

        euc_dist = np.linalg.norm(np.array(curr_vector, dtype=float) \
                                        - np.array(insp_vector, dtype=float))
        return euc_dist
    
    def dissimilarity_score(self):
        """ Calculates how dissimilar the flavors in the current recipe is to
            the flavors in the inspiring set using the Euclidean distance.
        """
        dir = "../inspiring_set"
        dissimilarities = []
        for inspiringRecipe in os.listdir(dir):
            with open(dir + "/" + inspiringRecipe, "r") as f:
                insp_dic = self.get_inpsiring_dic(dir + "/" + inspiringRecipe)
            euc_dist = self.calc_euc_dist(insp_dic)
            dissimilarities.append(euc_dist)
        dissimilarities = dissimilarities / sum(dissimilarities)
        return np.mean(dissimilarities)
    
    def emotion_score(self):
        """ Returns a value indicating how much the recipe coincides with 
            the chosen emotion.
        """
        if len(self.flavor_names) == 0:
            return 0

        emotion_df = pd.read_excel("../Ingredient_Matrix.xlsx")
        emotion_df.set_index('Ingredient', inplace=True)
  
        alignment_sum = sum(emotion_df.loc[ingr, self.emotion.lower()] \
        for ingr in self.flavor_names)

        return alignment_sum / len(self.flavor_names)
    
    def set_fitness_val(self, flavor_pairing_coef=4, dissimilarity_coef=10, 
                        emotion_coef=200, len_coef = 0.75, do_print=False):
        """ Sets fitness score considering how well the flavors are paired, 
            how dissimilar the recipe is from recipes in the inspiring set, and 
            how much the recipe coincides with the chosen emotion.
            Args:
                flavor_pairing_coef (float) : multiplier of flavor score
                dissimilarity_coef (float) : multiplier of uniqueness score
                emotion_coef (float) : multiplier of emotion score
                len_coef (float) : multiplier of recipe length score
                do_print (boolean) : where there fitness components will print
        """
        flavor_comp = self.flavor_pairing_score() * flavor_pairing_coef
        dissimilarity_comp = self.dissimilarity_score() * dissimilarity_coef 
        emotion_comp = self.emotion_score() * emotion_coef
        len_comp = len(self.flavor_names) * len_coef
        if do_print:
            print(f"flavor: {round(flavor_comp, 2)}, dissimilarity: " + \
            f"{round(dissimilarity_comp, 2)}, emotion: " + \
            f"{round(emotion_comp, 2)}, length: {round(len_comp, 2)}")
    
        self.fitness_val =  flavor_comp + dissimilarity_comp + emotion_comp \
        + len_comp

    def get_fitness_val(self):
        """ Returns the current fitness value.
        """
        return self.fitness_val
