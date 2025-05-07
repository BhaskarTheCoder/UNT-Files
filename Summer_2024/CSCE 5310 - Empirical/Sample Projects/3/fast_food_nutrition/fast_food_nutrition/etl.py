from abc import ABC, abstractmethod
import pandas as pd
from pandas import DataFrame

from fast_food_nutrition.model import DATA_TYPE, FoodNutritionFeatures, FoodNutritionMapping
from fast_food_nutrition.util import get_full_qualified_file_name


class FastFoodMenuETLInterface(ABC):
    @abstractmethod
    def load_menu_items(self) -> DataFrame: pass

    def convert_data_types(self, menu: DataFrame) -> DataFrame:
        return menu.astype({FoodNutritionFeatures.MENU_ITEM.value: FoodNutritionMapping[FoodNutritionFeatures.MENU_ITEM.value][DATA_TYPE],
                            FoodNutritionFeatures.CALORIES.value: FoodNutritionMapping[FoodNutritionFeatures.CALORIES.value][DATA_TYPE],
                            FoodNutritionFeatures.FAT.value: FoodNutritionMapping[FoodNutritionFeatures.CALORIES.value][DATA_TYPE],
                            FoodNutritionFeatures.CARBOHYDRATES.value: FoodNutritionMapping[FoodNutritionFeatures.CALORIES.value][DATA_TYPE],
                            FoodNutritionFeatures.PROTEIN.value: FoodNutritionMapping[FoodNutritionFeatures.CALORIES.value][DATA_TYPE],
                            FoodNutritionFeatures.FIBER.value: FoodNutritionMapping[FoodNutritionFeatures.CALORIES.value][DATA_TYPE]})


class FastFoodMenuETL(FastFoodMenuETLInterface):
    def __init__(self):
        self.star_bucks_menu_etl = StarbucksMenuETL()
        self.mcdonalds_menu_etl = McDonaldsMenuETL()
        self.burger_king_etl = BurgerKingMenuETL()
        self.wendys_menu_etl = WendysdMenuETL()
        self.chick_fila_menu_etl = ChickFilaMenuETL()

    def load_menu_items(self) -> DataFrame:
        return self.convert_data_types(pd.concat([self.star_bucks_menu_etl.load_menu_items(),
                                                  self.mcdonalds_menu_etl.load_menu_items(),
                                                  self.burger_king_etl.load_menu_items(),
                                                  self.wendys_menu_etl.load_menu_items(),
                                                  self.chick_fila_menu_etl.load_menu_items()], ignore_index=True))


class StarbucksMenuETL(FastFoodMenuETLInterface):
    def __init__(self):
        self.BASE_DIR = "starbucks"
        self.DRINKS_FILE_NAME = f"{self.BASE_DIR}/starbucks-menu-nutrition-drinks.csv"
        self.FOOD_FILE_NAME = f"{self.BASE_DIR}/starbucks-menu-nutrition-food.csv"
        self.EXPANDED_MENU_FILE = f"{self.BASE_DIR}/starbucks_drinkMenu_expanded.csv"
        self.FOOD_AND_DRINK_RENAME_COLUMNS = ["Unnamed: 0",
                                              "Calories",
                                              "Fat (g)",
                                              "Carb. (g)",
                                              "Fiber (g)",
                                              "Protein",
                                              "Protein (g)",
                                              "Total Fat (g)",
                                              "Total Carbohydrates (g)",
                                              "Dietary Fibre (g)",
                                              "Protein (g)",
                                              ]
        self.DRINK_DROP_COLUMNS = ["Sodium"]
        self.DRINK_EXPANDED_DROP_COLUMNS = ["Beverage_category",
                                            "Beverage",
                                            "Beverage_prep",
                                            "Trans Fat (g)",
                                            "Saturated Fat (g)",
                                            "Sodium (mg)",
                                            "Cholesterol (mg)",
                                            "Sugars (g)",
                                            "Vitamin A (% DV)",
                                            "Vitamin C (% DV)",
                                            "Calcium (% DV)",
                                            "Iron (% DV)",
                                            "Caffeine (mg)"]

    def load_menu_items(self) -> DataFrame:
        return self.convert_data_types(pd.concat([self.transform_starbucks_drinks(),
                                                      self.transform_starbucks_food(),
                                                      self.transform_starbucks_expanded_drinks()], ignore_index=True))

    def extract_starbucks_drinks(self) -> DataFrame:
        return pd.read_csv(get_full_qualified_file_name(self.DRINKS_FILE_NAME), index_col=False)

    def transform_starbucks_drinks(self) -> DataFrame:
        starbucks_drinks = self.extract_starbucks_drinks()

        starbucks_drinks = starbucks_drinks[~(starbucks_drinks[self.FOOD_AND_DRINK_RENAME_COLUMNS[1:6]] == "-").all(axis=1)]

        starbucks_drinks.rename(columns={self.FOOD_AND_DRINK_RENAME_COLUMNS[0]: FoodNutritionFeatures.MENU_ITEM.value,
                                         self.FOOD_AND_DRINK_RENAME_COLUMNS[1]: FoodNutritionFeatures.CALORIES.value,
                                         self.FOOD_AND_DRINK_RENAME_COLUMNS[2]: FoodNutritionFeatures.FAT.value,
                                         self.FOOD_AND_DRINK_RENAME_COLUMNS[3]: FoodNutritionFeatures.CARBOHYDRATES.value,
                                         self.FOOD_AND_DRINK_RENAME_COLUMNS[4]: FoodNutritionFeatures.FIBER.value,
                                         self.FOOD_AND_DRINK_RENAME_COLUMNS[5]: FoodNutritionFeatures.PROTEIN.value}, inplace=True)

        starbucks_drinks.drop(columns=self.DRINK_DROP_COLUMNS, inplace=True)

        return starbucks_drinks

    def extract_starbucks_food(self) -> DataFrame:
        return pd.read_csv(get_full_qualified_file_name(self.FOOD_FILE_NAME),
                           encoding="utf-16",
                           index_col=False)

    def transform_starbucks_food(self) -> DataFrame:
        starbucks_food = self.extract_starbucks_food()

        starbucks_food.rename(columns={self.FOOD_AND_DRINK_RENAME_COLUMNS[0]: FoodNutritionFeatures.MENU_ITEM.value,
                                       self.FOOD_AND_DRINK_RENAME_COLUMNS[1]: FoodNutritionFeatures.CALORIES.value,
                                       self.FOOD_AND_DRINK_RENAME_COLUMNS[2]: FoodNutritionFeatures.FAT.value,
                                       self.FOOD_AND_DRINK_RENAME_COLUMNS[3]: FoodNutritionFeatures.CARBOHYDRATES.value,
                                       self.FOOD_AND_DRINK_RENAME_COLUMNS[4]: FoodNutritionFeatures.FIBER.value,
                                       self.FOOD_AND_DRINK_RENAME_COLUMNS[6]: FoodNutritionFeatures.PROTEIN.value},
                              inplace=True)

        return starbucks_food

    def extract_starbucks_expanded_drinks(self) -> DataFrame:
        return pd.read_csv(get_full_qualified_file_name(self.EXPANDED_MENU_FILE),
                           index_col=False)

    def transform_starbucks_expanded_drinks(self) -> DataFrame:
        starbucks_drinks_expanded = self.extract_starbucks_expanded_drinks()

        starbucks_drinks_expanded[FoodNutritionFeatures.MENU_ITEM.value] = \
            starbucks_drinks_expanded[self.DRINK_EXPANDED_DROP_COLUMNS[1]] + \
            " " + \
            starbucks_drinks_expanded[self.DRINK_EXPANDED_DROP_COLUMNS[2]]

        starbucks_drinks_expanded.rename(columns={self.FOOD_AND_DRINK_RENAME_COLUMNS[1]: FoodNutritionFeatures.CALORIES.value,
                                                  self.FOOD_AND_DRINK_RENAME_COLUMNS[7]: FoodNutritionFeatures.FAT.value,
                                                  self.FOOD_AND_DRINK_RENAME_COLUMNS[8]: FoodNutritionFeatures.CARBOHYDRATES.value,
                                                  self.FOOD_AND_DRINK_RENAME_COLUMNS[9]: FoodNutritionFeatures.FIBER.value,
                                                  self.FOOD_AND_DRINK_RENAME_COLUMNS[10]: FoodNutritionFeatures.PROTEIN.value},
                                         inplace=True)

        starbucks_drinks_expanded.drop(columns=self.DRINK_EXPANDED_DROP_COLUMNS, inplace=True)

        return starbucks_drinks_expanded


class McDonaldsMenuETL(FastFoodMenuETLInterface):
    def __init__(self):
        self.BASE_DIR = "mcdonalds"
        self.MENU_FILE_NAME = f"{self.BASE_DIR}/mcdonalds.csv"
        self.MENU_DROP_COLUMNS = ["Category",
                                  "Serving Size",
                                  "Calories from Fat",
                                  "Total Fat (% Daily Value)",
                                  "Saturated Fat",
                                  "Saturated Fat (% Daily Value)",
                                  "Trans Fat",
                                  "Cholesterol",
                                  "Cholesterol (% Daily Value)",
                                  "Sodium",
                                  "Sodium (% Daily Value)",
                                  "Carbohydrates (% Daily Value)",
                                  "Dietary Fiber (% Daily Value)",
                                  "Sugars",
                                  "Vitamin A (% Daily Value)",
                                  "Vitamin C (% Daily Value)",
                                  "Calcium (% Daily Value)",
                                  "Iron (% Daily Value)"]

        self.MENU_RENAME_COLUMNS = ["Item",
                                    "Calories",
                                    "Total Fat",
                                    "Carbohydrates",
                                    "Protein",
                                    "Dietary Fiber"]

    def extract_mcdonalds_menu(self) -> DataFrame:
        return pd.read_csv(get_full_qualified_file_name(self.MENU_FILE_NAME),
                           index_col=False)

    def transform_mcdonalds_menu(self) -> DataFrame:
        mcdonalds_menu = self.extract_mcdonalds_menu()

        mcdonalds_menu.drop(columns=self.MENU_DROP_COLUMNS, inplace=True)

        mcdonalds_menu.rename(columns={self.MENU_RENAME_COLUMNS[0]: FoodNutritionFeatures.MENU_ITEM.value,
                                       self.MENU_RENAME_COLUMNS[1]: FoodNutritionFeatures.CALORIES.value,
                                       self.MENU_RENAME_COLUMNS[2]: FoodNutritionFeatures.FAT.value,
                                       self.MENU_RENAME_COLUMNS[3]: FoodNutritionFeatures.CARBOHYDRATES.value,
                                       self.MENU_RENAME_COLUMNS[4]: FoodNutritionFeatures.PROTEIN.value,
                                       self.MENU_RENAME_COLUMNS[5]: FoodNutritionFeatures.FIBER.value},
                              inplace=True)

        return mcdonalds_menu

    def load_menu_items(self) -> DataFrame:
        return self.convert_data_types(self.transform_mcdonalds_menu())


class BurgerKingMenuETL(FastFoodMenuETLInterface):
    def __init__(self):
        self.BASE_DIR = "burger-king"
        self.MENU_FILE_NAME = f"{self.BASE_DIR}/burger-king.csv"
        self.MENU_DROP_COLUMNS = ["Category",
                                  "Fat Calories",
                                  "Saturated Fat (g)",
                                  "Trans Fat (g)",
                                  "Cholesterol (mg)",
                                  "Sodium (mg)",
                                  "Sugars (g)",
                                  "Weight Watchers"]

        self.MENU_RENAME_COLUMNS = ["Item",
                                    "Calories",
                                    "Fat (g)",
                                    "Total Carb (g)",
                                    "Protein (g)",
                                    "Dietary Fiber (g)"]

    def extract_burger_king_menu(self) -> DataFrame:
        return pd.read_csv(get_full_qualified_file_name(self.MENU_FILE_NAME),
                           index_col=False)

    def transform_burger_king_menu(self) -> DataFrame:
        burger_king_menu = self.extract_burger_king_menu()

        burger_king_menu.drop(columns=self.MENU_DROP_COLUMNS, inplace=True)

        burger_king_menu.rename(columns={self.MENU_RENAME_COLUMNS[0]: FoodNutritionFeatures.MENU_ITEM.value,
                                         self.MENU_RENAME_COLUMNS[1]: FoodNutritionFeatures.CALORIES.value,
                                         self.MENU_RENAME_COLUMNS[2]: FoodNutritionFeatures.FAT.value,
                                         self.MENU_RENAME_COLUMNS[3]: FoodNutritionFeatures.CARBOHYDRATES.value,
                                         self.MENU_RENAME_COLUMNS[4]: FoodNutritionFeatures.PROTEIN.value,
                                         self.MENU_RENAME_COLUMNS[5]: FoodNutritionFeatures.FIBER.value},
                                inplace=True)

        return burger_king_menu

    def load_menu_items(self) -> DataFrame:
        return self.convert_data_types(self.transform_burger_king_menu())


class WendysdMenuETL(FastFoodMenuETLInterface):
    def __init__(self):
        self.BASE_DIR = "wendys"
        self.MENU_FILE_NAME = f"{self.BASE_DIR}/wendys.csv"
        self.MENU_DROP_COLUMNS = ["Category",
                                  "Sat Fat (g)",
                                  "Trans Fat (g)",
                                  "Cholesterol (mg)",
                                  "Sodium (mg)",
                                  "Sugars (g)",
                                  "Weight Watchers"]

        self.MENU_RENAME_COLUMNS = ["Item",
                                    "Calories",
                                    "Fat (g)",
                                    "Total Carb (g)",
                                    "Protein (g)",
                                    "Dietary Fiber (g)"]

    def extract_wendys_menu(self) -> DataFrame:
        return pd.read_csv(get_full_qualified_file_name(self.MENU_FILE_NAME),
                           index_col=False)

    def transform_wendys_menu(self) -> DataFrame:
        wendys_menu = self.extract_wendys_menu()

        wendys_menu.drop(columns=self.MENU_DROP_COLUMNS, inplace=True)

        wendys_menu.rename(columns={self.MENU_RENAME_COLUMNS[0]: FoodNutritionFeatures.MENU_ITEM.value,
                                    self.MENU_RENAME_COLUMNS[1]: FoodNutritionFeatures.CALORIES.value,
                                    self.MENU_RENAME_COLUMNS[2]: FoodNutritionFeatures.FAT.value,
                                    self.MENU_RENAME_COLUMNS[3]: FoodNutritionFeatures.CARBOHYDRATES.value,
                                    self.MENU_RENAME_COLUMNS[4]: FoodNutritionFeatures.PROTEIN.value,
                                    self.MENU_RENAME_COLUMNS[5]: FoodNutritionFeatures.FIBER.value},
                           inplace=True)

        return wendys_menu

    def load_menu_items(self) -> DataFrame:
        return self.convert_data_types(self.transform_wendys_menu())


class ChickFilaMenuETL(FastFoodMenuETLInterface):
    def __init__(self):
        self.BASE_DIR = "chick-fila"
        self.MENU_FILE_NAME = f"{self.BASE_DIR}/chick-fila.csv"
        self.MENU_DROP_COLUMNS = ["Serving size",
                                  "Sat. Fat (G)",
                                  "Trans Fat (G)",
                                  "Cholesterol (MG)",
                                  "Sodium (MG)",
                                  "Sugar (G)"]

        self.MENU_RENAME_COLUMNS = ["Menu",
                                    "Calories",
                                    "Fat (G)",
                                    "Carbohydrates (G)",
                                    "Protein (G)",
                                    "Fiber (G)"]

    def extract_chick_fila_menu(self) -> DataFrame:
        return pd.read_csv(get_full_qualified_file_name(self.MENU_FILE_NAME),
                           index_col=False)

    def transform_chick_fila_menu(self) -> DataFrame:
        chick_fila = self.extract_chick_fila_menu()

        chick_fila.drop(columns=self.MENU_DROP_COLUMNS, inplace=True)

        chick_fila.rename(columns={self.MENU_RENAME_COLUMNS[0]: FoodNutritionFeatures.MENU_ITEM.value,
                                   self.MENU_RENAME_COLUMNS[1]: FoodNutritionFeatures.CALORIES.value,
                                   self.MENU_RENAME_COLUMNS[2]: FoodNutritionFeatures.FAT.value,
                                   self.MENU_RENAME_COLUMNS[3]: FoodNutritionFeatures.CARBOHYDRATES.value,
                                   self.MENU_RENAME_COLUMNS[4]: FoodNutritionFeatures.PROTEIN.value,
                                   self.MENU_RENAME_COLUMNS[5]: FoodNutritionFeatures.FIBER.value},
                          inplace=True)

        return chick_fila
    
    def load_menu_items(self) -> DataFrame:
        return self.convert_data_types(self.transform_chick_fila_menu())










