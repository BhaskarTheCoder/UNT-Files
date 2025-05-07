from dataclasses import dataclass
from enum import Enum


class Test(Enum):
    RIGHT_TAILED = "RT"
    LEFT_TAILED = "LT"
    TWO_TAILED = "TT"


class HypothesisTestMethod:
    P_VALUE_METHOD = "p_value"
    CRITICAL_VALUE_METHOD = "critical_value"
    CONFIDENCE_INTERVAL_METHOD = "confidence_interval"


class HypothesisTestConclusion:
    REJECT_H_0 = "reject_h_0"
    FAIL_TO_REJECT_H0 = "do_not_reject_h_0"


class FoodNutritionFeatures(Enum):
    CALORIES = "calories"
    FAT = "fat"
    CARBOHYDRATES = "carbohydrates"
    FIBER = "fiber"
    PROTEIN = "protein"
    MENU_ITEM = "menu_item"


DATA_TYPE = "data_type"
STRING = "string"
FLOAT = "float64"
COLOR = "color"

COLORS = ["#add8e6", "#90ee90", "#ffb6c1", "#dda0dd", "#ffd580"]


FoodNutritionMapping = {
                            FoodNutritionFeatures.MENU_ITEM.value: {DATA_TYPE: STRING},
                            FoodNutritionFeatures.CALORIES.value: {DATA_TYPE: FLOAT,
                                                                   COLOR: COLORS[0]},
                            FoodNutritionFeatures.FAT.value: {DATA_TYPE: FLOAT,
                                                              COLOR: COLORS[1]},
                            FoodNutritionFeatures.CARBOHYDRATES.value: {DATA_TYPE: FLOAT,
                                                                        COLOR: COLORS[2]},
                            FoodNutritionFeatures.PROTEIN.value: {DATA_TYPE: FLOAT,
                                                                  COLOR: COLORS[3]},
                            FoodNutritionFeatures.FIBER.value: {DATA_TYPE: FLOAT,
                                                                COLOR: COLORS[4]}
                       }


class Sex(Enum):
    MALE = "M"
    FEMALE = "F"
    COMBINE = "MF"


class FoodRankingType(Enum):
    MINIMUM = 1
    MAXIMUM = 2
    MEDIAN = 3
    MEAN = 4


class FoodIntakeType(Enum):
    CALORIES = 1
    FAT = 2
    CARBOHYDRATES = 3
    FIBER = 4
    PROTEIN = 5


# CALORIC INTAKE
MINIMUM_FEMALE_CALORIC_INTAKE = 1600
MAXIMUM_FEMALE_CALORIC_INTAKE = 2400
MINIMUM_MALE_CALORIC_INTAKE = 2000
MAXIMUM_MALE_CALORIC_INTAKE = 3000

# FIBER INTAKE (grams)
MINIMUM_MALE_FIBER_INTAKE = 30
MAXIMUM_MALE_FIBER_INTAKE = 38
MINIMUM_FEMALE_FIBER_INTAKE = 21
MAXIMUM_FEMALE_FIBER_INTAKE = 25

# (SATURATED) FAT INTAKE (grams)
MINIMUM_MALE_FAT_INTAKE = 30
MAXIMUM_MALE_FAT_INTAKE = 30
MINIMUM_FEMALE_FAT_INTAKE = 20
MAXIMUM_FEMALE_FAT_INTAKE = 20

# CARBOHYDRATES INTAKE (grams)
MINIMUM_MALE_CARBOHYDRATES_INTAKE = 338
MAXIMUM_MALE_CARBOHYDRATES_INTAKE = 488
MINIMUM_FEMALE_CARBOHYDRATES_INTAKE = 180
MAXIMUM_FEMALE_CARBOHYDRATES_INTAKE = 420

# PROTEIN INTAKE
MINIMUM_MALE_PROTEIN_INTAKE = 88
MAXIMUM_MALE_PROTEIN_INTAKE = 122
MINIMUM_FEMALE_PROTEIN_INTAKE = 105
MAXIMUM_FEMALE_PROTEIN_INTAKE = 145


FOOD_INTAKE_CONF = {
    FoodIntakeType.CALORIES: {
        Sex.MALE: {
            FoodRankingType.MINIMUM: MINIMUM_MALE_CALORIC_INTAKE,
            FoodRankingType.MAXIMUM: MAXIMUM_MALE_CALORIC_INTAKE
        },
        Sex.FEMALE: {
            FoodRankingType.MINIMUM: MINIMUM_FEMALE_CALORIC_INTAKE,
            FoodRankingType.MAXIMUM: MAXIMUM_FEMALE_CALORIC_INTAKE
        },
    },
    FoodIntakeType.FIBER: {
        Sex.MALE: {
            FoodRankingType.MINIMUM: MINIMUM_MALE_FIBER_INTAKE,
            FoodRankingType.MAXIMUM: MAXIMUM_MALE_FIBER_INTAKE
        },
        Sex.FEMALE: {
            FoodRankingType.MINIMUM: MINIMUM_FEMALE_FIBER_INTAKE,
            FoodRankingType.MAXIMUM: MAXIMUM_FEMALE_FIBER_INTAKE
        },
    },
    FoodIntakeType.FAT: {
        Sex.MALE: {
            FoodRankingType.MINIMUM: MINIMUM_MALE_FAT_INTAKE,
            FoodRankingType.MAXIMUM: MAXIMUM_MALE_FAT_INTAKE
        },
        Sex.FEMALE: {
            FoodRankingType.MINIMUM: MINIMUM_FEMALE_FAT_INTAKE,
            FoodRankingType.MAXIMUM: MAXIMUM_FEMALE_FAT_INTAKE
        },
    },
    FoodIntakeType.CARBOHYDRATES: {
        Sex.MALE: {
            FoodRankingType.MINIMUM: MINIMUM_MALE_CARBOHYDRATES_INTAKE,
            FoodRankingType.MAXIMUM: MAXIMUM_MALE_CARBOHYDRATES_INTAKE
        },
        Sex.FEMALE: {
            FoodRankingType.MINIMUM: MINIMUM_FEMALE_CARBOHYDRATES_INTAKE,
            FoodRankingType.MAXIMUM: MAXIMUM_FEMALE_CARBOHYDRATES_INTAKE
        },
    },
    FoodIntakeType.PROTEIN: {
        Sex.MALE: {
            FoodRankingType.MINIMUM: MINIMUM_MALE_PROTEIN_INTAKE,
            FoodRankingType.MAXIMUM: MAXIMUM_MALE_PROTEIN_INTAKE
        },
        Sex.FEMALE: {
            FoodRankingType.MINIMUM: MINIMUM_FEMALE_PROTEIN_INTAKE,
            FoodRankingType.MAXIMUM: MAXIMUM_FEMALE_PROTEIN_INTAKE
        },
    }
}


@dataclass
class Nutrition:
    item: str
    calories: float
    fiber: float
    fat: float
    carb: float
    protein: float
    min_meals: int = 1
    max_meals: int = 3

