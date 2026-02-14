import Utils



def main():
    iso_path = Utils.open_filename("Path to ISO to patch", [("ISO", [".iso"])])
    if iso_path == "":
        return
    new_data_path = Utils.open_filename("file with new data for the iso", [("bin", [".bin"])])
    if new_data_path == "":
        return

    bin_offset = int(input("Offset to the bin file in the iso (should be at the end of the file)"), 16)
    if bin_offset < 0:
        return

    bin_index = int(input("file index within the bin to inject data into (0 indexed)"))
    if bin_index < 0:
        return

    with open(new_data_path, "rb") as bin_file:
        new_data = bin_file.read(bin_offset)

    with open(iso_path, "r+b") as iso_file:
        iso_file.seek(bin_offset)
        section_count = int.from_bytes(iso_file.read(4), "big")

        section_offsets = []
        for i in range(section_count):
            section_offsets.append(int.from_bytes(iso_file.read(4), "big"))

        section_sizes = [section_offsets[i + 1] - section_offsets[i] for i in range(section_count - 1)]
        section_sizes.append(float("inf")) # the size of the last one doesn't really matter

        selected_offset = section_offsets[bin_index]
        selected_size = section_sizes[bin_index]

        if len(new_data) > selected_size:
            size_diff = len(new_data) - selected_size
            size_diff += size_diff % 2 # everything should start at an even byte index
            # shift old data
            start_offset = section_offsets[bin_index + 1]
            iso_file.seek(bin_offset + start_offset)
            copy_data = iso_file.read()
            iso_file.seek(bin_offset + start_offset + size_diff)
            iso_file.write(copy_data)

            # update headers
            for i in range(bin_index + 1, section_count):
                # update the header with the new offsets
                iso_file.seek(bin_offset + 4 + i * 4) # first 4 bytes aren't an offset, and each offset is 4 bytes
                new_offset_bytes = (section_offsets[i] + size_diff).to_bytes(4, byteorder='big')
                iso_file.write(new_offset_bytes)

        # set the new data
        iso_file.seek(bin_offset + selected_offset)
        iso_file.write(new_data)

if __name__ == "__main__":
    main()