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

all: pod-build/Makefile jsoncpp-fetch-and-make
	$(MAKE) -C pod-build all install

pod-build/Makefile:
	$(MAKE) configure

.PHONY: configure
configure:
	@echo "\nBUILD_PREFIX: $(BUILD_PREFIX)\n\n"

	# create the temporary build directory if needed
	@mkdir -p pod-build

	# run CMake to generate and configure the build scripts
	@cd pod-build && cmake -DCMAKE_INSTALL_PREFIX=$(BUILD_PREFIX) \
		   -DCMAKE_BUILD_TYPE=$(BUILD_TYPE) ..


jsoncpp-fetch-and-make:
	@echo "\n fetching JSONCpp (and SCons-Local) \n"

	# grab jsoncpp source
	wget -O jsoncpp-0.5.0.tar.gz "http://downloads.sourceforge.net/project/jsoncpp/jsoncpp/0.5.0/jsoncpp-src-0.5.0.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fjsoncpp%2Ffiles%2Fjsoncpp%2F0.5.0%2F"


	# untar sources
	tar xvzf jsoncpp-0.5.0.tar.gz

	# grab scons-local 1.2.0 source and untar it
	cd jsoncpp-src-0.5.0 && wget -O scons-local-1.2.0.tar.gz "http://downloads.sourceforge.net/project/scons/scons-local/1.2.0/scons-local-1.2.0.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fscons%2Ffiles%2Fscons-local%2F1.2.0%2F"
	cd jsoncpp-src-0.5.0 && tar xvzf scons-local-1.2.0.tar.gz

	# ok, make using scons
	cd jsoncpp-src-0.5.0 && python scons.py platform=linux-gcc check
	cd jsoncpp-src-0.5.0 && python amalganate.py

clean:
	-if [ -e pod-build/install_manifest.txt ]; then rm -f `cat pod-build/install_manifest.txt`; fi
	-if [ -d pod-build ]; then $(MAKE) -C pod-build clean; rm -rf pod-build; fi

# other (custom) targets are passed through to the cmake-generated Makefile 
%::
	$(MAKE) -C pod-build $@
