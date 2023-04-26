# spec

![PyPI - Version](https://img.shields.io/badge/python-3.11-%231182c3)

A statically typed data structure validator with support for advance features.

-----

**Table of Contents**

- [Installation](#installation)
- [How To Use](#usage)
- [License](#license)

## Installation

```console
$ pip install git+https://github.com/zomatree/spec
```

# Usage

### A simple class
```python
class MyModel(spec.Model):
    a: int
    b: str

foo = MyModel({"a": 1, "b": "bar"})

print(foo.a)
print(foo.b)
```

### Nested classes

```python
class Inner(spec.Model):
    v: int

class Outer(spec.Model):
    inner: Inner
    other: str

data = Outer({"inner": {"v": 1}, "other": "foo"})
```

### Renaming

```python
from typing import Annotated

class MyModel(spec.Model):
    my_foo = Annotated[int, spec.rename("myFoo")]

data = MyModel({"myFoo": 1})
```

## License

`spec` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
