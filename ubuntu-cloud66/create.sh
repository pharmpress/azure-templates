#!/usr/bin/env bash

TEMPLATE=${1:-azuredeploy}

azure group deployment create -f "${TEMPLATE}.json" -e "${TEMPLATE}.parameters.json" -g cloud66 rpsDeployment

