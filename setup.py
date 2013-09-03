from distutils.core import setup

setup(name='exception-notifier',
      version='0.2.1',
      description='Notify uncaught exceptions in your Python code',
      author='Yongzhi Pan',
      author_email='panyongzhi@gmail.com',
      url='https://github.com/fossilet/exception-notifier',
      py_modules=['exception_notifier'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ]
      )
