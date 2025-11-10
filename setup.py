from setuptools import setup, find_packages

setup(
    name="lognexus",
    version="1.0.0",
    description="A foundational sentence extraction tool for noisy drone logs.",
    author="Swardiantara Silalahi",
    author_email="swardyantara@gmail.com",
    packages=find_packages(),
    install_requires=[
        "simpletransformers",
        "pandas",
        "openpyxl",
        "tqdm",
        "torch"
        "transformers",
        "huggingface-hub",

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