#!/bin/bash

function performance {
    python performance.py `find $1/* -type f -name 'performance.json' | grep -v $1/performance.json` -o $1/performance.json
}


performance ../../data/manual-labels/malware
performance ../../data/manual-labels/obfuscations
performance ../../data/manual-labels/optimizations
performance ../../data/manual-labels/semantic
performance ../../data/manual-labels/versions

python performance.py \
    ../../data/manual-labels/malware/performance.json \
    ../../data/manual-labels/obfuscations/performance.json \
    ../../data/manual-labels/optimizations/performance.json \
    ../../data/manual-labels/semantic/performance.json \
    ../../data/manual-labels/versions/performance.json \
    -o ../../data/manual-labels/performance.json

python performance.py \
    ../../data/manual-labels/malware/performance.json \
    ../../data/manual-labels/obfuscations/performance.json \
    ../../data/manual-labels/optimizations/performance.json \
    ../../data/manual-labels/semantic/performance.json \
    ../../data/manual-labels/versions/performance.json
