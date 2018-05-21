#!/bin/bash

# ln -sv /Users/Shared/Epic\ Games/UE_4.16 /Users/Shared/UnrealEngine/4.16

UE_VERSION=$1
UE_PLUGIN_NAME="UEAdMob"
if [[ "$#" -ne 2 ]]; then
    UE_VERSION="4.13"
    echo "./build.sh UE_4.19 UEAdMob"
    exit 0
fi

if [[ -n "$2" ]]; then
    UE_PLUGIN_NAME=$2
fi

UE_PATH="/Users/Shared/UnrealEngine/"${UE_VERSION}"/Engine/"
UAT_PATH="Build/BatchFiles/"

echo "Building Plugin for UnrealEngine " ${UE_VERSION}

CURR_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

${UE_PATH}${UAT_PATH}RunUAT.sh BuildPlugin -Plugin="${CURR_PATH}/Plugins/${UE_PLUGIN_NAME}/${UE_PLUGIN_NAME}.uplugin" -TargetPlatforms=Mac+IOS -Package="${CURR_PATH}/output"

cp -R "${CURR_PATH}/output/Binaries" "${CURR_PATH}/Plugins/${UE_PLUGIN_NAME}/"
