from setuptools import setup, find_packages

version = '0.1.2'

setup(name='pool',
      version=version,
      description="general purposed connection pool for gevent, split from sqlalchemy",
      long_description="""\
when we use gevent and pymysql, mysql connections would create and release in a request lifetime. that's why we need a pool to manage mysql connections.""",
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
      tests_require=['nose'],
      test_suite='nose.collector',
      )
