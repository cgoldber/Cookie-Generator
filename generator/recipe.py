import numpy as np
from ingredient import Ingredient
from recipe_instructions import RecipeInstructions
from base_ingredients import BaseIngredients
from flavor_ingredients import FlavorIngredients
from fitness import Fitness
from name_generator import Name


class Recipe:
    def __init__(self, recipe_strs, emot, instructions=RecipeInstructions()):
        self.emotion = emot
        self.instructions = instructions

        ing_list = self.make_ingredient_list(recipe_strs)
        self.base_ingredients = BaseIngredients(ing_list)
        self.flavor_ingredients = FlavorIngredients(ing_list)

        self.fitness = Fitness(self.flavor_ingredients, emot) 
        name_obj = Name(self.emotion)
        self.name = name_obj.get_name()
    
    def make_ingredient_list(self, recipe_strs):
        """
        """
        ing_list = []
        for line in recipe_strs: 
            if not line.startswith("-") and line != "":
                split_line = line.split(" ")
                amt = float(split_line[0])
                unit = split_line[1]
                ingr_name = " ".join(split_line[2:]).strip()
                
                if "butter" in ingr_name and unit == "tbsp":
                    amt *= 14.2
                    
                ing_list.append(Ingredient(ingr_name, amt, unit))
        return ing_list
    
    def format_instructions(self):
        """ Returns formatted, step-by-step instructions for the recipe with
        elements from the base ingredient, flavor ingredient, and instruction 
        attributes of the Recipe object. 
        """
        return self.instructions.fill_in_quantities(self)

    def mutate(self):
        """Based on some set probability (20%), returns original recipe 80% of 
        the time. Otherwise, calls for the mutation of the base ingredients, 
        flavor ingredients, or recipe instruction with set probability (20%,
        60%, and 20% respectively).
        """
        mutate = np.random.choice([True, False], p=[0.8,0.2])
        if mutate: 
            self.flavor_ingredients.mutate()       
        mutate = np.random.choice([True, False], p=[0.3,0.7])
        if mutate: 
            self.base_ingredients.mutate()
        mutate = np.random.choice([True, False], p=[0.3,0.7])
        if mutate: 
            self.instructions.mutate()
    
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
 
    def get_fitness(self, do_print=False):
        self.fitness.set_fitness_val(do_print=do_print)
        return self.fitness.get_fitness_val()

    def __str__(self):
        recipe_str = ("-" + self.name  + ":\n-Base Ingredients\n" + 
        str(self.base_ingredients) + "\n-Flavor Ingredients\n" +
        str(self.flavor_ingredients) + "\n---\nInstructions\n" + 
        self.format_instructions())
        return recipe_str
    
    def __repr__(self):
        return self.emotion + ", " + repr(self.flavor_ingredients)