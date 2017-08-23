from setuptools import setup

version = '0.1.1'
with open('README.rst', 'r') as f:
    long_description = f.read()

setup(name='slackmentions',
      version=version,
      description='Some functions for dealing with mentions in slack messages',
      long_description=long_description,

      author='Rick Henry',
      author_email='fredericmhenry@gmail.com',
      url='https://github.com/rickh94/slackmentions',

      tests_require=['pytest', 'pytest-cov'],

      license='MIT',
      python_requires='>=3',
      install_requires=['slackperson'],

      py_modules=['slackmentions'],

      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Operating System :: OS Independent',
          'Topic :: Communications :: Chat',
      ],
      keywords=['slack', 'text', 'messages', 'mentions'],

      )
