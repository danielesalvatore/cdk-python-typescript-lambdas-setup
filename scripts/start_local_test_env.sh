#!/bin/sh

# Synth CDK template and simulate CI execution
CI=true cdk synth --no-staging > template.yaml

# Start local server to test lambda
sam local start-api --skip-pull-image --warm-containers LAZY 2>&1 | tr "\r" "\n"