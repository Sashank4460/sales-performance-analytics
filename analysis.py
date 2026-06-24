"""
Sales Performance Analytics Dashboard
--------------------------------------
Run:  python generate_data.py   (first time only)
      python analysis.py
Outputs: outputs/ folder with charts + cleaned CSV
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os, warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid", palette="Blues_d")
os.makedirs("outputs", exist_ok=True)

# ── 1. LOAD & CLEAN ──────────────────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv("data/raw_sales.csv")
print(f"  Raw rows      : {len(df)}")

# Remove duplicates
df.drop_duplicates(subset=["order_id"], inplace=True)
print(f"  After dedup   : {len(df)}")

# Fill missing discount with 0
df["discount_pct"].fillna(0, inplace=True)

# Parse dates
df["date"]  = pd.to_datetime(df["date"])
df["year"]  = df["date"].dt.year
df["month"] = df["date"].dt.month
df["month_name"] = df["date"].dt.strftime("%b")
df["quarter"]    = df["date"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})

df.to_csv("outputs/cleaned_sales.csv", index=False)
print(f"  Cleaned rows  : {len(df)}  →  outputs/cleaned_sales.csv")

# ── 2. MONTHLY REVENUE TREND ─────────────────────────────────────────────────
monthly = (df.groupby(["year","month"])["revenue"]
             .sum().reset_index()
             .sort_values(["year","month"]))
monthly["label"] = monthly["year"].astype(str) + "-" + monthly["month"].apply(lambda x: f"{x:02d}")

fig, ax = plt.subplots(figsize=(14, 5))
for yr, grp in monthly.groupby("year"):
    ax.plot(grp["label"], grp["revenue"]/1e6, marker="o", linewidth=2.2, label=str(yr))
ax.set_title("Monthly Revenue Trend (2023–2024)", fontsize=14, fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("Revenue (₹ Millions)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"₹{x:.1f}M"))
plt.xticks(rotation=45, ha="right"); ax.legend(); plt.tight_layout()
plt.savefig("outputs/01_monthly_revenue_trend.png", dpi=150); plt.close()
print("  Chart 1 saved")

# ── 3. REVENUE BY CATEGORY ───────────────────────────────────────────────────
cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(cat_rev.index, cat_rev.values/1e6, color=sns.color_palette("Blues_d", len(cat_rev)))
ax.bar_label(bars, fmt=lambda x: f"₹{x:.1f}M", padding=4, fontsize=9)
ax.set_title("Total Revenue by Product Category", fontsize=14, fontweight="bold")
ax.set_ylabel("Revenue (₹ Millions)"); plt.tight_layout()
plt.savefig("outputs/02_revenue_by_category.png", dpi=150); plt.close()
print("  Chart 2 saved")

# ── 4. REGION PERFORMANCE ────────────────────────────────────────────────────
reg = df.groupby("region").agg(
    total_revenue=("revenue","sum"),
    total_orders=("order_id","count"),
    avg_order_value=("revenue","mean")
).reset_index().sort_values("total_revenue", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].barh(reg["region"], reg["total_revenue"]/1e6,
             color=sns.color_palette("Blues_d", len(reg)))
axes[0].set_title("Revenue by Region", fontweight="bold")
axes[0].set_xlabel("Revenue (₹ Millions)")
axes[1].barh(reg["region"], reg["avg_order_value"],
             color=sns.color_palette("Greens_d", len(reg)))
axes[1].set_title("Avg Order Value by Region", fontweight="bold")
axes[1].set_xlabel("Avg Order Value (₹)")
plt.tight_layout()
plt.savefig("outputs/03_region_performance.png", dpi=150); plt.close()
print("  Chart 3 saved")

# ── 5. QUARTERLY REVENUE SHARE ───────────────────────────────────────────────
q_rev = df.groupby(["year","quarter"])["revenue"].sum().unstack().fillna(0)
q_rev.T.plot(kind="bar", figsize=(9,5), colormap="Blues")
plt.title("Quarterly Revenue Comparison (2023 vs 2024)", fontsize=13, fontweight="bold")
plt.xlabel("Quarter"); plt.ylabel("Revenue (₹)")
plt.xticks(rotation=0); plt.legend(title="Year"); plt.tight_layout()
plt.savefig("outputs/04_quarterly_revenue.png", dpi=150); plt.close()
print("  Chart 4 saved")

# ── 6. DISCOUNT VS REVENUE IMPACT ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
disc_rev = df.groupby("discount_pct")["revenue"].mean()
ax.bar(disc_rev.index.astype(str), disc_rev.values,
       color=sns.color_palette("Reds_d", len(disc_rev)))
ax.set_title("Avg Revenue per Order by Discount Level", fontsize=13, fontweight="bold")
ax.set_xlabel("Discount %"); ax.set_ylabel("Avg Revenue (₹)")
plt.tight_layout()
plt.savefig("outputs/05_discount_impact.png", dpi=150); plt.close()
print("  Chart 5 saved")

# ── 7. TOP 10 PRODUCTS ───────────────────────────────────────────────────────
top10 = df.groupby("product")["revenue"].sum().nlargest(10).sort_values()
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top10.index, top10.values/1e6,
        color=sns.color_palette("viridis", 10))
ax.set_title("Top 10 Products by Revenue", fontsize=13, fontweight="bold")
ax.set_xlabel("Revenue (₹ Millions)"); plt.tight_layout()
plt.savefig("outputs/06_top10_products.png", dpi=150); plt.close()
print("  Chart 6 saved")

# ── 8. SUMMARY STATS ─────────────────────────────────────────────────────────
print("\n========  SUMMARY  ========")
print(f"  Total Revenue  : ₹{df['revenue'].sum()/1e7:.2f} Cr")
print(f"  Total Orders   : {len(df):,}")
print(f"  Avg Order Value: ₹{df['revenue'].mean():,.0f}")
best_region  = reg.iloc[0]['region']
worst_region = reg.iloc[-1]['region']
q4_share = (df[df['quarter']=='Q4']['revenue'].sum() / df['revenue'].sum()) * 100
print(f"  Best Region    : {best_region}")
print(f"  Weakest Region : {worst_region}  ← actionable insight")
print(f"  Q4 Revenue Share: {q4_share:.1f}%  ← high concentration risk")
print("===========================")
print("\nAll outputs saved to  outputs/")
