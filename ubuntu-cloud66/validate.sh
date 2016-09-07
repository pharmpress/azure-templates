#!/usr/bin/env bash

TEMPLATE=${1:-azuredeploy}

azure group template validate -vv --json -f "${TEMPLATE}.json" -e "${TEMPLATE}.parameters.json" -g cloud66 | grep -A 20  "silly: returnObject" | sed '1d' | jq -r '.body' | jq '.' > generated.json

