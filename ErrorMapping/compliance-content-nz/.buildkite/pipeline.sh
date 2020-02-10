#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cat << EOF
env:
  SCRIPT_ROOT: ./.buildkite/scripts
  FORMS_ENGINE_CLIENT_ID: compliance-form-content
  COMPLIANCE_CONTENT_NAMESPACE: compliance-content-nz

  TAX_FORMS_NAMESPACE: tax-forms-nz
  WORKPAPERS_NAMESPACE: workpapers-nz

steps:
  - label: 'Validate forms'
    command:
      - \$\$SCRIPT_ROOT/forms-engine-cli-dynamic.sh ./Forms Returns validate
      - \$\$SCRIPT_ROOT/forms-engine-cli-dynamic.sh ./Forms Schedules validate
      - \$\$SCRIPT_ROOT/forms-engine-cli-dynamic.sh ./Forms Workpapers validate
    agents:
      queue: cc-dev-dflt

  - block: ':rocket: Release to SIT'
    branches: master
    fields:
      - select: 'Which release files should be published?'
        key: 'release-files'
        required: true
        multiple: true
        default:
          - compliance ir4 company 2020 nz
        options:
$(${DIR}/scripts/build-release-file-options.sh Forms Releases '          ')
  - label: 'Upload to SIT'
    branches: master
    command:
      - export FORMS_ENGINE_CLIENT_SECRET=\$\$FORMS_ENGINE_CLIENT_SECRET
      - \$\$SCRIPT_ROOT/forms-engine-cli-dynamic.sh ./Forms Returns upload --namespace \$\$TAX_FORMS_NAMESPACE
      - \$\$SCRIPT_ROOT/forms-engine-cli-dynamic.sh ./Forms Schedules upload --namespace \$\$TAX_FORMS_NAMESPACE
      - \$\$SCRIPT_ROOT/forms-engine-cli-dynamic.sh ./Forms Workpapers upload --namespace \$\$WORKPAPERS_NAMESPACE
    agents:
      queue: cc-dev-dflt

  - wait

  - label: 'Publish to SIT'
    branches: master
    command:
      - export FORMS_ENGINE_CLIENT_SECRET=\$\$FORMS_ENGINE_CLIENT_SECRET
      - export RELEASE_FILES=\$\$(buildkite-agent meta-data get "release-files")
      - \$\$SCRIPT_ROOT/forms-engine-cli-release-multiselect.sh "\$\$RELEASE_FILES" publishRelease
    agents:
      queue: cc-dev-dflt

  - block: ':rocket: Release to PROD'
    branches: master

  - label: 'Upload to PROD'
    branches: master
    command:
      - export FORMS_ENGINE_CLIENT_SECRET=\$\$FORMS_ENGINE_CLIENT_SECRET
      - \$\$SCRIPT_ROOT/forms-engine-cli-dynamic.sh ./Forms Returns upload --environment prod --namespace \$\$TAX_FORMS_NAMESPACE
      - \$\$SCRIPT_ROOT/forms-engine-cli-dynamic.sh ./Forms Schedules upload --environment prod --namespace \$\$TAX_FORMS_NAMESPACE
      - \$\$SCRIPT_ROOT/forms-engine-cli-dynamic.sh ./Forms Workpapers upload --environment prod --namespace \$\$WORKPAPERS_NAMESPACE
    agents:
      queue: cc-prod-dflt

  - wait

  - label: 'Publish Release to PROD'
    branches: master
    command:
      - export FORMS_ENGINE_CLIENT_SECRET=\$\$FORMS_ENGINE_CLIENT_SECRET
      - export RELEASE_FILES=\$\$(buildkite-agent meta-data get "release-files")
      - \$\$SCRIPT_ROOT/forms-engine-cli-release-multiselect.sh "\$\$RELEASE_FILES" publishRelease --environment prod
    agents:
      queue: 'cc-prod-dflt'
EOF
