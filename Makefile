# images
IMAGE_PUBLIC_REGISTRY = alfss
IMAGE_NAME = homeassistant-daichi-cloud-climate-provider

# get current tag
GIT_TAG := $(shell git describe --tags --exact-match 2>/dev/null || echo "")

# set default value YYYYMMDD if this not git tag
ifeq ($(GIT_TAG),)
    TAG := $(shell date +%Y%m%d)
else
    TAG := $(GIT_TAG)
endif

.PHONY: build

# Make and publish
build_for_public:
	podman build -t $(IMAGE_PUBLIC_REGISTRY)/$(IMAGE_NAME):$(TAG) .

publish_public:
	podman push $(IMAGE_PUBLIC_REGISTRY)/$(IMAGE_NAME):$(TAG)

print_tag:
	@echo "Docker image tag: $(TAG)"
