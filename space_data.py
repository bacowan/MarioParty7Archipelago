import struct
from dataclasses import dataclass
from typing import List
from itertools import chain

@dataclass
class Space:
    def __init__(self, byt: bytes):
        self._bytes = bytearray(byt)

    def get_bytes(self) -> bytearray:
        return self._bytes

    def set_color(self, color: int):
        self._bytes[0x2B] = color

    def get_color(self) -> int:
        return self._bytes[0x2B]

@dataclass
class SpaceData:
    count: int
    spaces: List[Space]

    def to_binary(self) -> bytes:
        byte_array = bytearray()
        byte_array.extend(self.count.to_bytes(4, byteorder="big"))
        byte_array.extend(chain.from_iterable([space.get_bytes() for space in self.spaces]))
        return byte_array

    @classmethod
    def from_binary(cls, data: bytes) -> 'SpaceData':
        count = struct.unpack(">I", data[:4])[0]
        spaces = []
        i = 4
        while i < len(data):
            connection_count = struct.unpack(">H", data[i + 0x2C:i + 0x2C + 2])[0]
            space_length = 0x2E + connection_count * 2
            spaces.append(Space(data[i:i + space_length]))
            i += space_length

        return cls(
            count,
            spaces
        )
