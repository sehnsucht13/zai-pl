import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zai-pl",
    version="0.8.0",
    author="Yavor Konstantinov",
    author_email="ykonstantinov1@gmail.com",
    description="A small programming language written for learning purposes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sehnsucht13/zai-pl",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Programming Language :: Other",
        "Topic :: Software Development :: Interpreters",
    ],
    packages=['zai'],
    python_requires='>=3.6',
)
