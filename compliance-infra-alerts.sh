#!/bin/bash

if [ $TRAVIS_TEST_RESULT = 0 ];then 
	color="#ff0000"; 
elif [ $TRAVIS_TEST_RESULT = 1 ];then
    color="#00ff00";
else
	color="#e8ba59";
fi

curl -s -X POST -H 'Content-type: application/json' -d \
'{"channel":"@harshdeep.harshdeep", "attachments": [{ "color": $color, "text": "Build $TRAVIS_BUILD_ID ($TRAVIS_COMMIT) of $TRAVIS_REPO_SLUG@TRAVIS_BRANCH" by Bot}], "username": "Travis CI", "icon_emoji": ":travis_ci:"}' \
"https://hooks.slack.com/services/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"
