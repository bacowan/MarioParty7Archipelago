import Utils


def mp7_lzss_decompress(data: bytes, out_size: int) -> bytes:
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

def main():
    compressed_path = Utils.open_filename("Path to file with compressed data", [("all", ["*"])])
    if compressed_path == "":
        return
    output_path = Utils.open_filename("Path to file to dump data", [("all", ["*"])])
    if output_path == "":
        return

    offset = int(input("Offset of data to decode: "))
    if offset < 0:
        return
    expected_size = int(input("Size of data to decode: "))
    if expected_size < 0:
        return

    with open(compressed_path, "rb") as compressed_file:
        compressed_file.seek(offset)
        compressed_data = compressed_file.read()
        decompressed = mp7_lzss_decompress(compressed_data, out_size=expected_size)
        with open(output_path, "r+b") as output_file:
            output_file.write(decompressed)


if __name__ == "__main__":
    main()