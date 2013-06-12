

##
## This file contains global variables used for defaults in the 
## experimental resutls framework library.
##
## You should explicitly import this file *BEFORE* any of the library modules
## and se the variables if you want to change them


import os

#----------------------------------------------------------------------------

##
## The default code repository dorectory to use.
## default: the current working dirextory
code_repo_directory = os.getcwd()

#----------------------------------------------------------------------------

##
## The default couchdb local databse server url
## default: http://localhost:5984/
couchdb_local_server_url = "http://localhost:5984"

#----------------------------------------------------------------------------

##
## The default databse name for logging results
## default: local_resutls
couchdb_local_log_results_db_name = "local_results"

#----------------------------------------------------------------------------
