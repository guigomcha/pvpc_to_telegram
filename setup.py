import os
import shutil
from setuptools import find_packages, setup

# # Clone loggingbot repo
# shutil.rmtree('./loggingbot', ignore_errors=True)
# os.system('git clone -b master --single-branch https://github.com/Guillelerial/loggingbot.git')
# # Install loggingbot
# os.system('pip install -e loggingbot/')


setup(name='pvpcservice',
      description='Context Provider for PVPC Energy prices in Spain',
      version='master',
      python_requires='>=3.7',
      install_requires=[
            'bs4==0.0.1',
            'connexion[swagger-ui]==2.7.0',
            'matplotlib==3.3.0',
            'numpy==1.19.1',
            'pandas==1.1.0',
            'requests==2.24.0',
      ],
      author='Guillelerial',
      author_email='guillermo.gc1994@gmail.com',
      url='https://github.com/Guillelerial/pvpc_to_telegram.git',
      packages=find_packages())