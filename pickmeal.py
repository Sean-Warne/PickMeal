import argparse
import json
from random import randint
import warnings

# this app will eventually be converted to Django where
# these classes will be the models

class Recipe:
    """
    A recipe and how many meals it serves
    """
    def __init__(
            self,
            name,
            servings,
            url=None,
            tags=[]
        ):
        self.name = name
        self.servings = servings
        self.url = url
        self.tags = tags

class Meal:
    """
    Represents a mealtime e.g. breakfast, second breakfast,
    elevensies, lunch, supper, and snacks

    Contains a list of recipes where the cumulative recipe.servings
    is equal to or greater than num_recipes
    """
    def __init__(
            self,
            name,
            num_recipes,
            recipes = []
        ):
        self.name = name
        self.num_recipes = num_recipes
        self.recipes = recipes

class MealPlan:
    """
    A weekly meal plan containing meals and their recipes
    """

    RECIPES_PER_MEAL_PER_WEEK = 7
    
    def __init__(self, json_path):
        self.json_path = json_path
        self.json = self._open_meal_list()

        self.breakfast = {}
        self.lunch  = {}
        self.dinner = {}
        self.snacks = {}

    def generate_meal_plan(self):
        self.breakfast = self._generate_meal("Breakfast", 3)
        self.lunch = self._generate_meal("Lunch", 2)
        self.dinner = self._generate_meal("Dinner", 2)
        self.snacks = self._generate_meal("Snacks", 2)

    def get_meal_str(self, meal_dict):
        str_list = []
        for recipe in meal_dict:
            try:
                str_list.append(f'  - {recipe["Name"]} x{recipe["Servings"]}')
            except:
                str_list.append(f'  - {recipe["Name"]}')
        return "\n".join(str_list)

    def _generate_meal(self, meal, recipes_per_meal=3):
        if recipes_per_meal > MealPlan.RECIPES_PER_MEAL_PER_WEEK:
            raise ValueError(f'Cannot choose more than {MealPlan.RECIPES_PER_MEAL_PER_WEEK} recipes per meal per week')
        elif recipes_per_meal <= 0:
            raise ValueError(f'recipes_per_meal must be greater than 0')
        
        recipes = self.json['Meals'][meal]

        if len(recipes) < recipes_per_meal:
            warnings.warn(f'Desired recipe recipes_per_meal ({recipes_per_meal}) exceeds number of recipes in list ({len(recipes)})')
            recipes_per_meal = len(recipes)

        chosen_recipes = []
        for i in range(0, recipes_per_meal):
            rand = randint(0, len(recipes)-1)
            chosen_recipe = recipes[rand]
            if chosen_recipe not in chosen_recipes:
                chosen_recipes.append(chosen_recipe)

        return chosen_recipes

    def _open_meal_list(self):
        with open(self.json_path) as meal_list:
            meal_json = json.load(meal_list)
        return meal_json

    def __str__(self):
        # TODO: Fix this formatting, dedent wasn't working
        return (
        f'''
Breakfast
{self.get_meal_str(self.breakfast)}

Lunch
{self.get_meal_str(self.lunch)}

Dinner
{self.get_meal_str(self.dinner)}

Snacks
{self.get_meal_str(self.snacks)}
         '''
        )

def main(json_path):
    meal_plan = MealPlan(json_path)
    meal_plan.generate_meal_plan()
    print(meal_plan)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", help="Path to JSON file containing list of meals")
    args = parser.parse_args()
    
    main(args.json_path)