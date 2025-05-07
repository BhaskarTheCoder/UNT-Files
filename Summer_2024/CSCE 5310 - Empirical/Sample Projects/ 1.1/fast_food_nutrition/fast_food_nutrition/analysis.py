import math

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from scipy.stats import chi2, norm, t as t_test
import scipy.stats as stats
from typing import List, Tuple, Union

from fast_food_nutrition.model import HypothesisTestConclusion, HypothesisTestMethod, Test


class Outliers:
    @staticmethod
    def filter_outliers(menu: DataFrame, columns: List[str]):
        def remove_outliers(column: Series) -> DataFrame:
            Q1 = column.quantile(0.25)
            Q3 = column.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            return (column >= lower_bound) & (column <= upper_bound)

        mask = pd.Series([True] * len(menu))

        for col in columns:
            mask &= remove_outliers(menu[col])

        return menu[mask]


class ZTest:
    """
    Method that runs the z-test and return the critical value and p-value
    """
    @staticmethod
    def calculate(p0: int, phat: float, n: int, level_of_significance=0.05):
        # Calculate the z-score
        z = (phat - p0) / ((p0 * (1 - p0) / n) ** level_of_significance)

        # Calculate the p-value for a right-tailed test
        p_value = norm.sf(z)  # This is the survival function, equivalent to 1 - CDF

        return z, p_value

    """
        Method that runs the z-test and return the critical value and p-value
    """
    @staticmethod
    def calculate_proportion(p0: int, x: int, n: int, test: Test) -> Tuple[float, float]:
        # Calculate the z-score
        p_hat = x / n
        z = (p_hat - p0) / math.sqrt((p0 * (1 - p0)) / n)
        p_value = ZTest.get_p_value_table_value(z, test)

        return round(z, 2), round(p_value, 3)

    @staticmethod
    def calculate_hypothesis_critical_value_test_method(z: float, alpha: float, test: Test) -> HypothesisTestConclusion:
        if test == Test.TWO_TAILED:
            z_alpha_2 = 1 - (alpha / 2)
            critical_value_upper = norm.ppf(z_alpha_2)
            critical_value_lower = norm.ppf(1 - z_alpha_2)

            if z <= critical_value_lower or z >= critical_value_upper:
                return HypothesisTestConclusion.REJECT_H_0
            else:
                return HypothesisTestConclusion.FAIL_TO_REJECT_H0
        elif test == Test.LEFT_TAILED:
            critical_value = norm.ppf(alpha)

            if z <= critical_value:
                return HypothesisTestConclusion.REJECT_H_0
            else:
                return HypothesisTestConclusion.FAIL_TO_REJECT_H0
        elif test == Test.RIGHT_TAILED:
            critical_value = norm.ppf(1 - alpha)

            if z >= critical_value:
                return HypothesisTestConclusion.REJECT_H_0
            else:
                return HypothesisTestConclusion.FAIL_TO_REJECT_H0

    @staticmethod
    def calculate_p_value_test_method(p_value: float, alpha: float) -> HypothesisTestConclusion:
        if p_value <= alpha:
            return HypothesisTestConclusion.REJECT_H_0
        else:
            return HypothesisTestConclusion.FAIL_TO_REJECT_H0

    @staticmethod
    def calculate_proporation_confidence_interval(x: int, n: int, alpha: float, test: Test) -> Tuple[float, float]:
        p_hat = x / n
        q_hat = 1 - p_hat

        z_score_table = ZTest.get_z_score_table_value(alpha, test)

        E = z_score_table * math.sqrt((p_hat * q_hat) / n)

        min = round(p_hat - E, 3)
        max = round(p_hat + E, 3)

        return min, max

    @staticmethod
    def calculate_confidence_interval_test_method(p0: float, min: float, max: float) -> Test:
        if p0 >= min and p0 <= max:
            return HypothesisTestConclusion.FAIL_TO_REJECT_H0
        else:
            return HypothesisTestConclusion.REJECT_H_0

    @staticmethod
    def calculate_mean(x_bar: float,
                       mu: float,
                       sigma: float,
                       n: int,
                       test: Test) -> Tuple[float, float]:
        # Calculate the z-score
        z = (x_bar - mu) / (sigma / math.sqrt(n))

        p_value = ZTest.get_p_value_table_value(z, test)

        return round(z, 2), round(p_value, 3)

    @staticmethod
    def calculate_mean_confidence_interval(x_bar: float,
                                           sigma: float,
                                           n: int,
                                           alpha: float,
                                           test: Test) -> Tuple[float, float]:

        z_score_table = ZTest.get_z_score_table_value(alpha, test)

        E = z_score_table * (sigma / math.sqrt(n))

        min = round(x_bar - E, 3)
        max = round(x_bar + E, 3)

        return min, max

    @staticmethod
    def get_z_score_table_value(alpha: float, test: Test) -> float:
        if test == Test.TWO_TAILED:
            probalility = 1 - (alpha / 2)
        else:
            probalility = 1 - alpha

        return norm.ppf(probalility)

    @staticmethod
    def get_p_value_table_value(z: float, test: Test) -> float:
        if test == Test.TWO_TAILED:  # Calculate the p-value for a two-tailed test
            p_value = 2 * (1 - norm.cdf(abs(z)))
        elif test == Test.LEFT_TAILED:  # Calculate the p-value for a left-tailed test
            p_value = norm.cdf(z)
        elif test == Test.RIGHT_TAILED:  # Calculate the p-value for a right-tailed test
            p_value = 1 - norm.cdf(z)

        return p_value


class TTest:
    @staticmethod
    def calculate(x_bar: float, mu_0: float, n: int, s: float):
        # Calculate the t statistic
        t = (x_bar - mu_0) / (s / (n ** 0.5))

        # Degrees of freedom
        df = n - 1

        # Calculate the p-value for a right-tailed test
        p_value = t_test.sf(t, df)

        return t, p_value

    @staticmethod
    def calculate_two_means(x_bar_1: float,
                            x_bar_2: float,
                            mu_1: float,
                            mu_2: float,
                            sigma_1: float,
                            sigma_2: float,
                            n_1: int,
                            n_2: int,
                            test: Test) -> Tuple[float, float]:
        # Calculate the t statistic
        t = ((x_bar_1 - x_bar_2) - (mu_1 - mu_2)) / math.sqrt((math.pow(sigma_1, 2) / n_1) +
                                                              (math.pow(sigma_2, 2) / n_2))

        # Degrees of freedom
        df = TTest.df(TTest.A(sigma_1, n_1), TTest.B(sigma_2, n_2), n_1, n_2)
        p_value = TTest.get_p_value_table_value(t, df, test)

        return round(t, 2), round(p_value, 3)

    @staticmethod
    def calculate_r(x: np.ndarray[Union[float, int]],
                    y: np.ndarray[Union[float, int]],
                    test: Test) -> Tuple[float, float]:
        r = CoLinearity.calculate_r(x, y)
        n = len(x)
        t = r / math.sqrt((1 - math.pow(r, 2)) / (n - 2))

        # Degrees of freedom
        df = n - 2

        p_value = TTest.get_p_value_table_value(t, df, test)

        return r, round(p_value, 3)

    @staticmethod
    def A(sigma_1: float, n_1: int) -> float:
        return math.pow(sigma_1, 2) / n_1

    @staticmethod
    def B(sigma_2: float, n_2: int) -> float:
        return math.pow(sigma_2, 2) / n_2

    @staticmethod
    def df(A: int, B: int, n_1: int, n_2: int) -> float:
        return math.pow(A + B, 2) / ((math.pow(A, 2) / (n_1 - 1)) + (math.pow(A, 2) / (n_2 - 1)))

    @staticmethod
    def get_p_value_table_value(t: float, df: float, test: Test) -> float:
        if test == Test.RIGHT_TAILED:
            p_value = t_test.sf(t, df)
        elif test == Test.LEFT_TAILED:
            p_value = t_test.cdf(t, df)
        elif test == Test.TWO_TAILED:
            if t < 0:
                p_value = 2 * t_test.cdf(t, df)
            else:
                p_value = 2 * t_test.sf(t, df)

        return p_value

    @staticmethod
    def calculate_two_means_confidence_interval(x_bar_1: float,
                                                x_bar_2: float,
                                                sigma_1: float,
                                                sigma_2: float,
                                                n_1: int,
                                                n_2: int,
                                                alpha: float,
                                                test: Test) -> Tuple[float, float]:

        df = TTest.df(TTest.A(sigma_1, n_1), TTest.B(sigma_2, n_2), n_1, n_2)
        t_score_table = TTest.get_t_score_table_value(alpha, df, test)

        E = t_score_table * math.sqrt(TTest.A(sigma_1, n_1) + TTest.B(sigma_2, n_2))

        x_bar_dif = (x_bar_1 - x_bar_2)
        min = round(x_bar_dif - E, 3)
        max = round(x_bar_dif + E, 3)

        return min, max

    @staticmethod
    def get_t_score_table_value(alpha: float, df: int, test: Test) -> float:
        if test == Test.TWO_TAILED:
            probability = 1 - (alpha / 2)
        else:
            probability = 1 - alpha

        return t_test.ppf(probability, df)

    @staticmethod
    def calculate_hypothesis_critical_value_test_method(t: float, alpha: float, df: int, test: Test) -> HypothesisTestConclusion:
        if test == Test.TWO_TAILED:
            t_alpha_2 = 1 - (alpha / 2)
            critial_value_upper = t_test.ppf(t_alpha_2, df)
            crital_value_lower = t_test.ppf(1 - t_alpha_2, df)

            if t <= crital_value_lower or t >= critial_value_upper:
                return HypothesisTestConclusion.REJECT_H_0
            else:
                return HypothesisTestConclusion.FAIL_TO_REJECT_H0

        elif test == Test.LEFT_TAILED:
            critical_value = t_test.ppf(alpha, df)

            if t <= critical_value:
                return HypothesisTestConclusion.REJECT_H_0
            else:
                return HypothesisTestConclusion.FAIL_TO_REJECT_H0
        elif test == Test.RIGHT_TAILED:
            critical_value = t_test.ppf(1 - alpha, df)

            if t >= critical_value:
                return HypothesisTestConclusion.REJECT_H_0
            else:
                return HypothesisTestConclusion.FAIL_TO_REJECT_H0

    @staticmethod
    def convert_from_r_to_t(r: float, n: int) -> float:
        df = n - 2
        t = r / math.sqrt((1 - math.pow(r, 2)) / df)

        return round(t, 3)


class ChiSquaredTest:
    @staticmethod
    def calculate(n: int, s: float, sigma_0):
        # Calculate the chi-squared statistic
        chi_squared_statistic = ((n - 1) * s ** 2) / (sigma_0 ** 2)

        # Degrees of freedom
        df = n - 1

        # Calculate the p-value for a right-tailed test
        p_value = chi2.sf(chi_squared_statistic, df)

        return chi_squared_statistic, p_value


class CoLinearity:
    @staticmethod
    def calculate_r(x: np.ndarray[Union[float, int]], y: np.ndarray[Union[float, int]]) -> float:
        def sum_x(x: np.ndarray[Union[float, int]]) -> float:
            return np.sum(x)

        def sum_x_squared(x: np.ndarray[Union[float, int]]) -> float:
            return (x ** 2).sum()

        def sum_y(y: np.ndarray[Union[float, int]]) -> float:
            return np.sum(y)

        def sum_y_squared(y: np.ndarray[Union[float, int]]) -> float:
            return (y ** 2).sum()

        def sum_x_y(x: np.ndarray[Union[float, int]], y: np.ndarray[Union[float, int]]) -> float:
            xy = 0

            for x_1, y_1 in zip(x, y):
                xy += x_1 * y_1

            return xy

        n_1 = len(x)
        n_2 = len(y)

        if n_1 != n_2:
            raise ValueError("The number of samples for each list must be equal")
        else:
            n = n_1

        r = (n * sum_x_y(x, y) - sum_x(x) * sum_y(y)) / \
            ((math.sqrt(n * sum_x_squared(x) - math.pow(sum_x(x), 2))) *
             (math.sqrt(n * sum_y_squared(y) - math.pow(sum_y(y), 2))))

        return round(r, 3)

    @staticmethod
    def pearson_r_confidence_interval(x: int, y: int, alpha=float) -> Tuple[float, float]:
        # Calculate Pearson correlation coefficient
        r, _ = stats.pearsonr(x, y)

        # Convert r to Fisher's z
        r_z = np.arctanh(r)
        # Standard error
        se = 1.0 / np.sqrt(len(x) - 3)

        # Critical value for the confidence level
        z_critical = stats.norm.ppf(1 - alpha / 2)

        # Margin of error
        moe = z_critical * se

        # Confidence interval
        z_ci_lower = r_z - moe
        z_ci_upper = r_z + moe

        # Convert back to r scale
        r_ci_lower = np.tanh(z_ci_lower)
        r_ci_upper = np.tanh(z_ci_upper)

        return round(r_ci_lower, 3), round(r_ci_upper, 3)


