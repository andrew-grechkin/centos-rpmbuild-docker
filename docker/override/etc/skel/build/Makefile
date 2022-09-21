OS_RELEASE      := $(shell rpm --eval '%{centos_ver}')
RPMBUILD_FOLDER := $(HOME)/rpmbuild

.DEFAULT_GOAL := build
.PHONY:                \
	build              \
	build-bin-8        \
	build-bin-9        \
	build-from-source  \
	build-install-deps \
	build-mock         \
	build-src          \
	expose             \
	lint               \
	sign

$(RPMBUILD_FOLDER):
	@rpmdev-setuptree

build: lint build-src build-from-source sign

build-bin-8: lint build-src
	@mock -r centos-stream-8-x86_64 --rebuild --resultdir=~/rpmbuild/RPMS/ $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm

build-bin-9: lint build-src
	@mock -r centos-stream-9-x86_64 --rebuild --resultdir=~/rpmbuild/RPMS/ $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm

build-from-source: build-install-deps
	@echo
	@echo '> Building RPMs...'
	@QA_CHECK_RPATHS=0 rpmbuild --noclean -rb $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm
	@chmod -R a+wX "$(HOME)"/rpmbuild || true
	@echo
	@tree "$(HOME)"/rpmbuild
	@echo

#@rpmbuild -rb $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm
# spectool -g -R *.spec
# @sudo dnf builddep -y $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm

build-install-deps:
	@echo
	@echo '> Installing dependencies...'
	@sudo yum-builddep -y $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm

build-mock: lint build-src
	@mock -r centos-stream-$(OS_RELEASE)-x86_64 --rebuild --resultdir=~/rpmbuild/RPMS/ $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm

build-src:
	@echo
	@echo '> Building source RPMs...'
	@cp -f * $(RPMBUILD_FOLDER)/SOURCES || true
	@rpmbuild --undefine=_disable_source_fetch -bs *.spec

expose:
	sudo cp -rf $(RPMBUILD_FOLDER)/RPMS/*.rpm  /srv/http/local/RPMS
	sudo cp -rf $(RPMBUILD_FOLDER)/SRPMS/*.rpm /srv/http/local/SRPMS
	sudo createrepo --update /srv/http/local/RPMS
	sudo createrepo --update /srv/http/local/SRPMS

lint: $(RPMBUILD_FOLDER)
	@echo '> Linting...'
	@rpmlint *.spec

sign:
	@$(HOME)/build/sign-rpms
