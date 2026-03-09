"""
dashboard.py
Generates a multi-panel Sales Dashboard using matplotlib & seaborn.
Run:  python dashboard.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

# ── Style ───────────────────────────────────────────────────────────────────
sns.set_theme(style='darkgrid', palette='muted')
plt.rcParams.update({
    'figure.facecolor': '#0f1117',
    'axes.facecolor':   '#1a1d27',
    'axes.edgecolor':   '#3a3d4a',
    'axes.labelcolor':  '#c9d1d9',
    'xtick.color':      '#8b949e',
    'ytick.color':      '#8b949e',
    'text.color':       '#c9d1d9',
    'grid.color':       '#2a2d3a',
    'grid.linewidth':   0.6,
    'font.family':      'DejaVu Sans',
})
ACCENT = '#58a6ff'
PALETTE = ['#58a6ff', '#3fb950', '#f78166', '#d2a8ff', '#ffa657']

# ── Load data ────────────────────────────────────────────────────────────────
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_data.csv')
    if not os.path.exists(csv_path):
        from generate_data import generate_sales_data
        generate_sales_data()
    df = pd.read_csv(csv_path, parse_dates=['date'])
    return df

# ── KPI helpers ──────────────────────────────────────────────────────────────
def compute_kpis(df):
    return {
        'Total Revenue':     f"${df['revenue'].sum():,.0f}",
        'Total Units Sold':  f"{df['units_sold'].sum():,}",
        'Avg Deal Size':     f"${df['revenue'].mean():,.2f}",
        'Avg Discount':      f"{df['discount_pct'].mean()*100:.1f}%",
    }

# ── Chart builders ───────────────────────────────────────────────────────────
def plot_kpi_strip(ax, kpis):
    ax.axis('off')
    n = len(kpis)
    for i, (label, value) in enumerate(kpis.items()):
        x = (i + 0.5) / n
        ax.text(x, 0.72, value, ha='center', va='center',
                fontsize=22, fontweight='bold', color=ACCENT,
                transform=ax.transAxes)
        ax.text(x, 0.28, label, ha='center', va='center',
                fontsize=10, color='#8b949e',
                transform=ax.transAxes)


def plot_monthly_revenue(ax, df):
    monthly = df.groupby(df['date'].dt.to_period('M'))['revenue'].sum().reset_index()
    monthly['date'] = monthly['date'].dt.to_timestamp()
    ax.fill_between(monthly['date'], monthly['revenue'], alpha=0.25, color=ACCENT)
    ax.plot(monthly['date'], monthly['revenue'], color=ACCENT, linewidth=2.2, marker='o', markersize=4)
    ax.set_title('Monthly Revenue', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'${v/1e3:.0f}k'))
    ax.tick_params(axis='x', rotation=30)


def plot_revenue_by_category(ax, df):
    cat = df.groupby('category')['revenue'].sum().sort_values(ascending=True)
    bars = ax.barh(cat.index, cat.values, color=PALETTE[:len(cat)], edgecolor='none', height=0.6)
    for bar, val in zip(bars, cat.values):
        ax.text(val + cat.values.max() * 0.01, bar.get_y() + bar.get_height()/2,
                f'${val/1e3:.1f}k', va='center', fontsize=9, color='#c9d1d9')
    ax.set_title('Revenue by Category', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Revenue ($)')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'${v/1e3:.0f}k'))


def plot_region_pie(ax, df):
    reg = df.groupby('region')['revenue'].sum()
    wedges, texts, autotexts = ax.pie(
        reg.values, labels=reg.index, colors=PALETTE,
        autopct='%1.1f%%', startangle=140,
        wedgeprops=dict(edgecolor='#0f1117', linewidth=2),
        textprops=dict(color='#c9d1d9', fontsize=9))
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color('#0f1117')
        at.set_fontweight('bold')
    ax.set_title('Revenue by Region', fontsize=13, fontweight='bold', pad=12)


def plot_top_salespersons(ax, df):
    sp = df.groupby('salesperson')['revenue'].sum().sort_values(ascending=False).head(6)
    bars = ax.bar(sp.index, sp.values, color=PALETTE, edgecolor='none', width=0.55)
    for bar, val in zip(bars, sp.values):
        ax.text(bar.get_x() + bar.get_width()/2, val + sp.values.max()*0.015,
                f'${val/1e3:.1f}k', ha='center', fontsize=9, color='#c9d1d9')
    ax.set_title('Top Salespersons', fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel('Revenue ($)')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'${v/1e3:.0f}k'))
    ax.tick_params(axis='x', rotation=20)


def plot_quarterly_category(ax, df):
    pivot = df.groupby(['quarter', 'category'])['revenue'].sum().unstack(fill_value=0)
    pivot.plot(kind='bar', ax=ax, color=PALETTE[:len(pivot.columns)], edgecolor='none', width=0.7)
    ax.set_title('Quarterly Revenue by Category', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'${v/1e3:.0f}k'))
    ax.tick_params(axis='x', rotation=15)
    ax.legend(fontsize=8, framealpha=0.3, loc='upper left')


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    df = load_data()
    kpis = compute_kpis(df)

    fig = plt.figure(figsize=(20, 14), facecolor='#0f1117')
    fig.suptitle('📊  Sales Performance Dashboard — 2023',
                 fontsize=20, fontweight='bold', color='#e6edf3', y=0.98)

    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.42, wspace=0.32,
                           top=0.93, bottom=0.06, left=0.06, right=0.97)

    ax_kpi  = fig.add_subplot(gs[0, :])
    ax_line = fig.add_subplot(gs[1, :2])
    ax_pie  = fig.add_subplot(gs[1, 2])
    ax_hbar = fig.add_subplot(gs[2, 0])
    ax_bar  = fig.add_subplot(gs[2, 1])
    ax_qtr  = fig.add_subplot(gs[2, 2])   # reuse as quarterly stacked

    # Quarterly stacked uses full bottom row — rearrange
    ax_hbar2 = fig.add_subplot(gs[2, :2])
    ax_qtr2  = fig.add_subplot(gs[2, 2])
    ax_hbar.remove(); ax_bar.remove()

    plot_kpi_strip(ax_kpi, kpis)
    plot_monthly_revenue(ax_line, df)
    plot_region_pie(ax_pie, df)
    plot_revenue_by_category(ax_hbar2, df)
    plot_top_salespersons(ax_qtr2, df)

    os.makedirs('../plots', exist_ok=True)
    out = os.path.join(os.path.dirname(__file__), '..', 'plots', 'sales_dashboard.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='#0f1117')
    print(f"✅ Dashboard saved → {os.path.abspath(out)}")
    plt.show()


if __name__ == '__main__':
    main()
