class Computation(object):
    """Base class used for all computations."""

    def __init__(self, puid=None):
        self.puid = puid

    def run(self, **kwargs):
        """Runs the computation

        This run function can be used

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