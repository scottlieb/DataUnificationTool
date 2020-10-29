import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='DUT',
    version='0.1',
    scripts=[],
    author='Pangea',
    author_email='amitaigottlieb@gmail.com',
    description='A genomic Data Unification Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/scottlieb/DataUnificationTool',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'

    )