import numpy as np
import random
from ingredient import Ingredient


INGREDIENT_TYPES = {
    "spices": ["allspice", "cinnamon", "clove", "cardamom", "ginger", "nutmeg", 
               "black pepper", "cocoa", "basil", "mint", "rosemary", "fennel", 
               "thyme", "coriander","turmeric", "anise","chamomile","chive",
               "spearmint", "lemon", "lemon balm", "lemon zest", "grapefruit", 
               "lime", "lime zest", "grapefruit zest", "mandarin orange", 
               "citrus zest", "mandarin orange zest", "thyme", "black tea",
               "green tea","sage","parsley", "poppy seed", "garlic", "flaxseed",
               "dill", "cocoa", "coffee", "cumin", "oregano", "wasabi"],
    "mix-ins": ["apple", "apricot", "banana",  "beetroot", "black raspberry", 
                "blackberry", "blueberry", "brazil nut", "camembert cheese", 
                "cashew nut", "cherry", "chestnut", "chocolate", "citrus", 
                "coconut", "corn", "cranberry", "cream cheese", "currant", 
                "dates", "elderberry", "fig", "goat cheese", "grape", 
                "gruyere cheese", "guava", "hazelnut", "kiwifruit", "licorice", 
                "macadamia nut", "mango", "melon", "nut", "oats", "orange", 
                "papaya", "parmesan cheese", "passionfruit", "peach", "peanut", 
                "peanut butter", "pear", "pecan", "persimmon", "pineapple", 
                "pistachio", "plum", "pomegranate", "pumpkin", "raisin", 
                "raspberry", "rhubarb", "starfruit", "strawberry", "sunflower", 
                "tamarind", "tangerine", "walnut", "zucchini"],
    "oils": ["lavender", "soy sauce", "vanilla","peppermint"],
}


class FlavorIngredients: 
    """ Need to write 
    """
    def __init__(self, ing_list): 
        self.spices = {}
        self.mix_ins = {}
        self.oils = {}
        self.sort_ingredients(ing_list)
    
    def sort_ingredients(self, ing_list):
        """ From a list of flavors in the recipe, sort into either spices 
        (including cinnamon, pepper, basil, etc.) or mix-ins (including 
        chocolate chips, nuts, dried fruit, etc.). Note that spices will have 
        a much
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
            elif name in INGREDIENT_TYPES["oils"]: 
                self.oils[name] = ing


    def add_ingredient(self):
        """ With equal probability, add a new spice, mix-in, or oil to their 
        respective dictionaries from the constant list INGREDIENT_TYPES. If
        adding a mix-in, normalize the amount. 
        """
        prob = np.random.randint(0,3)
        if prob == 0:
            new_spice = np.random.choice(tuple(INGREDIENT_TYPES["spices"]))
            amt = random.randint(1,4) * 0.5
            new_ing = Ingredient(new_spice, amt, "tsp")
            self.spices[new_spice] = new_ing
        elif prob == 1: 
            new_mix_in = np.random.choice(tuple(INGREDIENT_TYPES["mix-ins"]))
            amt = random.randint(1,4) * 50
            new_ing = Ingredient(new_mix_in, amt)
            self.mix_ins[new_mix_in] = new_ing
            self.normalize_mix_in_amt()
        elif prob == 2:
            new_oil = np.random.choice(tuple(INGREDIENT_TYPES["oils"]))
            amt = random.randint(1,4) * 0.5
            new_ing = Ingredient(new_oil, amt, "tsp")
            self.oils[new_oil] = new_ing

    def delete_ingredient(self):
        """ With equal probability, delete a spice or mix-in from their 
        respective dictionaries. 
        """
        prob = np.random.randint(0,1)
        if prob == 0 and len(self.spices.keys()) > 0:
            spice = np.random.choice(tuple(self.spices.keys()))
            del self.spices[spice]
        elif len(self.mix_ins.keys()) > 0: 
            mix_in = np.random.choice(tuple(self.mix_ins.keys()))
            del self.mix_ins[mix_in]

    def swap_ingredient(self):
        """ With equal probability, swap a spice or mix-in from their 
        respective dictionaries with a new spice or mix-in from the constant
        list INGREDIENT_TYPES.
        """
        prob = np.random.randint(0,1)
        if prob == 0 and len(self.spices.keys()) > 0:
            spice = np.random.choice(tuple(self.spices.keys()))
            del self.spices[spice]
            new_spice = np.random.choice(tuple(INGREDIENT_TYPES["spices"]))
            # preset volume to 0.5 tsp 
            new_ing = Ingredient(new_spice, .5, "tsp")
            self.spices[new_spice] = new_ing
        elif len(self.mix_ins.keys()) > 0: 
            mix_in = np.random.choice(tuple(self.mix_ins.keys()))
            del self.mix_ins[mix_in]
            new_mix_in = np.random.choice(tuple(INGREDIENT_TYPES["mix-ins"]))
            # preset volume to 50 g
            new_ing = Ingredient(new_mix_in, 50)
            self.mix_ins[new_mix_in] = new_ing

    def normalize_mix_in_amt(self):
        """ After adding a new mix-in ingredient, normalize to ensure the total
        mix-in volume is not greater than 250 grams.
        """
        volume = 0
        for mix_in in self.mix_ins.values():
            volume += mix_in.get_amount()
        if volume <= 250:
            return
        multiplier = 250 / volume
        for mix_in in self.mix_ins.values():
            amt = mix_in.get_amount() * multiplier
            mix_in.set_amount(amt)

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

    def get_flavor_ing_names(self):
        """ Returns a list of flavors to be evaluated with a flavor
        pairing score in the Recipe class.
        """
        ing_list = []
        for ing in self.spices.values():
            ing_list.append(ing.get_name())
        for ing in self.mix_ins.values():
            ing_list.append(ing.get_name())
        for ing in self.oils.values():
            ing_list.append(ing.get_name())
        return ing_list

    def get_amount_byname(self, ingr_name):
        """ Search for the amount of flavor ingredient with the flavor 
        ingredient string, returning the amount if the ingredient exists. 
        Otherwise return -1. 
            Args:
            ingr_name : string name of ingredient
        """
        all_types = [self.spices, self.mix_ins, self.oils]
        for flav_type in all_types:
            if ingr_name in flav_type.keys():
                return flav_type[ingr_name].get_amount()
        return -1
    
    def get_mix_in(self):
        """ String representation of mix-ins, separated by commas, to be 
        written in the final recipe instructions
        """
        return ", ".join(self.mix_ins.keys())
    
    def get_oil(self):
        """ String representation of oils, separated by commas, to be written 
        in the final recipe instructions
        """
        return ", ".join(self.oils.keys())
        
    def get_spice(self):
        """ String representation of spices, separated by commas, to be written 
        in the final recipe instructions
        """
        return ", ".join(self.spices.keys())

    def __str__(self):
        """ String representation of flavor ingredients as a list of string 
        representation of Ingredient objects, separated by line breaks. To be 
        used by in the string representation of a Recipe object. 
        """
        ing_list = []
        for ing in self.spices.values():
            ing_list.append(str(ing))
        for ing in self.mix_ins.values():
            ing_list.append(str(ing))
        for ing in self.oils.values():
            ing_list.append(str(ing))
        return "\n".join(ing_list)
    
    def __repr__(self):
        """ String representation of flavor ingredients as a list of string 
        representation of Ingredient objects, divided by characters and 
        separated by commas. To be used when debugging. 
        """
        spices_list = "Spices: " + ", ".join(\
            [str(ing) for ing in self.spices.values()]) + ", "
        mix_ins_list = "Mix-Ins: " + ", ".join(\
            [str(ing) for ing in self.mix_ins.values()]) + ", "
        oils_list = "Oils: " + ", ".join(\
            [str(ing) for ing in self.oils.values()]) + ", "
        return spices_list + mix_ins_list + oils_list 