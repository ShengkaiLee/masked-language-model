from config import VERSIONS, BINARY_FORMATS
import os
import shutil

BINARY_DIR = "binary"
OUTPUT = "assembly"

# remove previous output
if os.path.exists(OUTPUT) and os.path.isdir(OUTPUT):
    shutil.rmtree(OUTPUT)
os.mkdir(OUTPUT)

# process all compiled binaries
all_packages = list(VERSIONS.keys())
for b_format in BINARY_FORMATS:
    os.mkdir(os.path.join(OUTPUT, b_format))
    all_dirs = [x for x in os.listdir(os.path.join("binary", b_format))]

    for package in all_packages:
        for version in VERSIONS[package]:

            all_compiles = [x for x in all_dirs if x.startswith("{}-{}".format(package, version))]
            for compile_dir in all_compiles:
                print("Dumping {}/{}".format(b_format, compile_dir))
                os.mkdir(os.path.join(OUTPUT, b_format, compile_dir))
                binaries = set(os.listdir(os.path.join(BINARY_DIR, b_format, compile_dir)))
                for binary in binaries:
                    binary_full_path = os.path.join(BINARY_DIR, b_format, compile_dir, binary)
                    output_full_path = os.path.join(OUTPUT, b_format, compile_dir, binary + ".asm")
                    os.system("objdump -j .text -d \"{}\" > \"{}\"".format(binary_full_path, output_full_path))

