import logging_with_processing_info as log
import argparse
from json_utils import parse_json_dict
from log_result import log_result as push_result_into_couchdb
from computations import *


###################################
# define the command-line arguments
parser = argparse.ArgumentParser(description= "A job which runs an estimator.")

# computation arguments
parser.add_argument("-c", "--computation", required=True)
parser.add_argument("-cpars", "--computation-parameters")
parser.add_argument("-cin", "--computation-inputs")

# unique process id which is passed to the computation for logging
parser.add_argument("-upid", "--unique-process-id")

# parse the given arguments
args = parser.parse_args()
###################################

# configure logging messages
log.basicConfig(format='[%(levelname)s %(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=log.INFO)

# convert the arguments to a dictionary
kwargs = args.__dict__

# parse the json strings of computation-parameters and computation-inputs into dictionaries
kwargs['computation_parameters'] = parse_json_dict(kwargs['computation_parameters'])
kwargs['computation_inputs'] = parse_json_dict(kwargs['computation_inputs'])

# build computation
computation = eval(kwargs['computation'])(kwargs['unique_process_id'], kwargs['computation_parameters'])

# run the computation
result = computation.run(kwargs['computation_inputs'])

# log the result into couchdb
push_result_into_couchdb(result)