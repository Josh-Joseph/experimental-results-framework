



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
    

