import numpy as np
from ingredient import Ingredient
from recipe_instructions import RecipeInstructions
from base_ingredients import BaseIngredients
from flavor_ingredients import FlavorIngredients
from fitness import Fitness
from name_generator import Name


class Recipe:
    """ A class to represent a recipe.

    ...

    Attributes
    ----------
    emotion : strin
        The user's emotion that the recipe is inspired by.
    instructions : RecipeInstructions
        The instructions for baking this recipe.
    base_ingredients : BaseIngredients
        Stores and performs operations on the recipe's base ingredients.
    flavor_ingredients : FlavorIngredients
        Stores and performs operations on the recipe's flavor ingredients.
    fitness : float
        Stores and computes the recipe's fitness score.
    name : String
        The recipe's name.

    Methods
    -------
    make_ingredient_list():
        Converts string representation of recipe into list of Ingredient 
        objects.
    format_instructions():
        Returns recipe's baking instructions with filled in quantities.
    mutate():
        Potentially calls to mutate recipe's flavor ingredients, 
        base ingredients, or baking instructions.
    get_base_ing_strings():
        Returns base ingredients as strings.
    get_flavor_ing_strings():
        Returns flavor ingredients as strings.
    get_flavor_ingredients():
        Returns recipe's flavor ingredient objects.
    get_instructions():
        Returns recipe's baking instructions.
    get_name():
        Returns recipe's name.
    get_fitness():
        Returns recipe's fitness score.
    """

    def __init__(self, recipe_strs, emot, instructions=""):
        """ Creates recipe based on user's emotion, the instructions for baking
            the recipe, and populates the recipe's ingredient storage objects.
            Args:
                recipe_strs (list) : list of ingredient strings to be converted
                                     into ingredient objects
                emot (string) : the user's current emotion
                instructions (RecipeInstructions) : the instructions for baking
                                                    this recipe
        """
        self.emotion = emot

        ing_list = self.make_ingredient_list(recipe_strs)
        self.base_ingredients = BaseIngredients(ing_list)
        self.flavor_ingredients = FlavorIngredients(ing_list)

        self.fitness = Fitness(self.flavor_ingredients, emot)
        name_obj = Name(emot)
        self.name = name_obj.get_name()

        if instructions == "":
            self.instructions = RecipeInstructions(emot)
        else:
            self.instructions = instructions

    
    def make_ingredient_list(self, recipe_strs):
        """ Reads the string representation of a recipe and converts each
            ingredient to an Ingredient object, storing it in ing_list.
            Args:
                recipe_strs (list) : the strings representing the recipe
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
            elements from the base ingredient, flavor ingredient, and 
            instruction attributes of the Recipe object. 
        """
        return self.instructions.fill_in_quantities(self)

    def mutate(self):
        """ Based on some set probability (20%), returns original recipe 80% of 
            the time. Otherwise, calls for the mutation of the base 
            ingredients, flavor ingredients, or recipe instruction with set 
            probability (20%, 60%, and 20% respectively).
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
        """ Returns base ingredients as strings.
        """
        return str(self.base_ingredients).split("\n")
    
    def get_flavor_ing_strings(self): 
        """ Returns flavor ingredients as strings.
        """
        return str(self.flavor_ingredients).split("\n")

    def get_flavor_ingredients(self):
        """ Returns the flavor ingredient list.
        """
        return self.flavor_ingredients.values()
    
    def get_instructions(self):
        """ Returns RecipeInstruction object. 
        """
        return self.instructions

    def get_name(self):
        """ Makes Name object to compute name and returns string 
            representation.
        """
        name_obj = Name(self.emotion)
        return name_obj.get_name()
 
    def get_fitness(self, do_print=False):
        """ Calls for fitness computation and returns it.
        """
        self.fitness.set_fitness_val(do_print=do_print)
        return self.fitness.get_fitness_val()

    def __str__(self):
        """ String representaiton of recipe.
        """
        recipe_str = ("-" + self.name  + ":\n-Base Ingredients\n" + 
        str(self.base_ingredients) + "\n-Flavor Ingredients\n" +
        str(self.flavor_ingredients) + "\n---\nInstructions\n" + 
        self.format_instructions())
        return recipe_str
    
    def __repr__(self):
        """ String representation of recipe for debugging.
        """
        return self.emotion + ", " + repr(self.flavor_ingredients)