from config import VERSIONS, BINARY_FORMATS
from assemblyParsing import assemblyParsing_main
from sourceParsing import sourceParsing_main
import os
import shutil
import json


SRC_DIR = "src_code"
BINARY_DIR = "binary"
ASSEMBLY_DIR = "assembly"
OUTPUT = "assembly_src_match"

# remove previous output
if os.path.exists(OUTPUT) and os.path.isdir(OUTPUT):
    shutil.rmtree(OUTPUT)
os.mkdir(OUTPUT)

# process all compiled binaries
all_packages = list(VERSIONS.keys())
for b_format in ["x86-64"]:  # TODO only works with x86 for now
    os.mkdir(os.path.join(OUTPUT, b_format))
    all_dirs = [x for x in os.listdir(os.path.join(BINARY_DIR, b_format))]

    for package in all_packages:
        os.mkdir(os.path.join(OUTPUT, b_format, package))
        for version in VERSIONS[package]:

            source_fun_count = 0
            assembly_fun_count = 0
            matched_fun_count = 0

            src_code_dir = os.path.join(SRC_DIR, package, version)

            all_compiles = [x for x in all_dirs if x.startswith("{}-{}".format(package, version))]
            if package in ("binutils", "coreutils", "diffutils", "findutils"):
                # There are multiple compiled executable binary files
                # Each binary file corresponds to a .c file with same name
                
                for compile_dir in all_compiles:

                    # print("processing {}".format(compile_dir))

                    all_results = dict()

                    # get all compiled binaries
                    binaries = set(os.listdir(os.path.join(BINARY_DIR, b_format, compile_dir)))
                    
                    # get all c scripts
                    c_scripts = dict()
                    for root, d_names, f_names in os.walk(src_code_dir):
                        
                        for f_name in f_names:
                            if f_name.endswith(".c") and f_name[:-2] in binaries:
                                c_scripts[f_name[:-2]] = os.path.join(root, f_name)
                    
                    for binary, source_code_path in c_scripts.items():

                        assembly_path = os.path.join(ASSEMBLY_DIR, b_format, compile_dir, binary + ".asm")
                        assembly_functions = assemblyParsing_main(assembly_path)
                        source_functions = sourceParsing_main(source_code_path)

                        assembly_fun_count += len(assembly_functions)
                        source_fun_count += len(source_functions)

                        matched_names = set(assembly_functions.keys()).intersection(set(source_functions.keys()))
                        
                        for name in matched_names:
                            all_results[binary + "/" + name] = {
                                "source": source_functions[name].replace("\n", ""),
                                "assembly": assembly_functions[name]
                            }
                        
                    matched_fun_count += len(all_results)
                    
                    with open(os.path.join(OUTPUT, b_format, package, compile_dir + ".json"), "w") as fout:
                        json.dump(all_results, fout, indent=2)
            
            elif package in ("curl", "libtomcrypt", "sqlite"):
                # the source code is located in the "src" folder,
                # and there is only one output binary
                
                for compile_dir in all_compiles:

                    # print("processing {}".format(compile_dir))

                    # get binary
                    binary = list(os.listdir(os.path.join(BINARY_DIR, b_format, compile_dir)))[0]

                    # get assembly info
                    assembly_path = os.path.join(ASSEMBLY_DIR, b_format, compile_dir, binary + ".asm")
                    assembly_functions = assemblyParsing_main(assembly_path)

                    assembly_fun_count += len(assembly_functions)

                    # get all c scripts
                    c_scripts = dict()
                    src_name = list(os.listdir(src_code_dir))[0]
                    for root, d_names, f_names in os.walk(os.path.join(src_code_dir, src_name, "src")):

                        for f_name in f_names:
                            if f_name.endswith(".c") and os.path.isfile(os.path.join(root, f_name)):

                                rel_path = os.path.relpath(
                                    os.path.join(root, f_name), os.path.join(src_code_dir, src_name, "src")
                                )
                                source_functions = sourceParsing_main(os.path.join(root, f_name))
                                c_scripts[rel_path] = source_functions

                                source_fun_count += len(source_functions)
                                

                    all_results = dict()
                    seen = set()
                    badset = set()
                    for assembly_name, assembly_code in assembly_functions.items():

                        for src_filename, src_dict in c_scripts.items():
                            for src_func_name, src_code in src_dict.items():

                                if assembly_name == src_func_name:
                                    save_key = src_filename + "/" + src_func_name

                                    if assembly_name in seen:
                                        badset.add(assembly_name)
                                    else:
                                        if all_results.get(save_key, None) is None:
                                            all_results[save_key] = {
                                                "source": src_code.replace("\n", ""),
                                                "assembly": assembly_code
                                            }
                                            seen.add(assembly_name)
                    
                    all_results_new = dict()
                    for key, val in all_results.items():

                        if key.split("/")[-1] not in badset:
                            all_results_new[key] = val
                    
                    all_results = all_results_new
                    with open(os.path.join(OUTPUT, b_format, package, compile_dir + ".json"), "w") as fout:
                        json.dump(all_results, fout, indent=2)
                    
                    matched_fun_count += len(all_results)

            if matched_fun_count != 0:
                print("{}-{}, assembly functions {}, source functions {}, matched: {}".format(
                    package, version, assembly_fun_count, source_fun_count, matched_fun_count
                ))

