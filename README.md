experimental-results-framework
==============================


Required Packages:

Jetty 9 from http://download.eclipse.org/jetty/stable-9/dist/
openjdk-7 (apt-get install openjdk-7-jdk openjdk-7-jre )
dojo 1.9.0:  http://download.dojotoolkit.org/release-1.9.0/dojo-release-1.9.0-src.tar.gz
pip install couchdb


Webapps and Jetty
=================

Jetty by default will take anything inside of the webapps folder and
use it as a static ocntent page. This folder is scanned by jkett yas
it runs for hot-plug contents.  So we just needc to create a folder
inside of webapps and copy in all of the dojo sources as well as make
a subfolder for our own UI sources and we are set. The webapp/<folder>
will be at url localhost:8080/<folder>.

