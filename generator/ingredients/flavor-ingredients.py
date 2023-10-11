import numpy as np
from ingredient import Ingredient

INGREDIENT_TYPES = {
    "spices": ["allspice", "cinnamon", "cloves", "cardamom", "ginger", "ground ginger", "nutmeg", "cayenne", 
               "cayenne pepper", "black pepper", "cocoa powder","basil", "mint", "rosemary", "fennel", "thyme", 
               "lavender", "vanilla", "vanilla extract", "almond extract", "butterscotch extract"],
    "mix-ins": ["chocolate chips", "chocolate chunks", "raisins", "sprinkles", "almonds", "walnuts", "pecans",
                "pretzels", "m&ms", "coconut"],
}

class FlavorIngredients: 
    def __init__(self, ing_list): 
        self.spices = {}
        self.mix_ins = {}
        self.sort_ingredients(ing_list)
    
    def sort_ingredients(self, ing_list):
        """ From a list of flavors in the recipe, sort into either spices (including cinnamon, chili powder, almond extract, 
        basil, etc.) or mix-ins (including chocolate chips, nuts, dried fruit, etc.). Note that spices will have a much
        smaller volume compared to mix-ins.
            Args: 
            ing_list (list) : list of ingredients
        """
        for ing in ing_list: 
            name = ing.get_name().lower()
            if name in INGREDIENT_TYPES["spices"]: 
                self.spices[name] = ing
            elif name in INGREDIENT_TYPES["mix-ins"]: 
                self.mix_ins[name] = ing


    def add_ingredient(self):
        """ With equal probability, add a new spice or a new mix-in
        """
        prob = np.random.randint(0,1)
        if prob == 0:
            new_spice = np.random.choice(tuple(INGREDIENT_TYPES["spices"]))
            new_ing = Ingredient(new_spice, .5)
            self.spices[new_spice] = new_ing
        else: 
            new_mix_in = np.random.choice(tuple(INGREDIENT_TYPES["mix-ins"]))
            new_ing = Ingredient(new_mix_in, 50)
            self.mix_ins[new_mix_in] = new_ing


    def delete_ingredient(self):
        """ With equal probability, delete a spice or mix-in
        """
        prob = np.random.randint(0,1)
        if prob == 0:
            spice = np.random.choice(tuple(self.spices.keys()))
            del self.spices[spice]
        else: 
            mix_in = np.random.choice(tuple(self.mix_ins.keys()))
            del self.mix_ins[mix_in]


    def swap_ingredient(self):
        """ With equal probability, swap a spice or mix-in with a new spice or mix-in
        """
        prob = np.random.randint(0,1)
        if prob == 0:
            spice = np.random.choice(tuple(self.spices.keys()))
            del self.spices[spice]
            new_spice = np.random.choice(tuple(INGREDIENT_TYPES["spices"]))
            # preset volume to 0.5 oz 
            new_ing = Ingredient(new_spice, .5)
            self.spices[new_spice] = new_ing
        else: 
            mix_in = np.random.choice(tuple(self.mix_ins.keys()))
            del self.mix_ins[mix_in]
            new_mix_in = np.random.choice(tuple(INGREDIENT_TYPES["mix-ins"]))
            # preset volume to 50 oz
            new_ing = Ingredient(new_mix_in, 50)
            self.mix_ins[new_mix_in] = new_ing


    def mutate(self):
        """ Calls an above mutation with equal probability.
        """
        mutation = np.random.randint(0,3)
        if mutation == 0: 
            self.add_ingredient() 
        elif mutation == 1: 
            self.delete_ingredient()
        elif mutation == 2: 
            self.swap_ingredient()