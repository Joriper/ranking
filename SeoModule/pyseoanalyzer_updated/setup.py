from setuptools import setup, find_packages

setup(
    name='my_seo_module',
    version='0.1.0',
    description='A Python library for SEO analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'selenium'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
