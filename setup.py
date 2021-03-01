import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zai-pl",
    version="0.8.1",
    author="Yavor Konstantinov",
    author_email="ykonstantinov1@gmail.com",
    description="A small programming language written for learning purposes.",
    license="GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': ['zai-pl=zai.__main__:main'],
        },
    url="https://github.com/sehnsucht13/zai-pl",
    keywords=['zai', 'programming-language', 'zai-pl'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Programming Language :: Other",
        "Topic :: Software Development :: Interpreters",
    ],
    packages=['zai', 'zai/stdlib'],
    python_requires='>=3.6',
)
