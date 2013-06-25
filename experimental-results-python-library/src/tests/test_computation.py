from nose.tools import assert_equals, assert_true
import numpy as np
import pandas as pd
from datetime import date, timedelta, time, datetime
from experimental_results_python_library.computations import Computation


def test_computation():

    upid = '32-32fdsfdsfaifj_ewf32ewfsdfs4499dsfds'
    computation = Computation(upid=upid)
    assert_equals(upid, computation.upid)

    results = computation.run(results=[1, 2, 3, 4, 5])
    assert_true(np.all(results == [1, 2, 3, 4, 5]))



