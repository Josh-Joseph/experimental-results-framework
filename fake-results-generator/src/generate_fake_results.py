
import sys
import argparse
import datetime
import random
import couchdb
import numpy
sys.path.append( "../../experimental-results-python-library/src/")
import experimental_results_python_library as EXL



def generate_fake_results( couch_db, trial_id="0" ):
    
    n_samples = random.randint( 10, 1000 )
    data = [ random.random() * 100 for x in xrange(n_samples) ]
    results = { "trial" :
                    { "trial_id" : trial_id,
                      "agent" :
                          { "generator" :
                                { "name" : "fake",
                                  "p_args" : [],
                                  "kw_args" : {} } },
                      "result" :
                          { "mean" : numpy.mean(data),
                            "variance" : numpy.var(data),
                            "num_samples" : n_samples,
                            "data_samples" : data },
                      "parameters" :
                          { "num_evaluation_episodes" : random.randint( 1, 50 ) },
                      "domain" :
                          { "generator" :
                                { "name" : "fake_domain",
                                  "p_args" : [],
                                  "kw_args" : {} },
                            "parameters" : {} },
                      "code" :
                          { "version" :
                                EXL.code_version.get_code_version() },
                      "stored_on" : None,
                      "log_filename" : None } }
    couch_db.save( EXL.podify(results) )


if __name__ == "__main__":

    parser = argparse.ArgumentParser( description= "Generate fake results" )
    parser.add_argument( "--num-trials", default=10, type=int )
    parser.add_argument( "--trial-id-gen", default="sequential", choices=["sequential", "random"] )
    parser.add_argument( "--couchdb-base-url", default="http://localhost:5984/" )
    parser.add_argument( "--couchdb-target-db", default="fake_results_" + datetime.datetime.now().isoformat().lower().replace(":","_").replace(".","_").replace("-","_") )
    args = parser.parse_args()

    # get couchdb connection and database target
    couch = couchdb.Server( args.couchdb_base_url )
    try:
        couch.create( args.couchdb_target_db )
        print "created database %s for storing results" % args.couchdb_target_db
    except couchdb.PreconditionFailed:
        pass
    db = couch[args.couchdb_target_db]

    # ok, generate trial id's and then generate results for each trial
    for t in xrange( args.num_trials ):
        trial_id = str(t)
        if args.trial_id_gen != "sequential":
            trial_id = str(random.randint( 0, args.num_trials * 1000 ))
        
        generate_fake_results( db, trial_id = trial_id )
    
    
    print "Running fake result generation finished, generated %d trials" % args.num_trials 




