import numpy as np
import os
from recipe import Recipe

class RecipeManager():
    """Run generation and evaluation"""
    def __init__(self):
        self.recipes = []
        self.num_new_recipes = 0
        self.all_ingredients = set() # inspiring set of unique ingredients 
    
    def parse_files(self):
        """ Read file of recipes and populates recipe list with recipe object,
        passing in a list representation of recipe.
        """
        print("Reading Initial Recipe Files")
        dir = "inspiring-set"
        for file in os.listdir(dir):
            with open(dir + "/" + file, "r") as f:
                recipe_str = f.readlines()
                self.recipes.append(Recipe(self.num_new_recipes, recipe_str))
            self.num_new_recipes += 1

    def get_unique_ingredients(self):
        """ Iterates through all of the recipe objects and gets all of the unique ingredients.
        """
        for recipe in self.recipes:
            ingredients = recipe.get_ingredients()
            for ingredient in ingredients:
                self.all_ingredients.add(ingredient.get_name())
        print(f"There are {len(self.all_ingredients)} possible ingredients in the inspiring set")

    def crossover(self, recipe1, recipe2):
        """Chooses a random pivot index to concatenate the recipes. Creates a new recipe object. Then
        calls the mutate function on the new recipe and stores what's returned.
            Args:
                recipe1 (Recipe) : first recipe to be crossed
                recipe2 (Recipe) : second recipe to be crossed
        """
        #randomly select pivot
        shortest_recipe_len = min((recipe1.get_fitness()), (recipe2.get_fitness()))
        pivot = np.random.randint(0, shortest_recipe_len)

        #split the recipes based on the pivot and make a new recipe
        recipe1_strs = recipe1.get_ingredient_strings()
        recipe2_strs = recipe2.get_ingredient_strings()
        cross = recipe1_strs[:pivot] + recipe2_strs[pivot:]

        newRecipe = Recipe(self.num_new_recipes, cross)
        self.num_new_recipes += 1

        #call recipe to be potentially mutated
        newRecipe.mutate(self.all_ingredients)
        return newRecipe
    
    def fittest_half(self, recipes):
        """ Returns the fittest 50% of a given population.
            Args:
                recipes (list) : list of recipes
        """
        sorted_recipes = sorted(recipes, key = lambda x : x.get_fitness())
        return sorted_recipes[int(len(recipes)/2):]

    def genetic_algo(self):
        """ Iterate len(self.recipes) times. Choose recipe1 and recipe2 based on fitness probabilites
        and cross them over (making new recipe object). Then it's going to call the mutate function on
        it and stores all of the new recipes in new_recipes. At the end, it is going to taking the top
        50% of the new and old recipes and store it in self.recipes. 
        """
        new_recipes = []
        for _ in range(len(self.recipes)):
            #chooses two recipes based on probability corresponding to their fitness
            fitnesses = [recipe.get_fitness() for recipe in self.recipes]
            sum_fit = sum(fitnesses)
            p = [fit / sum_fit for fit in fitnesses]
            recipe1, recipe2 = np.random.choice(self.recipes, p = p, size = 2, replace = False)

            #cross the recipes together
            new_recipe = self.crossover(recipe1, recipe2)
            new_recipes.append(new_recipe)

        #keep top 50% of old recipes and newly generated recipes for next generation
        self.recipes = self.fittest_half(self.recipes) + self.fittest_half(new_recipes)   

    def run_genetic_algo(self, generations):
        """ Run genetic algorithm for the # of generations that the user inputs.
            Args:
                generations (int) : number of times the genetic algo will run
        """
        for i in range(generations):
            print(f"Running genetic algorithm for generation {i + 1}")
            self.genetic_algo()  
    
    def write_fittest_recipes(self):
        """ Writes the 5 fittest recipes to files in the fittest recipes folder.
        """
        sorted_recipes = sorted(self.recipes, key = lambda x : x.get_fitness())
        top_5 = sorted_recipes[-5:]
        for i in range(5):
            recipe = top_5[i]
            with open("fittest recipes/rank_" + str(5 - i), "w") as f:
                f.write(f"{recipe.get_name()} ({recipe.get_fitness()} ingredients)\n")
                f.writelines(recipe.get_ingredient_strings())


def main():
    generations = int(input("How many generations would you like to run this algorithm for? "))
    manager = RecipeManager()
    manager.parse_files()
    manager.get_unique_ingredients()
    manager.run_genetic_algo(generations)
    manager.write_fittest_recipes() #writes top 5 fittest recipes (after algo) to a file
    print("All done :)")


if __name__ == "__main__":
    main()