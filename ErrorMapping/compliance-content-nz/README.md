# Compliance Content NZ

## Adding Forms

When adding a Form (Rule), adding it to either a `Returns`, `Schedules` or `Workpapers` directory under the top-level `Forms` directory will see it automatically included in the following build steps:

- Validate forms
- Upload to SIT
- Upload to PROD

This is due to the aforementioned build steps using the `.buildkite/scripts/forms-engine-cli-dynamic.sh` script, which searches a BASE_DIRECTORY for all directories matching the WORKING_DIRECTORY_NAME and then calls the Forms Engine CLI with the given command for each working directory.


If you would like to include another entrypoint (other than `Forms`) or a new working directory, you can simply add another call to the script in each of the aforementioned build steps.

## Releasing

When adding a Release, adding it to a `Releases` directory under the top-level `Forms` directory will see it automatically included as an option in the `Release to SIT` build block step.

This is due to the aforementioned build block step using the `.buildkite/scripts/build-release-file-options.sh` script, which searches a BASE_DIRECTORY for all directories matching the WORKING_DIRECTORY_NAM and then builds and returns a list of options to be added to a buildkite block step select field.
