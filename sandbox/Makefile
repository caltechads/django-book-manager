VERSION = 0.3.2

PACKAGE = book_manager_demo

.PHONY: clean dist build force-build tag dev dev-detached devup devdown logall log exec restart docker-clean docker-destroy-db docker-destroy list
#======================================================================

clean:
	rm -rf *.tar.gz dist *.egg-info *.rpm
	find . -name "*.pyc" -exec rm '{}' ';'

dist: clean
	@python setup.py sdist

package:
	(cd ..; python setup.py sdist)
	cp ../dist/django-book-manager-${VERSION}.tar.gz django-book-manager.tar.gz

build: package
	docker build -t ${PACKAGE}:${VERSION} .
	docker tag ${PACKAGE}:${VERSION} ${PACKAGE}:latest
	docker image prune -f

force-build:
	docker build --no-cache -t ${PACKAGE}:${VERSION} .
	docker tag ${PACKAGE}:${VERSION} ${PACKAGE}:latest
	docker image prune -f

tag:
	docker tag ${PACKAGE}:${VERSION} ${DOCKER_REGISTRY}/${PACKAGE}:${VERSION}
	docker tag ${PACKAGE}:latest ${DOCKER_REGISTRY}/${PACKAGE}:latest

dev:
	docker-compose up

dev-detached:
	docker-compose up -d

devup: dev-detached

devdown:
	docker-compose down

logall:
	docker-compose logs -f

log:
	docker logs -f book_manager_demo

exec:
	docker exec -it book_manager_demo /bin/bash

restart:
	docker-compose restart book_manager_demo

docker-clean:
	docker stop $(shell docker ps -a -q)
	docker rm $(shell docker ps -a -q)

docker-destroy-db:
	rm -Rf sql/docker/mysql-data/

docker-destroy: docker-clean docker-destroy-db
	docker rmi -f $(shell docker images -q | uniq)
	docker image prune -f; docker volume prune -f; docker container prune -f

list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs
