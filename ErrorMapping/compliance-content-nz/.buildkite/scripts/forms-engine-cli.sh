#!/bin/bash
set -ef -o pipefail

usage() {
  echo "Usage: $0 <MODEL_DIR_PATH> <COMMAND>"
}

if [ $# -lt 2 ]; then
  echo "ERROR: Not enough arguments"
  usage
  exit 1
fi

MODEL_DIR_PATH=$1
shift 1
COMMAND=$@
REPO_NAME=011034713097.dkr.ecr.ap-southeast-2.amazonaws.com/forms-engine-cli

if [ ! -d "$MODEL_DIR_PATH" ]; then
  echo "ERROR: $MODEL_DIR_PATH does not exist"
  usage
  exit 1
fi

$(aws ecr get-login --registry-ids 011034713097 --no-include-email)
docker pull $REPO_NAME
docker run -e FORMS_ENGINE_CLIENT_SECRET="$FORMS_ENGINE_CLIENT_SECRET" -e FORMS_ENGINE_CLIENT_ID="$FORMS_ENGINE_CLIENT_ID" -v `pwd`:/rules -it --rm $REPO_NAME -w $MODEL_DIR_PATH $COMMAND

