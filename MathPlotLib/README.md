# P08.PY Usage Guide

## Overview

This assignment implements two functions for visualizing produce sales data from 2019:

1. `bar_plot()` - Creates a bar chart for a single subcategory
2. `bars_plot()` - Creates multiple bar charts for subcategories starting with a given phrase

## Files Required

- `p08.py` - Main implementation
- `food_cleaned.csv` - The cleaned produce data file

## How to Run

### Method 1: Interactive Mode

```bash
python p08.py
```

This will give you options:

1. Single subcategory bar plot
2. Multiple subcategories bar plots
3. Run single subcategory (default)

### Method 2: Direct Function Testing

Use the included test files:

- `test_p08.py` - Basic functionality test
- `demo_p08.py` - Comprehensive demonstration

## Example Inputs

### For Single Bar Plot (bar_plot):

- "Apples, Blushing Gold"
- "Apples, Chehalis"
- "Berries, Blueberries"

### For Multiple Bar Plots (bars_plot):

- "Apples" (shows all apple varieties)
- "Berries" (shows all berry types)
- "Herbs" (shows all herb varieties)

## Features Implemented

### Base Requirements (B Grade):

✅ `bar_plot()` function with correct signature
✅ `bars_plot()` function with correct signature  
✅ Aggregates units sold by month for 2019
✅ Returns matplotlib axes objects
✅ Proper file naming (p08.py)

### Extra Features (Higher Grade):

✅ Proper date parsing and chronological month ordering
✅ Enhanced error handling for invalid subcategories
✅ Improved subplot spacing and formatting
✅ Color customization for better visualization
✅ Value labels on top of bars
✅ Grid lines for easier reading
✅ Professional styling and layout
✅ Interactive menu system
✅ Comprehensive test coverage
✅ Demonstration script with examples

## Sample Output

The functions create bar charts showing:

- X-axis: Months (Jan, Feb, Mar, etc.)
- Y-axis: Units Sold
- Title: Specific to the subcategory/categories being displayed
- Values displayed on top of each bar
- Professional formatting with colors and grid

## Data Structure

The CSV file contains columns:

- Category: Main category (e.g., "Fruits & Vegetables - Apples")
- SubCategory: Specific product (e.g., "Apples, Blushing Gold")
- Unit: Measurement unit (e.g., "1/4 Peck")
- Month Sold: Date in "19-MMM" format (e.g., "19-Sep")
- Units Sold: Numeric quantity sold
