import numpy as np
from generator.ingredient import Ingredient


INGREDIENT_TYPES = {
    "spices": ["allspice", "cinnamon", "clove", "cardamom", "ginger",  "nutmeg", 
               "cayenne", "cayenne pepper", "black pepper", "cocoa", "basil", 
               "mint", "rosemary", "fennel", "thyme", "coriander","turmeric",
               "anise","chamomile","chive","mustard","peppermint","spearmint",
               "thyme", "black tea","green tea","tea","sage","parsley", 
               "garlic", "flaxseed","dill","cocoa","beetroot","coffee","cumin",
               "oregano",],
    "mix-ins": ["apple", "apricot", "artichoke", "banana",  "beetroot", 
                "black raspberry", "blackberry", "blueberry", "brazil nut", 
                "camembert cheese", "capers", "cashew nut", "cherry", 
                "chestnut", "chocolate", "citrus", "citrus zest", "coconut",
                "comte cheese", "corn", "cottage cheese", "cranberry", 
                "cream cheese", "cucumber", "currant", "dates", "elderberry", 
                "fig", "garlic", "goat cheese", "grape", "grapefruit", 
                "grapefruit zest", "gruyere cheese", "guava", "hazelnut", 
                "kiwifruit", "lemon", "lemon balm", "lemon zest", "licorice", 
                "lime", "lime zest", "macadamia nut", "mandarin orange", 
                "mandarin orange zest", "mango", "melon", "nut", "oats", 
                "olive", "onion", "orange", "papaya", "parmesan cheese", 
                "passionfruit", "peach", "peanut", "peanut butter", "pear", 
                "pecan", "persimmon", "pineapple", "pistachio", "plum", 
                "pomegranate", "poppy seed",  "pumpkin", "raisin", "raspberry", 
                "rhubarb", "rose",  "starfruit", "strawberry", "sunflower", 
                "tamarind", "tangerine", "walnut", "wasabi", "zucchini"],
    "oils": ["lavender", "soy sauce", "vanilla", "almond"],
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
        spices_list = "Spices:\n" + "\n".join([str(ing) for ing in self.spices.values()])
        mix_ins_list = "Mix-Ins:\n" + "\n".join([str(ing) for ing in self.mix_ins.values()])
        oils_list = "Oils:\n" + "\n".join([str(ing) for ing in self.oils.values()])
        toppings_list = "Toppings:\n" + "\n".join([str(ing) for ing in self.toppings.values()])
        return spices_list + mix_ins_list + oils_list + toppings_list