import io
import os
import glob
import subprocess

from setuptools import setup, find_packages

import torch
from torch.utils.cpp_extension import CUDA_HOME, CppExtension, CUDAExtension

cwd = os.path.dirname(os.path.abspath(__file__))

version = '0.0.1'

def create_version_file():
    global version, cwd
    print('-- building version ' + version)
    version_path = os.path.join(cwd, 'version.py')
    with open(version_path, 'w') as f:
        f.write('"""This is version file"""')
        f.write("__version__ = '{}'\n".format(version))


requirements = [
    'tqdm'
]


def get_extensions():
    pass


if __name__ == '__main__':
    create_version_file()
    setup(
        name='torch_extension',
        version=version,
        author='muzhial',
        author_email='',
        url='',
        install_requires=requirements,
        packages=find_packages(exclude=[]),
        package_data={
            'torch_extension': [
                'lib/cpu/*.h',
                'lib/cpu/*.cpp'
            ]
        },
        ext_modules=get_extensions(),
        cmdclass={'build_ext': torch.utils.cpp_extension.BuildExtension}
    )
