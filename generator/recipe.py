import numpy as np
from ingredient import Ingredient
from recipe_instructions import RecipeInstructions
from base_ingredients import BaseIngredients
from flavor_ingredients import FlavorIngredients
from fitness import Fitness


class Recipe:
    def __init__(self, recipe_strs, emot, instructions=RecipeInstructions()):
        self.emotion = emot
        ing_list = self.make_ingredient_list(recipe_strs)
        self.base_ingredients = BaseIngredients(ing_list)
        self.flavor_ingredients = FlavorIngredients(ing_list)
        self.instructions = instructions

        self.name_generator(emot)
        self.fitness = Fitness(self.flavor_ingredients, emot)

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
        
        syn_opts = emotional_repetoire[emotion]
        syn_choice = np.random.choice(syn_opts)       
        self.name = syn_choice + " " + emotion + " Cookies"        
    
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
    
 
    def get_fitness(self, do_print=False):
        self.fitness.set_fitness_val(do_print)
        return self.fitness.get_fitness_val()

    def __str__(self):
        recipe_str = "-" + self.name  + ":\n-Base Ingredients\n" 
        recipe_str += str(self.base_ingredients) + "\n-Flavor Ingredients\n" 
        recipe_str += str(self.flavor_ingredients) + "\n---\nInstructions\n"
        recipe_str += self.format_instructions()
        return recipe_str
    
    def __repr__(self):
        return self.emotion + ", " + repr(self.flavor_ingredients)