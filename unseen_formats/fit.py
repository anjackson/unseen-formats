import csv
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

def generate_fit(x_data, y_data, min_x=None, max_x=None, steps=100):
  if not min_x:
    min_x = min(x_data)
  if not max_x:
    max_x = max(x_data)

  # Fit the model to the data
  # popt: optimal parameters [a, b]
  # pcov: estimated covariance of popt
  popt, pcov = curve_fit(log_func, x_data, y_data)

  # Extract the optimal parameters
  a_opt, b_opt = popt
  #print(f"Optimal parameters: a = {a_opt:.3f}, b = {b_opt:.3f}")

  # Create a set of x-values for a smooth curve
  x_fit = np.linspace(min_x, max_x, steps)

  # Calculate the standard deviation of the parameters
  # perr = np.sqrt(np.diag(pcov))
  # print(perr)

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

  return x_fit, y_fit, a_opt, b_opt, y_lower, y_upper


def generate_fit_plot(x_data, y_data, labels, x_fit, y_fit, a_opt, b_opt, y_lower, y_upper, prefix="out"):

  plt.figure(figsize=(12, 7))

  # Plot the original data
  fig, ax = plt.subplots()
  for i in range(len(x_data)):
    ax.scatter(x_data[i], y_data[i], label=labels[i], s=20)

  # Set the limits
  ax.set_xlim([0, 50000])
  ax.set_ylim([0, 14000])

  # Plot the fitted curve
  plt.plot(x_fit, y_fit, 'r-', label=f'Fit: y = {a_opt:.2f}ln(x) + {b_opt:.2f}')

  # Plot the 95% confidence interval
  plt.fill_between(x_fit, y_lower, y_upper, color='red', alpha=0.2, label='95% Confidence Interval')

  # Final plot styling
  plt.xlabel('Total File Extensions Recorded', fontsize=10)
  plt.ylabel('Total Unique File Extensions', fontsize=10)
  plt.legend(fontsize=9)
  plt.grid(True, linestyle='--', alpha=0.6)
  #plt.show()
  plt.savefig(f"{prefix}.plot.png", dpi=300)
  plt.savefig(f"{prefix}.plot.svg")