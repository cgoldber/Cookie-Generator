import numpy as np
import random
from ingredient import Ingredient


INGREDIENT_TYPES = {
    "spices": ["allspice", "cinnamon", "clove", "cardamom", "ginger",  "nutmeg", 
               "black pepper", "cocoa", "basil", 
               "mint", "rosemary", "fennel", "thyme", "coriander","turmeric",
               "anise","chamomile","chive","spearmint",
               "thyme", "black tea","green tea","sage","parsley", 
               "garlic", "flaxseed","dill","cocoa","coffee","cumin",
               "oregano",],
    "mix-ins": ["apple", "apricot", "banana",  "beetroot", 
                "black raspberry", "blackberry", "blueberry", "brazil nut", 
                "camembert cheese", "cashew nut", "cherry", 
                "chestnut", "chocolate", "citrus", "citrus zest", "coconut",
                "corn", "cottage cheese", "cranberry", 
                "cream cheese", "currant", "dates", "elderberry", 
                "fig", "goat cheese", "grape", "grapefruit", 
                "grapefruit zest", "gruyere cheese", "guava", "hazelnut", 
                "kiwifruit", "lemon", "lemon balm", "lemon zest", "licorice", 
                "lime", "lime zest", "macadamia nut", "mandarin orange", 
                "mandarin orange zest", "mango", "melon", "nut", "oats", 
                "orange", "papaya", "parmesan cheese", 
                "passionfruit", "peach", "peanut", "peanut butter", "pear", 
                "pecan", "persimmon", "pineapple", "pistachio", "plum", 
                "pomegranate", "poppy seed",  "pumpkin", "raisin", "raspberry", 
                "rhubarb", "rose",  "starfruit", "strawberry", "sunflower", 
                "tamarind", "tangerine", "walnut", "wasabi", "zucchini"],
    "oils": ["lavender", "soy sauce", "vanilla","peppermint"],
    "toppings": ["flaky sea salt", "caramel drizzle", "honey", "citrus zest"]
}


class FlavorIngredients: 
    def __init__(self, ing_list): 
        self.spices = {}
        self.mix_ins = {}
        self.oils = {}
        self.toppings = {}

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
            elif name in INGREDIENT_TYPES["toppings"]: 
                self.toppings[name] = ing
            elif name in INGREDIENT_TYPES["oils"]: 
                self.oils[name] = ing


    def add_ingredient(self):
        """ With equal probability, add a new spice or a new mix-in
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
        elif prob == 2:
            new_oil = np.random.choice(tuple(INGREDIENT_TYPES["oils"]))
            amt = random.randint(1,4) * 0.5
            new_ing = Ingredient(new_oil, amt, "tsp")
            self.oils[new_oil] = new_ing
        else: 
            new_topping = np.random.choice(tuple(INGREDIENT_TYPES["toppings"]))
            amt = random.randint(1,4) * 25
            new_ing = Ingredient(new_oil, amt)
            self.toppings[new_topping] = new_ing



    def delete_ingredient(self):
        """ With equal probability, delete a spice or mix-in
        """
        prob = np.random.randint(0,1)
        if prob == 0 and len(self.spices.keys()) > 0:
            spice = np.random.choice(tuple(self.spices.keys()))
            del self.spices[spice]
        elif len(self.mix_ins.keys()) > 0: 
            mix_in = np.random.choice(tuple(self.mix_ins.keys()))
            del self.mix_ins[mix_in]

    def swap_ingredient(self):
        """ With equal probability, swap a spice or mix-in with a new spice or mix-in
        """
        prob = np.random.randint(0,1)
        if prob == 0 and len(self.spices.keys()) > 0:
            spice = np.random.choice(tuple(self.spices.keys()))
            del self.spices[spice]
            new_spice = np.random.choice(tuple(INGREDIENT_TYPES["spices"]))
            # preset volume to 0.5 oz 
            new_ing = Ingredient(new_spice, .5, "tsp")
            self.spices[new_spice] = new_ing
        elif len(self.mix_ins.keys()) > 0: 
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

    def get_flavor_ing_names(self):
        """ Returns a list of non-topping flavors to be evaluated with a flavor
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
        all_types = [self.spices, self.mix_ins, self.oils, self.toppings]
        for flav_type in all_types:
            if ingr_name in flav_type.keys():
                return flav_type[ingr_name].get_amount()
        return -1
    
    def get_mix_in(self):
        return ", ".join(self.mix_ins.keys())
    
    def get_oil(self):
        return ", ".join(self.oils.keys())
    
    def get_topping(self):
        return ", ".join(self.toppings.keys())
    
    def get_spice(self):
        return ", ".join(self.spices.keys())

    def __str__(self):
        ing_list = []
        for ing in self.spices.values():
            ing_list.append(str(ing))
        for ing in self.mix_ins.values():
            ing_list.append(str(ing))
        for ing in self.oils.values():
            ing_list.append(str(ing))
        for ing in self.toppings.values():
            ing_list.append(str(ing))
        return "\n".join(ing_list)
    
    def __repr__(self) -> str:
        spices_list = "Spices: " + ", ".join([str(ing) for ing in self.spices.values()]) + ", "
        mix_ins_list = "Mix-Ins: " + ", ".join([str(ing) for ing in self.mix_ins.values()]) + ", "
        oils_list = "Oils: " + ", ".join([str(ing) for ing in self.oils.values()]) + ", "
        toppings_list = "Toppings: " + ", ".join([str(ing) for ing in self.toppings.values()]) + ", "
        return spices_list + mix_ins_list + oils_list + toppings_list