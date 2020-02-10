#!/usr/bin/env bash
set -ef -o pipefail

description() {
  echo "Description: Searches a BASE_DIRECTORY for all directories matching the WORKING_DIRECTORY_NAME";
  echo "             and then builds and returns a list of options to be added to a buildkite block";
  echo "             step select field";
}

usage() {
  echo "Usage: $0 <BASE_DIRECTORY> <WORKING_DIRECTORY_NAME> <INDENTATION>"
}

if [ $# -lt 3 ]; then
  echo "ERROR: Not enough arguments"
  description
  usage
  exit 1
fi

BASE_DIRECTORY=$1
WORKING_DIRECTORY_NAME=$2
INDENTATION=$3

FILEPATHS=$(find $BASE_DIRECTORY -type f -path "*\/${WORKING_DIRECTORY_NAME}\/*\.yml" | sort --unique --reverse)

for FILEPATH in $FILEPATHS; do
    FILENAME=$(basename -- $FILEPATH)
    FILENAME_NO_EXTENSION="${FILENAME%.*}"
    LABEL=$(echo $FILENAME_NO_EXTENSION | sed -e 's/[-_]/ /g')
    echo "${INDENTATION}- label: ${LABEL}"
    echo "${INDENTATION}  value: ${FILEPATH}"
done
