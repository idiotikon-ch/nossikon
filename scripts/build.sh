#!/usr/bin/env bash
set -euo pipefail

NOTO_TAG=NotoSans-v2.015
ROOT=$(cd "$(dirname "$0")/.." && pwd)
BUILD=$ROOT/build

if [ ! -d "$BUILD/noto/$NOTO_TAG" ]; then
    mkdir -p "$BUILD/noto/$NOTO_TAG"
    curl -sSL "https://github.com/notofonts/latin-greek-cyrillic/archive/refs/tags/$NOTO_TAG.tar.gz" \
        | tar xz -C "$BUILD/noto/$NOTO_TAG" --strip-components=1
fi

rm -rf "$BUILD/src" "$BUILD/ufo" "$BUILD/fonts"
mkdir -p "$BUILD/src" "$BUILD/ufo"
for style in NotoSans NotoSans-Italic; do
    pkg=${style/NotoSans/NossikonSans}.glyphspackage
    cp -r "$BUILD/noto/$NOTO_TAG/sources/$style.glyphspackage" "$BUILD/src/$pkg"
    sed -i 's/^familyName = "Noto Sans";$/familyName = "Nossikon Sans";/' "$BUILD/src/$pkg/fontinfo.plist"
    glyphs2ufo --generate-GDEF "$BUILD/src/$pkg" -m "$BUILD/ufo"
done

python3 "$ROOT/scripts/patch_noto.py" "$BUILD"/ufo/*.designspace
gftools builder "$ROOT/sources/config.yaml"

for style in NossikonSans NossikonSans-Italic; do
    cp "$BUILD/fonts/variable/$style[wdth,wght].ttf" "$ROOT/fonts/"
    cp "$BUILD/fonts/webfonts/$style[wdth,wght].woff2" "$ROOT/fonts/$style-VF.woff2"
    cp "$BUILD/fonts/webfonts/$style[wdth,wght].woff2" "$ROOT/docs/assets/css/fonts/$style-VF.woff2"
done
cp "$ROOT/fonts/nossikon.css" "$ROOT/docs/assets/css/fonts/nossikon.css"
