from setuptools import setup, find_packages
import os

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

def readme():
    rst_text = read_md('README.md')
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'w+') as f:
        f.write(rst_text)

setup(
    name='dynmap_timemachine',
    version='0.9.3',
    description='Create extremely large images from Minecraft server\'s Dynmap plugin.',
    long_description=readme(),
    url='https://github.com/martinsik/minecraft-dynmap-timemachine',
    author='Martin Sikora',
    author_email='martin.sikora.ahoj@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Topic :: Games/Entertainment',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities',
    ],
    install_requires=[
        'Pillow',
        'requests',
    ],
    tests_require=[
        'nose',
    ],
    scripts=['dynmap-timemachine.py'],
    test_suite='tests',
)