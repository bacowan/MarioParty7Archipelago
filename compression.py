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

def lzss_compress(data: bytes) -> bytes:
    out = bytearray()
    src = 0
    window = bytearray(0x400)
    win_pos = 0x3BE  # Match decompressor's initial position

    flag_buffer = []
    data_buffer = []

    def flush_flags():
        nonlocal flag_buffer, data_buffer
        if flag_buffer:
            flags = 0
            for i, bit in enumerate(flag_buffer):
                if bit:
                    flags |= (1 << i)
            out.append(flags)
            out.extend(data_buffer)
            flag_buffer = []
            data_buffer = []

    while src < len(data):
        best_length = 0
        best_offset = 0

        # Try each possible offset
        for start_offset in range(0x400):
            # Simulate the decompression to see what we'd get
            temp_window = window.copy()
            temp_win_pos = win_pos
            offset = start_offset
            length = 0

            # Simulate decompressor: read, write, increment
            while (length < 66 and src + length < len(data)):
                # Read from window at current offset
                b = temp_window[offset & 0x3FF]

                # Does it match input?
                if b != data[src + length]:
                    break

                # Simulate decompressor writing to window
                temp_window[temp_win_pos] = b
                temp_win_pos = (temp_win_pos + 1) & 0x3FF
                offset += 1
                length += 1

            if length > best_length:
                best_length = length
                best_offset = start_offset

        # Use backreference if length >= 3
        if best_length >= 3:
            flag_buffer.append(0)

            b1 = best_offset & 0xFF
            b2 = ((best_offset & 0x300) >> 2) | ((best_length - 3) & 0x3F)
            data_buffer.append(b1)
            data_buffer.append(b2)

            # Update window exactly as decompressor would
            offset = best_offset
            for i in range(best_length):
                b = window[offset & 0x3FF]
                window[win_pos] = b
                win_pos = (win_pos + 1) & 0x3FF
                offset += 1
            src += best_length
        else:
            # Literal
            flag_buffer.append(1)
            b = data[src]
            data_buffer.append(b)

            window[win_pos] = b
            win_pos = (win_pos + 1) & 0x3FF
            src += 1

        if len(flag_buffer) == 8:
            flush_flags()

    flush_flags()

    return bytes(out)