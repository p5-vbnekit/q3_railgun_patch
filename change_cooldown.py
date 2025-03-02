#!/usr/bin/env python3

import sys
import shlex
import struct
import pathlib


try:
    _path = sys.argv[1]
    _path = pathlib.Path(_path).resolve(strict = True)
    if not _path.is_file(): raise ValueError("regular file expected")
except BaseException: raise ValueError(f"bad qagame.qvm path: {_path}")

_new_value = int(sys.argv[2])
if not ((0 <= _new_value) and ((1 << 16) > _new_value)): raise ValueError("bad new value: not in [0:65535]")
_new_value = struct.pack('<h', _new_value)

try: _old_value = sys.argv[3]
except IndexError: _old_value = 1500
else:
    _old_value = int(_old_value)
    if not ((0 <= _old_value) and ((1 << 16) > _old_value)): raise ValueError("bad old value: not in [0:65535]")
_old_value = struct.pack('<h', _old_value)

with open(_path, mode = "rb") as _source: _source = _source.read()
if not _source: raise ValueError("empty qvm binary")

_original_chunks = (
    bytes.fromhex("0000 2008 1621 0100 0a09 0c00 0000 08"),
    bytes.fromhex("00 0020 0816 2101 000a 090c 0000 0008")
)

_source = _source.split(_old_value.join(_original_chunks))
if 2 != len(_source): raise RuntimeError("unable to find old value")

_original = _path.parent / f"{_path.name}.orig"
print(f"moving original {shlex.quote(_path.as_posix())} to {shlex.quote(_original.as_posix())}", file = sys.stderr, flush = True)
_path.replace(_original)

with open(_path, mode = "wb") as _stream:
    _stream.write(_source[0])
    _stream.write(_original_chunks[0])
    _stream.write(_new_value)
    _stream.write(_original_chunks[1])
    _stream.write(_source[1])

print(f"{shlex.quote(_path.as_posix())} patched", file = sys.stderr, flush = True)
