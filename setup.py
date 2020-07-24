from pip._internal.req import parse_requirements
from operator import attrgetter
from os import path
from setuptools import setup, find_packages

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

def from_here(relative_path):
    return path.join(path.dirname(__file__), relative_path)

with open('requirements.txt') as f: 
    requirements = f.readlines() 

# source env/bin/activate

#? test.pypi
# rm -rf build dist shipapp.egg-info
# python setup.py sdist bdist_wheel 
# python3 -m twine upload --skip-existing --repository testpypi dist/*

# pip install --index-url https://test.pypi.org/simple/ --upgrade --no-cache-dir --extra-index-url=https://pypi.org/simple/ shipapp

#? pypi
# rm -rf build dist shipapp.egg-info
# python setup.py sdist bdist_wheel 
# python -m twine upload --skip-existing dist/*
# python -m twine upload dist/*

#? git steps
# git init
# git status
# git add .
# git init && git status && git add .
# git commit -m "alpha release v0.0.3.x"
# git push origin master

# git tag -a v0.0.3.x -m "alpha release v0.0.3.x"
# git push origin v0.0.3.x

#? delete tag remote and local
# git push --delete origin v0.0.3.x
#  git tag --delete v0.0.3.x

setup(
    name="shipapp",
    version="0.0.3.1",
    author="Yusuf Ahmed",
    author_email="yusufahmed172@gmail.com",
    packages=find_packages(exclude=['test_files']),
    description="The best way to move files between your devices",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/yusuf8ahmed/Ship",
    install_requires=['qrcode==6.1','pillow', 'pyngrok', 'loguru'],
    package_data={
        'ship': ['*.ico', "*.js", "*.css"],
    },
    entry_points ={ 
        'console_scripts': [ 
            'ship = ship.__main__:main'
        ] 
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords ='ship shipapp filetransfer shiplite shipu',
    python_requires='>=3',
    zip_safe = False
)