#!/bin/bash
set -ef -o pipefail

DECLARATION_FILE=$(grep "declarationFileName" "$(pwd)/Forms/$1" || true)

if [ -z "$DECLARATION_FILE" ]; then
  FILENAME="ir4.html"
else
  FILENAME=$(echo "$DECLARATION_FILE" | sed 's/.*:[^A-Za-z]*\([A-Za-z.]*\)[^A-Za-z]*/\1/')
fi

aws s3 cp "$(pwd)/Declarations/$FILENAME" s3://compliance-content-nz-declarations-templates
