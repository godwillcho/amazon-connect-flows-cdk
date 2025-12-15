from setuptools import setup, find_packages

setup(
    name="amazon-connect-flows-cdk",
    version="1.0.0",
    description="CDK stack for deploying Amazon Connect flows",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(exclude=["tests*", "scripts*", "docs*", "examples*"]),
    install_requires=[
        "aws-cdk-lib>=2.120.0",
        "constructs>=10.0.0,<11.0.0",
        "boto3>=1.34.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
