class Ingredient_Parser():
    def __init__(self, ing_strs):
        self.ingr_strs = ingr_strs


        self.base_ingredient_types = {
            "wet": ["egg", "eggs", "milk", "buttermilk"],
            "flour": ["all-purpose", "whole wheat"],
            "dry": ["salt", "baking powder", "baking soda", "cornstarch"],
            "sugars": ["white sugar", "brown sugar", "honey", "molasses"],
            "fats": ["butter", "vegetable oil", "olive oil", "coconut oil"]         
        }
        self.flavor_types = {
            "spices": ["allspice", "cinnamon", "cloves", "cardamom", "ginger", "ground ginger", "nutmeg", "cayenne", 
               "cayenne pepper", "black pepper", "cocoa powder","basil", "mint", "rosemary", "fennel", "thyme", 
               "lavender", "vanilla", "vanilla extract", "almond extract", "butterscotch extract"],
            "mix-ins": ["chocolate chips", "chocolate chunks", "raisins", "sprinkles", "almonds", "walnuts", "pecans",
                "pretzels", "m&ms", "coconut"],
        }
        self.toppings = ["flaky sea salt", "caramel drizzle", "chocolate drizzle", "powder sugar", "crushed nuts"]
    
    



        