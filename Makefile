SHELL := /bin/bash
CWD := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ME := $(shell whoami)

up:
	docker-compose up --remove-orphans --build \
		pii__balancer \
		pii__api__general \
		pii__db__general \
		pii__db__auth \
		pii__api__auth \

drop:
	docker-compose down -v

docker_login_unic_lab:
	docker login gitlab.neroelectronics.by:5050 -u unic_lab_developers -p Vw3o4gBzgH_GGUzFs7NM

fix_own:
	@echo "me: $(ME)"
	sudo chown $(ME):$(ME) -R .

lint:
	./src/bin-lint.sh

cleanup:
	pipenv sync --dev

	# pre-commit
	cp -f "${CWD}/srv/git.hook.pre-commit.sh" "${CWD}/.git/hooks/pre-commit"
	chmod +x "${CWD}/.git/hooks/pre-commit"

	# pre-push
	cp -f "${CWD}/srv/git.hook.pre-push.sh" "${CWD}/.git/hooks/pre-push"
	chmod +x "${CWD}/.git/hooks/pre-push"
######################## SERVICE MANAGER DEVICE DB START ########################

manager__pii_db_general__migrations:
	docker-compose run --rm manager__pii__db__general /docker_app/src/pii__db__general/bin-migrate.sh --migrate

manager__pii_db_general__revision:
	docker-compose run --rm manager__pii__db__general /docker_app/src/pii__db__general/bin-migrate.sh --revision

manager__pii_db_general__init:
	docker-compose run --rm manager__pii__db__general /docker_app/src/pii__db__general/bin-migrate.sh --init

manager__pii_db_general__upgrade:
	docker-compose run --rm manager__pii__db__general /docker_app/src/pii__db__general/bin-migrate.sh --upgrade

manager__pii_db_general__downgrade:
	docker-compose run --rm manager__pii__db__general /docker_app/src/pii__db__general/bin-migrate.sh --downgrade

######################## SERVICE MANAGER DEVICE DB END ########################
