# Default pod makefile distributed with pods version: 12.09.21

FETCH_URL="https://www.openssl.org/source/openssl-1.0.1e.tar.gz"
POD_NAME="openssl-1.0.1e"

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
configure: pkgconfiged.touch
	@echo "\nBUILD_PREFIX: $(BUILD_PREFIX)\n\n"

	# create the temporary build directory if needed
	@mkdir -p pod-build

	# run CMake to generate and configure the build scripts
	@cd pod-build && cmake -DCMAKE_INSTALL_PREFIX=$(BUILD_PREFIX) \
		   -DCMAKE_BUILD_TYPE=$(BUILD_TYPE) ..


fetched.touch:
	$(MAKE) fetch

unarchived.touch: fetched.touch
	$(MAKE) unarchive

built.touch: unarchived.touch
	$(MAKE) build-source

installed.touch: built.touch
	$(MAKE) install-source

pkgconfiged.touch: installed.touch
	$(MAKE) pkgconfig-source

fetch:
	@echo "\n Fetching $(POD_NAME) from $(FETCH_URL) \n"
	wget -O $(POD_NAME).tar.gz $(FETCH_URL)
	@touch fetched.touch

unarchive:
	@echo "\n UnArchiving $(POD_NAME) \n"
	@tar xzf $(POD_NAME).tar.gz
	@touch unarchived.touch

build-source:
	@echo "\n Building $(POD_NAME) \n"
	@mkdir -p pod_build
	cd $(POD_NAME) && ./config --prefix=$(BUILD_PREFIX)
	cd $(POD_NAME) && make
	@touch built.touch

install-source:
	@echo "\n Installing $(POD_NAME) \n"
	cd $(POD_NAME) && make install
	@touch installed.touch

pkgconfig-source:
	@echo "\n Creating pkg-config files for $(POD_NAME) \n"
	cp $(BUILD_PREFIX)/lib/pkgconfig/openssl.pc $(BUILD_PREFIX)/lib/pkgconfig/$(POD_NAME).pc
	@touch pkgconfiged.touch



clean:
	-if [ -e pod-build/install_manifest.txt ]; then rm -f `cat pod-build/install_manifest.txt`; fi
	-if [ -d pod-build ]; then $(MAKE) -C pod-build clean; rm -rf pod-build; fi
	rm -rf $(POD_NAME)
	rm unarchived.touch built.touch installed.touch pkgconfiged.touch

# other (custom) targets are passed through to the cmake-generated Makefile 
%::
	$(MAKE) -C pod-build $@
