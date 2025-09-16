from setuptools import setup, find_packages

setup(
    name='opentargets_coloc_analysis',
    version='0.1.0',
    author='Oleg Vlasovets',
    author_email='oleg.vlasovets@helmholtz-munich.de',
    description='A module for computing GWAS-QTL colocalization extract and summary statistics.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/opentargets_coloc_analysis',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'duckdb',
        'pyarrow',
        'pandas',
        'numpy',
        'argparse',
        # Add other dependencies as needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)