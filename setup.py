from setuptools import setup

setup(name='tier3tools',
      version='0.1.0',
      description='Some tools for tier 3 to use',
      install_requires=[
          'requests',
          'gspread',
          'python-simple-hipchat'
      ])