from computation import Computation
import numpy as np
from datetime import datetime, date


class FakeResultsGenerator(Computation):
    def __index__(self, upid=None):
        super(FakeResultsGenerator, self).__init__(upid)

    def run(self, computation_id=None, output_type=None):

        if output_type is None:
            n_samples = np.random.randint(10, 1000)
            data = [np.random.random() * 100 for x in xrange(n_samples)]
            results = {"computation":
                           {"computation_id": computation_id,
                            "agent": {"generator": {"name": "fake", "p_args": [], "kw_args": {}}},
                            "result": {"mean": np.mean(data),
                                       "variance": np.var(data),
                                       "num_samples": n_samples,
                                       "data_samples": data},
                            "parameters": {"num_evaluation_episodes": np.random.randint(1, 50)},
                            "domain": {"generator": {"name": "fake_domain", "p_args": [], "kw_args": {}},
                                       "parameters": {}},
                            "log_filename": None}}

        elif output_type == '1D-list':
            num_results=10
            np.random.seed(0)
            data = np.random.random(num_results)
            results = {"computation": {"result": list(data)}}

        elif output_type == '2D-list':
            num_results=10
            np.random.seed(0)
            data = np.random.random((num_results, 2))
            results = {"computation": {"result": [list(arr) for arr in data]}}

        elif output_type == 'datetime-list':
            dts = [datetime(2013, 1, 4, 12, 32, 4), datetime(2012, 11, 11, 11, 11, 11), datetime(2013, 1, 5, 9, 32, 14),
                   datetime(2013, 2, 3, 14, 3, 35), datetime(2013, 2, 4, 12, 32, 32), datetime(2013, 4, 4, 15, 32, 44)]
            results = {"computation": {"result": dts}}

        elif output_type == 'trades':
            enter_dts = [datetime(2013, 1, 4, 12, 32, 4), datetime(2012, 11, 11, 11, 11, 11),
                         datetime(2013, 1, 5, 9, 32, 14), datetime(2013, 2, 3, 14, 3, 35),
                         datetime(2013, 2, 4, 12, 32, 32), datetime(2013, 4, 4, 15, 32, 44)]
            exit_dts = [datetime(2013, 1, 4, 12, 32, 14), datetime(2012, 11, 11, 11, 12, 11),
                         datetime(2013, 1, 5, 9, 32, 15), datetime(2013, 2, 3, 15, 3, 35),
                         datetime(2013, 2, 4, 12, 52, 32), datetime(2013, 4, 4, 15, 38, 44)]
            symbols = ['XYZ', 'ABC', 'QWE', 'RTY', 'CBA', 'ZYX']
            profit_perc = [1.1, -1.1, 2.2, -2.2, 0.0, 0.0]
            keys = ['enter_datetime', 'exit_datetime', 'symbol', 'profit_perc']
            values = zip(*[enter_dts, exit_dts, symbols, profit_perc])
            results = {"computation": {"result": [dict(zip(keys, trade)) for trade in values],
                                       "strategy": "money-for-science",
                                       "features": ["phase-of-the-moon", "bangkok-humidity"]}}

        elif output_type == 'cross-validation':
            num_results=10
            num_folds = 4
            np.random.seed(0)
            results = {"computation": {"folds": {}}}
            for i in range(num_folds):
                data = np.random.random(num_results)
                results['computation']['folds'][i] = list(data)

        return results