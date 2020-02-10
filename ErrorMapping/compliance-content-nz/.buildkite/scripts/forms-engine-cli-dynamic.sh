#!/usr/bin/env bash
set -ef -o pipefail

description() {
  echo "Description: Searches a BASE_DIRECTORY for all directories matching the WORKING_DIRECTORY_NAME";
  echo "             and then calls the Forms Engine CLI with the given command for each working directory.";
}

usage() {
  echo "Usage: $0 <BASE_DIRECTORY> <WORKING_DIRECTORY_NAME> <COMMAND>"
}

if [ $# -lt 3 ]; then
  echo "ERROR: Not enough arguments"
  description
  usage
  exit 1
fi

BASE_DIRECTORY=$1
WORKING_DIRECTORY_NAME=$2
shift 2
COMMAND=$@

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
WORKING_DIRECTORIES=$(find ${BASE_DIRECTORY} -iname "${WORKING_DIRECTORY_NAME}" -d)

for WORKING_DIRECTORY in $WORKING_DIRECTORIES; do
  ${DIR}/forms-engine-cli.sh $WORKING_DIRECTORY $COMMAND;
done
