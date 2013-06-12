
import global_defaults
import code_version
import json_utils
import couchdb
import datetime
import uuid


#----------------------------------------------------------------------------

##
## Description:
## This variable stores the code version information. It is cached here and
## only filled once when this module starts up for performance reasons.
_global_code_version = code_version.get_code_version(global_defaults.code_repo_directory)

#----------------------------------------------------------------------------

##
## Description:
## This variable stores the default couch_db database to use for log_result
## and friends.  By default, we just use our local couchdb instance to log to.
## We store log results into "https://localhost:5984/local_log_results" 
## database.
couch_server = couchdb.Server( global_defaults.couchdb_local_server_url )
_couch_db_name = global_defaults.couchdb_local_log_results_db_name
try:
    couch_server.create( _couch_db_name )
    print "created database %s for storing local log results" %  _couch_db_name
except couchdb.PreconditionFailed:
    pass
couch_db = couch_server[ _couch_db_name ]


#----------------------------------------------------------------------------


def log_result( result=None,                         
                couch_db=couch_db,                   
                code_version=_global_code_version,   
                **extra_keys):
    """Log the given result. You *must*
       supply the result keyword.  Any extra keywords will
       be added into the top-level result dictionary if it is a dictionary,
       otherwise a dict will be created with the 'result' key and the given 
       result structure as the value.
       The result dictionary will have a 'code/version' dictionary with the
       code_version argument.
       The result dictionary will have a 'stored_on' key with the current 
       datetime.
       
       Returns the (id,rev) of teh stored result from the database."""
    
    # build up the result dictionary
    res_dict = result
    if not isinstance( result, dict ):
        res_dict = {}
        res_dict['result'] = result
    res_dict['code'] = {}
    res_dict['code']['version'] = code_version
    res_dict.update( extra_keys )
    res_dict['stored_on'] = datetime.datetime.now()
    
    # given results an id unless already specified
    if not "_id" in res_dict:
        res_dict["_id"] = uuid.uuid1().hex
    
    # store the result dictionary in the db
    return couch_db.save( json_utils.podify( res_dict ) )
    

#----------------------------------------------------------------------------
