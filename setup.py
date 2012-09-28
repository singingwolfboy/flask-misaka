from setuptools import setup, find_packages

setup(
    name='Flask-Misaka',
    version='0.1',
    url='https://github.com/singingwolfboy/flask-misaka/',
    license='MIT',
    author='David Baumgold',
    author_email='david@davidbaumgold.com',
    description='Flask interface to Sundown, a markdown parsing library',
    packages=find_packages(),
    install_requires=[
        'Flask>=0.7',
        'misaka',
    ],
    tests_require=[
        'nose>=1.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='nose.collector'
)