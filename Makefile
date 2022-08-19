BUILD_MAKEFILE = $(THIS_DIR)/docker/override/etc/skel/build/Makefile
GIT_REPO       = $(shell git config --file $(THIS_DIR)/.git/config --get remote.origin.url)
GIT_REPO_NAME  = $(shell basename -s .git $(GIT_REPO))
IMAGE8         = cos8-repo-sync
IMAGE8_DUMMY   = /tmp/dummy-image-$(GIT_REPO_NAME)-build8
IMAGE9         = cos9-repo-sync
IMAGE9_DUMMY   = /tmp/dummy-image-$(GIT_REPO_NAME)-build9
THIS_DIR       = $(dir $(THIS_FILE))
THIS_FILE      = $(abspath $(firstword $(MAKEFILE_LIST)))
USER_HOME      = /home/$(USER_NAME)
USER_NAME      = builder
USER_UID       = $(shell id -u)

$(IMAGE8_DUMMY): $(THIS_FILE) $(BUILD_MAKEFILE) $(THIS_DIR)/docker/Dockerfile-8-stream
	@docker build                             \
		--build-arg USER_NAME=$(USER_NAME)    \
		--build-arg USER_UID=$(USER_UID)      \
	-t $(IMAGE8)                              \
	-f $(THIS_DIR)/docker/Dockerfile-8-stream \
	$(THIS_DIR)/docker
	@touch $@

$(IMAGE9_DUMMY): $(THIS_FILE) $(BUILD_MAKEFILE) $(THIS_DIR)/docker/Dockerfile-9-stream
	@docker build                             \
		--build-arg USER_NAME=$(USER_NAME)    \
		--build-arg USER_UID=$(USER_UID)      \
	-t $(IMAGE9)                              \
	-f $(THIS_DIR)/docker/Dockerfile-9-stream \
	$(THIS_DIR)/docker
	@touch $@

$(PWD)/.rpmbuild:
	@mkdir -p $@/{BUILD,BUILDROOT,SOURCES,SPECS,SRPMS} $@/RPMS/{noarch,x86_64,arm}
	@chmod -R g+rs,a+wX $@ || true

.PHONY: build8 build9 run8 run9 run-home

build8: $(IMAGE8_DUMMY) $(PWD)/.rpmbuild
	@docker run --rm -it --privileged               \
		-h 8-stream-$(USER_NAME)                    \
		-e TERM=xterm-256color                      \
		-v $(PWD)/.rpmbuild:$(USER_HOME)/rpmbuild   \
		-v $(PWD):$(USER_HOME)/mnt:ro               \
		-w $(USER_HOME)/mnt                         \
		$(IMAGE8)                                   \
		make -f $(USER_HOME)/build/Makefile build

build8-from-source: $(IMAGE8_DUMMY) $(PWD)/.rpmbuild
	@cp -f *.src.rpm $(PWD)/.rpmbuild/SRPMS/
	@docker run --rm -it --privileged               \
		-h 8-stream-$(USER_NAME)                    \
		-e TERM=xterm-256color                      \
		-v $(PWD)/.rpmbuild:$(USER_HOME)/rpmbuild   \
		-v $(PWD):$(USER_HOME)/mnt:ro               \
		-w $(USER_HOME)/mnt                         \
		$(IMAGE8)                                   \
		make -f $(USER_HOME)/build/Makefile build-from-source

build9: $(IMAGE9_DUMMY) $(PWD)/.rpmbuild
	@docker run --rm -it --privileged               \
		-h 9-stream-$(USER_NAME)                    \
		-e TERM=xterm-256color                      \
		-v $(PWD)/.rpmbuild:$(USER_HOME)/rpmbuild   \
		-v $(PWD):$(USER_HOME)/mnt:ro               \
		-w $(USER_HOME)/mnt                         \
		$(IMAGE9)                                   \
		make -f $(USER_HOME)/build/Makefile build

run8: $(IMAGE8_DUMMY)
	@docker run --rm -it --privileged      \
		-h 8-stream-$(USER_NAME)           \
		-e TERM=xterm-256color             \
		-v /media/nfs/home/public/rpm:/rpm \
		-v $(PWD):$(USER_HOME)/mnt:ro      \
		$(IMAGE8)

run9: $(IMAGE9_DUMMY)
	@docker run --rm -it --privileged      \
		-h 9-stream-$(USER_NAME)           \
		-e TERM=xterm-256color             \
		-v /media/nfs/home/public/rpm:/rpm \
		-v $(PWD):$(USER_HOME)/mnt:ro      \
		$(IMAGE9)

run-home: $(IMAGE9_DUMMY)
	@sudo docker run --rm -it       \
		-h 9-stream-$(USER_NAME)    \
		-e TERM=xterm-256color      \
		-v /volume1/public/rpm:/rpm \
		$(IMAGE9)
