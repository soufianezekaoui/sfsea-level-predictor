import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np


# Load Data
# ============================================================================
df = pd.read_csv('data/epa-sea-level.csv')


# Draw Sea Level Plot
# ============================================================================

def draw_plot():
    
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create scatter plot ====================================================
    ax.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], color='blue', 
               alpha=0.6, edgecolors='k', s=50, label='Actual Data')
    
    
    # First line of best fit (ALL data: 1880-2013) ===========================
    res = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    years_all = np.arange(1880, 2051)
    
    predictions_all = res.slope * years_all + res.intercept
    
    ax.plot(years_all, predictions_all, 'r-', linewidth=2, label='1880-2013')
    
    # Second line of best fit (RECENT data: 2000-2013) =======================
    df_recent = df[df['Year'] >= 2000]
    res_recent = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
    
    years_recent = np.arange(2000, 2051)
    
    predictions_recent = res_recent.slope * years_recent + res_recent.intercept

    ax.plot(years_recent, predictions_recent, 'g-', linewidth = 2, label = '2000-2013')
    
    # Add labels and formatting
    ax.set_title('Rise in Sea Level', fontsize = 16, fontweight = 'bold')
    ax.set_xlabel('Year', fontsize = 12)
    ax.set_ylabel('Sea Level (inches)', fontsize = 12)
    ax.legend()
    ax.grid(True, alpha = 0.3)

    # Save
    plt.tight_layout()
    plt.savefig('data/files/sea_level_plot.png', dpi=100)
    return fig


# BONUS 1: Compare 2050 Predictions
# ============================================================================

def bonus_compare_predictions():
    
    # Using all data:
    res_all = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    predict_2050_all = res_all.slope * 2050 + res_all.intercept
    
    # Using recent data:
    df_recent = df[df['Year'] >= 2000]
    res_recent = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
    predict_2050_recent = res_recent.slope * 2051 + res_recent.intercept
    
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = ['All Data (1880-2013)', 'Recent Data (2000-2013)']
    values = [predict_2050_all, predict_2050_recent]
    ax.bar(labels, values, color=['#e74c3c', '#2ecc71'], alpha=0.7)
    
    for i, v in enumerate(values):
        ax.text(i, v, f'{v:.2f}"', ha='center', va='bottom', fontweight='bold')
    
    ax.set_ylabel('Predicted Sea Level (inches)')
    ax.set_title('2050 Predictions Comparison')
    plt.savefig('data/files/prediction_comparison.png', dpi=100)
    
    pass


# BONUS 2: Acceleration Analysis
# ============================================================================

def bonus_analyze_acceleration():
    
    # Period 1: 1880-1999
    df_old = df[df['Year'] < 2000]
    slope_old = linregress(df_old['Year'], df_old['CSIRO Adjusted Sea Level']).slope
    
    # Period 2: 2000-2013
    df_new = df[df['Year'] >= 2000]
    slope_new = linregress(df_new['Year'], df_new['CSIRO Adjusted Sea Level']).slope

    accel_pct = ((slope_new - slope_old) / slope_old) * 100

    print(f"Old rate: {slope_old:.4f} inches/year")
    print(f"New rate: {slope_new:.4f} inches/year")
    print(f"Acceleration: {accel_pct:+.1f}%")
    
    pass

# BONUS 3: Milestone Predictions
# ============================================================================

def predict_milestones():
    
    # Use recent trend (more conservative)
    df_recent = df[df['Year'] >= 2000]
    res = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
    
    current_level = df['CSIRO Adjusted Sea Level'].iloc[-1]
    current_year = df['Year'].iloc[-1]
    
    milestones = [10, 12, 15, 18, 20]  # inches
    
    print("\n" + "="*60)
    print("🎯 MILESTONE PREDICTIONS (based on 2000-2013 trend)")
    print("="*60)
    print(f"\nCurrent sea level ({current_year}): {current_level:.2f} inches")
    print(f"\nWhen will sea level reach:")
    
    for milestone in milestones:
        if milestone > current_level:
            # Note : milestone = slope * year + intercept
            year_predicted = (milestone - res.intercept) / res.slope
            years_from_now = year_predicted - current_year
            
            if year_predicted <= 2100:
                print(f"  {milestone:2d} inches → Year {year_predicted:.0f} "
                      f"({years_from_now:.0f} years from {current_year})")
            else:
                print(f"  {milestone:2d} inches → After 2100")
    
    print("="*60)

# BONUS 4: Statistical Summary
# ============================================================================

def print_statistics():
    
    res_all = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    df_recent = df[df['Year'] >= 2000]
    res_recent = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
    
    print("\n" + "="*60)
    print("📊 STATISTICAL SUMMARY")
    print("="*60)
    
    print("\n🔹 ALL DATA (1880-2013):")
    print(f"   Slope:        {res_all.slope:.6f} inches/year")
    print(f"   Intercept:    {res_all.intercept:.4f}")
    print(f"   R² (fit):     {res_all.rvalue**2:.4f}")
    print(f"   P-value:      {res_all.pvalue:.2e}")
    print(f"   Std Error:    {res_all.stderr:.6f}")
    
    pred_2050_all = res_all.slope * 2050 + res_all.intercept
    print(f"   2050 Prediction: {pred_2050_all:.2f} inches")
    
    print("\n🔹 RECENT DATA (2000-2013):")
    print(f"   Slope:        {res_recent.slope:.6f} inches/year")
    print(f"   Intercept:    {res_recent.intercept:.4f}")
    print(f"   R² (fit):     {res_recent.rvalue**2:.4f}")
    print(f"   P-value:      {res_recent.pvalue:.2e}")
    print(f"   Std Error:    {res_recent.stderr:.6f}")
    
    pred_2050_recent = res_recent.slope * 2050 + res_recent.intercept
    print(f"   2050 Prediction: {pred_2050_recent:.2f} inches")
    
    print(f"\n🔹 DIFFERENCE IN 2050 PREDICTIONS:")
    diff = pred_2050_recent - pred_2050_all
    print(f"   {diff:+.2f} inches ({abs(diff)/pred_2050_all*100:.1f}% difference)")
  


# TEST
# ============================================================================

if __name__ == '__main__':
    
    # Required visualization
    print("\n🎨 Generating required visualization...")
    draw_plot()
    print("   ✓ Main plot saved → data/files/sea_level_plot.png")
    
    # Bonus analyses
    print("\n🎁 Running bonus analyses...")
    bonus_compare_predictions()
    print("   ✓ Prediction comparison → data/files/prediction_comparison.png")
    
    bonus_analyze_acceleration()
    predict_milestones()
    print_statistics()
    
    print("\n" + "="*60)
    print("✅ ALL ANALYSES COMPLETE!")
    print("="*60)
    print("\n📂 Generated files in data/files/:")
    print("   1. sea_level_plot.png         (Required for freeCodeCamp)")
    print("   2. prediction_comparison.png  (Bonus)")
    print("\n💡 Key Findings:")
    
    # Quick summary
    res_all = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    res_recent = linregress(df[df['Year'] >= 2000]['Year'],
                            df[df['Year'] >= 2000]['CSIRO Adjusted Sea Level'])
    
    accel = ((res_recent.slope - res_all.slope) / res_all.slope) * 100
    
    print(f"   • Sea level rose {df['CSIRO Adjusted Sea Level'].iloc[-1] - df['CSIRO Adjusted Sea Level'].iloc[0]:.1f} inches from 1880-2013")
    print(f"   • Rise rate is {accel:+.1f}% faster since 2000")
    print(f"   • 2050 prediction: {res_recent.slope * 2050 + res_recent.intercept:.1f} inches (recent trend)")
    
    print("\n" + "="*60)

