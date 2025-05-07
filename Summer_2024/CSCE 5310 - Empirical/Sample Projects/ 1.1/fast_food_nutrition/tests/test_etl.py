from pandas import DataFrame

from fast_food_nutrition.etl import (BurgerKingMenuETL,
                                     ChickFilaMenuETL,
                                     FastFoodMenuETL,
                                     McDonaldsMenuETL,
                                     StarbucksMenuETL,
                                     WendysdMenuETL)
from fast_food_nutrition.model import FoodNutritionFeatures

FOOD_NUTRITION_FEATURES = [nutrition.value for nutrition in FoodNutritionFeatures]

FAST_FOOD_MENU_ITEM_COUNTS = {"starbucks_drinks": 92,
                              "starbucks_food": 113,
                              "starbucks_expanded_drinks": 242,
                              "starbucks_menu": 447,
                              "mcdonalds_menu": 260,
                              "burger_king_menu": 77,
                              "wendys_menu": 43,
                              "chick_fila_menu": 290,
                              "menu": 1117}


def test_transform_starbucks_drinks():
    etl = StarbucksMenuETL()
    starbucks_drinks = etl.transform_starbucks_drinks()
    assert_menu_items(starbucks_drinks, "starbucks_drinks")


def test_transform_starbucks_food():
    etl = StarbucksMenuETL()
    starbucks_drinks = etl.transform_starbucks_food()
    assert_menu_items(starbucks_drinks, "starbucks_food")


def test_transform_starbucks_expanded_drinks():
    etl = StarbucksMenuETL()
    starbucks_expanded_drinks = etl.transform_starbucks_expanded_drinks()
    assert_menu_items(starbucks_expanded_drinks, "starbucks_expanded_drinks")


def test_load_starbucks_menu_items():
    etl = StarbucksMenuETL()
    starbucks_menu = etl.load_menu_items()
    assert_menu_items(starbucks_menu, "starbucks_menu")


def test_load_mcdonalds_menu_items():
    etl = McDonaldsMenuETL()
    mdonalds_menu = etl.load_menu_items()
    assert_menu_items(mdonalds_menu, "mcdonalds_menu")


def test_load_burger_king_menu_items():
    etl = BurgerKingMenuETL()
    burger_king_menu = etl.load_menu_items()
    assert_menu_items(burger_king_menu, "burger_king_menu")


def test_load_burger_wendys_menu_items():
    etl = WendysdMenuETL()
    wendys_menu = etl.load_menu_items()
    assert_menu_items(wendys_menu, "wendys_menu")


def test_load_chick_fila_menu_items():
    etl = ChickFilaMenuETL()
    chick_fila_menu = etl.load_menu_items()
    assert_menu_items(chick_fila_menu, "chick_fila_menu")


def test_load_all_menu_items():
    etl = FastFoodMenuETL()
    menu = etl.load_menu_items()
    assert_menu_items(menu, "menu")


def assert_menu_items(food_menu_items: DataFrame, menu_item: str) -> None:
    for feature in food_menu_items.columns:
        assert feature in FOOD_NUTRITION_FEATURES

    assert FAST_FOOD_MENU_ITEM_COUNTS[menu_item] == len(food_menu_items)





