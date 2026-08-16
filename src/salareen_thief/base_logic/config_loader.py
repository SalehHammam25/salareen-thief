"""Local loading of validated Base Logic configuration."""

import json
from pathlib import Path

from .config_decode import DuplicateKeyError, decode_json
from .config_errors import ConfigErrorCategory as Category
from .config_errors import ConfigIssue
from .config_results import ConfigRejected, ConfigResult
from .config_validation import validate_config


def _rejected(
    category: Category, path: tuple[str | int, ...], message: str
) -> ConfigRejected:
    return ConfigRejected((ConfigIssue(category, path, message),))


def load_config(path: str | Path) -> ConfigResult:
    """Load and validate one local shared JSON file."""
    source = Path(path)
    try:
        text = source.read_text(encoding="utf-8")
    except FileNotFoundError:
        return _rejected(Category.FILE_NOT_FOUND, (), "file not found")
    except UnicodeDecodeError:
        return _rejected(Category.MALFORMED_JSON, (), "invalid UTF-8 JSON")
    except OSError:
        return _rejected(Category.FILE_READ_ERROR, (), "file could not be read")
    try:
        data = decode_json(text)
    except DuplicateKeyError as error:
        return _rejected(
            Category.DUPLICATE_KEY,
            (error.key,),
            f"duplicate key {error.key!r}",
        )
    except json.JSONDecodeError:
        return _rejected(Category.MALFORMED_JSON, (), "invalid JSON")
    return validate_config(data)
