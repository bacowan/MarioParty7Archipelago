import os
import subprocess
import tempfile

def create_patch_files():
    object_file_path = os.path.join(tempfile.gettempdir(), "obj.o")
    for assembly in os.listdir(os.path.join(os.path.dirname(__file__), "assembly")):
        if not assembly.endswith(".s"):
            continue

        # run the assembler
        subprocess.run(
            [
                "powerpc-eabi-as",
                os.path.join(os.path.dirname(__file__), "assembly", assembly), # input assembly
                "-o", object_file_path, # output to
                "-I", os.path.join(os.path.dirname(__file__), "assembly"), # include path
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

if __name__ == "__main__":
    create_patch_files()