#!/bin/bash
echo "setting shell as environment variables for pygeoapi"

export PYGEOAPI_CONFIG=example-config.yml
echo "PYGEOAPI_CONFIG set to: $PYGEOAPI_CONFIG"

export PYGEOAPI_OPENAPI=example-openapi.yml
echo "PYGEOAPI_OPENAPI set to: $PYGEOAPI_OPENAPI"