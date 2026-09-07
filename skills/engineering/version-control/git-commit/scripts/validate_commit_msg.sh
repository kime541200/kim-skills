#!/bin/bash

MESSAGE="$1"

if [ -z "$MESSAGE" ]; then
    MESSAGE=""
fi

FIRST_LINE=$(echo "$MESSAGE" | head -n 1)

PATTERN="^(feat|fix|docs|style|refactor|perf|test|chore)(\([a-z0-9._-]+\))?: [^[:space:]].{0,71}$"

if [[ "$FIRST_LINE" =~ $PATTERN && ! "$FIRST_LINE" =~ [[:space:]]$ && ! "$FIRST_LINE" =~ \.$ ]]; then
    echo "Valid commit message format"
    exit 0
else
    echo "Invalid format. Expected: type(scope): subject"
    exit 1
fi
