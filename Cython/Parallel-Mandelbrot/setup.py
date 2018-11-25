from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "mandelbrot",
        ["mandelbrot.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]

setup(
    name='parallel-mandelbrot',
    ext_modules=cythonize(ext_modules),
)