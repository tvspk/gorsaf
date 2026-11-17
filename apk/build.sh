#!/usr/bin/env bash
# Builds the Android APK of Gorsaf Abercastell from ../game/gorsaf-abercastell.html.
# Usage:  ./build.sh <versionCode> <versionName>      e.g.  ./build.sh 6 2.4
# Needs: java + javac (JDK 17+), python3, npm (only the first time, to fetch the Android tools).
# The keystore password is read from signing/KEYSTORE.txt (line "password: ...") or $GORSAF_KS_PASS.
set -euo pipefail
cd "$(dirname "$0")"
VC="${1:?versionCode (integer, must be higher than the installed one)}"
VN="${2:?versionName, e.g. 2.4}"
PASS="${GORSAF_KS_PASS:-$(sed -n 's/^password: *//p' signing/KEYSTORE.txt)}"

# 1) Android build tools, fetched from npm (works where Google's servers are blocked)
if [ ! -f tools/android.jar ]; then
  mkdir -p tools/.dl && (cd tools/.dl && npm pack @drxiaozhi/minapk@0.4.0 aaptjs3@2.0.2 >/dev/null)
  mkdir -p tools/.x1 tools/.x2
  tar xzf tools/.dl/drxiaozhi-minapk-0.4.0.tgz -C tools/.x1
  tar xzf tools/.dl/aaptjs3-2.0.2.tgz -C tools/.x2
  cp tools/.x1/package/tools/android.jar tools/.x1/package/tools/d8.jar tools/.x1/package/tools/apksigner.jar tools/
  cp tools/.x2/package/bin/x64/linux/aapt2 tools/ && chmod +x tools/aapt2
fi
T=tools

# 2a) Every recorded clip must be in ../game/audio (python3 ../audio/unpack_packs.py), or the app would ship without sound
NEED=$(python3 -c "import re,json;s=open('../game/gorsaf-abercastell.html',encoding='utf8').read();print(len(json.loads(re.search(r'const AUDIO_INDEX=(\{.*?\});',s,re.S).group(1))))")
HAVE=$(ls ../game/audio/*.mp3 2>/dev/null | wc -l)
if [ "$HAVE" -lt "$NEED" ]; then echo "game/audio has $HAVE of $NEED clips: run python3 audio/unpack_packs.py first" >&2; exit 1; fi
mkdir -p project/assets
# 2) The page inside the app: offline header (local-storage shim + embedded fonts) + the game without its Google Fonts link
python3 - <<'EOF'
g=open('../game/gorsaf-abercastell.html',encoding='utf8').read().split('\n',2)
assert g[0].startswith('<title>') and 'fonts.googleapis' in g[1], 'game file should start with <title> then the Google Fonts <link>'
h=open('web-header.html',encoding='utf8').read()
open('project/assets/index.html','w',encoding='utf8').write(h+g[2])
EOF
# Recorded Welsh lines (made by ../audio/make_audio.py), played from file:///android_asset/audio/
rm -rf project/assets/audio
if [ -d ../game/audio ]; then cp -r ../game/audio project/assets/audio; fi

# 3) Version
sed -i -E "s/android:versionCode=\"[0-9]+\" android:versionName=\"[^\"]+\"/android:versionCode=\"$VC\" android:versionName=\"$VN\"/" project/AndroidManifest.xml

# 4) Compile, dex, package, align, sign
B=build/v$VN; rm -rf "$B"; mkdir -p "$B/classes" "$B/dex"
$T/aapt2 compile --dir project/res -o "$B/res.zip"
$T/aapt2 link -o "$B/base.apk" -I $T/android.jar --manifest project/AndroidManifest.xml -A project/assets "$B/res.zip" --min-sdk-version 26 --target-sdk-version 34
javac -nowarn -source 1.8 -target 1.8 -bootclasspath $T/android.jar -cp $T/android.jar -d "$B/classes" $(find project/src -name '*.java') 2>&1 | grep -v -e '^warning' -e '^Note' -e '^Picked' || true
java -cp $T/d8.jar com.android.tools.r8.D8 --lib $T/android.jar --min-api 26 --output "$B/dex" $(find "$B/classes" -name '*.class')
python3 align.py "$B/base.apk" "$B/dex/classes.dex" "$B/aligned.apk"
java -jar $T/apksigner.jar sign --ks signing/gorsaf.jks --ks-pass "pass:$PASS" --ks-key-alias gorsaf --out "gorsaf-abercastell-$VN.apk" "$B/aligned.apk"
java -jar $T/apksigner.jar verify --print-certs "gorsaf-abercastell-$VN.apk" | grep -E 'SHA-256|Verifies' || true
echo "Built apk/gorsaf-abercastell-$VN.apk (versionCode $VC)"
