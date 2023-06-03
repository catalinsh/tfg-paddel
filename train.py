import io
import os
import pickle
import sys
from pathlib import Path

import click
import pandas as pd

from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import QuantileTransformer

from paddel.preprocessing import get_data
from paddel.preprocessing.transformer import FeatureSelector


class ChoiceOption(click.Option):
    def __init__(self, param_decls=None, **attrs):
        click.Option.__init__(self, param_decls, **attrs)
        if not isinstance(self.type, click.Choice):
            raise Exception('ChoiceOption type arg must be click.Choice')

        if self.prompt:
            prompt_text = '{}:\n{}\n'.format(
                self.prompt,
                '\n'.join(f'{idx: >4}: {c}' for idx, c in enumerate(self.type.choices, start=1))
            )
            self.prompt = prompt_text

    def process_prompt_value(self, ctx, value, prompt_type):
        if value is not None:
            index = prompt_type(value, self, ctx)
            return self.type.choices[index - 1]

    def prompt_for_value(self, ctx):
        # Calculate the default before prompting anything to be stable.
        default = self.get_default(ctx)

        prompt_type = click.IntRange(min=1, max=len(self.type.choices))
        return click.prompt(
            self.prompt, default=default, type=prompt_type,
            hide_input=self.hide_input, show_choices=False,
            confirmation_prompt=self.confirmation_prompt,
            value_proc=lambda x: self.process_prompt_value(ctx, x, prompt_type))


@click.command()
@click.option(
    '--c',
    prompt='Regularization parameter',
    default=1.0,
    type=click.FloatRange(min=0, min_open=True)
)
@click.option(
    '--kernel',
    prompt='SVM kernel to use',
    default=3,
    type=click.Choice(['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']),
    cls=ChoiceOption
)
@click.option(
    '--degree',
    prompt='Degree of the function (only for poly kernel)',
    default=2,
    type=click.INT
)
@click.option(
    '--coef0',
    prompt='Independent term for kernel function (only for poly and sigmoid kernel)',
    default=0.0,
    type=click.INT
)
@click.option(
    '--tol',
    prompt='Stopping criterion tolerance',
    default=1e-3,
    type=click.FloatRange(min=0, min_open=True)
)
def svc_function(c, kernel, degree, coef0, tol):
    return SVC(
        C=c,
        kernel=kernel,
        degree=degree,
        coef0=coef0,
        probability=True,
        tol=tol,
    )


def nb_function():
    return GaussianNB()


@click.command()
@click.option(
    '--n_neighbors',
    prompt='Number of neighbors',
    default=1,
    type=click.IntRange(min=1)
)
@click.option(
    '--metric',
    prompt='Distance metric',
    default=1,
    type=click.Choice(["euclidean", "manhattan", "haversine", "cosine", "nan_euclidean"]),
    cls=ChoiceOption
)
def knn_function(n_neighbors):
    return KNeighborsClassifier(
        n_neighbors=n_neighbors,

    )


algorithmFunctions = {
    "Support Vector Machine": svc_function,
    "Naive Bayes": nb_function,
    "K Nearest Neighbors": knn_function,
    "Random Forest": RandomForestClassifier,
    "Decision Tree": DecisionTreeClassifier,
    "Multilayer Perceptron": MLPClassifier,
    "AdaBoost": AdaBoostClassifier,
    "XGB": XGBClassifier,
}


@click.command()
@click.option(
    '--video_dir',
    prompt='Directory where videos are located',
    default='./data/raw',
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option(
    '--cache_dir',
    prompt='Directory where feature extraction cache is located',
    default='./data/cache',
    type=click.Path(exists=False, file_okay=False, dir_okay=True)
)
@click.option(
    '--output_file',
    prompt='Directory where feature extraction cache is located',
    default='./model.pkl',
    type=click.Path(exists=False, file_okay=True, dir_okay=False)
)
@click.option(
    '--algorithm',
    prompt='Algorithm to use',
    type=click.Choice(list(algorithmFunctions.keys())),
    cls=ChoiceOption
)
@click.option(
    '--feature_amount',
    default=320,
    prompt='Feature amount to select',
    type=click.IntRange(min=5),
)
def main(video_dir, cache_dir, output_file, algorithm, feature_amount):
    clf = algorithmFunctions[algorithm]()

    save_stderr = sys.stderr
    sys.stderr = io.BytesIO()

    misc_df, classic_df, fresh_df, y = get_data(Path(video_dir), Path(cache_dir))
    data = pd.concat([misc_df, classic_df, fresh_df], axis=1)

    pipe = Pipeline([
        ("scaler", QuantileTransformer(n_quantiles=50).set_output(transform="pandas")),
        ("select", FeatureSelector(n_features=feature_amount)),
        ("model", clf),
    ])

    sys.stderr = save_stderr

    pipe.fit(data, y)

    with open(Path(output_file), "wb") as f:
        pickle.dump(pipe, f)

    click.echo(f"Trained model saved at {output_file}. You can go to https://paddel.catalin.sh/ and upload it.")


if __name__ == '__main__':
    main()
