import numpy as np
import os
from recipe import Recipe


class RecipeManager():
    """Run generation and evaluation"""
    def __init__(self):
        self.recipes = []
        self.num_new_recipes = 0
    
    def parse_files(self, emotion):
        """ Read file of recipes and populates recipe list with recipe object,
        passing in a list representation of recipe.
        """
        print("Reading Initial Recipe Files")
        dir = "inspiring_set"
        for file in os.listdir(dir):
            print("file:", file)
            with open(dir + "/" + file, "r") as f:
                recipe_str = f.readlines()
                self.recipes.append(Recipe(recipe_str, emotion))
            self.num_new_recipes += 1
    
    def crossover(self, recipe1, recipe2):
        """Chooses the base ingredients from one recipe with equal probability.
        Chooses a random pivot index to concatenate the flavor ingredients. 
        Creates a new recipe object. Then calls the mutate function on the new 
        recipe and stores what's returned.
            Args:
                recipe1 (Recipe) : first recipe to be crossed
                recipe2 (Recipe) : second recipe to be crossed
        """
        # choose base ingredients of one recipe with equal probability 
        new_base = np.random.choice([recipe1, recipe2]).get_base_ing_strings()

        # randomly select pivot to split flavor ingredients
        recipe1_flavor_strs = recipe1.get_flavor_ing_strings()
        recipe2_flavor_strs = recipe2.get_flavor_ing_strings()
        pivot = np.random.randint(0, min(len(recipe1_flavor_strs), 
                                         len(recipe1_flavor_strs)))
        new_flavors = recipe1_flavor_strs[:pivot] + recipe2_flavor_strs[pivot:]

        new_recipe = Recipe(new_base + new_flavors)
        self.num_new_recipes += 1

        # call recipe to be potentially mutated
        new_recipe.mutate()
        return new_recipe
    
    def fittest_half(self, recipes):
        """ Returns the fittest 50% of a given population.
            Args:
                recipes (list) : list of recipes
        """
        sorted_recipes = sorted(recipes, key = lambda x : x.get_fitness())
        return sorted_recipes[int(len(recipes)/2):]
    
    def emotion_prompt(self):
        emotion_key = input("How are you feeling? \n (1) : Happy \n (2) : Sad \n (3) : Angry \n" + \
            " (4) : Excited \n (5) : Tired \n (6) : Stressed \n Input Number 1-6: ")
        return emotion_key
    
    def get_emotion(self):
        emotion_dic ={"1" : "Happy", "2" : "Sad", "3": "Angry",
                     "4" : "Excited", "5" : "Tired", "6" : "Stressed"}
        emotion_key = self.emotion_prompt()
        while emotion_key not in emotion_dic.keys():
            print("\nUnknown Emotion Key: Try Again!\n")
            emotion_key = self.emotion_prompt()
        emotion = emotion_dic[emotion_key]
        print(f"\nYou are feeling {emotion.lower()}!\n")
        return emotion

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
        """ Writes the top 3 fittest recipes to files in the fittest recipes folder.
        """
        sorted_recipes = sorted(self.recipes, key = lambda x : x.get_fitness())
        top_3 = sorted_recipes[-3:]
        for i in range(3):
            recipe = top_3[i]
            with open("generator/fittest_recipes/rank_" + str(3 - i), "w") as f:
                f.write(f"{recipe.get_name()} ({recipe.get_fitness()} ingredients)\n")
                f.write("-base\n")
                f.writelines(recipe.get_base_ingredient_strings())
                f.write("-flavors\n")
                f.writelines(recipe.get_flavor_ingredient_strings())


def main():
    manager = RecipeManager()
    emotion = manager.get_emotion()
    generations = int(input("How many generations would you like to run this algorithm for? "))
    manager.parse_files(emotion)
    manager.run_genetic_algo(generations)
    manager.write_fittest_recipes() #writes top 5 fittest recipes (after algo) to a file
    print("All done :)")


if __name__ == "__main__":
    main()