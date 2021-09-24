#!/bin/bash

function compare {
    python compare.py $1/labels.json $1/scores/*.json -o $1/performance.json
}

compare ../../data/manual-labels/malware/cosmicduke-dropper
compare ../../data/manual-labels/malware/cosmicduke-loader

compare ../../data/manual-labels/obfuscations/ollvm-ndk-camera-texture-view
compare ../../data/manual-labels/obfuscations/ollvm-ndk-endless-tunnel
compare ../../data/manual-labels/obfuscations/ollvm-ndk-native-plasma
compare ../../data/manual-labels/obfuscations/ollvm-ndk-webp-view

compare ../../data/manual-labels/optimizations/coreutils-base64
compare ../../data/manual-labels/optimizations/coreutils-du
compare ../../data/manual-labels/optimizations/coreutils-ls
compare ../../data/manual-labels/optimizations/findutils-find

compare ../../data/manual-labels/semantic/gcj-2010-509101
compare ../../data/manual-labels/semantic/gcj-2012-1475486
compare ../../data/manual-labels/semantic/gcj-2014-5158144455999488
compare ../../data/manual-labels/semantic/gcj-2020-00000000003775e9

compare ../../data/manual-labels/versions/coreutils-base64
compare ../../data/manual-labels/versions/coreutils-du
compare ../../data/manual-labels/versions/coreutils-ls
compare ../../data/manual-labels/versions/coreutils-mv

compare ../../data/blind-helix/
