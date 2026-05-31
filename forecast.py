import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

# 1. GENERATING DATA
np.random.seed(42)
date_range = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")
trend = np.linspace(100, 250, len(date_range))
weekly_seasonality = 30 * np.sin(2 * np.pi * date_range.dayofweek / 7)
noise = np.random.normal(0, 15, len(date_range))
df = pd.DataFrame({"sales": trend + weekly_seasonality + noise}, index=date_range)

# 2. TIME-BASED FEATURE ENGINEERING
df['Time'] = np.arange(len(df.index))
df['DayOfWeek'] = df.index.dayofweek
df = pd.get_dummies(df, columns=['DayOfWeek'], drop_first=True)

X = df.drop(columns=['sales'])
y = df['sales']

# 3. CHRONOLOGICAL SPLIT
split_point = len(df) - 30
X_train, X_test = X.iloc[:split_point], X.iloc[split_point:]
y_train, y_test = y.iloc[:split_point], y.iloc[split_point:]

# 4. MODEL TRAINING
model = LinearRegression()
model.fit(X_train, y_train)
y_fit = pd.Series(model.predict(X_train), index=y_train.index)
y_pred = pd.Series(model.predict(X_test), index=y_test.index)

# 5. METRICS
print("--- Model Performance ---")
print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")
print(f"RMSE: {root_mean_squared_error(y_test, y_pred):.2f}\n")

# 6. SAVE VISUALIZATION
plt.figure(figsize=(12, 6))
plt.plot(y_train.index[-90:], y_train.values[-90:], label="Historical Actual Sales", color="#2b5c8f", alpha=0.6)
plt.plot(y_fit.index[-90:], y_fit.values[-90:], label="Model Fit", color="#2b5c8f", linestyle="--")
plt.plot(y_test.index, y_test.values, label="Observed Future Sales", color="#e056fd")
plt.plot(y_pred.index, y_pred.values, label="Model Forecasted Demand", color="#22a6b3", linewidth=2.5)
plt.title("30-Day Sales Demand Forecast", fontsize=14, fontweight='bold')
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("forecast_evaluation.png", dpi=300)
print("Saved forecast_evaluation.png successfully!")
