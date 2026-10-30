# InPage brand (zaqqwe/rustdesk): build-time rename + icons
import os, urllib.request
from PIL import Image, ImageDraw, ImageFont
NAME = "InPage"
FONT = "poppins-bold.ttf"
if not os.path.exists(FONT):
    urllib.request.urlretrieve("https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf", FONT)
S = 1024
def mk(fg_only=False, fs=250):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    if not fg_only:
        g = Image.new("RGBA", (S, S)); gd = ImageDraw.Draw(g)
        for y in range(S):
            t = y / S; gd.line([(0, y), (S, y)], fill=(int(30 - 30 * t), int(94 + 76 * t), int(255 - 25 * t), 255))
        m = Image.new("L", (S, S), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, S - 1, S - 1], radius=220, fill=255)
        im.paste(g, (0, 0), m)
    d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, fs); b = d.textbbox((0, 0), NAME, font=f)
    d.text(((S - (b[2] - b[0])) / 2 - b[0], (S - (b[3] - b[1])) / 2 - b[1]), NAME, font=f, fill="white")
    return im
ICON, FG = mk(), mk(True, 170)
def png(path, size, im=None):
    if os.path.isdir(os.path.dirname(path) or "."):
        (im or ICON).resize((size, size), Image.LANCZOS).save(path); print("png", path)
def ico(path):
    if os.path.isdir(os.path.dirname(path) or "."):
        ICON.save(path, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]); print("ico", path)
def sub(path, a, b):
    if not os.path.exists(path): print("skip", path); return
    s = open(path, encoding="utf-8").read(); t = s.replace(a, b, 1)
    open(path, "w", encoding="utf-8").write(t); print("sub", path, s != t)
sub("libs/hbb_common/src/config.rs", 'RwLock::new("RustDesk".to_owned())', 'RwLock::new("%s".to_owned())' % NAME)
sub("flutter/android/app/src/main/res/values/strings.xml", '<string name="app_name">RustDesk</string>', '<string name="app_name">%s</string>' % NAME)
sub("flutter/windows/runner/Runner.rc", '"RustDesk Remote Desktop"', '"%s Remote Desktop"' % NAME)
sub("flutter/windows/runner/Runner.rc", 'VALUE "ProductName", "RustDesk"', 'VALUE "ProductName", "%s"' % NAME)
sub("flutter/android/app/src/main/res/values/ic_launcher_background.xml", "#ffffff", "#1677ff")
for p in ["res/icon.ico", "res/tray-icon.ico", "flutter/windows/runner/resources/app_icon.ico"]: ico(p)
for p, s in [("res/icon.png", 1024), ("res/32x32.png", 32), ("res/64x64.png", 64), ("res/128x128.png", 128), ("res/128x128@2x.png", 256), ("res/mac-icon.png", 1024), ("flutter/assets/icon.png", 256)]: png(p, s)
for k, s in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
    b = "flutter/android/app/src/main/res/mipmap-%s/" % k
    png(b + "ic_launcher.png", s); png(b + "ic_launcher_round.png", s); png(b + "ic_launcher_foreground.png", int(s * 108 / 48), FG)
open("flutter/assets/icon.svg", "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1677ff"/><text x="32" y="38" font-family="Arial, sans-serif" font-weight="700" font-size="15" fill="#fff" text-anchor="middle">InPage</text></svg>')
print("InPage brand done")
os.remove(FONT)
sub("flutter/android/app/src/main/AndroidManifest.xml", 'android:label="RustDesk"', 'android:label="InPage"')
sub("flutter/android/app/src/main/AndroidManifest.xml", 'android:label="RustDesk Input"', 'android:label="InPage Input"')
# ★ 261030 우리 서버 · 숫자 일회용 비밀번호 · 폰 패키지 이름 (못 찾으면 빌드를 멈춤)
import sys
def must(path, a, b):
    s = open(path, encoding="utf-8").read()
    if a not in s:
        print("MISSING", path, a); sys.exit(1)
    open(path, "w", encoding="utf-8").write(s.replace(a, b, 1)); print("must", path)
C = "libs/hbb_common/src/config.rs"
must(C, 'pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"];', 'pub const RENDEZVOUS_SERVERS: &[&str] = &["13.124.54.46"];')
must(C, 'pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=";', 'pub const RS_PUB_KEY: &str = "AGNHQh68Q3oJzmavwiFyPIX1Ut6Bh2odni6SSWZEOBQ=";')
must(C, 'pub static ref DEFAULT_SETTINGS: RwLock<HashMap<String, String>> = Default::default();', 'pub static ref DEFAULT_SETTINGS: RwLock<HashMap<String, String>> = RwLock::new(HashMap::from([("allow-numeric-one-time-password".to_owned(), "Y".to_owned())]));')
must("flutter/android/app/build.gradle", 'applicationId "com.carriez.flutter_hbb"', 'applicationId "kr.co.inpage.remote"')
