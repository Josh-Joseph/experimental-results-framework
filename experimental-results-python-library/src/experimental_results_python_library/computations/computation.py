class Computation(object):
    """Base class used for all computations."""

    def __init__(self, upid=None):
        self.upid = upid

    def run(self, **kwargs):
        """Runs the computation

        This method is mainly used for testing and directly returns the value of 'results', if given.

        Parameters
        ----------
        **kwargs : arbitrary keyword arguments

        Returns
        -------
        results : object
            If 'results' was given, its value is returned. If not, None is returned.
        """
        return kwargs.get('results')