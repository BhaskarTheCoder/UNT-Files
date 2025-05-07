import matplotlib.pyplot as plt
from pandas import DataFrame
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
from typing import Dict

from fast_food_nutrition.model import COLOR, FoodNutritionFeatures, FoodNutritionMapping


class FastFoodNutritionVisualizer:

    @staticmethod
    def generate_scatter_plots(menu: DataFrame):
        menu = FastFoodNutritionVisualizer.filter_menu(menu)

        variables = menu.columns
        n = len(variables)

        fig, axes = plt.subplots(nrows=n, ncols=n, figsize=(15, 15))

        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables):
                if i == j:  # Diagonal: Plot a histogram
                    axes[i, j].hist(menu[var1], color=[FoodNutritionMapping[var1][COLOR]])
                else:  # Off-diagonal: Plot scatter
                    axes[i, j].scatter(menu[var2], menu[var1], color=[FoodNutritionMapping[var1][COLOR]])
                if j == 0:  # Y-axis labels only on the first column
                    axes[i, j].set_ylabel(var1)
                if i == n - 1:  # X-axis labels only on the last row
                    axes[i, j].set_xlabel(var2)
                if i < n - 1:  # Remove x-axis labels for all but the last row
                    axes[i, j].set_xticklabels([])
                if j > 0:  # Remove y-axis labels for all but the first column
                    axes[i, j].set_yticklabels([])

        plt.tight_layout()
        plt.show()

    @staticmethod
    def generate_box_plot(menu, merge=False):
        variables = menu.columns
        n = len(variables)

        if merge:
            plt.figure(figsize=(20, 5))
            plt.boxplot([menu[column] for column in variables], labels=variables, patch_artist=True)
            plt.grid(True)
        else:
            fig, axes = plt.subplots(1, n, figsize=(20, 5))

            for i, (ax, column) in enumerate(zip(axes, variables)):
                boxplot = ax.boxplot(menu[column], patch_artist=True)
                color = FoodNutritionMapping[column][COLOR]

                for median in boxplot['medians']:
                    median.set_color(color)

                for flier in boxplot['fliers']:
                    flier.set_marker('o')
                    flier.set_markerfacecolor(color)
                    flier.set_markeredgecolor('black')

                ax.set_title(column)
                ax.grid(True)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def generate_histogram_plots(menu: DataFrame):
        menu = FastFoodNutritionVisualizer.filter_menu(menu)
        variables = menu.columns
        n = len(variables)

        fig, axes = plt.subplots(1, n, figsize=(20, 5))

        for ax, column in zip(axes, variables):
            ax.hist(menu[column], color=FoodNutritionMapping[column][COLOR], bins=20, edgecolor='black')
            ax.set_title(column)
            ax.grid(True)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def filter_menu(menu: DataFrame) -> DataFrame:
        if FoodNutritionFeatures.MENU_ITEM in menu.keys():
            return menu.drop(FoodNutritionFeatures.MENU_ITEM, axis=1)
        else:
            return menu

    @staticmethod
    def generate_single_linear_regression(menu: DataFrame, independent_vars: Dict[str, str], target_var: str) -> None:
        # Setup the matplotlib figure and axes
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
        axes = axes.flatten()  # Flatten to easily index them

        # Remove the last subplot (since we have 5 variables and 6 subplots)
        fig.delaxes(axes[-1])

        # Loop through each independent variable and create plots
        for i, var in enumerate(independent_vars.keys()):
            # Perform linear regression
            slope, intercept, r_value, p_value, std_err = linregress(menu[var], menu[target_var])

            # Generate values for the regression line
            line = slope * menu[var] + intercept

            # Scatter plot and regression line
            axes[i].scatter(menu[var], menu[target_var], label=f'{var} vs {target_var}', color=FoodNutritionMapping[independent_vars[var]][COLOR], alpha=0.5)
            axes[i].plot(menu[var], line, color='red', label=f'Fit: {slope:.2f}*x + {intercept:.2f}')

            # Labeling
            axes[i].set_title(f'Regression of {var}')
            axes[i].set_xlabel(f'{var}')
            axes[i].set_ylabel(f'{target_var}')
            axes[i].legend()

        # Adjust layout
        plt.tight_layout()
        plt.show()

    @staticmethod
    def generate_multi_linear_regresssion(menu: DataFrame, independent_vars: Dict[str, str], target_var: str) -> None:
        # Prepare the data
        X = menu[independent_vars.keys()]
        y = menu[target_var]

        # Create and fit the model
        model = LinearRegression()
        model.fit(X, y)

        # Make predictions
        y_pred = model.predict(X)

        # Plot actual vs predicted values
        plt.figure(figsize=(10, 6))
        plt.scatter(y, y_pred, alpha=0.5)
        plt.plot([y.min(), y.max()], [y.min(), y.max()], '--r', linewidth=2)
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title('Actual vs. Predicted Composite Intake Score')
        plt.show()



