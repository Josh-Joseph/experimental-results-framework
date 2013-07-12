experimental-results-framework
==============================

The experimental results framework is composed of two parts:

1.  (Distributed computation) A framework for starting and monitoring jobs across multiple clusters composed of multiple machines.
2.  (Results Storage) A distrubted syncing and storage framework for the results produced by a job.

Distributed computation uses:
* Starcluster to manage the machines of EC2 clusters
* CouchDB to maintain the state of new/submitted/running/done jobs across clusters
* Sun Grid Engine (SGE) to run and monitor jobs inside each cluster
* job-sever.py to start new jobs on SGE and update the jobs state on CouchDB
* job-tracker.py to monitor the jobs running/done on SGE and update the jobs state on CouchDB

Results Storage uses:
* CouchDB to sync results from clusters with local machines

A special type of a job, called a "computation", is generally used throughout the framework which has two requirements:
* It can be started as an commandline executable script (with commandline arguments, if desired),
* Produces results that are pushed to the cluster's CouchDB

A typical job flow looks like:
* A document is pushed into CouchDB containing the script(s) executation details with a field "status" with value "new"
* If the push was done on a local machine, the local CouchDB updates the CouchDB running on a cluster's master node with the new document
* job-server.py, running on the cluster's master node, is notified about the new document, sends SGE the execution details, and updates the "status" field to "submitted"
* SGE executes the script(s) on the cluster
* job-tracker.py periodically queries SGE for the status of the jobs and updates "status" to "running" or "done"
* The jobs pushed their results into the master's CouchDB 
* The master's CouchDB's results are pushed to the local CouchDB

Required Processes on each Machine:
-----------------------------------

On the cluster's master:
* SGE
* job-server.py (python /experimental-results-framework/task-manager/src/task_manager/couchdb-job-server.py)
* job-tracker.py (python /experimental-results-framework/task-manager/src/task_manager/couchdb-job-tracker.py)
* CouchDB

On the cluster's nodes:
* SGE

Locally:
* CouchDB


Required Packages:
-----------------

* pip install couchdb uptime drmaa
* apt-get install libdrmaa-dev


Getting CouchDB running:
------------------------

See [this](https://github.com/josh00/experimental-results-framework-couchdb) project for instructions on setting up CouchDB


To start up CouchDB just run:

    build-couchdb/build/bin/couchdb


Generating Fake Results:
------------------------
    
Put fake results into the database

    git clone git@github.com:josh00/experimental-results-framework.git

    cd experimental-results-framework/fake-results-generator/

    python generate_fake_results.py --num-trials 200
    
To view the fake results locally:
* Start a local couchdb (build-couchdb/build/bin/couchdb)
* View the results at http://localhost:5984/_utils/database.html?local_results


Getting Sun Grid Engine running:
--------------------------

* Follow the instructions at

                http://scidom.wordpress.com/tag/parallel/
                
* Other useful pages:

                http://webappl.blogspot.com/2011/05/install-sun-grid-engine-sge-on-ubuntu.html
                http://www.cbi.utsa.edu/sge_tutorial
                http://www.gridengine.info/2005/09/29/things-to-think-about-before-installing-grid-engine/
                http://manpages.ubuntu.com/manpages/lucid/man8/sge_qmaster.8.html

License:
-------
This module is distrubted under the MIT license.
