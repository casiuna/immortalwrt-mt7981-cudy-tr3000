#!/usr/bin/env python3
"""Offline BOARD/CONTROL/rootfs check. This does not run sysupgrade -T."""
import argparse
import hashlib
import json
import tarfile
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--sha256")
    args = parser.parse_args()
    digest = hashlib.sha256(args.image.read_bytes()).hexdigest()
    if args.sha256 and digest != args.sha256.lower():
        raise SystemExit("SHA256 mismatch")
    prefix = "sysupgrade-cudy_tr3000-v1-256mb"
    with tarfile.open(args.image) as archive:
        control = archive.extractfile(prefix + "/CONTROL").read().decode().strip()
        if control != "BOARD=cudy_tr3000-v1-256mb":
            raise SystemExit("BOARD mismatch")
        if any(m.name.startswith("sysupgrade-cudy_tr3000-256mb-v1/") for m in archive.getmembers()):
            raise SystemExit("Obsolete CONTROL directory")
        if archive.extractfile(prefix + "/root").read(4) != b"hsqs":
            raise SystemExit("Not squashfs")
    print(json.dumps({"filename": args.image.name, "bytes": args.image.stat().st_size,
                      "sha256": digest, "CONTROL": control, "runtime_test": False}))

if __name__ == "__main__":
    main()
