.DEFAULT_GOAL   := build
OS_RELEASE      := $(shell rpm --eval '%{centos_ver}')
RPMBUILD_FOLDER := $(HOME)/rpmbuild

.PHONY:                \
	build              \
	build-bin-8        \
	build-bin-9        \
	build-install-deps \
	build-mock         \
	build-src          \
	expose             \
	lint

$(RPMBUILD_FOLDER):
	@rpmdev-setuptree

inst-devel:
	dnf group install -y 'Development Tools'
	dnf install -y sqlite
	dnf install -y rpm-build rpm-devel rpmlint mock coreutils rpmdevtools python

lint: $(RPMBUILD_FOLDER)
	@echo 'Linting...'
	@rpmlint *.spec

build-src:
	@echo
	@echo 'Building source RPMs...'
	@cp -f * $(RPMBUILD_FOLDER)/SOURCES || true
	@rpmbuild --undefine=_disable_source_fetch -bs *.spec

build-install-deps:
	@echo
	@echo 'Installing dependencies...'
	@sudo yum-builddep -y $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm

build-from-source: build-install-deps
	@echo
	@echo 'Building RPMs...'
	@QA_CHECK_RPATHS=0 rpmbuild --noclean -rb $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm
	@chmod -R a+wX "$(HOME)"/rpmbuild || true
	@echo
	@tree "$(HOME)"/rpmbuild
	@echo

build: lint build-src build-from-source sign

#@rpmbuild -rb $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm
# spectool -g -R *.spec
# @sudo dnf builddep -y $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm

build-mock: lint build-src
	@mock -r centos-stream-$(OS_RELEASE)-x86_64 --rebuild --resultdir=~/rpmbuild/RPMS/ $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm

build-bin-8: lint build-src
	@mock -r centos-stream-8-x86_64 --rebuild --resultdir=~/rpmbuild/RPMS/ $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm

build-bin-9: lint build-src
	@mock -r centos-stream-9-x86_64 --rebuild --resultdir=~/rpmbuild/RPMS/ $(RPMBUILD_FOLDER)/SRPMS/*.el$(OS_RELEASE).src.rpm

expose:
	sudo cp -rf ~/rpmbuild/RPMS/*.rpm  /srv/http/local/RPMS
	sudo cp -rf ~/rpmbuild/SRPMS/*.rpm /srv/http/local/SRPMS
	sudo createrepo --update /srv/http/local/RPMS
	sudo createrepo --update /srv/http/local/SRPMS

sign:
	@$(HOME)/build/sign-rpms
