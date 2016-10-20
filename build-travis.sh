#!/bin/bash

if [ "${TRAVIS_BRANCH}" == "test-branch" ]; then 
	echo "It is working" ; 
else
	echo "It is not working";
fi