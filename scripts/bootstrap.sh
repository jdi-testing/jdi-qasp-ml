#!/usr/bin/env bash

set -euf -o pipefail

SUCCESS=0
FAILURE=1

platform="$(uname -s)"
repo_url="https://raw.githubusercontent.com/jdi-testing/jdi-qasp-ml"

help()
{
    echo "\
Usage: ./bootstrap.sh [ options ]
 -b, --branch <branch>                    Branch used as a source for downloading files. Default is 'master'
 -c, --cores-to-use <cores>               Amount of allowed parallel Selenium sessions. Default is number of cores on your machine
 -d, --detached                           Run Docker Compose in 'detached' mode
 -l, --label <label>                      Docker image label to pull. Default is 'latest'
 --no-cleanup                             Do not remove old Docker resources with the same label
 -p, --pull-policy <always|missing|never> Docker Compose pull policy. Defaults to 'always'

Examples:
  1. Start a latest stable application version

    ./bootstrap.sh

  2. Start a release candidate application version

    ./bootstrap.sh -b release/0.3.0 -l rc

  3. Start a latest version of application under development

    ./bootstrap.sh -b develop -l develop

  4. Start a version from pull request to test it:

    ./bootstrap.sh -b issue_183-ci-workflow-fix -l pr-186
"
}

isdigit ()    # Tests whether *entire string* is numerical.
{             # In other words, tests for integer variable.
  [ $# -eq 1 ] || return $FAILURE

  case $1 in
    *[!0-9]*|"") return $FAILURE;;
              *) return $SUCCESS;;
  esac
}

LABEL=latest
BRANCH=master
PULL_POLICY=always
SELENOID_PARALLEL_SESSIONS_COUNT=$(nproc)
DO_CLEANUP="true"
DETACHED="false"

while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      help
      exit $SUCCESS
      ;;
    -l|--label)
      LABEL="$2"
      shift
      shift
      ;;
    -b|--branch)
      BRANCH="$2"
      shift
      shift
      ;;
    -p|--pull-policy)
      PULL_POLICY="$2"
      case $PULL_POLICY in
        always|missing|never)
          ;;
        *)
          echo "Unknown value for --pull-policy: $2. Valid values are 'always', 'missing' and 'never'"
          exit $FAILURE
          ;;
      esac
      shift
      shift
      ;;
    -c|--cores-to-use)
      if isdigit "$2"
      then
        SELENOID_PARALLEL_SESSIONS_COUNT="$2"
      else
        echo "Cores to use should be an integer"
        exit $FAILURE
      fi
      shift
      shift
      ;;
    --no-cleanup)
      DO_CLEANUP="false"
      shift
      ;;
    -d|--detached)
      DETACHED="true"
      shift
      ;;
    --*|-*)
      echo "Unknown option $1"
      exit $FAILURE
      ;;
    *)
      echo "Unknown argument $1"
      exit $FAILURE
      ;;
  esac
done

echo "LABEL                            = ${LABEL}"
echo "BRANCH                           = ${BRANCH}"
echo "PULL_POLICY                      = ${PULL_POLICY}"
echo "SELENOID_PARALLEL_SESSIONS_COUNT = ${SELENOID_PARALLEL_SESSIONS_COUNT}"

# shellcheck disable=SC2046
if [[ "$DO_CLEANUP" == "true" ]]
then
  set +e

  echo "Cleaning up old Docker things with the '$LABEL' label..."
  label_selector="label=org.jdi-qasp-ml.version_label=$LABEL"

  docker stop $(docker ps -f "$label_selector" -q) 2>/dev/null
  docker container rm -f $(docker ps -af "$label_selector" -q) 2>/dev/null
  docker volume rm $(docker volume ls -f "$label_selector" -q) 2>/dev/null
  docker network rm $(docker network ls -f "$label_selector" -q) 2>/dev/null

  rm docker-compose.yaml docker-compose.override.yaml browsers.json .env

  set -e
fi

echo "Downloading required files..."

curl --output docker-compose.yaml "$repo_url/$BRANCH/docker-compose.yaml"
curl --output browsers.json "$repo_url/$BRANCH/browsers.json"

docker pull selenoid/vnc_chrome:118.0

random_bytes=$(head -c 4 /dev/urandom)
hex_string=$(od -An -tx1 -N4 -v <<< "$random_bytes" | tr -d ' \n')
NETWORK_NAME="jdi-qasp-ml-${hex_string:0:8}"

echo "\
JDI_VERSION_LABEL=${LABEL}
SELENOID_PARALLEL_SESSIONS_COUNT=${SELENOID_PARALLEL_SESSIONS_COUNT}
JDI_DEFAULT_NETWORK_NAME=${NETWORK_NAME}
" > .env

case $LABEL in
latest)
  ;;
*)
  curl --output docker-compose.override.yaml "$repo_url/$BRANCH/docker-compose.override.arbitrary-tag.yaml"
  ;;
esac

echo "Starting application..."

if [[ "$platform" = "Darwin" ]]
then
  dc_alias="docker-compose"
elif [[ "$platform" = "Linux" ]]
then
  dc_alias="docker compose"
fi

if [[ "$DETACHED" = "true" ]]
then
  $dc_alias up -d --pull "$PULL_POLICY"
else
  $dc_alias up --pull "$PULL_POLICY"
fi
