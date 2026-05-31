import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

# ==========================================
# 1. DATA LOADING & SIMULATION
# ==========================================
# For demonstration, we generate a synthetic dataset mirroring typical retail attributes.
# Replace this section with your Kaggle 'train.csv' loading logic:
# df = pd.read_csv('train.csv', parse_dates=['date'], index_col='date')

np.random.seed(42)
date_range = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")
trend = np.linspace(100, 250, len(date_range))
weekly_seasonality = 30 * np.sin(2 * np.pi * date_range.dayofweek / 7)
noise = np.random.normal(0, 15, len(date_range))

sales = trend + weekly_seasonality + noise
df = pd.DataFrame({"sales": sales}, index=date_range)
df.index.name = "date"

# ==========================================
# 2. FEATURE ENGINEERING
# ==========================================
def create_time_features(data):
    df_features = data.copy()
    
    # Time dummy for modeling the long-term trend
    df_features['Time'] = np.arange(len(df_features.index))
    
    # Categorical calendar features for seasonality
    df_features['DayOfWeek'] = df_features.index.dayofweek
    df_features['Month'] = df_features.index.month
    
    # One-hot encoding the day of the week to capture weekly patterns
    df_features = pd.get_dummies(df_features, columns=['DayOfWeek'], drop_first=True)
    return df_features

df_ready = create_time_features(df)

# Separate features (X) and target variable (y)
X = df_ready.drop(columns=['sales'])
y = df_ready['sales']

# ==========================================
# 3. TRAIN-TEST SPLIT (Chronological)
# ==========================================
# We reserve the final 30 days of the historical dataset to evaluate model performance
split_point = len(df_ready) - 30
X_train, X_test = X.iloc[:split_point], X.iloc[split_point:]
y_train, y_test = y.iloc[:split_point], y.iloc[split_point:]

# ==========================================
# 4. MODEL TRAINING & PREDICTION
# ==========================================
model = LinearRegression()
model.fit(X_train, y_train)

# Generate predictions for both the training and testing sets
y_fit = pd.Series(model.predict(X_train), index=y_train.index)
y_pred = pd.Series(model.predict(X_test), index=y_test.index)

# ==========================================
# 5. MODEL EVALUATION
# ==========================================
mae = mean_absolute_error(y_test, y_pred)
rmse = root_mean_squared_error(y_test, y_pred)

print("--- Model Performance Metrics ---")
print(f"Mean Absolute Error (MAE): {mae:.2f} units")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f} units\n")

# ==========================================
# 6. BUSINESS-FRIENDLY VISUALIZATION
# ==========================================
plt.figure(figsize=(12, 6))

# Plot historical actuals vs fitted baseline
plt.plot(y_train.index[-90:], y_train.values[-90:], label="Historical Actual Sales", color="#2b5c8f", alpha=0.6)
plt.plot(y_fit.index[-90:], y_fit.values[-90:], label="Model Fit (Historical)", color="#2b5c8f", linestyle="--")

# Plot validation actuals vs our future predictions
plt.plot(y_test.index, y_test.values, label="Observed Future Sales", color="#e056fd", fontweight='bold')
plt.plot(y_pred.index, y_pred.values, label="Model Forecasted Demand", color="#22a6b3", linewidth=2.5)

plt.title("30-Day Sales Demand Forecast for Stakeholders", fontsize=14, fontweight='bold', pad=15)
plt.xlabel("Timeline", fontsize=11)
plt.ylabel("Units Sold / Sales Volume", fontsize=11)
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none")
plt.tight_layout()

# Save the plot directly so you can embed it into your GitHub README
plt.savefig("forecast_evaluation.png", dpi=300)
plt.show()
