from setuptools import setup, find_packages

setup(
    name='Flask-Misaka',
    version='0.1',
    url='https://github.com/singingwolfboy/flask-misaka/',
    license='MIT',
    author='David Baumgold',
    author_email='david@davidbaumgold.com',
    description='A pleasant interface between the Flask web framework and the Misaka Markdown parser.',
    packages=find_packages(),
    install_requires=[
        'Flask>=0.7',
        'misaka',
    ],
    test_suite='nose.collector',
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
)