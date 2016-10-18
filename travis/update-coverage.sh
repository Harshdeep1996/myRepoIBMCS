#!/bin/bash

[ "$TRAVIS_PULL_REQUEST" == "false" ] || ( echo "Nothing to do" && exit 0 )
[ "$ACTION" != "test-reports" ] && echo "Nothing to do" && exit 0

git clone --quiet git@github.ibm.com:cloudant/travis-tools.git travis-tools > /dev/null
./travis-tools/publish-coverage.sh reports/html cloudant-compliance-checks
