import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='iTunesLibrary',
    version='1.2.0',
    author='Steven Scholnick',
    author_email='scholnicks@gmail.com',
    description="Represents an iTunes library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords=['iTunesLibrary','iTunes'],
    url='https://github.com/scholnicks/itunes-library',
    download_url='https://github.com/scholnicks/itunes-library',
    py_modules=['iTunesLibrary'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License'
    ]
)
