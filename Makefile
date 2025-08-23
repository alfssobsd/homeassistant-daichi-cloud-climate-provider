# Имя образа
IMAGE_REGISTRY = cr.yandex/crpt6a9sphouc986n0ji
IMAGE_NAME = homeassistant-daichi-cloud-climate-provider

# Получить последний git tag или пустую строку
GIT_TAG := $(shell git describe --tags --exact-match 2>/dev/null || echo "")

# Если GIT_TAG пустой, ставим дату YYYYMMDD
ifeq ($(GIT_TAG),)
    TAG := $(shell date +%Y%m%d)
else
    TAG := $(GIT_TAG)
endif

.PHONY: build

build:
	docker build -t $(IMAGE_REGISTRY)/$(IMAGE_NAME):$(TAG) .

build_podman:
	podman build -t $(IMAGE_REGISTRY)/$(IMAGE_NAME):$(TAG) .

print-tag:
	@echo "Docker image tag: $(TAG)"
