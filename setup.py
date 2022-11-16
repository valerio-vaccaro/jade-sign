from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'jade-sign',
    version = '0.1',
    author = 'Valerio Vaccaro',
    author_email = 'valerio.vaccaro@gmail.com',
    license = 'MIT',
    description = 'Derive addresses and sign messages using Blockstream Jade',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://gitlab.com/valerio-vaccaro/jade-sign',
    py_modules = ['jade'],
    include_package_data=True,
    package_data={'': ['*.ui']},
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        jade-sign=jade.main:main
    '''
)
