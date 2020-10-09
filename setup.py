from setuptools import setup, find_packages
import contract

with open('requirements.txt') as f:
    required = f.read().splitlines()

setupconf = dict(
    name='contract',
    url='https://github.com/AlexeyPichugin/contract',
    license='MIT License',
    version=contract.__version__,
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
