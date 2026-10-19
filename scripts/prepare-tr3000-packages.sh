#!/bin/bash
# Only called for the opt-in 20261011 profile, before feeds update.
set -euo pipefail
PROJECT="${GITHUB_WORKSPACE:?GITHUB_WORKSPACE must point to the automation repository}"
cp "$PROJECT/profiles/tr3000-v1-256mb-20261011/feeds.conf" feeds.conf.default
mkdir -p package
if [ ! -d package/luci-compat-keep ]; then
    cp -R "$PROJECT/package/luci-compat-keep" package/
fi
while read -r name url revision; do
    [ -n "$name" ] || continue
    dest="package/$name"
    if [ ! -d "$dest/.git" ]; then
        git clone "$url" "$dest"
    fi
    test -z "$(git -C "$dest" status --porcelain)"
    git -C "$dest" checkout --detach "$revision"
done < "$PROJECT/profiles/tr3000-v1-256mb-20261011/custom-packages.lock"
