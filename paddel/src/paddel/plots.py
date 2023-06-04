from matplotlib import pyplot as plt
import pandas as pd


def select_by_values(data, column, *values):
    return data.loc[data[column] in values]


def plot_grid_search(
        data: pd.DataFrame,
        title: str,
        param_left: str,
        param_bottom: str,
        param_left_name: str,
        param_bottom_name: str,
        param_legend: str = None,
        param_legend_name: str = None,
):
    """Generates and shows the results of a grid search done with sklean.

    Args:
        data (pd.Dataframe): Sklearn grid search result dataframe.
        title (str): Plot title.
        param_left (str): Parameter from data for the left axis.
        param_bottom (str): Parameter from data for the bottom axis.
        param_legend (str): Parameter from data for the legend.
        param_left_name (str): Tag for the left axis.
        param_bottom_name (str): Tag for the bottom axis.
        param_legend_name (str): Tag for the legend.
    """
    _, ax = plt.subplots(1, 1)

    if param_legend and param_legend_name:
        data = data.groupby([param_bottom, param_legend], as_index=False).agg({param_left: 'max'})
        legends = data[param_legend].unique()

        for legend in legends:
            legend_data = data[data[param_legend] == legend]

            ax.plot(
                legend_data[param_bottom],
                legend_data[param_left],
                "-o",
                label=f"{param_legend_name}: {legend}",
            )

        ax.legend(loc="best", fontsize=7)

    else:
        data = data.groupby([param_bottom], as_index=False).agg({param_left: 'max'})
        ax.plot(
            data[param_bottom],
            data[param_left],
            "-o",
        )

    ax.set_title(title, fontsize=16, fontweight="bold")
    ax.set_xlabel(param_bottom_name, fontsize=12)
    ax.set_xticklabels(
        [item.get_text() for item in ax.get_xticklabels()], rotation=45, ha="right"
    )
    ax.set_ylabel(param_left_name, fontsize=12)
    ax.grid("on")
