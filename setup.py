from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cryptobot",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A professional-grade Bitcoin trading bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cryptobot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-binance>=1.0.16",
        "ccxt>=2.8.0",
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "ta-lib>=0.4.24",
        "websockets>=10.3",
        "pandas-ta>=0.3.14b0",
        "scipy>=1.7.0",
        "aiohttp>=3.8.1",
        "python-dotenv>=0.19.0",
        "pyyaml>=6.0",
        "structlog>=21.1.0"
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.18.0',
            'pytest-cov>=3.0.0',
            'pytest-mock>=3.6.1',
            'mypy>=0.910',
            'black>=22.0.0',
            'isort>=5.9.0',
            'flake8>=4.0.0',
        ],
        'docs': [
            'sphinx>=4.5.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
    },
)