import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the logarithmic model function
# Note: np.log() is the natural logarithm (ln)
def log_func(x, a, b):
  """
  Logarithmic function: y = a * ln(x) + b
  """
  # Ensure x is positive to avoid math domain errors
  return a * np.log(x) + b

# Generate some sample data to demonstrate
# Let's create data that roughly follows y = 2.5 * ln(x) + 0.8
x_data = np.linspace(1, 15, 50)
noise = 0.3 * np.random.normal(size=x_data.size)
y_data = log_func(x_data, 2.5, 0.8) + noise

# Fit the model to the data
# popt: optimal parameters [a, b]
# pcov: estimated covariance of popt
popt, pcov = curve_fit(log_func, x_data, y_data)

# Extract the optimal parameters
a_opt, b_opt = popt
print(f"Optimal parameters: a = {a_opt:.3f}, b = {b_opt:.3f}")

# Create a set of x-values for a smooth curve
x_fit = np.linspace(min(x_data), max(x_data), 100)

# Calculate the standard deviation of the parameters
perr = np.sqrt(np.diag(pcov))

# To get the uncertainty of the fitted curve, we must propagate the error.
# The variance of the function y = a*ln(x) + b is given by:
# Var(y) = (∂y/∂a)²σₐ² + (∂y/∂b)²σᵦ² + 2(∂y/∂a)(∂y/∂b)σₐᵦ
# This can be computed elegantly using the Jacobian and covariance matrix.
# Jacobian matrix J = [[∂y/∂a], [∂y/∂b]] = [[ln(x)], [1]]
J = np.array([np.log(x_fit), np.ones(len(x_fit))]).T

# The variance of the fit at each x_fit point
# Var(y_fit) = J @ pcov @ J.T
var_y_fit = np.sum(J @ pcov * J, axis=1)
std_dev_y_fit = np.sqrt(var_y_fit)

# Confidence interval factor (1.96 for 95% confidence)
# For a more rigorous approach with small sample sizes, use the t-distribution
# from scipy.stats import t
# t_val = t.ppf(1 - 0.05 / 2, len(x_data) - len(popt))
conf_factor = 1.96

# Calculate the upper and lower confidence bounds
y_fit = log_func(x_fit, a_opt, b_opt)
y_upper = y_fit + conf_factor * std_dev_y_fit
y_lower = y_fit - conf_factor * std_dev_y_fit

plt.figure(figsize=(10, 7))

# Plot the original data
plt.scatter(x_data, y_data, label='Data', color='dodgerblue', s=30)

# Plot the fitted curve
plt.plot(x_fit, y_fit, 'r-', label=f'Fit: y = {a_opt:.2f}ln(x) + {b_opt:.2f}')

# Plot the 95% confidence interval
plt.fill_between(x_fit, y_lower, y_upper, color='red', alpha=0.2, label='95% Confidence Interval')

# Final plot styling
plt.xlabel('X Value', fontsize=12)
plt.ylabel('Y Value', fontsize=12)
plt.title('Logarithmic Regression with Confidence Bounds', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
#plt.show()
plt.savefig("out.png")