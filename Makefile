.PHONY: build-de

build-de:
	ansible-builder build -v3 -t quay.io/mancubus77/de -f de.yml
