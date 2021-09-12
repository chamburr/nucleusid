#!/bin/bash

echo "Linting..."
poetry run poe lint
yarn lint
