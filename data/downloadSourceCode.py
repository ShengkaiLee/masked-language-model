import os
import shutil
from config import VERSIONS


# configurations
OUTPUT = 'src_code'
URLS = {
    "binutils": "https://ftp.gnu.org/gnu/binutils/binutils-{}.tar.gz",
    "busybox": "https://git.busybox.net/busybox/snapshot/busybox-{}.tar.gz",
    "coreutils": "https://ftp.gnu.org/gnu/coreutils/coreutils-{}.tar.xz",
    "curl": "git@github.com:curl/curl.git",
    "diffutils": "https://ftp.gnu.org/gnu/diffutils/diffutils-{}.tar.xz",
    "findutils": "https://ftp.gnu.org/gnu/findutils/findutils-{}.{}",
    "gmp": "https://ftp.gnu.org/gnu/gmp/gmp-{}.tar.xz",
    "ImageMagick": "git@github.com:ImageMagick/ImageMagick.git",
    "libmicrohttpd": "https://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-{}.tar.gz",
    "libtomcrypt": "git@github.com:libtom/libtomcrypt.git",
    "openssl": "https://ftp.openssl.org/source/old/1.0.1/openssl-{}.tar.gz",
    "putty": "https://the.earth.li/~sgtatham/putty/latest/putty-{}.tar.gz",
    "sqlite": "https://www.sqlite.org/src/tarball/a26b6597/SQLite-a26b6597.tar.gz",
    "zlib": "https://zlib.net/zlib-{}.tar.gz" 
}
FINDUTILS_FORMAT = {
    "4.4.2": "tar.gz",
    "4.6.0": "tar.gz",
    "4.7.0": "tar.xz"
}
GIT_VERSION_TO_TAG = {
    "curl": {
        "7.71.1": "curl-7_71_1"
    },
    "ImageMagick": {
        "7.0.10-27": "7.0.10-27"
    },
    "libtomcrypt": {
        "1.18.2": "v1.18.2"
    }
}


# remove previous download
if os.path.exists(OUTPUT) and os.path.isdir(OUTPUT):
    shutil.rmtree(OUTPUT)
os.mkdir(OUTPUT)

# download source codes
all_packages = list(VERSIONS.keys())
for package in all_packages:
    os.mkdir(os.path.join(OUTPUT, package))
    for version in VERSIONS[package]:
        os.mkdir(os.path.join(OUTPUT, package, version))

        # for tar formats
        if package in ("binutils", "libmicrohttpd", "openssl", "putty", "zlib", "busybox", "sqlite") or\
            package in ("coreutils", "diffutils", "gmp") or\
            package == "findutils":

            if package == "findutils":
                url = URLS[package].format(version, FINDUTILS_FORMAT[version])
            elif package == "sqlite":
                url = URLS[package]
            elif package == "busybox":
                url = URLS[package].format(version.replace(".", "_"))
            else:
                url = URLS[package].format(version)

            # download tar file
            os.system("wget {} -P {}".format(
                url,
                os.path.join(OUTPUT, package, version)
            ))

            if package == "busybox":
                fname = "{}-{}.tar.gz".format(package, version.replace(".", "_"))
            elif package == "sqlite":
                fname = "SQLite-a26b6597.tar.gz"
            elif package == "findutils":
                fname = "findutils-{}.{}".format(version, FINDUTILS_FORMAT[version])
            else:
                if package in ("binutils", "libmicrohttpd", "openssl", "putty", "zlib", "busybox", "sqlite"):
                    fname = "{}-{}.tar.gz".format(package, version)
                else:
                    fname = "{}-{}.tar.xz".format(package, version)

            # extract source codes
            os.system("tar -xf {} -C {}".format(
                os.path.join(OUTPUT, package, version, fname),
                os.path.join(OUTPUT, package, version)
            ))

            # remove tar file
            os.system("rm -r {}".format(
                os.path.join(OUTPUT, package, version, fname)
            ))
        
        # for sources codes on git
        elif package in ("curl", "ImageMagick", "libtomcrypt"):

            # clone the repo with the given tag from git
            os.system("git clone --depth 1 --branch {} {} {}".format(
                GIT_VERSION_TO_TAG[package][version],
                URLS[package],
                os.path.join(OUTPUT, package, version, package)
            ))

        # for unhandled packages
        else:
            print("WARNING: package {} not processed.".format(package))
