#!/bin/bash

# Build zip
rm -f build.zip
zip -r build.zip environment.yml saliencyservice Dockerfile .ebextensions

# Deploy to EB
eb deploy
