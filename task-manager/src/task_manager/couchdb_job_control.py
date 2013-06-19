import couchdb
import sge_manager
from cluster_id import *
import os
import os.path
import uuid
import datetime


#-----------------------------------------------------------------------------

def structured_key_to_list( skey, separator="." ):
    """Returns a list representation of the strucutred key.
       This splits "a.b.c" into [ "a", "b", "c" ].
       The optional separator to use to define sturctured keys (default .)"""
    
    return skey.split( separator )

#-----------------------------------------------------------------------------

def structure_has( skey, d, separator="."  ):
    """Returns true iff the given structure key is inside the dictionary.
       Each element of the structure is treated as a subdictionary.
       Optionaly, give the spearator to use for structured keys."""

    klist = structured_key_to_list( skey, separator )
    subd = d
    for k in klist:
        if not k in subd:
            return False
        subd = subd[k]
    return True

#-----------------------------------------------------------------------------

def structure_get( skey, d, separator=".", default=None  ):
    """Returns the element at the sturctured key in hte dictionary.
       Each element of the structure is treated as a subdictionary.
       Optionally, give the separator to use for structured keys."""

    klist = structured_key_to_list( skey, separator )
    subd = d
    for k in klist:
        if not k in subd:
            return default
        subd = subd[k]
    return subd

#-----------------------------------------------------------------------------

def structure_put( skey, val, d, separator="." ):
    """Puts a given value into a sturcutred key.
       This creates subdictionaries as needed for the structured key."""
    
    klist = structured_key_to_list( skey, separator )
    subd = d
    for k in klist[:-1]:
        if not k in subd:
            subd[k] = {}
        subd = subd[k]
    subd[klist[-1]] = val
    return d

#-----------------------------------------------------------------------------


def revision_number_from_revision( rev ):
    """Extract the revision number as in int ( also know as the number 
       of  document changes that have happened ) from a couchdb revision tag.
       This is the number before the first hiupen (#-uuid)."""
    
    return int(rev[:rev.index('-')])

#-----------------------------------------------------------------------------

def fetch_previous_revision( couch_db, json_doc ):
    """Returns the previous revision of hte given docomunet from the
       couchdb databse given."""
    
    # fetch the current revision of hte document using id
    revision_gen = couch_db.revisions( json_doc["_id"] )
    
    # find the revision *after* the given one
    previous = None
    found = False
    for doc_rev in revision_gen:
        if found:
            previous = doc_rev
            break
        if doc_rev["_rev"] == json_doc["_rev"]:
            found = True
    
    # return the previous revision (or None)
    return previous
    

#-----------------------------------------------------------------------------

def process_single_change( couch_db, couchdb_json_change, last_seq_filename ):
    """Process a single change event from the couchdb jobs databse.
       This will take care of the following:
         (1) start up any new sasked for jobs on the current cluster if
             we want to job to be on the current clsuter.
         (2) stop any jobs running on hte current cluster that were 
             asked to stop
         (3) pause/resume jobs on the current clsuter when asked.
        
       The changes are to the actual job documents in the jobs databse
       and the documents themselves include all relevant information to
       perform the actual processing (such as a SGE id and clsuter id).
       We also overwrite the given file with the sequence number of the
       last change processed."""
    
    # skip "deleted" changes
    if "deleted" in couchdb_json_change:
        # overwrite file with last change procesed
        with open( last_seq_filename, 'w' ) as f:
            f.write( couchdb_json_change["seq"] )
        return
        
    # ensure that we have the document with us
    if not "doc" in couchdb_json_change:
        raise Exception( "We need to have the document included in the changesets!, change: " + str(couchdb_json_change) )
    
    # grab the document that change
    job_doc = couchdb_json_change["doc"]
    
    # check if this is a completely new document using it's revision prefix
    rev_number = revision_number_from_revision( couchdb_json_change["changes"][0]["rev"] )
    if structure_get( "job.status", job_doc ) == "request:new":
        
        # we are a new job, so treat it as such
        process_new_job( couch_db, job_doc )
    else:
        
        # we are a job that has changed,
        # process the changes
        process_job_change( couch_db, job_doc )

    # overwrite file with last change procesed
    with open( last_seq_filename, 'w' ) as f:
        f.write( str(couchdb_json_change["seq"]) )
        
    

#-----------------------------------------------------------------------------

def process_new_job( couch_db, job_doc ):
    """Process a new job document comming into the database.
       This will fill out the fields for the SGE and will submit this
       new job to hte master quere."""
    
    
    # make sure we have a new job here
    if not structure_has( "job.status", job_doc ) or not structure_get( "job.status", job_doc ) == "request:new":
        raise Exception( "Unable to process new job, job document malformed or of unknown type: " + str(job_doc) )
    
    
    # check if this is for us (for our clsuter)
    # return and do nothing otherwise
    if not structure_get( "job.cluster_id", job_doc ) == get_self_cluster_id():
        return
    
    # create a unique folder for this job
    uid = uuid.uuid1()
    unique_job_folder = os.path.abspath( os.path.join( ".", "job-local", str(uid) ) )
    os.makedirs( unique_job_folder )
    
    # get any dependencies and ensure they are all within this cluster
    dependencies = []
    for dep in structure_get( "job.depends_on", job_doc, default=[] ):
        dep_job = couch_db.get( dep )
        if not structure_get( "job.cluster_id", dep_job ) == get_self_cluster_id():
            raise Exception( "Cannot handle jobs with dependencies across different clusters! found inconsistency inside: " + str(job_doc) + "  Dependency " + dep + " is: " + str(dep_job) )
        
        # fetch the actual sge job id from the job
        dep_sge_id = structure_get( "job.sge_id", dep_job)
        if dep_sge_id is None:
            raise Exception( "Cannot have dependent job without an SGE job id! job: %s, Dependency %s:" %  ( str(job_doc), str(dep), str(dep_job) ) )
        dependencies.append( dep_sge_id )

    # Ok, submit the job using SGE
    sge_jid = sge_manager.submit_task( target = structure_get( "job.script", job_doc ),
                                       depends_on = dependencies,
                                       cwd = unique_job_folder,
                                       priority = structure_get( "job.priority", job_doc, default="-1023" ) )
    
    # update the job document to say that it has been submited
    # with a given local folder and SGE job id
    structure_put( "job.job_id", "%s_%s_%s" % ( get_self_cluster_id(), str(sge_jid), str(uid) ), job_doc )
    structure_put( "job.sge_id", sge_jid, job_doc )
    structure_put( "job.local_directory", unique_job_folder, job_doc )
    structure_put( "job.status" , "submitted", job_doc )

    # update the couchdb document
    couch_db.save( job_doc )
    

#-----------------------------------------------------------------------------

def process_job_change( couch_db, job_doc):
    """Process a change in a job document. This takes care of anything not 
       a new job.  For example, this handles stopping, pausing, and resuming 
       jobs if they are running within this clsuter."""
    
    # ignore submitted status jobs, nothing to do
    if structure_get( "job.status", job_doc ) == "submitted":
        return
    
    
    status = structure_get( "job.status", job_doc )
    
    # nothing to do if it is not a rewuest for stop, pause, or resume
    if not ( status == "request:stop" or status == "request:pause" or status == "request:resume" ):
        return

    # ignore jobs for different clusters
    if not structure_get( "job.cluster_id", job_doc ) == get_self_cluster_id():
        return

    # stop a job
    if status == "request:stop":
        process_stop_request( couch_db,
                              job_doc )
    else:
        
        # TODO: implement pause-request, and resume-request
        raise Exception( "Not Implemented: processing of job change: " + str(job_doc) )


#-----------------------------------------------------------------------------

def process_stop_request( couch_db, job_doc ):
    """Stops the given job and removesd it from the SGE master queye.
       This will update the status to stopped."""

    # get the sge job id and stop it
    sge_id = structure_get( "job.sge_id", job_doc )
    sge_manager.stop_job( sge_id )
    
    # update the status to stopped
    structure_put( "job.status", "stopped", job_doc )
    structure_put( "job.stop_date", str(datetime.datetime.now()), job_doc )
    couch_db.save( job_doc )
    

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

