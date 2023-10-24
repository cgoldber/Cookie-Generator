import numpy as np
import random
from ingredient import Ingredient

BASE_INGREDIENT_TYPES = {
    "wet": ["egg", "eggs", "milk", "buttermilk"],
    "flour": ["all-purpose", "whole wheat"],
    "dry": ["kosher salt", "salt", "baking powder", "baking soda", 
            "cornstarch"],
    "sugars": ["white sugar", "brown sugar", "honey", "molasses"],
    "fats": ["butter", "vegetable oil", "olive oil", "coconut oil"]
}


class BaseIngredients: 
    """ A class to represent base ingredients in a recipe.

    ...

    Attributes
    ----------
    wet : dict
        wet bases in the recipe's ingredients
    flour : dict
        types of flour in the recipe's ingredients
    dry : dict
        dry ingredients in the recipe's ingredients
    sugars : dict
        types of surgars in the recipe's ingredients
    fats : dict
        types of fats in the recipe's ingredients
    
    Methods
    -------
    sort_ingredients():
        Sorts ingredients into base ingredient categories.
    adjust_base_ratios():
        Adjusts the ratios of sugar to flour to fat.
    adjust_sugar_ratios():
        Changes ratios of types of sugars.
    adjust_fat_ratios():
        Changes ratios between the types of fats.
    adjust_eggs():
        Changes amount of eggs in the recipe.
    mutate():
        Chooses any of the mutations above with equal probability.
    change_base_type_volume(base _type, change):
        Takes in a base type and how much it's being changed by and adjusts the
        rest of recipe to keep it's same ratios.
    get_dry():
        Gets string representation of dry ingredients for recipe instructions.
    get_sugar():
        Gets string representation of sugars for recipe instructions.
    get_fat():
        Gets string representation of fats ingredients for recipe instructions.
    get_wet():
        Gets string representation of wet ingredients for recipe instructions.
    """

    def __init__(self, ing_list): 
        """ Initializes the base ingredients quantities to 0 and then uses
            given ingredient list to create and store various Ingredient
            objects that are of type base.
            Args:
                ing_list (list) : list of ingredient objects
        """
        self.wet = {}
        self.flour = {}
        self.dry = {}
        self.sugars = {}
        self.fats = {}
        self.base_ratio = {"sugar": 0, "flour": 0, "fat": 0}
        self.base_volumes = {"sugar": 0, "flour": 0, "fat": 0}
        self.volume = 0
        self.sort_ingredients(ing_list)
    
    def sort_ingredients(self, ing_list):
        """ Iterates through given ingredient objects and stores the ingredient
            name and its associated amount into the dictionary corresponding to
            what type of ingredient it is (wet, flour, etc). Also keeps
            track of volumes of different types of base ingredients.
            Args: 
                ing_list (list) : stores ingredients as Ingredient objects
        """
        sugar_volume = 0
        flour_volume = 0
        fats_volume = 0
        for ing in ing_list: 
            name = ing.get_name().lower()
            if "sugar" in name or name in BASE_INGREDIENT_TYPES["sugars"]: 
                self.sugars[name] = ing
                self.base_volumes["sugar"] += ing.get_amount()
                sugar_volume += ing.get_amount() 
            elif "flour" in name: 
                self.flour[name] = ing
                flour_volume += ing.get_amount()
                self.base_volumes["flour"] += ing.get_amount()
            elif name in BASE_INGREDIENT_TYPES["dry"]: 
                self.dry[name] = ing
            elif name in BASE_INGREDIENT_TYPES["wet"]: 
                self.wet[name] = ing
            elif ("butter" in name and "peanut" not in name) \
                or name in BASE_INGREDIENT_TYPES["fats"]: 
                self.fats[name] = ing
                self.base_volumes["fat"] += ing.get_amount()
                fats_volume += ing.get_amount()
            self.volume += ing.get_amount()
        
        #ensures the ratio between flavor types is consistent
        if sugar_volume != 0:
            self.base_ratio["sugar"] = (sugar_volume / sugar_volume) * 2 
            self.base_ratio["flour"] = (flour_volume / sugar_volume) * 2
            self.base_ratio["fat"] = (fats_volume / sugar_volume) * 2

    def adjust_base_ratios(self):
        """ Change ratio of sugar to flour to fat, maintaining 1-2 parts sugar, 
            1-2 parts fat, 1-3 parts flour. Updates ratios at the end for 
            future mutations and applies new ratio as a volume change to each 
            base type (sugar, flour, or fats). 
        """
        # choose base type to adjust
        mutation = np.random.randint(0,3)
        if mutation == 0: 
            # adjust sugar ratio
            base_type = "sugar"
        elif mutation == 1: 
            # adjust fat ratio
            base_type = "fat"
        elif mutation == 2: 
            # adjust flour ratio
            base_type = "flour"
        new_ratio = (random.uniform(-.5,.5) + 1) * self.base_ratio[base_type]
        multiplier = new_ratio / self.base_ratio[base_type]
        # apply new ratio to change volumes
        for key in self.base_ratio.keys(): 
            if key == base_type: 
                change_in_vol = (multiplier - 1) * self.base_volumes[base_type]
            else: 
                change_in_vol = \
                -((multiplier - 1) * self.base_volumes[base_type]) / 2
            self.change_base_type_volume(key, change_in_vol)
        for key in self.base_ratio.keys(): 
            self.base_ratio[key] = \
            2 * self.base_volumes[key] / self.base_volumes["sugar"]
 
    def adjust_sugar_ratios(self):
        """ Adjust types and ratios of two sugars in the sugar dictionary
            by a random percentage.
        """
        if len(self.sugars) <= 1: 
            return 
        percent = random.uniform(0,1)
        sugar_1 = np.random.choice(tuple(self.sugars.values()))
        sugar_2 = np.random.choice(tuple(self.sugars.values()))
        new_amt = percent
        sugar_1_amt = sugar_1.get_amount()
        sugar_2_amt = sugar_2.get_amount()
        if sugar_1_amt <= sugar_2_amt: 
            new_amt *= sugar_1_amt
            sugar_1.set_amount(sugar_1_amt + new_amt)
            sugar_2.set_amount(sugar_2_amt - new_amt)
        else: 
            new_amt *= sugar_2_amt
            sugar_1.set_amount(sugar_1_amt - new_amt)
            sugar_2.set_amount(sugar_2_amt + new_amt)

    def adjust_fat_ratios(self):
        """ Adjust types and ratios of two fats in the fats dictionary by a
            random percentage.
        """
        if len(self.fats) <= 1: 
            return 
        percent = random.uniform(0,1)
        fat_1 = np.random.choice(tuple(self.fats.values()))
        fat_2 = np.random.choice(tuple(self.fats.values()))
        new_amt = percent
        fat_1_amt = fat_1.get_amount()
        fat_2_amt = fat_2.get_amount()
        if fat_1_amt <= fat_2_amt: 
            new_amt *= fat_1_amt
            fat_1.set_amount(fat_1_amt + new_amt)
            fat_2.set_amount(fat_2_amt - new_amt)
        else: 
            new_amt *= fat_2_amt
            fat_1.set_amount(fat_1_amt - new_amt)
            fat_2.set_amount(fat_2_amt + new_amt)

    def adjust_eggs(self): 
        """ Adjust ratio of eggs between 1 and 2 eggs (based on random
            probability), where each egg is 50g.
        """
        num_eggs = np.random.randint(1,3)
        if "egg" in self.wet.keys(): 
            self.wet["egg"] = Ingredient("egg", 50 * num_eggs)
        elif "eggs" in self.wet.keys():
            self.wet["eggs"] = Ingredient("eggs", 50 * num_eggs)

    def change_base_type_volume(self, base_type, change):
        """ Normalizes volume of a base type (sugar, flour, fat) by evenly 
            distributing the change across all elements of the dictionary, 
            updating total volume for that base type at the same time.
            Args:
                base_type (string) : either "sugar", "flour", or "fat"
                change (int) : num that total base type volume will change by
        """
        new_volume = 0
        if base_type == "sugar": 
            per_ing_change = change / len(self.sugars.keys())
            for ing in self.sugars.values(): 
                ing_volume = ing.get_amount() + per_ing_change
                ing.set_amount(ing_volume)
                new_volume += ing_volume
        elif base_type == "fat":
            per_ing_change = change / len(self.fats.keys())
            for ing in self.fats.values(): 
                ing_volume = ing.get_amount() + per_ing_change
                ing.set_amount(ing_volume)
                new_volume += ing_volume
        elif base_type == "flour":
            per_ing_change = change / len(self.flour.keys())
            for ing in self.flour.values(): 
                ing_volume = ing.get_amount() + per_ing_change
                ing.set_amount(ing_volume)
                new_volume += ing_volume
        self.base_volumes[base_type] = new_volume
    
    def mutate(self):
        """ Calls an above mutation based on a rangom probability, defaulting 
            to adjusting base ratios if other mutations cannot be called.
        """
        mutation = np.random.randint(0,4)
        if mutation == 0: 
            self.adjust_base_ratios() 
        elif mutation == 1 and len(self.sugars.keys()) > 1: 
            self.adjust_sugar_ratios()
        elif mutation == 2 and len(self.fats.keys()) > 1: 
            self.adjust_fat_ratios()
        elif mutation == 3: 
            self.adjust_eggs()
        else: 
            self.adjust_base_ratios()
    
    def get_dry(self):
        """ String representation of dry ingredients, separated by commas, to 
            be written in the final recipe instructions.
        """
        return ", ".join(self.dry.keys())
    
    def get_sugar(self):
        """ String representation of sugars, separated by commas, to be written 
            in the final recipe instructions.
        """
        return ", ".join(self.sugars.keys())
    
    def get_fat(self):
        """ String representation of fats, separated by commas, to be written 
            in the final recipe instructions.
        """
        return ", ".join(self.fats.keys())
    
    def get_wet(self):
        """ String representation of wet ingredients, separated by commas, to 
            be written in the final recipe instructions.
        """
        return ", ".join(self.wet.keys())

    def __str__(self):
        """ String representation of base ingredients as a list of string 
            representation of Ingredient objects, separated by line breaks. To
            be used by in the string representation of a Recipe object. 
        """
        ing_list = []
        for ing in self.flour.values():
            ing_list.append(str(ing))
        for ing in self.sugars.values():
            ing_list.append(str(ing))
        for ing in self.fats.values():
            ing_list.append(str(ing))
        for ing in self.dry.values():
            ing_list.append(str(ing))
        for ing in self.wet.values():
            ing_list.append(str(ing))
        return "\n".join(ing_list)
    
    def __repr__(self) -> str:
        """ String representation of base ingredients as a list of string 
            representation of Ingredient objects, divided by characters and 
            separated by commas. To be used when debugging. 
        """
        flour_list = "Flours: " + ", ".join(\
            [str(ing) for ing in self.flour.values()]) + ", "
        sugar_list = "Sugars: " + ", ".join(\
            [str(ing) for ing in self.sugars.values()]) + ", "
        fats_list = "Fats: " + ", ".join(\
            [str(ing) for ing in self.fats.values()]) + ", "
        dry_list = "Dry Ingredients: " + ", ".join(\
            [str(ing) for ing in self.dry.values()]) + ", "
        wet_list = "Wet Ingredients: " + ", ".join(\
            [str(ing) for ing in self.wet.values()])
        return flour_list + sugar_list + fats_list + dry_list + wet_list
