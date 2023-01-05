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

```python
import spec

class MyModel(spec.Model):
    a: int
    b: str

foo = MyModel({"a": 1, "b": "bar"})

print(foo.a)
print(foo.b)
```

## License

`spec` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
