from setuptools import setup, find_packages


setup(
    name='django-test-html-form',
    version='0.1',
    description="Make your Django HTML form tests more explicit and concise.",
    long_description=open('README.rst').read(),
    keywords='django test assert',
    author='Dan Claudiu Pop',
    author_email='dancladiupop@gmail.com',
    url='https://github.com/danclaudiupop/assertHtmlForm',
    license='BSD License',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
    ],
)
