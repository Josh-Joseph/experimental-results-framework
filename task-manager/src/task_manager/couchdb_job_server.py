
from couchdb_job_control import *

if __name__ == "__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser( description= "Listen for JOBS on the local (or given) couchdb jobs database" )
    parser.add_argument( "--couchdb-base-url", default="http://localhost:5984/" )
    parser.add_argument( "--couchdb-jobs-db", default="jobs" )
    parser.add_argument( "--sequence-number", 
                         default="now",
                         help="One of either: \"now\" (default) for the current changes, or a number to use as the first seuence number for changes to lsiten on, or a filename which has a sequence number in it to use.")
    parser.add_argument( "--last-change-processed-file", default="last-change-processed.txt" )
    args = parser.parse_args()

    # get couchdb connection and database target
    couch = couchdb.Server( args.couchdb_base_url )
    try:
        couch.create( args.couchdb_jobs_db )
        print "created database %s in order to listen to changes" % args.couchdb_jobs_db
    except couchdb.PreconditionFailed:
        pass
    db = couch[args.couchdb_jobs_db]

    # fech the wanted sequence number to start listening in on
    last_seq_number_or_now = args.sequence_number
    if not last_seq_number_or_now == "now" and not last_seq_number_or_now.isdigit():
        
        # something that is not "now" or an explicit number is treated as a file
        # with the last sequence number processed from before
        with open( last_seq_number_or_now ) as f:
            last_seq_number_or_now = f.read().strip()

    # ok, open a continuous changes feed from the last change seen
    for change in db.changes( feed="continuous", 
                              include_docs="true", 
                              since=last_seq_number_or_now ):
        
        print "got change: " + str(change["seq"])
        process_single_change( db, change, args.last_change_processed_file )
        
        
