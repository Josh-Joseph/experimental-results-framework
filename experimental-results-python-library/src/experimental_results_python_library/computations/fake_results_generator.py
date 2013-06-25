from computation import Computation
import numpy as np


class FakeResultsGenerator(Computation):
    def __index__(self, upid=None):
        super(FakeResultsGenerator, self).__init__(upid)

    def run(self, trial_id=None):
        n_samples = np.random.randint(10, 1000)
        data = [np.random.random() * 100 for x in xrange(n_samples)]
        results = {"computation":
                       {"trial_id": trial_id,
                        "agent": {"generator": {"name": "fake", "p_args": [], "kw_args": {}}},
                        "result": {"mean": np.mean(data),
                                   "variance": np.var(data),
                                   "num_samples": n_samples,
                                   "data_samples": data},
                        "parameters": {"num_evaluation_episodes": np.random.randint(1, 50)},
                        "domain": {"generator": {"name": "fake_domain", "p_args": [], "kw_args": {}},
                                   "parameters": {}},
                        "log_filename": None}}
        return results