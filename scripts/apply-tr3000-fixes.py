#!/usr/bin/env python3
"""Apply narrowly scoped local TR3000 fixes, failing on unknown source changes."""
import argparse
import pathlib
import shutil
import subprocess

def apply(source, patch):
    reverse = subprocess.run(["git", "apply", "--reverse", "--check", str(patch)], cwd=source, capture_output=True)
    if reverse.returncode == 0:
        return
    subprocess.run(["git", "apply", "--check", str(patch)], cwd=source, check=True)
    subprocess.run(["git", "apply", str(patch)], cwd=source, check=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=pathlib.Path)
    parser.add_argument("--no-hnat", action="store_true")
    args = parser.parse_args()
    source = args.source.resolve()
    repo = pathlib.Path(__file__).resolve().parents[1]
    patches = repo / "patches/tr3000-v1-256mb"
    apply(source, patches / "0001-board-name.patch")
    mk = (source / "target/linux/mediatek/image/filogic.mk").read_text()
    block = mk.split("define Device/cudy_tr3000-v1-256mb\n", 1)[1].split("\nendef", 1)[0]
    if "BOARD_NAME := cudy_tr3000-v1-256mb" not in block:
        raise SystemExit("TR3000 BOARD_NAME verification failed")
    if args.no_hnat:
        cfg = source / ".config"
        text = cfg.read_text()
        target = "CONFIG_TARGET_mediatek_filogic_DEVICE_cudy_tr3000-v1-256mb=y"
        if target not in text.splitlines():
            raise SystemExit("--no-hnat requires the TR3000 v1 256MB config")
        apply(source, patches / "0002-optional-warp-proxy.patch")
        symbols = ("CONFIG_MTK_WHNAT_SUPPORT", "CONFIG_MTK_WARP_V2", "CONFIG_CCACHE_DIR")
        lines = [line for line in text.splitlines() if not any(line.startswith(s + "=") or line == "# " + s + " is not set" for s in symbols)]
        lines += ["# CONFIG_MTK_WHNAT_SUPPORT is not set", "# CONFIG_MTK_WARP_V2 is not set", 'CONFIG_CCACHE_DIR=""']
        cfg.write_text("\n".join(lines) + "\n")
        overlay = repo / "profiles/tr3000-v1-256mb-20261011/files"
        for item in overlay.rglob("*"):
            if item.is_file():
                dest = source / "files" / item.relative_to(overlay)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(item, dest)
                if dest.parent.name == "uci-defaults":
                    dest.chmod(0o755)
    print("TR3000 board fix verified" + ("; local No-HNAT profile applied" if args.no_hnat else ""))

if __name__ == "__main__":
    main()
