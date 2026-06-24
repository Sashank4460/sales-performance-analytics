import pandas as pd
import numpy as np
from faker import Faker
import random, os

fake = Faker()
np.random.seed(42)
random.seed(42)

regions    = ["North", "South", "East", "West", "Central"]
categories = ["Electronics", "Clothing", "Furniture", "Sports", "Groceries"]
products = {
    "Electronics": ["Laptop", "Phone", "Tablet", "Headphones", "Smartwatch"],
    "Clothing":    ["T-Shirt", "Jeans", "Jacket", "Shoes", "Dress"],
    "Furniture":   ["Chair", "Table", "Sofa", "Bed Frame", "Shelf"],
    "Sports":      ["Cricket Bat", "Football", "Yoga Mat", "Dumbbells", "Cycle"],
    "Groceries":   ["Rice", "Oil", "Flour", "Sugar", "Pulses"],
}
price_map = {
    "Laptop":9999,"Phone":6999,"Tablet":4999,"Headphones":1999,"Smartwatch":2999,
    "T-Shirt":499,"Jeans":999,"Jacket":1499,"Shoes":1299,"Dress":799,
    "Chair":2499,"Table":3999,"Sofa":12999,"Bed Frame":8999,"Shelf":1999,
    "Cricket Bat":799,"Football":499,"Yoga Mat":399,"Dumbbells":999,"Cycle":5999,
    "Rice":99,"Oil":149,"Flour":79,"Sugar":59,"Pulses":119,
}

rows = []
for i in range(10500):
    cat  = random.choice(categories)
    prod = random.choice(products[cat])
    month = random.randint(1, 12)
    year  = random.choice([2023, 2024])
    qty   = random.randint(1, 20)
    price = price_map[prod] * random.uniform(0.85, 1.15)
    disc  = random.choice([0, 5, 10, 15, 20])
    rev   = round(qty * price * (1 - disc / 100), 2)
    rows.append({
        "order_id":     f"ORD{10000+i}",
        "date":         f"{year}-{month:02d}-{random.randint(1,28):02d}",
        "region":       random.choice(regions),
        "category":     cat,
        "product":      prod,
        "quantity":     qty,
        "unit_price":   round(price, 2),
        "discount_pct": disc,
        "revenue":      rev,
        "salesperson":  fake.name(),
    })

df = pd.DataFrame(rows)
df.loc[df.sample(50).index, "discount_pct"] = np.nan   # inject nulls
df = pd.concat([df, df.sample(30)], ignore_index=True)  # inject duplicates

os.makedirs("data", exist_ok=True)
df.to_csv("data/raw_sales.csv", index=False)
print(f"Generated {len(df)} rows  →  data/raw_sales.csv")
