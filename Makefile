.PHONY: build
.PHONY: repo_add
.PHONY: changelog

build:
	docker build -t python-deb-builder .
	docker run -v `pwd`:/code -it python-deb-builder /build_in_docker.sh

repo_add: build
	add_to_repo_target.sh

changelog:
	dch -m -U
