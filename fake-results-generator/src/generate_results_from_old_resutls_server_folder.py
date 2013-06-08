
import cPickle
import numpy
import argparse
import os
import os.path
import couchdb
import re
import sys

sys.path.append( "/home/velezj/projects/gits/rl-classification/src/RL-Python/")
import Domains



def make_db_name( s ):
    name = s.lower().replace(".", "_" ).replace("-","_")
    if name[0].isdigit():
        return "db_" + name
    return name


##
## Returns a "Plain-Ol-Datatype (POD)" repreentation of the given python
## value.  This makes it able to be converted into JSON
def podify( v ):
    if isinstance( v, str ):
        return v
    if isinstance( v, int ):
        return v
    if isinstance( v, float ):
        return v
    if isinstance( v, list ):
        return map( podify, v )
    if isinstance( v, dict ):
        pod_t = {}
        for k,v in v.iteritems():
            tk,tv = transform_old_result_item( k,v )
            pod_t[ tk ] = tv
        return pod_t
    if isinstance( v, tuple ):
        return podify( list( v ) )
    return str(v)


##
## Returns the POD value for an old-style generator
def podify_genegator( gen ):
    res = {}
    res["generator"] = gen[0]
    res["p_args"] = gen[1]
    res["kw_args"] = gen[2]
    return podify( res )


def transform_old_result_item( k, v ):
    if isinstance( k, str ):
        return k, podify( v )
    if isinstance( k, tuple ):
        if k[0] == 'Agent':
            res = {}
            res["pargs"] = k[1]
            res["structure"] = podify_genegator( k[2] )
            if v is not None:
                res["result"] = v
            return "agent", podify( res )
        if k[0] == "METADATA":
            res = {}
            res['agent'] = transform_old_result_item( k[1], None )
            res['value'] = v
            return "metadata", podify( res )
        if isinstance(k[0], str ):
            res = {}
            res[ k[0] ] = podify( k[1:] )
            res[ "result" ] = v
            return k[0], podify(res)
        print "UNKNWON old-style tuple: " + str(k)
    return podify(k), podify(v)
    


def add_old_result_to_db( couch_db, result_file ):
    
    res = None
    with open( result_file ) as f:
        res = cPickle.load( f )
        res_t = podify( res )
        couch_db.save( res_t )


if __name__ == "__main__":

    parser = argparse.ArgumentParser( description= "Generate results from old results-server folders" )
    parser.add_argument( "results_folder" )
    parser.add_argument( "--couchdb-base-url", default="http://localhost:5984/" )
    parser.add_argument( "--couchdb-target-db", default="")
    parser.add_argument( "--recursive", default=False, 
                         action="store_const", const=True )
    args = parser.parse_args()
    #print args

    # get couchdb connection and database target
    couch = couchdb.Server( args.couchdb_base_url )
    target_db = args.couchdb_target_db
    if target_db == "":
        target_db = args.results_folder
        if target_db.endswith("/"):
            target_db = target_db[:-1]
        target_db = make_db_name( os.path.basename(target_db) )
    try:
        couch.create( target_db )
        print "created database %s for storing results" % target_db
    except couchdb.PreconditionFailed:
        pass
    db = couch[target_db]

    # get a list of the results to transform
    result_files = []
    if args.recursive:
        for root, dirs, files in os.walk( args.results_folder ):
            print "recursed into " + root
            for f in files:
                if f.startswith( 'results-trial' ) and f.endswith( '.pickle' ):
                    result_files.append( os.path.join( args.results_folder, root, f ) )
    else:
        for f0 in os.listdir( args.results_folder ):
            if os.path.isdir( os.path.join( args.results_folder, f0 ) ):
                print "checking inner dir " + f0
                for f in os.listdir( os.path.join( args.results_folder, f0 ) ):
                    if f.startswith('results-trial') and f.endswith( '.pickle'):
                        result_files.append( os.path.join( args.results_folder, f0, f ) )
                        #print "added file: " + result_files[-1]

    # print out info to the user
    print "Found %d matching results to add to database %s...." % (len(result_files), target_db)
    
    # actually add the results to the db
    for f in result_files:
        add_old_result_to_db( db, f )

    
            
