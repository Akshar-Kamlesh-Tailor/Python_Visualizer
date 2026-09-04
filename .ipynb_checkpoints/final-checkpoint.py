import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class SalesDataAnalyzer:
    """
    A class-based tool designed to execute standard data analysis pipelines
    on tabular retail logs. Supports loading, formatting, transforming,
    profiling, and exporting chart configurations.
    """
    def __init__(self, file=None):
        """Initializes internal class attributes and loads file context if provided."""
        self.data = None
        self.file = file
        self.figure = None

        if file:
            self.load_data()

        print("\n" + "═"*50)
        print("  SalesDataAnalyzer initialized successfully.")
        print("═"*50)

    def __del__(self):
        """Cleans memory addresses during garbage collection runs."""
        self.data = None
        self.figure = None

    def load_data(self):
        """Loads a localized retail CSV into an internal Pandas DataFrame."""
        self.file = 'sales_data.csv'
        if not os.path.exists(self.file):
            print(f"\n┌──────────────────────────────────────────┐")
            print(f"│ Error: '{self.file}' was not found. │")
            print(f"└──────────────────────────────────────────┘")
            return
        
        self.data = pd.read_csv(self.file)
        # Strip trailing text gaps from column labels to optimize query execution paths
        self.data.columns = self.data.columns.str.strip()
        
        print(f"\n┌──────────────────────────────────────────┐")
        print(f"│ Data successfully loaded from local log │")
        print(f"└──────────────────────────────────────────┘")

    def explore_data(self):
        """Provides an interactive loop to preview dataset layout, shapes, and structural fields."""
        if self.data is not None:
            def shape():
                print(f"\n[Dataset Structural Metrics]")
                print(f"Rows: {self.data.shape[0]} | Columns: {self.data.shape[1]}")
            
            def head():
                print(f"\n[First 5 Data Rows View]")
                print(self.data.head().to_string())

            def tail():
                print(f"\n[Last 5 Data Rows View]")
                print(self.data.tail().to_string())

            def columns():
                print(f"\n[Identified System Labels List]")
                print(self.data.columns.tolist())
            
            def datatypes():
                print(f"\n[Column Structural Classifications]")
                print(self.data.dtypes.to_string())
            
            def information():
                print(f"\n[Core DataFrame Meta-Profile Summary]")
                self.data.info()

            while True:
                print("\n┌" + "─"*38 + "┐")
                print("│        DATA EXPLORATION PROFILE       │")
                print("├" + "─"*38 + "┤")
                print("│  1. Display Layout Dimensions         │")
                print("│  2. Preview Leading Rows (Head)       │")
                print("│  3. Preview Trailing Rows (Tail)      │")
                print("│  4. Display Target Labels List       │")
                print("│  5. Profile Internal Gaps/Data-Types │")
                print("│  6. Print Consolidated Metadata Log   │")
                print("│  7. Back to Main Application Loop     │")
                print("└" + "─"*38 + "┘")
                
                try:
                    sub_choice = int(input('Please enter sub-choice (1-7): '))
                    if sub_choice == 1: shape()
                    elif sub_choice == 2: head()
                    elif sub_choice == 3: tail()
                    elif sub_choice == 4: columns()
                    elif sub_choice == 5: datatypes()
                    elif sub_choice == 6: information()
                    elif sub_choice == 7: break
                    else: print(">> Invalid input. Choose between 1 and 7.")
                except ValueError:
                    print(">> Invalid character entries detected. Input an integer number.")
        else:
            print('\n>> Access Error: Please execute dataset load step first via option 1.')
            return 
            
    def prepare_data(self):
        """Executes the standard cleaning pipeline: casts strings to datetime formats, indices, and drops anomalies."""
        if self.data is not None:
            print("\nExecuting Data Cleaning Sequence...")
            # Coerce corrupted strings safely to catch broken metadata strings
            self.data['Order_Date'] = pd.to_datetime(self.data['Order_Date'], errors='coerce')

            missing_values = self.data.isna().sum().sum()
            if missing_values == 0:
                print('>> Validation Confirmation: There are zero missing values present.')
            else:
                print(f">> Gaps Tracker: Found {missing_values} empty entries. Executing global Mode imputation...")
                for col in self.data.columns:
                    if self.data[col].isna().sum() > 0:
                        mode_series = self.data[col].mode()
                        if not mode_series.empty:
                            self.data[col] = self.data[col].fillna(mode_series[0])
            
            print(f"\n┌──────────────────────────────────────────┐")
            print(f"│ Cleaning complete. File registry secure. │")
            print(f"└──────────────────────────────────────────┘")
        else:
            print('\n>> Access Error: Please execute dataset load step first via option 1.')
            return

    def dataframe_operations(self):
        """Applies algebraic operations, conditional filtering metrics, and multidimensional slice indicators."""
        if self.data is None:
            print('\n>> Access Error: Please execute dataset load step first via option 1.')
            return

        def add_col():
            try:
                self.data['Day'] = self.data['Order_Date'].dt.day_name()
                self.month['Month'] = self.data['Order_Date'].dt.month_name()
                print("\n>> Operation Success: New attribute line 'Day' attached.")
                print("\n>> Operation Success: New attribute line 'Month' attached.")
                print(f"Updated Field Labels: {self.data.columns.tolist()}")
            except AttributeError:
                print(">> Parsing Error: Columns not structured as datetimes. Run preparation option first.")

        def state_city_max_revenue():
            print(f"\n" + "-"*45)
            print(" STATE & CITY WITH MAXIMUM GROSS REVENUE")
            print("-"*45)
            grouped = self.data.groupby(['State','City'])['Revenue'].sum().sort_values(ascending=False)
            print(grouped.head(1).to_frame().to_string())

        def categories_subcategories_max_and_min_profit():
            grouped = self.data.groupby(['Category','Sub_Category'])['Profit'].sum().sort_values(ascending=False)
            print(f"\n" + "-"*45)
            print(" PRODUCT BREAKDOWN: MAXIMUM REVENUE GAINS")
            print("-"*45)
            print(grouped.head(1).to_frame().to_string())
            print(f"\n" + "-"*45)
            print(" PRODUCT BREAKDOWN: MINIMUM REVENUE GAINS")
            print("-"*45)
            print(grouped.tail(1).to_frame().to_string())

        def correlation():
            print(f"\n" + "-"*45)
            print(" QUANTITATIVE VARIABLE CORRELATION MATRIX")
            print("-"*45)
            num_cols = self.data.select_dtypes(include=np.number)
            print(num_cols.corr().round(3).to_string())

        while True:
            print("\n┌" + "─"*38 + "┐")
            print("│         DATAFRAME OPERATIONS          │")
            print("├" + "─"*38 + "┤")
            print("│  1. Engineer Day-of-Week Column      │")
            print("│  2. Locate Maximum Regional Revenue   │")
            print("│  3. Sift Maximum & Minimum Profit Margins │")
            print("│  4. Extract Numeric Variable Matrix  │")
            print("│  5. Back to Main Application Loop     │")
            print("└" + "─"*38 + "┘")
            
            try:
                sub_choice = int(input('Please enter valid sub-choice (1-5): '))
                if sub_choice == 1: add_col()
                elif sub_choice == 2: state_city_max_revenue()
                elif sub_choice == 3: categories_subcategories_max_and_min_profit()
                elif sub_choice == 4: correlation()
                elif sub_choice == 5: break
                else: print(">> Invalid input. Choose between 1 and 5.")
            except ValueError:
                print(">> Invalid character entries detected. Input an integer number.")

    def des_statistics(self):
        """Generates a summary profile matrix containing means, counts, spreads, percentiles and variances."""
        if self.data is not None:
            print(f"\n" + "═"*50)
            print("          TRANSPOSED DATA SUMMARY METRICS")
            print("═"*50)
            print(self.data.describe().T.to_string())
            print("═"*50)
        else:
            print('\n>> Access Error: Please execute dataset load step first via option 1.')

    def visualization(self):
        """Opens a dynamic graphical generator engine module inside the active notebook or script."""
        if self.data is None:
            print('\n>> Access Error: Please execute dataset load step first via option 1.')
            return

        sns.set_theme(style="whitegrid")

        def bar_chart():
            plt.figure(figsize=(8, 5))
            sns.barplot(data=self.data, x='Category', y='Revenue', estimator=sum, errorbar=None)
            plt.title('Total Revenue by Category', fontweight='bold', pad=12)
            self.figure = plt.gcf()
            plt.show()
            
        def line_chart():
            plt.figure(figsize=(10, 5))
            monthly_sales = self.data.groupby('Month')['Revenue'].sum().reset_index()
            sns.lineplot(data=monthly_sales, x='Month', y='Revenue', marker='o', color='purple')
            plt.title('Monthly Revenue Timeline Trend', fontweight='bold', pad=12)
            plt.xticks(rotation=45)
            self.figure = plt.gcf()
            plt.show()
        
        def scatter_chart():
            plt.figure(figsize=(8, 5))
            sns.scatterplot(data=self.data, x='Revenue', y='Profit', hue='Category')
            plt.title('Transaction Level Revenue vs Profit Space', fontweight='bold', pad=12)
            self.figure = plt.gcf()
            plt.show()
            
        def pie_chart():
            plt.figure(figsize=(6, 6))
            region_data = self.data.groupby('Region')['Revenue'].sum()
            plt.pie(region_data, labels=region_data.index, autopct='%1.1f%%', startangle=140)
            plt.title('Revenue Contribution Split by Region', fontweight='bold', pad=12)
            self.figure = plt.gcf()
            plt.show()
        
        def histogram():
            plt.figure(figsize=(8, 5))
            sns.histplot(data=self.data, x='Quantity', bins=5, color='orange')
            plt.title('Distribution Frequency of Item Quantities Purchased', fontweight='bold', pad=12)
            self.figure = plt.gcf()
            plt.show()

        def stack_chart():
            plt.figure(figsize=(8, 5))
            stacked_data = self.data.groupby(['Region', 'Category'])['Revenue'].sum().unstack()
            stacked_data.plot(kind='bar', stacked=True, figsize=(8, 5), colormap='viridis')
            plt.title('Stacked Regional Revenue Segment Breakdown', fontweight='bold', pad=12)
            plt.ylabel('Total Revenue Value ($)')plt.xticks(rotation=0)
            self.figure = plt.gcf()
            plt.show()
            
        while True:
            print("\n┌" + "─"*38 + "┐")
            print("│         DATA VISUALIZATION MENU      │")
            print("├" + "─"*38 + "┤")
            print("│  1. Category Gross Bar Chart         │")
            print("│  2. Monthly Growth Line Graph        │")
            print("│  3. Value Matrix Sifting Scatter     │")
            print("│  4. Regional Segment Donut Pie Share │")
            print("│  5. Frequency Volume Histogram       │")
            print("│  6. Stacked Layer Regional Breakdown │")
            print("│  7. Return to Core Application Loop  │")
            print("└" + "─"*38 + "┘")
            
            try:
                sub_choice = int(input('Please enter valid sub-choice (1-7): '))
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
                    print(">> Invalid input. Choose between 1 and 7.")
            except ValueError:
                print(">> Invalid character entries detected. Input an integer number.")
                
        def save_visualization(self):
            """Saves whichever plot layout handle configuration was displayed last to disk filesystem."""
            if self.figure is None:
                print("\n>> System Flag Warning: No active figure generated inside active memory state yet.")
                print(">> Please display a figure chart under choice option 6 first.")
                returnfilename = input("\nEnter custom system image label file string (e.g. quarterly_returns.png): ").strip()
            if not filename:filename = "plot.png"self.figure.savefig(filename, dpi=150,bbox_inches="tight")
                print(f"\n┌──────────────────────────────────────────┐")
                print(f"│ Graphic successfully saved to local tree │")
                print(f"│ Path: {filename}                    │")
                print(f"└──────────────────────────────────────────┘")
            
def main():
    analyzer = SalesDataAnalyzer()
    while True:
        print("\n" + "═"*50)
        print("         CORE PIPELINE ANALYSIS CONSOLE")
        print("═"*50)
        print("  1. Load Target System File Log (.csv)")
        print("  2. Explore Structural Fields Parameters")
        print("  3. Run Pipeline Cleaning/Preparation Sequences")
        print("  4. Execute Group Slices & Operations")
        print("  5. Generate Descriptive Summaries Profile")
        print("  6. Launch Graphical Visualizations Module")
        print("  7. Export Memory Render Chart to Disk")
        print("  8. Close Application and Session")
        print("═"*50)
        try:
            choice = int(input('Please enter system choice choice (1-8): '))
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
                print("\nShutting down operational matrix modules. Safe exit confirmed.")
                break
            else:
                print(">> Out of bound indicator metric. Type integers 1-8.")
        except ValueError:
            print(">> Broken command sequence layer. Type a single integer.")
            
if name == 'main':main()