from setuptools import setup, find_packages
from pypandoc import convert

def readme():
    return convert('README.md', 'rst')

setup(
    name='minecraft-dynmap-timemachine',
    version='0.9.0',
    description='Create extremely large images from Minecraft server\'s Dynmap plugin.',
    long_description=readme(),
    url='https://github.com/martinsik/minecraft-dynmap-timemachine',
    author='Martin Sikora',
    author_email='martin.sikora.ahoj@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities',
    ],
    install_requires=[
        'Pillow',
    ],
    test_suite='tests',
)