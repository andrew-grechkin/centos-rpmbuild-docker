THIS_FILE     := $(abspath $(firstword $(MAKEFILE_LIST)))
THIS_DIR      := $(dir $(THIS_FILE))
GIT_REPO      := $(shell git config --file $(THIS_DIR)/.git/config --get remote.origin.url)
GIT_REPO_NAME := $(shell basename -s .git $(GIT_REPO))

IGNORE_RPATH_ERRORS = $(shell echo $$[ 0x0001|0x0020 ])

BUILD_MAKEFILE  = $(THIS_DIR)/docker/override/etc/skel/build/Makefile
IMAGE8          = cos8-rpm-build
IMAGE8_DUMMY    = /tmp/dummy-image-$(GIT_REPO_NAME)-build8
IMAGE9          = cos9-rpm-build
IMAGE9_DUMMY    = /tmp/dummy-image-$(GIT_REPO_NAME)-build9
NPROC          := $(shell nproc)
SIGN_SCRIPT     = $(THIS_DIR)/docker/override/etc/skel/build/sign-rpms
USER_HOME       = /home/$(USER_NAME)
USER_NAME       = builder
USER_UID       := $(shell id -u)

export PODMAN_USERNS=keep-id

$(IMAGE8_DUMMY): $(THIS_FILE) $(BUILD_MAKEFILE) $(THIS_DIR)/docker/Dockerfile-8-stream $(SIGN_SCRIPT)
	@echo "> Preparing docker centos-8-stream image..."
	@docker build                             \
		--build-arg USER_NAME=$(USER_NAME)    \
		--build-arg USER_UID=$(USER_UID)      \
	-t $(IMAGE8)                              \
	-f $(THIS_DIR)/docker/Dockerfile-8-stream \
	$(THIS_DIR)/docker
	@touch $@

$(IMAGE9_DUMMY): $(THIS_FILE) $(BUILD_MAKEFILE) $(THIS_DIR)/docker/Dockerfile-9-stream $(SIGN_SCRIPT)
	@echo "> Preparing docker centos-9-stream image..."
	@docker build                             \
		--build-arg USER_NAME=$(USER_NAME)    \
		--build-arg USER_UID=$(USER_UID)      \
	-t $(IMAGE9)                              \
	-f $(THIS_DIR)/docker/Dockerfile-9-stream \
	$(THIS_DIR)/docker
	@touch $@

$(PWD)/.rpmbuild:
	@mkdir -p $@/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

.PHONY: build8 build8-from-source build9 run8 run9 run-home sign sign-helper

# export GPG_KEY_ID=
# sign-help%: export GPG_PRIV_KEY_BASE64=$(shell gpg --export-secret-keys $(GPG_KEY_ID) | base64 -w 0)
sign-helper:
	@docker run --rm -it --privileged               \
		-h 8-stream-$(USER_NAME)                    \
		-e GPG_PRIV_KEY_ID                          \
		-e GPG_PRIV_KEY_BASE64                      \
		-e TERM=xterm-256color                      \
		-v $(PWD)/.rpmbuild:$(USER_HOME)/rpmbuild   \
		-v $(PWD):$(USER_HOME)/mnt:ro               \
		$(IMAGE8)                                   \
		make -f $(USER_HOME)/build/Makefile sign

sign: $(IMAGE8_DUMMY) $(PWD)/.rpmbuild sign-helper

build8: $(IMAGE8_DUMMY) $(PWD)/.rpmbuild
	@docker run --rm -it --privileged               \
		--cpus="$$(( $(NPROC) - 2 ))"               \
		-h 8-stream-$(USER_NAME)                    \
		-e GPG_PRIV_KEY_ID                          \
		-e GPG_PRIV_KEY_BASE64                      \
		-e TERM=xterm-256color                      \
		-e QA_RPATHS=$(IGNORE_RPATH_ERRORS)         \
		-v $(PWD)/.rpmbuild:$(USER_HOME)/rpmbuild   \
		-v $(PWD):$(USER_HOME)/mnt:ro               \
		-w $(USER_HOME)/mnt                         \
		$(IMAGE8)                                   \
		make -f $(USER_HOME)/build/Makefile build

build8-from-source: $(IMAGE8_DUMMY) $(PWD)/.rpmbuild
	@cp -f *.src.rpm $(PWD)/.rpmbuild/SRPMS/
	@docker run --rm -it --privileged               \
		--cpus="$$(( $(NPROC) - 2 ))"               \
		-h 8-stream-$(USER_NAME)                    \
		-e GPG_PRIV_KEY_ID                          \
		-e GPG_PRIV_KEY_BASE64                      \
		-e TERM=xterm-256color                      \
		-e QA_RPATHS=$(IGNORE_RPATH_ERRORS)         \
		-v $(PWD)/.rpmbuild:$(USER_HOME)/rpmbuild   \
		-v $(PWD):$(USER_HOME)/mnt:ro               \
		-w $(USER_HOME)/mnt                         \
		$(IMAGE8)                                   \
		make -f $(USER_HOME)/build/Makefile build-from-source

build9: $(IMAGE9_DUMMY) $(PWD)/.rpmbuild
	@docker run --rm -it --privileged               \
		--cpus="$$(( $(NPROC) - 2 ))"               \
		-h 9-stream-$(USER_NAME)                    \
		-e GPG_PRIV_KEY_ID                          \
		-e GPG_PRIV_KEY_BASE64                      \
		-e TERM=xterm-256color                      \
		-e QA_RPATHS=$(IGNORE_RPATH_ERRORS)         \
		-v $(PWD)/.rpmbuild:$(USER_HOME)/rpmbuild   \
		-v $(PWD):$(USER_HOME)/mnt:ro               \
		-w $(USER_HOME)/mnt                         \
		$(IMAGE9)                                   \
		make -f $(USER_HOME)/build/Makefile build

run8: $(IMAGE8_DUMMY)
	@docker run --rm -it --privileged               \
		--cpus="$$(( $(NPROC) - 2 ))"               \
		-h 8-stream-$(USER_NAME)                    \
		-e TERM=xterm-256color                      \
		-v /media/nfs/home/public/rpm:/rpm          \
		-v $(PWD):$(USER_HOME)/mnt:ro               \
		$(IMAGE8)

run9: $(IMAGE9_DUMMY)
	@docker run --rm -it --privileged               \
		--cpus="$$(( $(NPROC) - 2 ))"               \
		-h 9-stream-$(USER_NAME)                    \
		-e TERM=xterm-256color                      \
		-v /media/nfs/home/public/rpm:/rpm          \
		-v $(PWD):$(USER_HOME)/mnt:ro               \
		$(IMAGE9)

run-home: $(IMAGE9_DUMMY)
	@sudo docker run --rm -it                       \
		-h 9-stream-$(USER_NAME)                    \
		-e TERM=xterm-256color                      \
		-v /volume1/public/rpm:/rpm                 \
		$(IMAGE9)
