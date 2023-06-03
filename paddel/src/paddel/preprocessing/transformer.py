import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from tsfresh.feature_selection.relevance import calculate_relevance_table


class FeatureSelector(TransformerMixin, BaseEstimator):
    def __init__(self, n_features=None):
        self.n_features = n_features
        self.relevant_features = None

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """Fits selector to given data

        Args:
            X (pd.Dataframe): Dataset to fit to.
            y (pd.Series): Target variable to fit to.

        Returns:
            BaseEstimator: self.
        """
        if not self.n_features:
            return self

        relevance_table = calculate_relevance_table(X, y)
        relevance_table.sort_values("p_value", inplace=True)

        self.relevant_features = relevance_table["feature"][: self.n_features]

        return self

    def transform(self, X, y=None):
        """Selects the better attributes found in fitting phase.

        Args:
            X (pd.Dataframe): Dataset to transform.
            y (pd.Dataframe, optional): Target column. Defaults to None.

        Returns:
            pd.Dataframe: Dataset with only most relevant features.
        """
        if self.n_features:
            return X[self.relevant_features]
        return X
