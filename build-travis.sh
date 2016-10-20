#!/bin/bash

if [ "${TRAVIS_BRANCH}" == "test-branch" ]; then 
	echo "It is working" ; 
else
	echo ${TRAVIS_BRANCH}
	echo "It is not working";
fi