# p08.py
# Name: Liam Curiel
# Extra features implemented:
# - Month names on x-axis instead of numbers
# - Month abbreviations on bottom subplot
# - Average purchase month displayed on each subplot
# - Different colors for each plot
# - Subcategories sorted by increasing average month of purchase

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_expected_month(monthly_data):
    if monthly_data.empty or monthly_data['Units Sold'].sum() == 0:
        return 6.5  
    month_angles = {
        1: 0, 2: 30, 3: 60, 4: 90, 5: 120, 6: 150,
        7: 180, 8: 210, 9: 240, 10: 270, 11: 300, 12: 330
    }
    total_units = monthly_data['Units Sold'].sum()
    if total_units == 0:
        return 6.5  
    weighted_x = 0
    weighted_y = 0
    
    for _, row in monthly_data.iterrows():
        month_num = row['Month_Date'].month
        units = row['Units Sold']
        
        if month_num in month_angles and units > 0:
            angle_rad = np.radians(month_angles[month_num])
            weighted_x += (units * np.cos(angle_rad))
            weighted_y += (units * np.sin(angle_rad))
    if total_units == 0:
        return 6.5
        
    avg_x = weighted_x / total_units
    avg_y = weighted_y / total_units
    avg_angle_rad = np.arctan2(avg_y, avg_x)
    avg_angle_deg = np.degrees(avg_angle_rad)
    if avg_angle_deg < 0:
        avg_angle_deg += 360
    expected_month = (avg_angle_deg / 30) % 12 + 1
    if expected_month < 1 or expected_month > 12:
        return 6.5
    return expected_month


def bar_plot(df, subcategory):
    df = df.copy()
    df['Month_Date'] = pd.to_datetime('20' + df['Month Sold'], format='%Y-%b')
    filtered_df = df[df['SubCategory'] == subcategory].copy()
    if filtered_df.empty:
        print(f"No data found for subcategory: {subcategory}")
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"No data found for '{subcategory}'", 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f"Units and {subcategory}")
        return ax
    monthly_data = filtered_df.groupby('Month_Date')['Units Sold'].sum().reset_index()
    date_range = pd.date_range(start='2019-01-01', end='2019-12-01', freq='MS')
    monthly_data = monthly_data.set_index('Month_Date').reindex(date_range, fill_value=0).reset_index()
    monthly_data.columns = ['Month_Date', 'Units Sold']
    fig, ax = plt.subplots()
    monthly_data.set_index('Month_Date')['Units Sold'].plot(kind='bar', ax=ax)
    ax.set_title(f"Units and {subcategory}")
    ax.set_xlabel('Month')
    month_names = [date.strftime('%b') for date in monthly_data['Month_Date']]
    ax.set_xticklabels(month_names)
    expected_month = calculate_expected_month(monthly_data)
    month_names_full = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_index = int(expected_month - 1)
    month_decimal = expected_month - int(expected_month)
    
    if month_decimal < 0.5 and month_index < 11:
        expected_month_name = month_names_full[month_index]
    elif month_decimal >= 0.5 and month_index < 11:
        expected_month_name = f"{month_names_full[month_index]}-{month_names_full[month_index + 1]}"
    else:
        expected_month_name = month_names_full[month_index]
        
    ax.text(0.02, 0.98, f"Expected month: {expected_month:.1f} ({expected_month_name})", 
            transform=ax.transAxes, verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return ax

def bars_plot(df, starts_with):
    df = df.copy()
    df['Month_Date'] = pd.to_datetime('20' + df['Month Sold'], format='%Y-%b')
    filtered_df = df[df['SubCategory'].str.startswith(starts_with, na=False)].copy()
    if filtered_df.empty:
        print(f"No subcategories found starting with: {starts_with}")
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"No subcategories found starting with '{starts_with}'", 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f"Subcategories starting with \"{starts_with}\"")
        return ax
    agg_data = filtered_df.groupby(['SubCategory', 'Month_Date'])['Units Sold'].sum().reset_index()
    subcategories = filtered_df['SubCategory'].unique()
    subcategory_expected_months = {}
    date_range = pd.date_range(start='2019-01-01', end='2019-12-01', freq='MS')
    for subcat in subcategories:
        subcat_data = agg_data[agg_data['SubCategory'] == subcat]
        monthly_data = subcat_data.groupby('Month_Date')['Units Sold'].sum().reset_index()
        monthly_data = monthly_data.set_index('Month_Date').reindex(date_range, fill_value=0).reset_index()
        monthly_data.columns = ['Month_Date', 'Units Sold']
        
        expected_month = calculate_expected_month(monthly_data)
        subcategory_expected_months[subcat] = expected_month
    subcategories = sorted(subcategories, key=lambda x: subcategory_expected_months[x])
    num_plots = len(subcategories)
    fig, axes = plt.subplots(num_plots, 1, figsize=(10, 3 * num_plots))
    if num_plots == 1:
        axes = [axes]
    colors = plt.cm.tab10(np.linspace(0, 1, num_plots))
    for i, subcategory in enumerate(subcategories):
        subcat_data = agg_data[agg_data['SubCategory'] == subcategory]
        monthly_data = subcat_data.groupby('Month_Date')['Units Sold'].sum().reset_index()
        monthly_data = monthly_data.set_index('Month_Date').reindex(date_range, fill_value=0).reset_index()
        monthly_data.columns = ['Month_Date', 'Units Sold']
        monthly_data.set_index('Month_Date')['Units Sold'].plot(kind='bar', ax=axes[i], color=colors[i])
        axes[i].text(0.02, 0.95, subcategory, transform=axes[i].transAxes, 
                    verticalalignment='top', fontweight='bold')
        expected_month = subcategory_expected_months[subcategory]
        month_names_full = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_index = int(expected_month - 1) if expected_month <= 12 else 5
        month_decimal = expected_month - int(expected_month) if expected_month <= 12 else 0.5
        
        if month_decimal < 0.5 and month_index < 11:
            expected_month_name = month_names_full[month_index]
        elif month_decimal >= 0.5 and month_index < 11:
            expected_month_name = f"{month_names_full[month_index]}-{month_names_full[month_index + 1]}"
        else:
            expected_month_name = month_names_full[month_index] if month_index < 12 else 'Jun'
            
        axes[i].text(0.02, 0.85, f"Avg: {expected_month:.1f} ({expected_month_name})", 
                    transform=axes[i].transAxes, verticalalignment='top', fontsize=10)
        axes[i].legend().set_visible(False)
        if i == num_plots - 1:  
            month_names = [date.strftime('%b') for date in monthly_data['Month_Date']]
            axes[i].set_xticklabels(month_names)
            axes[i].set_xlabel('Month')
        else:
            axes[i].set_xticklabels([])  
        
        axes[i].tick_params(axis='x', rotation=45)
    if num_plots > 0:
        axes[0].set_title(f"Units Sold by Month - Subcategories starting with \"{starts_with}\"")
    
    plt.tight_layout()
    
    return axes

def main_bar():
    subcategory = input('Enter SubCategory: ')
    df = pd.read_csv('food_cleaned.csv')
    bar_plot(df, subcategory)
    plt.show()

def main_bars():
    starts_with = input('Enter starts-with phrase: ')
    df = pd.read_csv('food_cleaned.csv')
    bars_plot(df, starts_with)
    plt.show()
if __name__ == '__main__':
    print("Choose an option:")
    print("1. Single subcategory bar plot")
    print("2. Multiple subcategories bar plots") 
    print("3. Run single subcategory (default)")
    choice = input("Enter choice (1-3, or press Enter for default): ").strip()
    
    if choice == "2":
        main_bars()
    else:
        main_bar()
