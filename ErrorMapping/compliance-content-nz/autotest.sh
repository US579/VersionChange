#!/bin/sh

set -ef -o pipefail
usage() {
  path=`pwd`
  echo "Usage: sh $0 $path"
}

if [ $# -ne 1 ];
then
  usage
  exit 1
fi

BASE_DIRECTORY=$1

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
array=${WORKING_DIRECTORIES[@]}

dir=("Returns" "Schedules")
for name in ${dir[*]};do
  WORKING_DIRECTORIES=$(find ${BASE_DIRECTORY} -iname "${name}" -d)
  array=${WORKING_DIRECTORIES[@]}
    for i in $array;do
      cd $i
      pwd
       fe upload -a 
      # forms-engine validate
      cd - > /dev/null
    done
done

