import numpy as np
import random
from ingredient import Ingredient
from flavors import flavor_pairing

class Recipe:
    def __init__(self, recipe_strs, emotion="default"):
        self.emotion = emotion
        self.base_ingredients = {}
        self.flavor_ingredients = {}
        self.volume = 0
        self.make_ingredient_objects(recipe_strs)
        self.name = self.name_generator(emotion)

    def name_generator(self, emotion: str):
        return str(emotion).capitalize() + " Cookies"
    
    def make_ingredient_objects(self, recipe_strs):
        """Reads recipe_strs and populates self.ingredients with ingredient objects.
           Args:
                recipe_strs (list) : list of the strings corresponding to ingredient/amt in the recipe
        """
        #makes dictionary mapping ingredients to the corresponding amounts
 
        base_ingredient_item = True
        for line in recipe_strs: 
            print(line)
            if line.startswith("-"):
                if "flavors" in line:
                    base_ingredient_item = False
                continue

            information = line.split(" oz ")
            amt = float(information[0])
            name = information[1]

            if base_ingredient_item:
                self.base_ingredients[name] = Ingredient(name, amt)
            else:
                self.flavor_ingredients[name] = Ingredient(name, amt)

    ###Progress After Generator Day
    # def make_ingredient_objects(self, recipe_strs: list):
    #     """Reads recipe_strs and populates self.ingredients with ingredient objects.
    #        Args:
    #             recipe_strs (list) : list of the strings corresponding to ingredient/amt in the recipe
    #     """
    #     # makes dictionary mapping ingredient name to ingredient object
    #     base_ing = False
    #     flavor_ing = False
    #     for line in recipe_strs:
    #         if ("Base" in line): 
    #             base_ing = True
    #         elif ("Flavor" in line):
    #             base_ing = False
    #             flavor_ing = True
    #         information = line.strip().split(" g ")
    #         # check that line describes ingredients
    #         if (len(information) > 1):
    #             ingr_amt = float(information[0])
    #             name = information[1]
    #             new_ing = Ingredient(name, ingr_amt)
    #             self.volume += ingr_amt
    #             if (base_ing):
    #                 self.base_ingredients[name] = new_ing
    #             elif (flavor_ing):
    #                 self.flavor_ingredients[name] = new_ing
    #     print("volume of recipe is " + str(self.volume))

    def change_base_ratio(self):
        """A base ingredient is selected uniformly at random from the recipe.  
        Its quantity is set to a random new value, changing the texture of the cookie.
        """
        # TODO should this incorporate emotions? i.e. happy -> chewy cookies 
        ingredient = np.random.choice(tuple(self.base_ingredients.values()))
        # remove or add up to 100% of original amount 
        new_amt = (random.uniform(-.5,.5) + 1) * ingredient.get_amount()
        ingredient.set_amount(new_amt)
        print("changing base ratio of", ingredient.get_name())

    def add_flavor_ingredient(self, all_ingredients):
        """A flavor ingredient is selected uniformly at random from the inspiring set and added to the recipe. 
        The amount of the new ingredient is determined randomly as a random number between 0 and 100 oz.
        Args:
            all_ingredients (set) : A set containing all unique possible ingredients
        """
        # TODO should use emotion and existing ingredients to generate which flavor to add
        new_possible_ingredients = all_ingredients.difference(self.flavor_ingredients.keys())

        if len(new_possible_ingredients) == 0: #skip if no new ingredients to add
            return

        new_name = random.choice(tuple(new_possible_ingredients))
        # choose a random amount between 0 and 100 oz 
        new_amt = np.random.choice(range(0,100))

        self.flavor_ingredients[new_name] = Ingredient(new_name, new_amt)
        print("adding ", new_name)

    def delete_ingredient(self):
        """A flavor ingredient is selected uniformly at random from the recipe and removed from the recipe.
        """
        if len(self.flavor_ingredients.keys()) > 1:
            selected_ing = random.choice(tuple(self.flavor_ingredients.keys()))
            del self.flavor_ingredients[selected_ing]
            print("deleting " + str(selected_ing))
        else:
            print("Cannot delete: need to have at least one flavoring")


    def swap_ingredient(self):
        """An ingredient is selected uniformly at random from the recipe. Its name attribute 
        is changed to that of another ingredient that is chosen at random from the ones 
        stored in the inspiring set.
        """
        ingre_name_1 = random.choice(tuple(self.flavor_ingredients.keys()))
        ingredient1_amt = self.flavor_ingredients[ingre_name_1].get_amount()

        diff = set(self.flavor_ingredients.keys()).difference(ingre_name_1)
        ingre_name_2 = random.choice(tuple(diff))
        ingredient2_amt = self.flavor_ingredients[ingre_name_2].get_amount()

        print(f"swapping {ingre_name_1} (originally {ingredient1_amt}) and {ingre_name_2} (originally {ingredient2_amt})")

        self.flavor_ingredients[ingre_name_1] = Ingredient(ingre_name_1, ingredient2_amt)
        self.flavor_ingredients[ingre_name_2] = Ingredient(ingre_name_2, ingredient1_amt)
    
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
    
    # def normalize(self):
    #     """Normalizes all ingredients so amount adds up to 100 oz.
    #     """
    #     current_total = 0
    #     for ingredient in self.ingredients.values(): 
    #         current_total += ingredient.get_amount() 
    #     if current_total == 100: #already normalized
    #         return    
    #     sizing_factor = 100 / current_total
    #     for name, ingredient in self.ingredients.items(): 
    #         new_amt = ingredient.get_amount() * sizing_factor
    #         if new_amt < .01: #delete ingredient if normalization makes it below .01 oz
    #             self.ingredients.remove(name)
    #         else:
    #             ingredient.set_amount(new_amt)
        
    def get_fitness(self):
        """Returns fitness score (CURRENT PROB IS THAT INGREDIENTS MAY NOT BE IN FLAVOR PAIRING LIST)
        """
        total_ingredients = flavor_pairing.get_all_ingredients()
        all_ingredient_names = list(self.flavor_ingredients.keys()) + list(self.base_ingredients.keys())
        similarities = []
        for ingredient1 in all_ingredient_names:
            for ingredient2 in all_ingredient_names:
                ingredient1, ingredient2 = ingredient1.strip(), ingredient2.strip()
                if ingredient1 in total_ingredients and ingredient2 in total_ingredients:
                    similarity = flavor_pairing.similarity(ingredient1, ingredient2)
                    similarities.append(similarity)
        avg_similarity = sum(similarities) / len(similarities)
        print("avg similarity is ", avg_similarity)
        return avg_similarity
    
    def get_base_ingredient_strings(self):
        """Returns the ingredients of the recipes as a list of strings
        """
        return [str(ingredient) for ingredient in self.base_ingredients.values()]
    
    def get_base_ingredients(self):
        """Returns the base ingredient list
        """
        return self.base_ingredients.values()
    
    def get_flavor_ingredient_strings(self):
        """Returns the ingredients of the recipes as a list of strings
        """
        return [str(ingredient) for ingredient in self.flavor_ingredients.values()]


    def get_flavor_ingredients(self):
        """Returns the flavor ingredient list
        """
        return self.flavor_ingredients.values()

    
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
        # mutate = np.random.choice([True, False], p=[0.8,0.2])
        mutate = True
        if mutate: 
            mutation = np.random.randint(0,4)
            if mutation == 0: 
                self.change_base_ratio() 
            elif mutation == 1: 
                self.add_flavor_ingredient(all_ingredients)
            elif mutation == 2: 
                self.delete_ingredient()
            elif mutation == 3: 
                self.swap_ingredient()
            # normalize ingredient amounts after mutation 
            # self.normalize()
        print("mutated")
        print("base:")
        print(self.get_base_ingredient_strings())
        print("flavors:")
        print(self.get_flavor_ingredient_strings())

    def __str__(self) -> str:
        return self.get_name()

# def main(): 
#     with open("inspiring-set/cookie-base.txt") as f:
#         recipe_str = f.readlines()
#         recipe = Recipe(recipe_str,"happy")
#         print(recipe.get_base_ingredient_strings())
#         print(recipe.get_flavor_ingredient_strings())
#         all_ingr = {"chocolate chips", "marshmallows", "sprinkles", "cinnamon", "basil"}
#         recipe.mutate(all_ingr)
#         print(recipe.get_base_ingredient_strings())
#         print(recipe.get_flavor_ingredient_strings())
#         print(recipe.get_name())
    
# if __name__ == "__main__":
#     main()