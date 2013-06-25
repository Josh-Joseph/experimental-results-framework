
import time
from json_utils import *



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

def update_couchdb_document( couch_db, doc, update_list, 
                             max_retries=10, retry_wait_interval=0.1 ):
    """Updates the given document with the given updates and stores 
       the changes into couchdb.  This will retry a numb er of times
       defined by max-retries if a conflit arises. It initially tries to
       submit the changed document without first fetching it, so this
       implements a sort of optimistic conflict resolution strategy.
       Raises exception if we could not update the document (becasue 
       of an error or the maximum retries were tried.)
    
       Arguments:
       couch_db -- a couchdb database which will be updated.
       doc -- a document from the given couchdb databse that needs to be updated
       update_list -- a list of update tuples OR a dictionary.  The tuples
                      must be of the form ( structured-key, new-value )
                      where the structured kjey is a string.
                      IF a dictionary, the keys must be string structured keys 
                      and theyr mapped values are used as the new values for
                      the update.
       max_retries -- the number of times to retry the update before giving
                      up. Defaults to 10. If less than 0, will keep trying 
                      to update forever.
       retry_wait_interval -- the number of seconds to wait between retries.
                              Default = 0.1s
    
       Returns:
         Nothing
    
       Raises:
         Exception if max retries used and could not update the document.
         Any exceptions returned by couchdb.database.save().
    """
    
    # convert the updates to a dictionaryt
    update_dict = dict( update_list )
    
    # the number of times we have tried the update
    num_tries = 0
    did_update = False
    first_run = True
    
    # apply updates to document and try to save it
    while max_retries < 0 or num_tries < max_retries:

        # if this is not the first run, fetch the document
        # from hte couchdb databse
        if not first_run:
            doc = couch_db.get( doc["_id"] )
        
        # apply changes to doc
        for skey, val in update_dict.iteritems():
            structure_put( skey, val, doc )

        # try to save the doc
        try:
            couch_db.save( doc )
            did_update = True
            break
        except couchdb.ResourceConflit:
            num_tries += 1
            
        # no longer hte first run
        first_run = False
        
        # wait some time before retrying
        time.sleep( retry_wait_interval )
            
    # If we reached max tries, raise exception
    if not did_update:
        raise Exception( "Maximum retries (" + str(max_retries) + ") reached while trying to update document: " + str(doc) + " with updates: " + str(update_dict) )

    return None
