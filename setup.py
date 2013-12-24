from setuptools import setup, find_packages

# http://stackoverflow.com/questions/9352656/python-assertionerror-when-running-nose-tests-with-coverage
try:
    from multiprocessing import util # pyflakes.ignore
except ImportError:
    pass

setup(
    name='Flask-Misaka',
    version='0.2.0',
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
        'misaka',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose>=1.0',
        'mock',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)