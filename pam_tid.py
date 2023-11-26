#!/usr/bin/env python3
"""
Copyright (c) 2023 Paul Durivage
"""
import argparse
import pathlib
import re
import sys

LINE = "\nauth sufficient pam_tid.so"


def main():
    parser = argparse.ArgumentParser(description="Ensures Touch ID is enabled for sudo")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--file", type=str, default="/etc/pam.d/sudo")
    args = parser.parse_args()

    path = pathlib.Path(args.file)

    try:
        assert path.exists(), f"{path}: does not exist"
        assert path.is_file(), f"{path}: not a file"
    except AssertionError as e:
        raise SystemExit(str(e))

    with open(path) as f:
        data = f.read()

    p_tid = re.compile(r'^auth\s+sufficient\s+pam_tid\.so$',
                       flags=re.MULTILINE)

    match_tid = re.search(p_tid, data)

    if args.check and match_tid:
        sys.exit(0)
    elif args.check and not match_tid:
        sys.exit(1)

    if not match_tid:
        p_auth_suff = re.compile(r"^auth\s+sufficient\s+pam_\w+\.so$",
                                 flags=re.MULTILINE)
        match = list(re.finditer(p_auth_suff, data))[-1]
        s_out = data[:match.end()] + LINE + data[match.end():]

        with open(path, 'w') as f:
            f.write(s_out)


if __name__ == '__main__':
    main()
