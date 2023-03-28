from matplotlib import pyplot as plt


def select_by_values(data, column, *values):
    return data.loc[data[column] in values]


def plot_grid_search(
    data,
    title,
    param_left,
    param_bottom,
    param_legend,
    param_left_name,
    param_bottom_name,
    param_legend_name,
):
    data = data.groupby([param_bottom, param_legend], as_index=False).max(param_left)

    legends = data[param_legend].unique()

    _, ax = plt.subplots(1, 1)

    for legend in legends:
        legend_data = data[data[param_legend] == legend]

        ax.plot(legend_data[param_bottom], legend_data[param_left], "-o", label=f"{param_legend_name}: {legend}")

    ax.set_title(title, fontsize=16, fontweight="bold")
    ax.set_xlabel(param_bottom_name, fontsize=12)
    ax.set_xticklabels(
        [item.get_text() for item in ax.get_xticklabels()], rotation=45, ha="right"
    )
    ax.set_ylabel(param_left_name, fontsize=12)
    ax.legend(loc="best", fontsize=7)
    ax.grid("on")
