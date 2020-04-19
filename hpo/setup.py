from setuptools import setup

setup(name='hpo',
      version='0.1',
      description='The funniest joke in the world',
      url='https://github.com/robertbennett1998/ga_for_hpo',
      author='Robert Bennett',
      author_email='robertbennett1998@outlook.com',
      license='MIT',
      packages=['hpo', 'hpo.strategies', 'hpo.strategies.genetic_algorithm', 'hpo.strategies.bayesian_method', 'hpo.strategies.random_search'],
      zip_safe=False)
