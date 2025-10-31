# produce.py
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

user_name = 'silvasantiagoor'
item = items[myhash(user_name) % len(items)]
print(f'{user_name} cleans subcategory {item}')

def clean(row):
    if row['SubCategory'] == item:
        if 'Each' in row['Unit']:
            row['Unit'] = '1 pepper'
        elif 'Pound' in row['Unit']:
            row['Units Sold'] *= 3
            row['Unit'] = '1 pepper'
    return row

def main():
    # Load and process the 'food.csv' file.
    # Save the file 'cleaned_produce.csv' without the implicit index
    df = pd.read_csv('food.csv')
    # filtered_df = df[df['SubCategory'] == item]
    # print(filtered_df)
    # print(df.iloc[:, 1:])
    df = df.apply(clean, axis=1)
    # filtered_df = df[df['SubCategory'] == item]
    # print(filtered_df)
    df.to_csv('cleaned_produce.csv', index=False)


if __name__ == '__main__':
    main()