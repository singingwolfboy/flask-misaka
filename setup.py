import re
from setuptools import setup, find_packages

version = ''
with open('flask_misaka.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='Flask-Misaka',
    version=version,
    url='https://github.com/singingwolfboy/flask-misaka/',
    license='MIT',
    author='David Baumgold',
    author_email='david@davidbaumgold.com',
    description='A pleasant interface between the Flask web framework and the Misaka Markdown parser.',
    zip_safe=False,
    packages=find_packages(),
    py_modules=['flask_misaka'],
    install_requires=[
        'Flask>=0.7',
        'misaka>=2.0,<3.0',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose>=1.0',
        'mock',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
