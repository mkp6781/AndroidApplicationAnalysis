#!/bin/sh

set -xe

sudo docker run -it --rm -p 8000:8000 -p 1337:1337 -e MOBSF_ANALYZER_IDENTIFIER=127.0.0.1:6555 -e MOBSF_PLATFORM="some" --network="host" opensecurity/mobile-security-framework-mobsf:latest