from sklearn.base import BaseEstimator, TransformerMixin
from tsfresh.feature_selection.relevance import calculate_relevance_table


class FeatureSelector(TransformerMixin, BaseEstimator):
    def __init__(self, n_features=None):
        self.n_features = n_features
        self.relevant_features = None

    def fit(self, X, y):
        if not self.n_features:
            return self

        relevance_table = calculate_relevance_table(X, y)
        relevance_table.sort_values("p_value", inplace=True)

        self.relevant_features = relevance_table["feature"][: self.n_features]

        return self

    def transform(self, X, y=None):
        if self.n_features:
            return X[self.relevant_features]
        return X
