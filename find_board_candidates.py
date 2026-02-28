import struct
from dataclasses import dataclass
from typing import List
from itertools import chain
from collections import Counter

SPACE_TYPES = {
    "blue": 1,
    "red": 2,
    "question": 3,
    "bowser": 4,
    "duel": 5,
    "dk": 6,
    "mic": 11
}

def lzss_decompress(data: bytes, out_size: int) -> bytes:
    src = 0              # input pointer
    out = bytearray()
    flags = 0
    window = bytearray(0x400)
    win_pos = 0x3BE      # IMPORTANT: matches uVar7 init

    while len(out) < out_size:
        flags >>= 1
        if (flags & 0x100) == 0:
            flags = data[src] | 0xFF00
            src += 1

        if flags & 1:
            # literal
            b = data[src]
            src += 1

            out.append(b)
            window[win_pos] = b
            win_pos = (win_pos + 1) & 0x3FF
        else:
            # backreference
            b1 = data[src]
            b2 = data[src + 1]
            src += 2

            length = (b2 & 0x3F) + 3
            offset = ((b2 & 0xC0) << 2) | b1

            for _ in range(length):
                b = window[offset & 0x3FF]
                offset += 1

                out.append(b)
                window[win_pos] = b
                win_pos = (win_pos + 1) & 0x3FF

    return bytes(out[:out_size])


@dataclass
class Space:
    def __init__(self, id: int, byt: bytes):
        self._bytes = bytearray(byt)
        self.id = id

    def get_bytes(self) -> bytearray:
        return self._bytes

    def set_color(self, color: int):
        self._bytes[0x2B] = color

    def get_color(self) -> int:
        return self._bytes[0x2B]

    def __repr__(self):
        return f"id: {self.id}; color: {self.get_color()}"

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
        space_id = 0
        while i < len(data):
            connection_count = struct.unpack(">H", data[i + 0x2C:i + 0x2C + 2])[0]
            space_length = 0x2E + connection_count * 2
            spaces.append(Space(space_id, data[i:i + space_length]))
            i += space_length
            space_id += 1

        return cls(
            count,
            spaces
        )



def main():
    compressed_path = r"C:\archipelago\roms\marioparty7extraction\files\data\w06.bin"
    with open(compressed_path, "rb") as f:
        section_count = int.from_bytes(f.read(4), byteorder="big")
        section_offsets = [int.from_bytes(f.read(4), byteorder="big") for _ in range(section_count)]
        for i in range(section_count):
            f.seek(section_offsets[i])
            decompressed_size = int.from_bytes(f.read(4), byteorder="big")
            decompression_type = int.from_bytes(f.read(4), byteorder="big")
            if decompression_type != 1:
                continue
            if i == section_count - 1:
                compressed_data = f.read()
            else:
                compressed_data = f.read(section_offsets[i + 1] - section_offsets[i] - 8)
            decompressed_data = lzss_decompress(compressed_data, decompressed_size)
            space_data = SpaceData.from_binary(decompressed_data)
            if 0 < space_data.count < 300:
                colors = Counter([space.get_color() for space in space_data.spaces])
                print(f"index: {i}; count: {space_data.count}")
                print(f"blue: {colors[1]}")
                print(f"red: {colors[2]}")
                print(f"mic: {colors[11]}")
                print(f"duel: {colors[5]}")
                print(f"dk: {colors[6]}")
                print(f"bowser: {colors[4]}")
                print([hex(space.id) for space in space_data.spaces if space.get_color() in SPACE_TYPES.values()])
                print()




if __name__ == "__main__":
    main()