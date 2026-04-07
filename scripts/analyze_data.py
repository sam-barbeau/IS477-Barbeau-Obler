import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats
from pathlib import Path

# Set up style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

data_dir = Path("data")
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Load integrated data
df = pd.read_csv(data_dir / "integrated_data.csv", parse_dates=["date"])
print(f"Loaded {len(df)} rows of integrated data")

# ------------------------------------------
# FIGURE 1: Time Series Overview (Dual Axis)
# ------------------------------------------
print("\nCreating Figure 1: Time Series Overview...")

fig, ax1 = plt.subplots(figsize=(12, 6))

# Federal Funds Rate on left axis
color1 = '#2E86AB'
ax1.set_xlabel('Date', fontsize=11)
ax1.set_ylabel('Federal Funds Rate (%)', color=color1, fontsize=11)
line1 = ax1.plot(df['date'], df['fedfunds'], color=color1, linewidth=2, label='Fed Funds Rate')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_ylim(0, 6)

# Building Permits on right axis
ax2 = ax1.twinx()
color2 = '#E94F37'
ax2.set_ylabel('Building Permits (thousands)', color=color2, fontsize=11)
line2 = ax2.plot(df['date'], df['permit'], color=color2, linewidth=2, label='Building Permits')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(1000, 2000)

# Add period shading
ax1.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2021-12-31'), 
            alpha=0.15, color='gray', label='Pandemic Period')
ax1.axvspan(pd.Timestamp('2022-03-01'), pd.Timestamp('2023-07-31'), 
            alpha=0.15, color='orange', label='Rate Hike Period')

# Format x-axis
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.title('Federal Funds Rate vs Building Permits (2019-2024)', fontsize=14, fontweight='bold')
fig.legend(loc='upper right', bbox_to_anchor=(0.88, 0.88))
plt.tight_layout()
plt.savefig(output_dir / 'fig1_timeseries.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved fig1_timeseries.png")

# ---------------------------------------
# FIGURE 2: Scatter Plot with Correlation
# ---------------------------------------
print("\nCreating Figure 2: Scatter Plot...")

fig, ax = plt.subplots(figsize=(10, 7))

# Color by period
period_colors = {
    'Pre-COVID': '#2E86AB',
    'Pandemic': '#A23B72', 
    'Rate Hikes': '#F18F01',
    '2024': '#C73E1D'
}

for period in ['Pre-COVID', 'Pandemic', 'Rate Hikes', '2024']:
    subset = df[df['period'] == period]
    ax.scatter(subset['fedfunds'], subset['permit'], 
               c=period_colors[period], s=60, alpha=0.7, label=period, edgecolors='white')

# Add regression line for full dataset
slope, intercept, r_value, p_value, std_err = stats.linregress(df['fedfunds'], df['permit'])
x_line = np.linspace(df['fedfunds'].min(), df['fedfunds'].max(), 100)
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, 'k--', linewidth=2, alpha=0.7, 
        label=f'Trend (r={r_value:.3f}, p={p_value:.4f})')

ax.set_xlabel('Federal Funds Rate (%)', fontsize=12)
ax.set_ylabel('Building Permits (thousands)', fontsize=12)
ax.set_title('Relationship Between Fed Funds Rate and Building Permits', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig(output_dir / 'fig2_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved fig2_scatter.png")

# ---------------------------------------------------
# FIGURE 3: Cross-Correlation Analysis (Lag Analysis)
# ---------------------------------------------------

print("\nCreating Figure 3: Cross-Correlation...")

# Calculate cross-correlation at different lags
max_lag = 12  # Up to 12 months
lags = range(-max_lag, max_lag + 1)
correlations = []

for lag in lags:
    if lag < 0:
        # Negative lag: rate leads permits
        corr = df['fedfunds'].iloc[:lag].corr(df['permit'].iloc[-lag:])
    elif lag > 0:
        # Positive lag: permits lead rate
        corr = df['fedfunds'].iloc[lag:].corr(df['permit'].iloc[:-lag])
    else:
        corr = df['fedfunds'].corr(df['permit'])
    correlations.append(corr)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(lags, correlations, color='steelblue', edgecolor='white')

# Highlight the most negative correlation (strongest inverse relationship)
min_idx = correlations.index(min(correlations))
bars[min_idx].set_color('#E94F37')

ax.axhline(y=0, color='black', linewidth=0.5)
ax.set_xlabel('Lag (months)\n← Rate leads permits | Permits lead rate →', fontsize=11)
ax.set_ylabel('Correlation Coefficient', fontsize=11)
ax.set_title('Cross-Correlation: Fed Funds Rate vs Building Permits', fontsize=14, fontweight='bold')
ax.set_xticks(range(-12, 13, 2))

# Add annotation for strongest correlation
best_lag = lags[min_idx]
best_corr = correlations[min_idx]
ax.annotate(f'Strongest: lag={best_lag}, r={best_corr:.3f}',
            xy=(best_lag, best_corr), xytext=(best_lag+3, best_corr-0.1),
            arrowprops=dict(arrowstyle='->', color='black'),
            fontsize=10)

plt.tight_layout()
plt.savefig(output_dir / 'fig3_crosscorr.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved fig3_crosscorr.png")

# -------------------------------------
# FIGURE 4: Period Comparison Box Plots
# -------------------------------------
print("\nCreating Figure 4: Period Comparison...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

period_order = ['Pre-COVID', 'Pandemic', 'Rate Hikes', '2024']
colors = [period_colors[p] for p in period_order]

# Box plot for Federal Funds Rate
box1 = axes[0].boxplot([df[df['period']==p]['fedfunds'] for p in period_order],
                        labels=period_order, patch_artist=True)
for patch, color in zip(box1['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[0].set_ylabel('Federal Funds Rate (%)', fontsize=11)
axes[0].set_title('Fed Funds Rate by Period', fontsize=12, fontweight='bold')

# Box plot for Building Permits
box2 = axes[1].boxplot([df[df['period']==p]['permit'] for p in period_order],
                        labels=period_order, patch_artist=True)
for patch, color in zip(box2['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[1].set_ylabel('Building Permits (thousands)', fontsize=11)
axes[1].set_title('Building Permits by Period', fontsize=12, fontweight='bold')

plt.suptitle('Distribution by Economic Period', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(output_dir / 'fig4_periods.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved fig4_periods.png")

# =============================================================================
# STATISTICAL ANALYSIS
# =============================================================================
print("\n" + "="*60)
print("STATISTICAL ANALYSIS RESULTS")
print("="*60)

# Overall correlation
r, p = stats.pearsonr(df['fedfunds'], df['permit'])
print("\n1. OVERALL CORRELATION (Pearson)")
print(f"   r = {r:.4f}")
print(f"   p-value = {p:.6f}")
print(f"   Interpretation: {'Significant' if p < 0.05 else 'Not significant'} at alpha=0.05")

# Spearman (doesn't assume linearity)
rho, p_spearman = stats.spearmanr(df['fedfunds'], df['permit'])
print("\n2. SPEARMAN RANK CORRELATION")
print(f"   rho = {rho:.4f}")
print(f"   p-value = {p_spearman:.6f}")

# Correlation by period
print("\n3. CORRELATION BY PERIOD")
for period in period_order:
    subset = df[df['period'] == period]
    if len(subset) > 3:
        r_p, p_p = stats.pearsonr(subset['fedfunds'], subset['permit'])
        print(f"   {period}: r = {r_p:.3f} (n={len(subset)})")

# Summary statistics by period
print("\n4. SUMMARY BY PERIOD")
summary = df.groupby('period').agg({
    'fedfunds': ['mean', 'std'],
    'permit': ['mean', 'std']
}).round(2)
print(summary)

# Best lag analysis
print("\n5. LAG ANALYSIS")
print(f"   Best lag (strongest inverse correlation): {best_lag} months")
print(f"   Correlation at best lag: r = {best_corr:.4f}")
print("   Interpretation: Building permits respond most strongly to rate changes")
print(f"   with approximately a {abs(best_lag)}-month delay.")

# Save analysis summary to file
with open(output_dir / "analysis_summary.txt", "w") as f:
    f.write("Statistical Analysis Summary\n")
    f.write("="*50 + "\n\n")
    f.write(f"Overall Pearson correlation: r = {r:.4f}, p = {p:.6f}\n")
    f.write(f"Spearman correlation: rho = {rho:.4f}, p = {p_spearman:.6f}\n")
    f.write(f"Best lag: {best_lag} months (r = {best_corr:.4f})\n\n")
    f.write("Period Summary:\n")
    f.write(summary.to_string())

print("\n\nAnalysis complete! All figures saved to output/")
