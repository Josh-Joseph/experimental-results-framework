import logging_with_processing_info as log
import argparse
from json_utils import try_to_parse_dict_values_json
from estimators import *
from cross_validation_iterators import *

###################################
# define the command-line arguments
parser = argparse.ArgumentParser(description= "A job which runs an estimator.")

# estimator arguments
parser.add_argument("-e", "--estimator", required=True)
parser.add_argument("-epars", "--estimator-parameters")
parser.add_argument("-X", "--input-X")
parser.add_argument("-y", "--output-y")

# cross validation iterator arguments
parser.add_argument("-cvi", "--cross-validation-iterator", default='CrossValidationIterator')
parser.add_argument("-cvipars", "--cross-validation-iterator-parameters")

# process control parameters
parser.add_argument("-puid", "--process-unique-id")
parser.add_argument("-jpars", "--job-parameters")

# parse the given arguments
args = parser.parse_args()
###################################

# configure logging messages
log.basicConfig(format='[%(levelname)s %(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=log.INFO)

# convert the arguments to a dictionary
kwargs = args.__dict__

# attempt to parse the dictionary values using json
kwargs = try_to_parse_dict_values_json(kwargs)

# build iterator
cv_iterator = eval(kwargs['cross_validation_iterator'])(kwargs['cross_validation_iterator_parameters'])

# build estimator
estimator = eval(kwargs['estimator'])(kwargs['estimator_parameters'], cv=cv_iterator)

# run job
result = estimator.score(kwargs['input_X'], kwargs['output_y'])

# log the result into couchdb