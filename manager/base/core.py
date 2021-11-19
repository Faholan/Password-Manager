"""Core functions of password manager."""

from os import urandom

from .classes import CharacterRange


def _randbelow(maximum: int) -> int:
    """Generate a random number according to FIPS 186-4.

    :param maximum: The maximum (not included)
    :type maximum: int
    :return: A random number in the range [0, maximum - 1]
    :rtype: int
    """
    length = (len(bin(maximum)) - 3) // 8 + 1
    # The smallest integer so that 8 * length >= N,
    # Where N is the bit length of maximum

    return int(urandom(length + 8).hex(), base=16) % maximum


def gen_password(characters: CharacterRange, length: int) -> str:
    """Securely generate a password."""
    result = ""
    for _ in range(length):
        result += characters.characters[_randbelow(len(characters.characters))]
    return result
