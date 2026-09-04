"""
Sales Data Analyzer

A comprehensive interactive tool for loading, exploring, cleaning, analyzing,
and visualizing sales transaction data from a CSV file.

The dataset is expected to contain columns such as:
Order_ID, Order_Date, Customer_Name, City, State, Region, Country,
Category, Sub_Category, Product_Name, Quantity, Unit_Price, Revenue, Profit.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class SalesDataAnalyzer:
    """
    Interactive analyzer for sales transaction data.

    Provides menu-driven functionality to:
    - Load and clean sales data
    - Explore basic structure and statistics
    - Perform DataFrame operations (feature engineering, aggregations)
    - Generate various visualizations and save them
    """

    def __init__(self, file: str = None):
        """
        Initialize the SalesDataAnalyzer.

        Parameters
        ----------
        file : str, optional
            Path to the sales data CSV file. If provided, data is loaded
            automatically during initialization.
        """
        self.data = None
        self.file = file
        self.last_figure = None

        if file:
            self.load_data(file)

        print("SalesDataAnalyzer initialized successfully.")

    def __del__(self):
        """Clean up resources when the instance is destroyed."""
        self.data = None
        self.last_figure = None

    def load_data(self, file_path: str = None):
        """
        Load the sales dataset from a CSV file.

        Cleans column names by stripping whitespace. Defaults to
        'sales_data.csv' in the current working directory if no path
        is provided.

        Parameters
        ----------
        file_path : str, optional
            Full or relative path to the CSV file.
        """
        if file_path is None:
            candidates = [
                "sales_data.csv",
                "/home/workdir/attachments/sales_data.csv",
                os.path.join(os.path.dirname(__file__), "sales_data.csv"),
            ]
            for candidate in candidates:
                if os.path.exists(candidate):
                    file_path = candidate
                    break
            else:
                file_path = "sales_data.csv"

        try:
            self.data = pd.read_csv(file_path)
            self.data.columns = self.data.columns.str.strip()
            self.file = file_path
            print(f"Dataset loaded successfully from '{file_path}'.")
            print(f"Shape: {self.data.shape}")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            self.data = None
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = None

    def explore_data(self):
        """
        Interactive exploration of the loaded dataset.

        Offers options to display shape, head, tail, column names,
        data types, and basic DataFrame info.
        """
        if self.data is None:
            print("Please load the data first.")
            return

        def show_shape():
            print(self.data.shape)

        def show_head():
            print(self.data.head())

        def show_tail():
            print(self.data.tail())

        def show_columns():
            print(self.data.columns.tolist())

        def show_dtypes():
            print(self.data.dtypes)

        def show_info():
            self.data.info()

        while True:
            print(
                """
1. Display shape
2. Display the first 5 rows
3. Display the last 5 rows
4. Display column names
5. Display data types
6. Display basic info
7. Back to Main Menu
"""
            )
            try:
                sub_choice = int(input("Please enter valid sub-choice (1-7): "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if sub_choice == 1:
                show_shape()
            elif sub_choice == 2:
                show_head()
            elif sub_choice == 3:
                show_tail()
            elif sub_choice == 4:
                show_columns()
            elif sub_choice == 5:
                show_dtypes()
            elif sub_choice == 6:
                show_info()
            elif sub_choice == 7:
                break
            else:
                print("Invalid input. Please check.")

    def prepare_data(self):
        """
        Clean and prepare the dataset for analysis.

        - Converts Order_Date to datetime
        - Handles missing values by filling with the mode of each column
        - Creates helper columns (Month, Year, Day) useful for time-series plots
        """
        if self.data is None:
            print("Please load the data first.")
            return

        self.data.columns = self.data.columns.str.strip()

        self.data["Order_Date"] = pd.to_datetime(
            self.data["Order_Date"], format="%m-%d-%y", errors="coerce"
        )

        missing_values = self.data.isna().sum().sum()
        if missing_values == 0:
            print("There are no missing values in the data.")
        else:
            print(f"Found {missing_values} missing values. Filling with mode...")
            for col in self.data.columns:
                if self.data[col].isna().any():
                    mode_val = self.data[col].mode()
                    if not mode_val.empty:
                        self.data[col] = self.data[col].fillna(mode_val.iloc[0])

        self.data["Month"] = self.data["Order_Date"].dt.to_period("M").astype(str)
        self.data["Year"] = self.data["Order_Date"].dt.year
        self.data["Day"] = self.data["Order_Date"].dt.day_name()

        print("Data is clean and prepared now.")
        print(f"Date range: {self.data['Order_Date'].min()} to {self.data['Order_Date'].max()}")

    def dataframe_operations(self):
        """
        Perform various DataFrame operations and aggregations.

        Available operations:
        1. Add Day-of-week column
        2. Find State & City with highest average revenue
        3. Find Category/Sub-Category with max and min average profit
        4. Compute correlation matrix of numeric columns
        """
        if self.data is None:
            print("Please load the data first.")
            return

        def add_day_column():
            if "Order_Date" not in self.data.columns or not pd.api.types.is_datetime64_any_dtype(
                self.data["Order_Date"]
            ):
                print("Order_Date is not available or not converted. Run Prepare Data first.")
                return
            self.data["Day"] = self.data["Order_Date"].dt.day_name()
            self.data["Month"] = self.data["Order_Date"].dt.to_period("M").astype(str)
            print("Day and Month columns added successfully.")
            print(self.data[["Order_Date", "Day", "Month"]].head())

        def state_city_max_revenue():
            result = (
                self.data.groupby(["State", "City"])["Revenue"]
                .mean()
                .sort_values(ascending=False)
                .head(1)
            )
            print("\nState and City with maximum average Revenue:")
            print(result)

        def categories_subcategories_max_and_min_profit():
            grouped = (
                self.data.groupby(["Category", "Sub_Category"])["Profit"]
                .mean()
                .sort_values(ascending=False)
            )
            print("\nCategory & Sub-Category with MAXIMUM average Profit:")
            print(grouped.head(1))
            print("\nCategory & Sub-Category with MINIMUM average Profit:")
            print(grouped.tail(1))

        def correlation():
            num_cols = self.data.select_dtypes(include=np.number)
            print("\nCorrelation Matrix:")
            print(num_cols.corr().round(3))

        while True:
            print(
                """
1. Add Day and Month columns
2. State and City with max revenue
3. Categories and Subcategories with max and min profit
4. Find correlation
5. Back to Main Menu
"""
            )
            try:
                sub_choice = int(input("Please enter valid sub-choice (1-5): "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if sub_choice == 1:
                add_day_column()
            elif sub_choice == 2:
                state_city_max_revenue()
            elif sub_choice == 3:
                categories_subcategories_max_and_min_profit()
            elif sub_choice == 4:
                correlation()
            elif sub_choice == 5:
                break
            else:
                print("Invalid input. Please check.")

    def des_statistics(self):
        """
        Generate and display descriptive statistics for numeric columns.
        """
        if self.data is None:
            print("Please load the data first.")
            return
        print("\nDescriptive Statistics:")
        print(self.data.describe().T.round(2))

    def visualization(self):
        """
        Interactive visualization menu.

        Generates common sales analytics charts.
        """
        if self.data is None:
            print("Please load the data first.")
            return

        def bar_chart():
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(
                data=self.data,
                x="Category",
                y="Revenue",
                estimator="sum",
                errorbar=None,
                ax=ax,
            )
            ax.set_title("Total Revenue by Category")
            ax.tick_params(axis="x", rotation=15)
            plt.tight_layout()
            self.last_figure = fig
            plt.show()
            plt.close()

        def line_chart():
            if "Month" not in self.data.columns:
                print("Month column not available. Add Day and Month columns first (DataFrame Operations → option 1).")
                return
            monthly_sales = (
                self.data.groupby("Month")["Revenue"].sum().reset_index()
            )
            try:
                monthly_sales = monthly_sales.sort_values("Month")
            except Exception:
                pass

            fig, ax = plt.subplots(figsize=(10, 5))
            sns.lineplot(
                data=monthly_sales,
                x="Month",
                y="Revenue",
                marker="o",
                color="purple",
                ax=ax,
            )
            ax.set_title("Monthly Revenue Timeline Trend")
            ax.tick_params(axis="x", rotation=45)
            plt.tight_layout()
            self.last_figure = fig
            plt.show()
            plt.close()

        def scatter_chart():
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.scatterplot(
                data=self.data,
                x="Revenue",
                y="Profit",
                hue="Category",
                alpha=0.6,
                ax=ax,
            )
            ax.set_title("Transaction Level Revenue vs Profit")
            plt.tight_layout()
            self.last_figure = fig
            plt.show()
            plt.close()

        def pie_chart():
            region_data = self.data.groupby("Region")["Revenue"].sum()
            fig, ax = plt.subplots(figsize=(7, 7))
            ax.pie(
                region_data,
                labels=region_data.index,
                autopct="%1.1f%%",
                startangle=140,
            )
            ax.set_title("Revenue Contribution Split by Region")
            self.last_figure = fig
            plt.show()
            plt.close()

        def histogram():
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.histplot(
                data=self.data,
                x="Quantity",
                bins=10,
                color="orange",
                ax=ax,
            )
            ax.set_title("Distribution Frequency of Item Quantities Purchased")
            plt.tight_layout()
            self.last_figure = fig
            plt.show()
            plt.close()

        def stack_chart():
            stacked_data = (
                self.data.groupby(["Region", "Category"])["Revenue"]
                .sum()
                .unstack(fill_value=0)
            )
            fig, ax = plt.subplots(figsize=(9, 5))
            stacked_data.plot(
                kind="bar",
                stacked=True,
                ax=ax,
                colormap="viridis",
            )
            ax.set_title("Stacked Regional Revenue Segment Breakdown")
            ax.set_ylabel("Total Revenue")
            ax.tick_params(axis="x", rotation=0)
            ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
            plt.tight_layout()
            self.last_figure = fig
            plt.show()
            plt.close()

        while True:
            print(
                """
========== Visualization ==========
1. Bar Chart          (Total Revenue by Category)
2. Line Chart         (Monthly Revenue Trend)
3. Scatter Chart      (Revenue vs Profit)
4. Pie Chart          (Revenue by Region)
5. Histogram          (Quantity Distribution)
6. Stack Chart        (Region x Category Revenue)
7. Back to Main Menu
===================================
"""
            )
            try:
                sub_choice = int(input("Please enter valid sub-choice (1-7): "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if sub_choice == 1:
                bar_chart()
            elif sub_choice == 2:
                line_chart()
            elif sub_choice == 3:
                scatter_chart()
            elif sub_choice == 4:
                pie_chart()
            elif sub_choice == 5:
                histogram()
            elif sub_choice == 6:
                stack_chart()
            elif sub_choice == 7:
                break
            else:
                print("Invalid input. Please check.")

    def save_visualization(self):
        """
        Generate and directly save all charts with fixed filenames.

        Saves:
        - title_bar_chart.png
        - title_line_chart.png
        - title_scatter_chart.png
        - title_pie_chart.png
        - title_histogram.png
        - title_stack_chart.png
        """
        if self.data is None:
            print("Please load the data first.")
            return

        # 1. Bar Chart
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(
            data=self.data,
            x="Category",
            y="Revenue",
            estimator="sum",
            errorbar=None,
            ax=ax,
        )
        ax.set_title("Total Revenue by Category")
        ax.tick_params(axis="x", rotation=15)
        plt.tight_layout()
        fig.savefig("title_bar_chart.png", dpi=150, bbox_inches="tight")
        print("Saved as 'title_bar_chart.png'")
        plt.close(fig)

        # 2. Line Chart
        if "Month" in self.data.columns:
            monthly_sales = (
                self.data.groupby("Month")["Revenue"].sum().reset_index()
            )
            try:
                monthly_sales = monthly_sales.sort_values("Month")
            except Exception:
                pass

            fig, ax = plt.subplots(figsize=(10, 5))
            sns.lineplot(
                data=monthly_sales,
                x="Month",
                y="Revenue",
                marker="o",
                color="purple",
                ax=ax,
            )
            ax.set_title("Monthly Revenue Timeline Trend")
            ax.tick_params(axis="x", rotation=45)
            plt.tight_layout()
            fig.savefig("title_line_chart.png", dpi=150, bbox_inches="tight")
            print("Saved as 'title_line_chart.png'")
            plt.close(fig)
        else:
            print("Skipped line chart (Month column not available. Add Day and Month columns first).")

        # 3. Scatter Chart
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(
            data=self.data,
            x="Revenue",
            y="Profit",
            hue="Category",
            alpha=0.6,
            ax=ax,
        )
        ax.set_title("Transaction Level Revenue vs Profit")
        plt.tight_layout()
        fig.savefig("title_scatter_chart.png", dpi=150, bbox_inches="tight")
        print("Saved as 'title_scatter_chart.png'")
        plt.close(fig)

        # 4. Pie Chart
        region_data = self.data.groupby("Region")["Revenue"].sum()
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(
            region_data,
            labels=region_data.index,
            autopct="%1.1f%%",
            startangle=140,
        )
        ax.set_title("Revenue Contribution Split by Region")
        fig.savefig("title_pie_chart.png", dpi=150, bbox_inches="tight")
        print("Saved as 'title_pie_chart.png'")
        plt.close(fig)

        # 5. Histogram
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(
            data=self.data,
            x="Quantity",
            bins=10,
            color="orange",
            ax=ax,
        )
        ax.set_title("Distribution Frequency of Item Quantities Purchased")
        plt.tight_layout()
        fig.savefig("title_histogram.png", dpi=150, bbox_inches="tight")
        print("Saved as 'title_histogram.png'")
        plt.close(fig)

        # 6. Stack Chart
        stacked_data = (
            self.data.groupby(["Region", "Category"])["Revenue"]
            .sum()
            .unstack(fill_value=0)
        )
        fig, ax = plt.subplots(figsize=(9, 5))
        stacked_data.plot(
            kind="bar",
            stacked=True,
            ax=ax,
            colormap="viridis",
        )
        ax.set_title("Stacked Regional Revenue Segment Breakdown")
        ax.set_ylabel("Total Revenue")
        ax.tick_params(axis="x", rotation=0)
        ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
        plt.tight_layout()
        fig.savefig("title_stack_chart.png", dpi=150, bbox_inches="tight")
        print("Saved as 'title_stack_chart.png'")
        plt.close(fig)

        print("\nAll charts saved successfully.")


def main():
    """
    Entry point for the interactive Sales Data Analyzer application.
    """
    analyzer = SalesDataAnalyzer()

    while True:
        print(
            f"""
{'=' * 50}
1. Load Dataset
2. Explore Dataset
3. Preparing Dataset
4. DataFrame Operations
5. Generate Descriptive Statistics
6. Visualization
7. Save Visualization
8. Exit
{'=' * 50}
"""
        )
        try:
            choice = int(input("Please enter valid choice (1-8): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")
            continue

        if choice == 1:
            analyzer.load_data()
        elif choice == 2:
            analyzer.explore_data()
        elif choice == 3:
            analyzer.prepare_data()
        elif choice == 4:
            analyzer.dataframe_operations()
        elif choice == 5:
            analyzer.des_statistics()
        elif choice == 6:
            analyzer.visualization()
        elif choice == 7:
            analyzer.save_visualization()
        elif choice == 8:
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    main()
