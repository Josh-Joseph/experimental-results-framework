# Default pod makefile distributed with pods version: 12.09.21

default_target: all

# Default to a less-verbose build.  If you want all the gory compiler output,
# run "make VERBOSE=1"
$(VERBOSE).SILENT:

# Figure out where to build the software.
#   Use BUILD_PREFIX if it was passed in.
#   If not, search up to four parent directories for a 'build' directory.
#   Otherwise, use ./build.
ifeq "$(BUILD_PREFIX)" ""
BUILD_PREFIX:=$(shell for pfx in ./ .. ../.. ../../.. ../../../..; do d=`pwd`/$$pfx/build;\
               if [ -d $$d ]; then echo $$d; exit 0; fi; done; echo `pwd`/build)
endif
# create the build directory if needed, and normalize its path name
BUILD_PREFIX:=$(shell mkdir -p $(BUILD_PREFIX) && cd $(BUILD_PREFIX) && echo `pwd`)

# Default to a release build.  If you want to enable debugging flags, run
# "make BUILD_TYPE=Debug"
ifeq "$(BUILD_TYPE)" ""
BUILD_TYPE="Release"
endif

all: pod-build/Makefile
	$(MAKE) -C pod-build all install

pod-build/Makefile:
	$(MAKE) configure

.PHONY: configure
configure: jsoncpp-src-0.6.0-rc2/dist/jsoncpp.cpp
	@echo "\nBUILD_PREFIX: $(BUILD_PREFIX)\n\n"

	# create the temporary build directory if needed
	@mkdir -p pod-build

	# run CMake to generate and configure the build scripts
	@cd pod-build && cmake -DCMAKE_INSTALL_PREFIX=$(BUILD_PREFIX) \
		   -DCMAKE_BUILD_TYPE=$(BUILD_TYPE) ..

jsoncpp-src-0.6.0-rc2/dist/jsoncpp.cpp: jsoncpp-fetch-and-make
	@echo "\nFetched JSONCpp source and made amalgam\n"

jsoncpp-fetch-and-make:
	@echo "\n fetching JSONCpp (and SCons-Local) \n"

	# grab jsoncpp source
	wget -O jsoncpp-0.6.0.tar.gz "http://downloads.sourceforge.net/project/jsoncpp/jsoncpp/0.6.0-rc2/jsoncpp-src-0.6.0-rc2.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fjsoncpp%2Ffiles%2Fjsoncpp%2F0.6.0-rc2%2F"

	# untar sources
	tar xvzf jsoncpp-0.6.0.tar.gz

	# grab scons-local 1.2.0 source and untar it
	cd jsoncpp-src-0.6.0-rc2 && wget -O scons-local-1.2.0.tar.gz "http://downloads.sourceforge.net/project/scons/scons-local/1.2.0/scons-local-1.2.0.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fscons%2Ffiles%2Fscons-local%2F1.2.0%2F"
	cd jsoncpp-src-0.6.0-rc2 && tar xvzf scons-local-1.2.0.tar.gz

	# ok, make using scons
	cd jsoncpp-src-0.6.0-rc2 && python scons.py platform=linux-gcc check

	# grrrrr, fix stupid bug in amalgamate.poy and then use it
	# really, why are paths *incorrectly* harcoded you say? testing perhaps?
	sed 's/json\\json/json\/json/' jsoncpp-src-0.6.0-rc2/amalgamate.py >jsoncpp-src-0.6.0-rc2/amalgamate.py.2
	mv jsoncpp-src-0.6.0-rc2/amalgamate.py.2 jsoncpp-src-0.6.0-rc2/amalgamate.py
	cd jsoncpp-src-0.6.0-rc2 && python amalgamate.py

	touch jsoncpp-src-0.6.0-rc2/dist/jsoncpp.cpp

clean:
	-if [ -e pod-build/install_manifest.txt ]; then rm -f `cat pod-build/install_manifest.txt`; fi
	-if [ -d pod-build ]; then $(MAKE) -C pod-build clean; rm -rf pod-build; fi
	rm -f jsoncpp-0.6.0.tar.gz
	rm -rf jsoncpp-src-0.6.0-rc2/
	rm -f dist


# other (custom) targets are passed through to the cmake-generated Makefile 
%::
	$(MAKE) -C pod-build $@
