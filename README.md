# 📊 Sales Performance Dashboard

A fully self-contained **Python data analysis project** that generates synthetic retail sales data and renders a multi-panel interactive dashboard using `pandas`, `matplotlib`, and `seaborn`.

## 📸 Preview

![Sales Dashboard](plots/sales_dashboard.png)

## 🗂️ Project Structure

```
sales-dashboard/
├── data/
│   └── sales_data.csv          # Auto-generated on first run
├── plots/
│   └── sales_dashboard.png     # Output dashboard image
├── src/
│   ├── generate_data.py        # Synthetic data generator
│   └── dashboard.py            # Main dashboard script
├── requirements.txt
└── README.md
```

## 📈 Dashboard Panels

| Panel | Description |
|-------|-------------|
| **KPI Strip** | Total revenue, units sold, avg deal size, avg discount |
| **Monthly Revenue** | Line chart with area fill across all 12 months |
| **Revenue by Region** | Pie chart split across North/South/East/West |
| **Revenue by Category** | Horizontal bar chart per product category |
| **Top Salespersons** | Bar chart of top 6 reps by revenue |

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/sales-dashboard.git
cd sales-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
cd src
python dashboard.py
```

The script will:
1. Auto-generate `data/sales_data.csv` (500 records, full year 2023)
2. Render all charts and save to `plots/sales_dashboard.png`
3. Display the dashboard in a window

## 🛠️ Tech Stack

- **Python 3.8+**
- `pandas` — data wrangling
- `numpy` — synthetic data generation
- `matplotlib` — layout & charting engine
- `seaborn` — styling & palette

## 📊 Dataset Schema

| Column | Type | Description |
|--------|------|-------------|
| `date` | datetime | Transaction date (2023) |
| `region` | str | North / South / East / West |
| `category` | str | Product category |
| `salesperson` | str | Rep name |
| `units_sold` | int | Number of units |
| `unit_price` | float | Price per unit ($) |
| `discount_pct` | float | Discount applied (0–30%) |
| `revenue` | float | Computed: units × price × (1−discount) |

## 💡 Possible Extensions

- Add a Streamlit web app layer
- Connect to a real CSV/Excel file
- Export to PDF report
- Add time-series forecasting (Prophet / ARIMA)

## 📄 License
MIT
