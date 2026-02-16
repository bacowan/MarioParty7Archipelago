FST_OFFSET_POINTER = 0x424
FST_SIZE_POINTER = 0x428
FST_ENTRY_COUNT_OFFSET = 0x8
FST_ENTRY_SIZE = 12
FST_ENTRY_FILE_NAME_OFFSET_OFFSET = 1
FST_ENTRY_FILE_POINTER_OFFSET = 4
FST_ENTRY_FILE_SIZE_OFFSET = 8

def move_file(iso_file, file_offset, file_size):
    iso_file.seek(file_offset)
    data = iso_file.read(file_size)

    # Append to end of file
    iso_file.seek(0, 2)  # 2 = SEEK_END
    new_file_offset = iso_file.tell()
    iso_file.write(data)

    # make sure the file has a multiple of 16 bytes
    iso_file.seek(0, 2)
    new_file_size = iso_file.tell()
    iso_file.write(b'\x00' * (16 - (new_file_size % 16)))

    # Overwrite original section with zeros
    iso_file.seek(file_offset)
    iso_file.write(b'\x00' * file_size)

    return new_file_offset

def main():
    iso_path = r"C:\archipelago\roms\Mario Party 7 (USA) (Rev 1).iso"
    filename = input("Name of file to move to end: ")
    with open(iso_path, "r+b") as iso_file:
        iso_file.seek(FST_OFFSET_POINTER)
        fst_offset = int.from_bytes(iso_file.read(4), "big")

        iso_file.seek(FST_SIZE_POINTER)
        fst_size = int.from_bytes(iso_file.read(4), "big")

        iso_file.seek(fst_offset + FST_ENTRY_COUNT_OFFSET)
        fst_entry_count = int.from_bytes(iso_file.read(4), "big")

        string_table_start = fst_offset + fst_entry_count * FST_ENTRY_SIZE

        for offset in range(fst_offset, string_table_start, FST_ENTRY_SIZE):
            iso_file.seek(offset)

            # skip directory entries
            directory_flag = iso_file.read(1)[0]
            if directory_flag == 1:
                continue

            name_offset = int.from_bytes(iso_file.read(3), "big")

            iso_file.seek(string_table_start + name_offset)
            read_file_name = ""
            current_char = ""
            while current_char != "\0":
                current_char = chr(iso_file.read(1)[0])
                if current_char != "\0":
                    read_file_name += current_char

            if filename == read_file_name:
                iso_file.seek(offset + FST_ENTRY_FILE_POINTER_OFFSET)
                file_offset = int.from_bytes(iso_file.read(4), "big")
                iso_file.seek(offset + FST_ENTRY_FILE_SIZE_OFFSET)
                file_size = int.from_bytes(iso_file.read(4), "big")

                new_offset = move_file(iso_file, file_offset, file_size)
                new_offset_bytes = new_offset.to_bytes(4, byteorder='big')

                iso_file.seek(offset + FST_ENTRY_FILE_POINTER_OFFSET)
                iso_file.write(new_offset_bytes)

                break


if __name__ == "__main__":
    main()