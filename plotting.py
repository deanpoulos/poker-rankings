import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def plot_normal_distribution(mu, sigma, label):
    """
    Plots a normal distribution with mean `mu` and standard deviation `sigma`.
    Also draws a vertical line at `mu - 3*sigma`.

    Parameters:
        mu (float): Mean of the normal distribution.
        sigma (float): Standard deviation of the normal distribution.
    """
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)  # Range for the plot
    y = stats.norm.pdf(x, mu, sigma)  # Probability density function (PDF)

    plt.plot(x, y, label=label)
    plt.axvline(mu - 3 * sigma, color='red', linestyle='--', label=r'$\mu - 3\sigma$')
