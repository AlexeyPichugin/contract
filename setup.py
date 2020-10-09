from setuptools import setup, find_packages
import re

with open('requirements.txt') as f:
    required = f.read().splitlines()

pattern = re.compile(r'__version__\s=\s[\"\'](\d*.\d*.\d*)[\"\']')
with open('pycont/__init__.py') as f:
    version = pattern.findall(f.read())[0]

setupconf = dict(
    name='pycont',
    url='https://github.com/AlexeyPichugin/pycont',
    license='MIT License',
    version=version,
    author='Alexey Pichugin',
    author_email="a.o.pichugin@outlook.com",
    description='Validate and generate data from templates',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Text Processing :: Filters',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={
        '': ['requirements.txt']
    },
    install_requires=required,
    zip_safe=False,
)

if __name__ == '__main__':
    setup(**setupconf)
