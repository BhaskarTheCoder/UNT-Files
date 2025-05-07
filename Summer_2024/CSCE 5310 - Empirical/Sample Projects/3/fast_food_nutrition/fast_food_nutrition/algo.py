from fast_food_nutrition.model import Nutrition
from fast_food_nutrition.model import FOOD_INTAKE_CONF, FoodIntakeType, FoodRankingType, Sex


class NutritionCalculator:

    @staticmethod
    def get_caloric_intake_score(nutrition: Nutrition,
                                 sex=Sex.COMBINE) -> float:
        return NutritionCalculator._calculate(nutrition, FoodIntakeType.CALORIES, sex)

    @staticmethod
    def get_fat_intake_score(nutrition: Nutrition,
                             sex=Sex.COMBINE) -> float:
        return NutritionCalculator._calculate(nutrition, FoodIntakeType.FAT, sex)

    @staticmethod
    def get_carbohyrate_intake_score(nutrition: Nutrition,
                                     sex=Sex.COMBINE) -> float:
        return NutritionCalculator._calculate(nutrition, FoodIntakeType.CARBOHYDRATES, sex)

    @staticmethod
    def get_fiber_intake_score(nutrition: Nutrition,
                               sex=Sex.COMBINE) -> float:
        return NutritionCalculator._calculate(nutrition, FoodIntakeType.FIBER, sex)

    @staticmethod
    def get_protein_intake_score(nutrition: Nutrition,
                                 sex=Sex.COMBINE) -> float:
        return NutritionCalculator._calculate(nutrition, FoodIntakeType.PROTEIN, sex)

    @staticmethod
    def get_composite_nutrition_score(nutrition: Nutrition,
                                      sex=Sex.COMBINE) -> float:
        return NutritionCalculator._calculate(nutrition, FoodIntakeType.CALORIES, sex) * .35 + \
               NutritionCalculator._calculate(nutrition, FoodIntakeType.FAT, sex) * .30 + \
               NutritionCalculator._calculate(nutrition, FoodIntakeType.CARBOHYDRATES, sex) * .20 + \
               NutritionCalculator._calculate(nutrition, FoodIntakeType.FIBER, sex) * .10 + \
               NutritionCalculator._calculate(nutrition, FoodIntakeType.PROTEIN, sex) * .05

    @staticmethod
    def _calculate(nutrition: Nutrition,
                   food_intake_type: FoodIntakeType,
                   sex: Sex) -> float:
        food_contents = FOOD_INTAKE_CONF[food_intake_type]
        male_min = food_contents[Sex.MALE][FoodRankingType.MINIMUM] + food_contents[Sex.MALE][FoodRankingType.MINIMUM]
        male_max = food_contents[Sex.MALE][FoodRankingType.MINIMUM] + food_contents[Sex.MALE][FoodRankingType.MAXIMUM]
        female_min = food_contents[Sex.MALE][FoodRankingType.MINIMUM] + food_contents[Sex.FEMALE][FoodRankingType.MINIMUM]
        female_max = food_contents[Sex.MALE][FoodRankingType.MINIMUM] + food_contents[Sex.FEMALE][FoodRankingType.MAXIMUM]

        if sex == Sex.COMBINE:
            min_intake = (male_min + female_min) / 2
            max_intake = (male_max + female_max) / 2
        elif sex == Sex.MALE:
            min_intake = male_min
            max_intake = male_max
        elif sex == Sex.FEMALE:
            min_intake = female_min
            max_intake = female_max

        daily_food_intake = (min_intake + max_intake) / 2

        nutrition_for_intake_type = NutritionCalculator.get_nutrition_for_intake_type(nutrition, food_intake_type)

        return (nutrition.min_meals * (nutrition_for_intake_type / daily_food_intake)) / nutrition.max_meals

    @staticmethod
    def get_nutrition_for_intake_type(nutrition: Nutrition, food_intake_type) -> float:
        if food_intake_type == FoodIntakeType.CALORIES:
            return nutrition.calories
        elif food_intake_type == FoodIntakeType.FAT:
            return nutrition.fat
        elif food_intake_type == FoodIntakeType.FIBER:
            return nutrition.fiber
        elif food_intake_type == FoodIntakeType.CARBOHYDRATES:
            return nutrition.carb
        elif food_intake_type == FoodIntakeType.PROTEIN:
            return nutrition.protein
