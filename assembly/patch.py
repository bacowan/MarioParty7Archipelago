import csv
import os
import dolphin_memory_engine
import subprocess
import sys
import tempfile
from typing import NamedTuple

class Instructions(NamedTuple):
    start_address: int
    instructions: list[int]

def create_patch_files():
    object_file_path = os.path.join(tempfile.gettempdir(), "obj.o")
    for assembly in os.listdir(os.path.join(os.path.dirname(__file__), "assembly")):
        # run the assembler
        subprocess.run(
            [
                "powerpc-eabi-as",
                os.path.join(os.path.dirname(__file__), "assembly", assembly), # input assembly
                "-o", # output to
                object_file_path,
                "-mregnames" # enable rn syntax
            ],
            check=True) # error if there's an exception
        # convert the object file to raw binary
        subprocess.run(
            [
                "powerpc-eabi-objcopy",
                "-O", # output format
                "binary",
                object_file_path,
                os.path.join(os.path.dirname(__file__), "bin", os.path.splitext(assembly)[0])
            ],
            check=True)

def apply_patches():
    with open(os.path.join(os.path.dirname(__file__), "assembly_offsets.csv"), "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            with open(os.path.join(os.path.dirname(__file__), "bin", row["filename"]), "rb") as binary_file:
                code_bytes = binary_file.read()
                a = int(row["offset"], 16)
                dolphin_memory_engine.write_bytes(int(row["offset"], 16), code_bytes)

if __name__ == "__main__":
    create_patch_files()
    if len(sys.argv) > 0 and sys.argv[1] == "--apply":
        dolphin_memory_engine.hook()
        if dolphin_memory_engine.is_hooked():
            if dolphin_memory_engine.read_bytes(0x80000000, 6) == b"GP7E01":
                apply_patches()
            else:
                sys.exit("Hooked into dolphin, but game running was not Mario Party 7")
        else:
            sys.exit("Failed to hook into dolphin")