[![Build Status](https://travis-ci.org/MalSemik/My_cache.svg?branch=main)](https://travis-ci.org/MalSemik/My_cache)
[![Python version](https://img.shields.io/badge/Python-3.7-blue)](https://www.python.org/downloads/release/python-370/)
[![Test](https://img.shields.io/badge/test-pytest-orange)](https://docs.pytest.org/en/stable/)
# My_cache
My_cache is a project to learn and better understand OOP.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install My_cache.

```bash
pip install -r requirements.txt
```

## Usage

```python
from my_cache.lesson_classes_cache import DictCache

cache = DictCache()
cache.cached_get("http://worldtimeapi.org/api/timezone/Europe/Warsaw").status_code
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)