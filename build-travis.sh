#!/bin/bash

if [ "${TRAVIS_EVENT_TYPE}" == "api" ]; then 
    echo "It is working" 
 else
    echo "It is not working"
fi