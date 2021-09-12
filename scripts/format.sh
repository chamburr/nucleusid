#!/bin/bash

echo "Formatting..."
poetry run poe format
yarn format
