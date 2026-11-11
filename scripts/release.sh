#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
    echo "usage: $0 VERSION (e.g. $0 v2.0)" >&2
    exit 1
fi

VERSION=$1
ROOT=$(cd "$(dirname "$0")/.." && pwd)
BUILD=$ROOT/build
OUT=$BUILD/release/$VERSION

if [ ! -d "$BUILD/fonts/ttf" ] || [ ! -d "$BUILD/fonts/variable" ]; then
    echo "no build output in $BUILD/fonts, run scripts/build.sh first" >&2
    exit 1
fi

rm -rf "$OUT"
mkdir -p "$OUT"

package() {
    local name=$1
    shift
    local dir=$OUT/staging/Nossikon-$VERSION-$name
    mkdir -p "$dir"
    cp -L "$ROOT/LICENSE" "$dir/"
    cp -r "$@" "$dir/"
    (cd "$OUT/staging" && python3 -m zipfile -c "$OUT/Nossikon-$VERSION-$name.zip" "Nossikon-$VERSION-$name")
}

package static "$BUILD"/fonts/ttf/*.ttf
package variable "$BUILD"/fonts/variable/*.ttf
package web "$ROOT"/fonts/*.woff2 "$ROOT/fonts/nossikon.css" "$ROOT/fonts/sample.html"

rm -rf "$OUT/staging"

ls -l "$OUT"
echo
echo "upload with:"
echo "  gh release create $VERSION $OUT/*.zip --title 'Nossikon $VERSION'"
