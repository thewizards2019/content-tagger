import setuptools

setuptools.setup(
    name="datacurator-preference-tagger",
    version="0.0.1",
    packages=setuptools.find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'Flask',
        'confluent-kafka',
        'kafka',
        'flask_restful',
        'kafka-python',
        'requests'
    ],
    extras_require={
        'dev': [
            'pytest',
            'flake8',
            'pytest-cov',
            'bandit',
            'black'
        ]
    },
    entry_points={
        'console_scripts': [
            'app = app.cli:cli'
        ]
    },
)
