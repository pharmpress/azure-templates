#!/usr/bin/env bash

azure group deployment create -f trafficmanager.json -e trafficmanager.parameters.json -g cloud66 rpsTrafficDeployment

