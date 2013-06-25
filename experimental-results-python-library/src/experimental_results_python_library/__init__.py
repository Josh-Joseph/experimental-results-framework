import json_utils
from json_utils import podify, to_json, from_json
import computations
import code_version

# try to import log_result, will connect to couchdb
import warnings
import socket
try:
    import log_result
    from log_result import log_result
    import couchdb_utils
except socket.error, v:  # the connection was refused
    errorcode = v[0]
    if errorcode == 111:
        warnings.warn("Could not connect to couchdb.")
    else:
        raise
