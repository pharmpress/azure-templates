#!/usr/bin/env bash

azure group template validate -vv --json -f azuredeploy.json -e azuredeploy.parameters.json -g cloud66 | grep -A 20  "silly: returnObject" | sed '1d' | jq -r '.body' | jq '.' > generated.json

