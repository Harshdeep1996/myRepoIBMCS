#!/bin/bash

[ "$TRAVIS_PULL_REQUEST" == "false" ] || ( echo "Nothing to do" && exit 0 )
[ "$TRAVIS_BRANCH" != "master" ] && echo "Nothing to do" && exit 0


MAX_TRIES=3
HTML_DIR="doc/_build/html"
REPO_NAME="CloudDataServices/cloudant-compliance-checks"
GH_HOST="github.ibm.com"
GH_PAGES="git@$GH_HOST:$REPO_NAME.git"
DOC_URL="https://pages.$GH_HOST/$REPO_NAME"

echo -e "Publishing documentation for $REPO_NAME\n"

cp -R $HTML_DIR/* $HOME/html
touch $HOME/html/.nojekyll
cd $HOME
git config --global user.email "cldinfra@us.ibm.com"
git config --global user.name "Cloudant Service"

# This primitive mechanism of polling git pushes prevents to have race
# conditions with other travis jobs. This could be done much better
# (like creating a branch and merge it using a PR). However, it is
# good for the initial deployment.
tries=0
while true; do
    rm -rf gh-pages
    git clone --quiet --branch=gh-pages $GH_PAGES gh-pages > /dev/null

    cd gh-pages
    cp -Rf $HOME/html/* .

    git add -f .
    git commit -m "doc from build #$TRAVIS_BUILD_NUMBER"
    git push -fq origin gh-pages > /dev/null

    [ $? -eq 0 ] && break	
    [ $tries -gt $MAX_TRIES ] && \
        echo 'Unable to push documentation report after $MAX_TRIES attempts ' && \
        exit 1
    ((tries+=1))
done
echo -e "Documentation published! - $DOC_URL\n"
