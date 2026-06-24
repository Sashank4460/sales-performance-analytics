# 📊 Sales Performance Analytics Dashboard

> **Tech Stack:** Python · Pandas · NumPy · Seaborn · Matplotlib · CSV

A complete end-to-end data analysis project simulating a retail business with 10,000+ sales records. Covers data ingestion, cleaning, EDA, and multi-chart visualization.

---

## 🔍 What This Project Does

- Generates a realistic 10,500-row retail sales dataset (with injected nulls & duplicates for realism)
- Cleans and validates the data (deduplication, null handling, date parsing)
- Performs EDA across revenue, region, category, product, discount, and time dimensions
- Produces 6 publication-ready charts saved to the `outputs/` folder
- Derives actionable business insights (Q4 concentration risk, underperforming regions)

---

## 📁 Project Structure

```
sales-analytics/
├── data/
│   └── raw_sales.csv          ← generated dataset
├── outputs/
│   ├── cleaned_sales.csv
│   ├── 01_monthly_revenue_trend.png
│   ├── 02_revenue_by_category.png
│   ├── 03_region_performance.png
│   ├── 04_quarterly_revenue.png
│   ├── 05_discount_impact.png
│   └── 06_top10_products.png
├── generate_data.py           ← run first
├── analysis.py                ← main analysis
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Generate the dataset
```bash
python generate_data.py
```

### Step 3 — Run the full analysis
```bash
python analysis.py
```

### Step 4 — View results
Open the `outputs/` folder — all charts are saved as PNG files.

---

## 📈 Key Insights

| Insight | Finding |
|---|---|
| Q4 Revenue Share | ~26% of annual revenue concentrated in Q4 |
| Weakest Region | Identified region for targeted intervention |
| Top Category | Electronics drives highest revenue |
| Discount Impact | Orders with 20% discount show lowest avg revenue |

---

## 🛠 Requirements

```
pandas
numpy
matplotlib
seaborn
faker
openpyxl
```
