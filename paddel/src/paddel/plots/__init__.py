import numpy as np
from matplotlib import pyplot as plt


def select_by_values(data, column, *values):
    return data.loc[data[column] in values]


def plot_grid_search(data, title, param_left, param_bottom, param_legend, param_left_name, param_bottom_name,
                     param_legend_name):
    data = data.groupby([param_bottom, param_legend], as_index=False).max('mean_test_accuracy')
    grid_param_bottom = data[param_bottom].unique()
    grid_param_legend = data[param_legend].unique()

    # Get Test Scores Mean and std for each grid search
    scores_mean = data[param_left]
    scores_mean = np.array(scores_mean).reshape(len(grid_param_legend), len(grid_param_bottom))

    # Plot Grid search scores
    _, ax = plt.subplots(1, 1)

    # Param1 is the X-axis, Param 2 is represented as a different curve (color line)
    for idx, val in enumerate(grid_param_legend):
        ax.plot(grid_param_bottom, scores_mean[idx, :], '-o', label=param_legend_name + ': ' + str(val))

    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel(param_bottom_name, fontsize=12)
    ax.set_xticklabels([item.get_text() for item in ax.get_xticklabels()], rotation=45, ha="right")
    ax.set_ylabel(param_left_name, fontsize=12)
    ax.legend(loc="best", fontsize=8)
    ax.grid('on')
