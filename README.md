experimental-results-framework
==============================

This repo includes all of the results and process management code. It is responsible for coordinating all of the code. Includes all binds for the different programming languages.

Required Packages:
-----------------

* Jetty 9 from http://download.eclipse.org/jetty/stable-9/dist/
* openjdk-7 (apt-get install openjdk-7-jdk openjdk-7-jre )
* dojo 1.9.0:  http://download.dojotoolkit.org/release-1.9.0/dojo-release-1.9.0-src.tar.gz
* pip install couchdb uptime drmaa
* apt-get install libdrmaa-dev

Webapps and Jetty:
-----------------

Jetty by default will take anything inside of the webapps folder and
use it as a static ocntent page. This folder is scanned by jkett yas
it runs for hot-plug contents.  So we just needc to create a folder
inside of webapps and copy in all of the dojo sources as well as make
a subfolder for our own UI sources and we are set. The webapp/<folder>
will be at url localhost:8080/<folder>.

View results locally:
--------------------

* Start a local couchdb (build-couchdb/build/bin/couchdb)
* View the results at http://localhost:5984/_utils/database.html?local_results

Running jobs on an SGE cluster:
----------------------

On the cluster:
* Start a couchdb (build-couchdb/build/bin/couchdb)
* Start the jobs server (python /experimental-results-framework/task-manager/src/task_manager/couchdb-job-server.py)
* Start the jobs tracker (python /experimental-results-framework/task-manager/src/task_manager/couchdb-job-tracker.py)

Sun Grid Engine Quickstart: (THIS SECTION IS STILL UNDER CONSTRUCTION)
--------------------------

Much of this was taken from [here](http://webappl.blogspot.com/2011/05/install-sun-grid-engine-sge-on-ubuntu.html).

* Install the required SGE packages

        sudo apt-get install gridengine-client gridengine-common gridengine-master gridengine-qmon gridengine-exec
        
* During installation it will ask for a cell name and hostname. 
* The cell name is the cell in which a job is executed - just leave this as default unless you want to run multiple grid engine instances off the same set of bianaries.
* The hostname is the name of the computer (???).

* Set the environment variable for SGE_ROOT 

        export SGE_ROOT=/usr/lib/gridengine
        export SGE_CELL=default
        
* If qmon fails to start due to missing fonts and reboot (may just need xfonts-75dpi)

         sudo apt-get install xfs xfstt t1-xfree86-nonfree ttf-xfree86-nonfree ttf-xfree86-nonfree-syriac xfonts-75dpi xfonts-100dpi
         
* Start qmon and click any button, if you get the message "cannot reach qmaster", see [here](http://scidom.wordpress.com/tag/parallel/)
         
http://webappl.blogspot.com/2011/05/install-sun-grid-engine-sge-on-ubuntu.html
http://www.cbi.utsa.edu/sge_tutorial
http://www.gridengine.info/2005/09/29/things-to-think-about-before-installing-grid-engine/
http://manpages.ubuntu.com/manpages/lucid/man8/sge_qmaster.8.html

License:
-------
This module is distrubted under the MIT license.
