
import uuid


#-----------------------------------------------------------------------------

def get_self_cluster_id():
    """Return the id for the cluster we are running on."""
    
    return str( uuid.uuid5( uuid.NAMESPACE_URL, "https://github.com/josh00/experimental-results-framework?cluster-id=" + str(uuid.getnode())) )

#-----------------------------------------------------------------------------
