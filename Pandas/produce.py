import pandas as pd

items = [
    'Apples, Early Yellow Transparent', 'Apples, Gala', 'Apples, Gold Rush',
    'Apples, Red Rome Beauty', 'Apples, Spice', 'Basil, Fresh - Sweet Genovese (green)',
    'Beets, Without Greens', 'Collards', 'Garlic Scapes', 'Jerusalem Artichokes',
    'Lettuce, Head', 'Lettuce, Loose Leaf Green', 'Microgreens, Sunshine Mix',
    'Okra, Green', 'Peppers, Bell (Green)', 'Peppers, Jalapeno', 'Pumpkin, Seminole',
    'Rosemary, Fresh', 'Watermelon, Jubilee'
]

def myhash(user_name):
    import hashlib
    m = hashlib.sha256()
    m.update(bytes(user_name, 'utf-8'))
    return int(m.hexdigest()[:16], 16)

user_name = 'liamm'
item = items[myhash(user_name) % len(items)]
print(f'{user_name} cleans subcategory {item}')

def clean_row(row):
    if row['SubCategory'] != item:
        return row
    unit = row['Unit']
    units_sold = row['Units Sold']
    if item.startswith('Apples'):
        if 'bushel' in unit.lower() or 'Bushel' in unit:
            row['Unit'] = 'Peck'
            row['Units Sold'] = units_sold * 4
        elif '1/4 peck' in unit.lower() or '1/4 Peck' in unit:
            row['Unit'] = 'Peck'
            row['Units Sold'] = units_sold * 0.25
        elif 'peck' in unit.lower() or 'Peck' in unit:
            row['Unit'] = 'Peck'
    elif item == 'Collards':
        if 'bunch' in unit.lower() and '(' not in unit:
            row['Unit'] = 'bunch'
        elif 'lb' in unit.lower() and 'bag' in unit.lower():
            if '5 lb' in unit:
                row['Unit'] = 'bunch'
                row['Units Sold'] = units_sold * 5 * 16 / 14
        elif 'bunch' in unit.lower() and '(' in unit:
            row['Unit'] = 'bunch'
    
    elif item == 'Garlic Scapes':
        if 'bundle' in unit.lower():
            row['Unit'] = 'ounce'
            row['Units Sold'] = units_sold * 8
    elif item == 'Lettuce, Head':
        if 'case' in unit.lower():
            row['Unit'] = 'head'
            row['Units Sold'] = units_sold * 28
    elif item == 'Okra, Green':
        if 'quart' in unit.lower():
            row['Unit'] = 'lb'
            row['Units Sold'] = units_sold * 1.375
    elif item == 'Peppers, Bell (Green)':
        if 'pepper' in unit.lower():
            row['Unit'] = 'lb'
            row['Units Sold'] = units_sold * (1/3)
    elif item == 'Peppers, Jalapeno':
        if 'pint' in unit.lower():
            row['Unit'] = 'oz'
            row['Units Sold'] = units_sold * 16
        elif 'small bag' in unit.lower():
            row['Unit'] = 'oz'
            row['Units Sold'] = units_sold * 16
        elif 'pepper' in unit.lower():
            row['Unit'] = 'oz'
            row['Units Sold'] = units_sold * 4
    elif item == 'Rosemary, Fresh':
        if 'bunch' in unit.lower() and 'large' not in unit.lower():
            row['Unit'] = 'ounce'
            row['Units Sold'] = units_sold * 1
        elif 'large bunch' in unit.lower():
            row['Unit'] = 'ounce'
            row['Units Sold'] = units_sold * 1.5  # 1 / (2/3) = 1.5
    # Handle range values - use central value (only for items not specifically handled above)
    if '(' in unit and '-' in unit and ')' in unit and row['SubCategory'] != item:
        range_part = unit[unit.find('(')+1:unit.find(')')]
        if '-' in range_part:
            parts = range_part.split('-')
            if len(parts) == 2:
                try:
                    low = float(parts[0].strip().split()[0])
                    high_part = parts[1].strip().split()
                    high = float(high_part[0])
                    unit_name = high_part[1] if len(high_part) > 1 else parts[0].strip().split()[-1]
                    central_value = (low + high) / 2
                    row['Unit'] = unit_name
                    row['Units Sold'] = units_sold * central_value
                except:
                    pass  
    
    return row

def main():
    df = pd.read_csv('food.csv')
    df_cleaned = df.apply(clean_row, axis=1)
    df_cleaned.to_csv('cleaned_produce.csv', index=False)

if __name__ == '__main__':
    main()