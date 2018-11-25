import sys
from distutils.core import setup, Extension
from Cython.Build import cythonize

compile_args = ['-g', '-std=c++14']

basics_module = Extension('PyGoL',
                          sources=['PyGoL.pyx'],
                          extra_compile_args=compile_args,
                          language='c++')

setup(
    name='NewPyGameOfLifeXL',
    packages=['PyGoL'],
    ext_modules=cythonize(basics_module),
    requires=['Cython', 'pygame']
)
