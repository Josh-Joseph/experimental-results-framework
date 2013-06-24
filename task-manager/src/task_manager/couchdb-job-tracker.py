
import argparse
import drmaa
from cluster_id import *
import datetime
import socket
import couchdb
import time
from couchdb_job_status import *
import urllib
import sys
sys.path.append( "../../../experimental-results-python-library/src/" )
import experimental_results_python_library as EXL


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser( description= "Track the status of jobs on the local cluster and update couchdb" )
    parser.add_argument( "--check-interval", default=15.0, type=float,
                         help="The time to sleep between update checks, in seconds (default=15.0)")
    parser.add_argument( "--couchdb-base-url", default="http://localhost:5984/" )
    parser.add_argument( "--couchdb-jobs-db", default="jobs" )
    parser.add_argument( "--conflict-max-retries", default=10, type=int,
                         help="The number of times to retyr an update on a databse conflict (default=10).")
    parser.add_argument( "--conflict-sleep-interval", default=0.1, type=float,
                         help="The number of second to wait before retrying a conflicting update (default=0.1)" )
    args = parser.parse_args()

    # get couchdb connection and database target
    couch = couchdb.Server( args.couchdb_base_url )
    try:
        couch.create( args.couchdb_jobs_db )
        print "created database %s in order to listen to changes" % args.couchdb_jobs_db
    except couchdb.PreconditionFailed:
        pass
    db = couch[args.couchdb_jobs_db]


    # start a drmaa session
    drmaa_session = drmaa.Session()
    drmaa_session.initialize()

    # Fetch all interesting jobs from hte couchdb and update their status 
    # based on the DRMAA session status
    while True:
            
        
        # start fetching the view at
        # jobs/_design/job_tracker/_view/all_jobs_by_cluster_and_status
        # But we only want jobs from this cluster with the statius "submitted"
        #
        # for each such job document, we want to update it's status
        found = False
        # view_query = { "cluster_id" : str(get_self_cluster_id()),
        #                "status" : "submitted" }
        # for doc in db.iterview( "job_tracker/all_jobs_by_cluster_and_status",
        #                         20,
        #                         wrapper=None,
        #                         key=EXL.to_json(view_query)):
        for doc in db.iterview( "job_tracker/all_jobs_by_status",
                                20,
                                wrapper=None,
                                key=urllib.quote_plus("submitted") ):

            found = True
            update_job_status( db, doc["value"],
                               drmaa_session,
                               max_tries = args.conflict_max_retries,
                               sleep_time = args.conflict_sleep_interval )

        # print if none found
        if not found:
            print "did not find any jobs to update ..."
            # print "  view query: " + urllib.quote_plus( EXL.to_json(view_query))
            # print "  deconded: " + urllib.unquote_plus( urllib.quote_plus( EXL.to_json(view_query)) )

        # sleep some for next update lop
        time.sleep( args.check_interval )

    # exit drmaa session
    drmaa_session.exit()
