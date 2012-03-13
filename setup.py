from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pool',
      version=version,
      description="mysql connection pool for gevent",
      long_description="""\
split from sqlalchemy""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='gevent mysql sqlalchemy',
      author='CMGS',
      author_email='ilskdw@gmail.com',
      url='https://github.com/CMGS/pool',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
