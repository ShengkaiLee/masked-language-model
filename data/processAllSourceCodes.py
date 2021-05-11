from config import VERSIONS
import os
import shutil
from sourceParsing import sourceParsing_main
import json


SRC_DIR = 'src_code'
OUTPUT = 'extracted_src_func'


# remove previous output
if os.path.exists(OUTPUT) and os.path.isdir(OUTPUT):
    shutil.rmtree(OUTPUT)
os.mkdir(OUTPUT)

# process each package
all_packages = list(VERSIONS.keys())
for package in all_packages:
    os.mkdir(os.path.join(OUTPUT, package))
    for version in VERSIONS[package]:

        print("Processing package {} version {}".format(package, version))
        
        package_path = os.path.join(SRC_DIR, package, version)
        c_scripts = list()
        for root, d_names, f_names in os.walk(package_path):
            
            for f_name in f_names:
                if f_name.endswith(".c"):
                    c_scripts.append(os.path.join(root, f_name))
        
        # process each c-script
        all_functions = dict()
        for c_script in c_scripts:

            print("  processing file {}".format(c_script))

            func_dict = sourceParsing_main(c_script)
            if func_dict is not None:

                relative_path = os.path.relpath(c_script, package_path)
                    
                all_functions[relative_path] = dict()
                for func_name, func_content in func_dict.items():
                    all_functions[relative_path][func_name] = func_content.replace("\n", " ")


        with open(os.path.join(OUTPUT, package, "{}-{}.json".format(package, version)), "w") as fout:
            json.dump(all_functions, fout, indent=2)
