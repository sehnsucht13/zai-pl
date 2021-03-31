[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html) [![zai](https://circleci.com/gh/sehnsucht13/zai-pl.svg?style=shield)](https://app.circleci.com/pipelines/github/sehnsucht13/zai-pl) [![PyPI version fury.io](https://badge.fury.io/py/zai-pl.svg)](https://pypi.python.org/pypi/zai-pl/) [![PyPI status](https://img.shields.io/pypi/status/zai-pl.svg)](https://pypi.python.org/pypi/zai-pl/)

# Zai

Zai is a small programming language which I wrote for fun. The language:

- Is Dynamically typed
- Is Entirely written in Python
- Supports classes
- Supports first-class functions
- Supports writing and importing modules

**NOTE:** This is a project made for both learning and fun. It is not meant to be used in serious projects.

# Installation
## Git
```bash
git clone https://github.com/sehnsucht13/zai-pl.git
cd zai-pl
# Start a REPL
python3 -m zai
# Run a file called FILENAME.zai
python3 -m zai FILENAME.zai
```
## Pip
```bash
# Install from pip
pip install --user zai-pl

# Start a REPL
zai-pl

# Run a file called FILENAME.zai
zai-pl FILENAME.zai
```
# Language Tour
A small tour of the language showing some of the features available along with language syntax can be found within the [docs/language-tour.md](https://github.com/sehnsucht13/zai-pl/blob/master/docs/language-tour.md) file.

# Missing Features and Future Improvements
Here is a list of the features which are currently missing but will be implemented in the future
## Language Features
- [ ] Basic class inheritance
- [ ] `for` loops
- [ ] Multiline comments
- [ ] Prefix/Postfix increment and decrement operators
- [ ] Printing more than one variable at a time.
- [ ] Floating Point Numbers
- [x] Add support for source code comments

## Dev Features
- [ ] Improve test coverage
- [ ] Automatic Deploy of new versions with CircleCI

# Internals and Documentation
- The language grammar can be found within the [docs/grammar](https://github.com/sehnsucht13/zai-pl/blob/master/docs/grammar) file.
- Some more in-depth details about the implementation(how objects are represented internally, environment...) can be found within [docs/architecture.md](https://github.com/sehnsucht13/zai-pl/blob/master/docs/architecture.md) file.

# Resources
Below are some of the resources which I found helpful while making this.
- [Crafting Interpreters](https://craftinginterpreters.com/ "Crafting Interpreters Homepage")
- [Modern Compiler Design](https://dickgrune.com/Books/MCD_2nd_Edition/ "Modern Compiler Design Textbook Page")
- [Max Bernstein's Blog](https://bernsteinbear.com/blog/ "bernsteinbear")
