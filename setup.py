from setuptools import setup, find_packages

setup(
    name="lognexus",
    version="1.0.0",
    description="A foundational sentence extraction tool for noisy drone logs.",
    author="Swardiantara Silalahi",
    author_email="swardyantara@gmail.com",
    packages=find_packages(),
    install_requires=[
        "simpletransformers==0.70.1",
        "pandas==2.2.2",
        "openpyxl==3.1.5",
        "tqdm==4.66.4",
        "torch==2.3.1"
        "transformers==4.42.3",
        "huggingface-hub==0.31.4",

    ],
    entry_points={
        'console_scripts': [
            'lognexus=lognexus.cli:main',
            'lognexus-download=lognexus.utils:download_model_cli',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Digital Forensics",
        "Topic :: Scientific/Engineering :: Log Analysis",
    ],
)