#!/usr/bin/env bash
# Builds the Android APK of the ENGLISH variant "Gorsaf Abercastell EN" (Mnemo Hooks with English hooks)
# from ../game-en/gorsaf-abercastell-en.html (made by: python3 -I mnemo/make_en.py).
# Usage:  ./build_en.sh <versionCode> <versionName>      e.g.  ./build_en.sh 2 3.5-en
# A SEPARATE app: own applicationId and own key, so it installs NEXT TO the original app and never touches it.
#   applicationId  cymru.gorsaf.abercastell.en   (Java code stays in package cymru.gorsaf.abercastell)
#   label          Gorsaf Abercastell EN
#   key            signing-en/gorsaf-en.jks (or $GORSAF_EN_KS_FILE), alias gorsafen, password in signing-en/KEYSTORE.txt or $GORSAF_EN_KS_PASS
#   network        INTERNET (sync + new-version check, api.github.com only) and CAMERA (pairing QR code), added here only:
#                  project/AndroidManifest.xml of the original app stays without them.
#   audio          ../game/audio (or $GORSAF_AUDIO_DIR, e.g. ../audio in the GitHub repository)
# The original app (build.sh, project/AndroidManifest.xml, signing/gorsaf.jks) is not read for signing nor changed.
set -euo pipefail
cd "$(dirname "$0")"
VC="${1:?versionCode (integer, must be higher than the installed English app)}"
VN="${2:?versionName, e.g. 3.4-en}"
APPID=cymru.gorsaf.abercastell.en
LABEL="Gorsaf Abercastell EN"
GAME=../game-en/gorsaf-abercastell-en.html
KS="${GORSAF_EN_KS_FILE:-signing-en/gorsaf-en.jks}"
AUD="${GORSAF_AUDIO_DIR:-../game/audio}"
PASS="${GORSAF_EN_KS_PASS:-$(sed -n 's/^password: *//p' signing-en/KEYSTORE.txt 2>/dev/null)}"
[ -f "$GAME" ] || { echo "$GAME missing: run python3 -I mnemo/make_en.py first" >&2; exit 1; }

# 1) Android build tools, fetched from npm (shared with build.sh)
if [ ! -f tools/android.jar ]; then
  mkdir -p tools/.dl && (cd tools/.dl && npm pack @drxiaozhi/minapk@0.4.0 aaptjs3@2.0.2 >/dev/null)
  mkdir -p tools/.x1 tools/.x2
  tar xzf tools/.dl/drxiaozhi-minapk-0.4.0.tgz -C tools/.x1
  tar xzf tools/.dl/aaptjs3-2.0.2.tgz -C tools/.x2
  cp tools/.x1/package/tools/android.jar tools/.x1/package/tools/d8.jar tools/.x1/package/tools/apksigner.jar tools/
  cp tools/.x2/package/bin/x64/linux/aapt2 tools/ && chmod +x tools/aapt2
fi
T=tools
# The tools come from third-party npm packages and apksigner receives the signing key: refuse to run if any of them
# differs from the copies checked on 13 Nov 2026 (EN review). Update the hashes only after checking a new version.
(cd "$T" && sha256sum -c --quiet - <<'SUMS'
6cea1df3efb77103ac3e2beb9bf4718964b0e0869ab16d39d29d5cbae1c147ad  android.jar
d43c8a94c9b1f1da1a7cc49c32b81e8cee1708b37ee8b530a81a0688222b42c0  d8.jar
eefdd6aed9db9fb849e4c98a50d8741e19d1b674ba6547220bcb9c3ed152123a  apksigner.jar
e4dff6060827a3e401bce376e47916f2f93a89602af54973ffd3fdfc2528be3f  aapt2
SUMS
) || { echo "build tools in apk/tools differ from the checked copies: not building" >&2; exit 1; }

# 2) Every recorded clip must be in ../game/audio (same 60 packs as the original game)
NEED=$(python3 -c "import re,json;s=open('$GAME',encoding='utf8').read();print(len(json.loads(re.search(r'const AUDIO_INDEX=(\{.*?\});',s,re.S).group(1))))")
HAVE=$(ls "$AUD"/*.mp3 2>/dev/null | wc -l)
if [ "$HAVE" -lt "$NEED" ]; then echo "$AUD has $HAVE of $NEED clips: run python3 audio/unpack_packs.py first" >&2; exit 1; fi

# 3) A private copy of the project: manifest with the new applicationId + label, the page, the audio
P=build-en/project; rm -rf build-en/project; mkdir -p "$P/assets"
cp -r project/res project/src "$P/"
# Icon: the ORIGINAL one, without the "EN" badge (user's choice, 15 Nov 2026, from 3.7-en). The badged icons stay in icon-en/;
# to bring them back: cp -r icon-en/res/. "$P/res/"
python3 - "$GAME" "$P" "$APPID" "$LABEL" "$VC" "$VN" <<'EOF'
import re,sys
game,P,appid,label,vc,vn=sys.argv[1:]
g=open(game,encoding='utf8').read().split('\n',2)
assert g[0].startswith('<title>') and 'fonts.googleapis' in g[1], 'game file should start with <title> then the Google Fonts <link>'
h=open('web-header.html',encoding='utf8').read()
open(P+'/assets/index.html','w',encoding='utf8').write(h+g[2])
m=open('project/AndroidManifest.xml',encoding='utf8').read()
m,n1=re.subn(r'package="[^"]+" android:versionCode="\d+" android:versionName="[^"]+"',
             f'package="{appid}" android:versionCode="{vc}" android:versionName="{vn}"',m)
m,n2=re.subn(r'android:label="[^"]+"',f'android:label="{label}"',m)
m,n3=re.subn(r'android:name="\.MainActivity"','android:name="cymru.gorsaf.abercastell.MainActivity"',m)
# sync (api.github.com) and the new-version check; camera only for the pairing QR code, asked for when scanning
m,n4=re.subn(r'(<uses-sdk [^>]*/>)',r'\1\n    <uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.CAMERA" />\n    <uses-feature android:name="android.hardware.camera" android:required="false" />',m)
assert n1==n2==n3==n4==1,(n1,n2,n3,n4)
open(P+'/AndroidManifest.xml','w',encoding='utf8').write(m)
EOF
mkdir -p "$P/assets/audio" && cp "$AUD"/*.mp3 "$P/assets/audio/"

# 4) Compile, dex, package, align, sign with the ENGLISH key
B=build-en/v$VN; rm -rf "$B"; mkdir -p "$B/classes" "$B/dex"
$T/aapt2 compile --dir "$P/res" -o "$B/res.zip"
$T/aapt2 link -o "$B/base.apk" -I $T/android.jar --manifest "$P/AndroidManifest.xml" -A "$P/assets" "$B/res.zip" --min-sdk-version 26 --target-sdk-version 34
javac -nowarn -source 1.8 -target 1.8 -bootclasspath $T/android.jar -cp $T/android.jar -d "$B/classes" $(find "$P/src" -name '*.java') 2>&1 | grep -v -e '^warning' -e '^Note' -e '^Picked' || true
java -cp $T/d8.jar com.android.tools.r8.D8 --lib $T/android.jar --min-api 26 --output "$B/dex" $(find "$B/classes" -name '*.class') 2>&1 | grep -v '^Picked' || true
python3 align.py "$B/base.apk" "$B/dex/classes.dex" "$B/aligned.apk"
OUT="gorsaf-abercastell-en-$VN.apk"
java -jar $T/apksigner.jar sign --ks "$KS" --ks-pass "pass:$PASS" --ks-key-alias gorsafen --out "$OUT" "$B/aligned.apk" 2>&1 | grep -v '^Picked' || true
java -jar $T/apksigner.jar verify --print-certs "$OUT" 2>&1 | grep -E 'SHA-256|Verifies' || true
echo "Built apk/$OUT (applicationId $APPID, versionCode $VC)"
