#!/bin/bash
set -ef -o pipefail

usage() {
  echo "Usage: $0 <RELEASE_PATH_DIRS> <COMMAND>"
}

if [ $# -lt 2 ]; then
  echo "ERROR: Not enough arguments"
  usage
  exit 1
fi

RELEASE_PATH_DIRECTORIES=$1
shift 1
COMMAND=$@
REPO_NAME=011034713097.dkr.ecr.ap-southeast-2.amazonaws.com/forms-engine-cli

$(aws ecr get-login --registry-ids 011034713097 --no-include-email)
docker pull $REPO_NAME

for RELEASE_PATH_DIR in $RELEASE_PATH_DIRECTORIES; do
  if [ ! -f "`pwd`/$RELEASE_PATH_DIR" ]; then
    echo "ERROR: $RELEASE_PATH_DIR does not exist"
    usage
    exit 1
  fi

  docker run -e FORMS_ENGINE_CLIENT_SECRET="$FORMS_ENGINE_CLIENT_SECRET" -e FORMS_ENGINE_CLIENT_ID="$FORMS_ENGINE_CLIENT_ID" -v `pwd`:/rules -it --rm $REPO_NAME $COMMAND $RELEASE_PATH_DIR
done