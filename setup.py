import os
import sys
import platform
import sysconfig
from setuptools import setup, Extension, find_packages
from setuptools.dist import Distribution
import setuptools.command.build_ext
import setuptools.command.install
import setuptools.command.sdist

################################################################################
# At first, we need to check platform version
################################################################################

if sys.version_info < (3,):
    print("Python 2 has reached end-of-life and is no longer supported by TEST.")
    sys.exit(-1)
if sys.platform == 'win32' and sys.maxsize.bit_length() == 31:
    print("32-bit Windows Python runtime is not supported. Please switch to 64-bit Python.")
    sys.exit(-1)
python_min_version = (3, 6, 2)
python_min_version_str = '.'.join(map(str, python_min_version))
if sys.version_info < python_min_version:
    print("You are using Python {}. Python >={} is required.".format(
        platform.python_version(), python_min_version_str))
    sys.exit(-1)

################################################################################
# Parameters parsed from environment
################################################################################

VERBOSE_SCRIPT = True
RUN_BUILD_DEPS = True
EMIT_BUILD_WARNING = False
RERUN_CMAKE = False
CMAKE_ONLY = False
filtered_args = []
for i, arg in enumerate(sys.argv):
    if arg == '--cmake':
        RERUN_CMAKE = True
        continue
    if arg == '--cmake-only':
        # Stop once cmake terminates. Leave users a chance to adjust build
        # options.
        CMAKE_ONLY = True
        continue
    if arg == 'rebuild' or arg == 'build':
        arg = 'build'  # rebuild is gone, make it build
        EMIT_BUILD_WARNING = True
    if arg == "--":
        filtered_args += sys.argv[i:]
        break
    if arg == '-q' or arg == '--quiet':
        VERBOSE_SCRIPT = False
    if arg in ['clean', 'egg_info', 'sdist']:
        RUN_BUILD_DEPS = False
    filtered_args.append(arg)
sys.argv = filtered_args
if VERBOSE_SCRIPT:
    def report(*args):
        print(*args)
else:
    def report(*args):
        pass
    # Make distutils respect --quiet too
    setuptools.distutils.log.warn = report
# Constant known variables used throughout this file
cwd = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(cwd, "lib")
third_party_path = os.path.join(cwd, "third_party")
build_dir = os.path.join(cwd, "build")
# CMAKE: full path to python library
cmake_python_library = "{}/{}".format(
        sysconfig.get_config_var("LIBDIR"),
        sysconfig.get_config_var("INSTSONAME"))
cmake_python_include_dir = sysconfig.get_path("include")

################################################################################
# Version, create_version_file, and package_name
################################################################################

package_name = os.getenv('TEST_PACKAGE_NAME', 'mytest')
version = '0.0.1'
report("Building wheel {}-{}".format(package_name, version))

################################################################################
# Print info
################################################################################

report('VERBOSE_SCRIPT: ', VERBOSE_SCRIPT)
report('RUN_BUILD_DEPS: ', RUN_BUILD_DEPS)
report('EMIT_BUILD_WARNING: ', EMIT_BUILD_WARNING)
report('RERUN_CMAKE: ', RERUN_CMAKE)
report('CMAKE_ONLY: ', CMAKE_ONLY)
report('ARGV: ', sys.argv)
report('cwd: ', cwd)
report('lib_path: ', lib_path)
report('third_party_path: ', third_party_path)
report('build_dir: ', build_dir)
report('cmake_python_library: ', cmake_python_library)
report('cmake_python_include_dir: ', cmake_python_include_dir)
