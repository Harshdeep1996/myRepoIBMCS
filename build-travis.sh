#!/bin/bash

if [ -z "$TRAVIS_COMMIT_RANGE" ]; then
    echo "it is working"
else
    echo "it is not working"
fi
