#!/usr/bin/env python
import glob
import os
import sys
import codecs
from setuptools import setup, Extension

# monkey-patch for parallel compilation
def parallelCCompile(self, sources, output_dir=None, macros=None, include_dirs=None, debug=0, extra_preargs=None, extra_postargs=None, depends=None):
    # those lines are copied from distutils.ccompiler.CCompiler directly
    macros, objects, extra_postargs, pp_opts, build = self._setup_compile(output_dir, macros, include_dirs, sources, depends, extra_postargs)
    cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)
    # parallel code
    N=8 # number of parallel compilations
    import multiprocessing.pool
    def _single_compile(obj):
        try: src, ext = build[obj]
        except KeyError: return
        self._compile(obj, src, ext, cc_args, extra_postargs, pp_opts)
    # convert to list, imap is evaluated on-demand
    list(multiprocessing.pool.ThreadPool(N).imap(_single_compile,objects))
    return objects
import distutils.ccompiler
#distutils.ccompiler.CCompiler.compile=parallelCCompile


ltp_root="ltp"
ltp_source=os.path.join(ltp_root, "src")
ltp_thirdparty=os.path.join(ltp_root, "thirdparty")
patch_root="patch"
patch_libs=os.path.join(patch_root, "libs", "python", "src")

excluded_sources = (
        os.path.join(ltp_source, "segmentor", "otcws.cpp"),
        os.path.join(ltp_source, "segmentor", "io.cpp"),
        os.path.join(ltp_source, "segmentor", "segmentor_frontend.cpp"),
        os.path.join(ltp_source, "segmentor", "customized_segmentor_frontend.cpp"),
        os.path.join(ltp_source, "postagger", "otpos.cpp"),
        os.path.join(ltp_source, "postagger", "io.cpp"),
        os.path.join(ltp_source, "postagger", "postagger_frontend.cpp"),
        os.path.join(ltp_source, "ner", "otner.cpp"),
        os.path.join(ltp_source, "ner", "io.cpp"),
        os.path.join(ltp_source, "ner", "ner_frontend.cpp"),
        os.path.join(ltp_source, "parser.n", "main.cpp"),
        os.path.join(ltp_source, "parser.n", "io.cpp"),
        os.path.join(ltp_source, "parser.n", "parser_frontend.cpp"),
        os.path.join(ltp_source, "srl", "Pi", "pred.cpp"),
        os.path.join(ltp_source, "srl", "Pi", "train.cpp"),
        os.path.join(ltp_source, "srl", "Srl", "pred.cpp"),
        os.path.join(ltp_source, "srl", "Srl", "train.cpp"),
        os.path.join(ltp_source, "srl", "tool", "merge.cpp"),
        os.path.join(ltp_thirdparty, "maxent", "train.cpp"),
        os.path.join(ltp_thirdparty, "maxent", "predict.cpp"),
        os.path.join(ltp_thirdparty, "dynet", "dynet", "cuda.cc")
        )

sources = [os.path.join("src", "pyltp.cpp")]
sources += glob.glob(os.path.join(ltp_thirdparty, "boost", "libs", "regex", "src", "*.cpp"))
sources += glob.glob(os.path.join(ltp_thirdparty, "boost", "libs", "program_options", "src", "*.cpp"))
sources += glob.glob(os.path.join(ltp_thirdparty, "boost", "libs", "serialization", "src", "*.cpp"))
sources += glob.glob(os.path.join(ltp_thirdparty, "boost", "libs", "smart_ptr", "src", "*.cpp"))
sources += glob.glob(os.path.join(ltp_thirdparty, "dynet", "dynet", "*.cc"))
sources += glob.glob(os.path.join(ltp_thirdparty, "maxent", "*.cpp"))
sources += glob.glob(os.path.join(ltp_source, "splitsnt", "*.cpp"))
sources += glob.glob(os.path.join(ltp_source, "segmentor", "*.cpp"))
sources += glob.glob(os.path.join(ltp_source, "postagger", "*.cpp"))
sources += glob.glob(os.path.join(ltp_source, "ner", "*.cpp"))
sources += glob.glob(os.path.join(ltp_source, "parser.n", "*.cpp"))
sources += glob.glob(os.path.join(ltp_source, "srl", "*.cpp"))
sources += glob.glob(os.path.join(ltp_source, "srl", "common", "model", "*.cpp"))
sources += glob.glob(os.path.join(ltp_source, "srl", "common", "structure", "*.cpp"))
sources += glob.glob(os.path.join(ltp_source, "srl", "include", "base", "*.cpp"))
sources += glob.glob(os.path.join(ltp_source, "srl", "Srl", "model", "*.cpp"))
sources += glob.glob(os.path.join(ltp_source, "srl", "tool", "model", "*.cpp"))
sources += glob.glob(os.path.join(patch_libs, "*.cpp"))
sources += glob.glob(os.path.join(patch_libs, "object", "*.cpp"))
sources += glob.glob(os.path.join(patch_libs, "converter", "*.cpp"))

sources = [source for source in sources if source not in excluded_sources]

includes = [
        'ltp/include/',
        'ltp/thirdparty/boost/include/',
        'ltp/thirdparty/dynet/',
        'ltp/thirdparty/eigen/',
        'ltp/thirdparty/maxent/',
        'ltp/src/',
        'ltp/src/splitsnt',
        'ltp/src/segmentor/',
        'ltp/src/postagger/',
        'ltp/src/ner/',
        'ltp/src/parser.n/',
        'ltp/src/srl/',
        'ltp/src/srl/common/',
        'ltp/src/srl/include/',
        'ltp/src/srl/Pi/',
        'ltp/src/srl/Srl/',
        'ltp/src/srl/tool/',
        'ltp/src/utils/',
        'patch/include/'
        ]

extra_compile_args = []

if sys.platform == 'win32':
    extra_compile_args += ['/DNOMINMAX', '/DBOOST_PYTHON_SOURCE', '/DBOOST_PYTHON_STATIC_LIB', '/DBOOST_ALL_NO_LIB', '/D_WINDOWS', '/EHsc']
elif sys.platform == 'darwin':
    os.environ['CC'] = 'clang++'
    os.environ['CXX'] = 'clang++'
    extra_compile_args += ['-std=c++11',
                           '-Wno-c++11-narrowing',
                           '-Wno-unused-local-typedef',
                           '-Wno-unused-variable',
                           '-Wno-reorder',
                           '-Wno-sign-compare',
                           '-stdlib=libc++']
else:
    extra_compile_args += ['-std=c++0x']

if not 'MACOSX_DEPLOYMENT_TARGET' in os.environ:
    os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.12'

ext_modules = [Extension('pyltp',
    include_dirs=includes,
    language='c++',
    sources=sources,
    extra_compile_args=extra_compile_args
    )]

setup(
    name='pyltp',
    version='0.2.1',
    description='pyltp: the python extension for LTP',
    long_description=codecs.open('README.md', encoding='utf-8').read(),
    author='Yijia Liu, Zixiang Xu, Yang Liu',
    author_email='ltp-cloud@googlegroups.com',
    url='https://github.com/HIT-SCIR/pyltp',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Linguistic",
    ],
    zip_safe=False,
    #packages=['pyltp'],
    ext_modules=ext_modules
)
