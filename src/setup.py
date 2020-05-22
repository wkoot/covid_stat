from setuptools import setup

setup(
    name='covid_stat',
    version='0.1.0',
    description='Covid stats comparison',
    long_description='',
    classifiers=[],
    author='wkoot',
    author_email='3715211+wkoot@users.noreply.github.com',
    url='https://github.com/wkoot/covid_stat',
    license='',
    packages=["fetchers", "util"],
    package_dir={'': '.'},
    entry_points={
        'console_scripts': [
            'fetcher=util.script:run_fetcher',
            'fetch_ecdc=fetchers.fetch_ecdc:fetch_ecdc',
        ],
    },
    include_package_data=True,
    install_requires=[
        "requests"
    ],
    zip_safe=False,
)
