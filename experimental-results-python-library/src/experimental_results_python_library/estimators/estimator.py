class Estimator(object):
    """Base class used for all estimators (with a signature similar to scikit-learn's estimators)."""

    def __init__(self, cv=None):
        self.cv = cv

    def score(self, X, y=None):
        """Computes the prediction of the estimator

        This score function can be used as a passthrough of X or y.

        Parameters
        ----------
        X : object
            The input.

        y : object, optional (default=None)
            The output.

        Returns
        -------
        result : object
            Returns y if y is not None, otherwise it returns X.
        """
        if y is None:
            return X
        else:
            return y