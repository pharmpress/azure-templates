#!/usr/bin/env bash

azure group deployment create -f azuredeploy.json -e azuredeploy.parameters.json -g cloud66 rpsDeployment

