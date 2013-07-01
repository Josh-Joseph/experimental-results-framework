

import git
import os
import os.path



#----------------------------------------------------------------------------

def get_code_version( repo_filename = None, return_empty_keys=False ):
    """Return the code repository version of the GIT repository at the given
       lcoation. If no location is given, the current working directory is
       used instead.
       Right now, this will alway assume you have the "origin" remote set up
       and that is the URL returned under repo_url.
       The returned version is a python dictionary with the following fields:
         { "repo_url" : "<url>",
           "branch" : "<branch>",
           "head" : "<commit-hashtag>",
           "head_date" : "<timestamp>",
           "diffs: [<all diffs from head>],
           "untracked_files" : [<all files untracked>]}
           
       If any field is empty ([]), then the return dictionary will not
       have the keys unless return_empty_keys=True is given as argument.
       """
    
    if repo_filename is None:
        repo_filename = os.getcwd()
    repo = git.Repo( repo_filename )

    # gather all diffs from the current head
    working_diffs = repo.head.commit.diff( None, create_patch=True )
    all_diffs = { "deleted" : [],
                  "added" : [],
                  "modified" : [],
                  "renamed" : []}
    for d in working_diffs:
        if d.deleted_file:
            all_diffs["deleted"].append( { "path" : d.a_blob.path } )
        elif d.new_file:
            all_diffs["added"].append( { "path" : d.b_blob.path } )
        elif d.renamed:
            all_diffs["renamed"].append( {"from" : d.rename_from,
                                          "to" : d.rename_to} )
        else:
            all_diffs["modified"].append( {"path" : d.a_blob.path,
                                           "patch" : d.diff } )
            
    # ok, now gather all untracked files
    # (this will take care of using hte .gitignore! )
    ut = repo.untracked_files
    untracked_files = []
    for name in ut:
        path = os.path.join( repo.working_dir, name ) 
        
        # explicitly ignore job-local files
        # and last-changed-process.txt files
        if path.find( "job-local" ) == -1 or path.find( "last-change-processed" ) == -1:
            continue
        with open( path ) as f:
            untracked_files.append( { "path" : path,
                                      "contents" : f.read(),
                                      "modified_time" : os.path.getmtime( path ) } )
    
    # create the resulting dictionary
    res = {
        "repo_url" : repo.remotes.origin.url,
        "branch" : repo.active_branch.path,
        "head" : repo.head.reference.commit.hexsha,
        "head_date" : repo.head.reference.commit.committed_date,
        "diffs" : all_diffs,
        "untracked_files" : untracked_files }
    if return_empty_keys == False:
        if len(untracked_files) == 0:
            del res["untracked_files"]
        if len(working_diffs) == 0:
            del res["diffs"]
    
    return res

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
