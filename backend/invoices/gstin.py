"""GSTIN structure and checksum helpers; no registration lookup is made."""
import re

ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
GSTIN_PATTERN = re.compile(r'^\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]$')

def checksum(value):
    total, factor = 0, 2
    for char in reversed(value[:14]):
        code = ALPHABET.index(char); addend = code * factor
        total += addend // 36 + addend % 36; factor = 1 if factor == 2 else 2
    return ALPHABET[(36 - total % 36) % 36]

def valid(value):
    return bool(GSTIN_PATTERN.fullmatch(value or '')) and checksum(value) == value[-1]
