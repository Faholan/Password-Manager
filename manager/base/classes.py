"""Various base classes in use in the manager."""

import typing as t


class CharacterRange:
    """Represent a selectionable range of characters."""

    __slots__ = ("_characters", "characters", "name")

    def __init__(
        self,
        name: str,
        characters: t.Iterable[int],
    ) -> None:
        """Initialize self."""
        self.name = name
        self._characters = frozenset(chr(i) for i in characters)
        self.characters = tuple(self._characters)

    def __iter__(self) -> t.Iterable[str]:
        """Yield the characters in the range."""
        return self._characters.__iter__()

    def __hash__(self) -> int:
        """Return the hash of self."""
        return hash((self.name, self._characters))

    def __eq__(self, other: object) -> bool:
        """Implement self == other."""
        return (
            isinstance(
                other,
                CharacterRange,
            )
            and self.name == other.name
            and self._characters == other._characters
        )

    def __or__(self, other: object) -> "CharacterRange":
        """Implement self | other."""
        if not isinstance(other, CharacterRange):
            raise TypeError(
                "Unsupported operand type(s) for |: "
                f"'CharacterRange' and '{other.__class__.__name__}"
            )
        return CharacterRange(
            f"{self.name} | {other.name}",
            (ord(char) for char in self._characters | other._characters),
        )
