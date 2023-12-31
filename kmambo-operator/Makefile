VERSION=$(shell grep ^version pyproject.toml | gawk -F"[= ]" '{print $$NF}' | tr -d '"')
NAME=$(shell grep ^name pyproject.toml | gawk -F"[= ]" '{print $$NF}' | tr -d '"')
DOCKER=docker
REMOTE_DOCKER_NAME=kmambo-operator
REMOTE_DOCKER_REPO=pbhowmic

requirements.txt: poetry.lock
	poetry export -f requirements.txt --without-hashes \
		--without dev --output requirements.txt

poetry.lock: pyproject.toml
	poetry lock --no-update

.PHONY: image lint tag undeploy undeploy

image: requirements.txt Dockerfile
	$(DOCKER) build -f Dockerfile -t $(NAME):$(VERSION) .

tag: image
	$(DOCKER) tag $(NAME):$(VERSION) $(REMOTE_DOCKER_REPO)/$(REMOTE_DOCKER_NAME):$(VERSION)

lint:
	isort src/kmambo
	black src/kmambo
	flake8 src/kmambo
	mypy src/kmambo

deploy:
	helm install kmambo-operatory-py kmambo-operator-chart --namespace kmambo-ns --create-namespace

undeploy:
	helm uninstall  kmambo-operatory-py -n kmambo-ns
