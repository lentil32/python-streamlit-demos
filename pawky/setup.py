from setuptools import find_packages, setup

setup(
    name='PAWKY',
    version='0.1.0',
    description='PAWKY - AWK interpreter written in Python',
    author='lentil32',
    author_email='lentil32@icloud.com',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'ply',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
