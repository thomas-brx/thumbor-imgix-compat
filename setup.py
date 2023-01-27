from setuptools import setup, find_packages

setup(
    name="thumbor_imgix_compat",
    version="0.0.1",
    author="Car & Classic",
    description=("Translate imgix style requests to thumbor requests internally"),
    license="GPLv3",
    keywords=['thumbor', 'imgix compat'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "thumbor==7.*,>=7.0.6",
        "tornado==6.*,>=6.0.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
