"""Deterministic structural extraction of Base Logic fields."""

from typing import Any

from .config_errors import ConfigErrorCategory as Category
from .config_errors import ConfigIssue
from .config_schema import FIELD_KINDS, REQUIRED_SECTIONS

Path = tuple[str, ...]


def _issue(category: Category, path: Path, message: str) -> ConfigIssue:
    return ConfigIssue(category, path, message)


def _normalize(value: Any, kind: str, path: Path) -> tuple[Any, ConfigIssue | None]:
    if kind == "int":
        if type(value) is int:
            return value, None
        return None, _issue(Category.INCORRECT_TYPE, path, "expected integer")
    if kind == "string":
        if type(value) is str:
            return value, None
        return None, _issue(Category.INCORRECT_TYPE, path, "expected string")
    if kind == "coordinate":
        valid = (
            type(value) is list
            and len(value) == 2
            and all(type(part) is int for part in value)
        )
        if valid:
            return tuple(value), None
        return None, _issue(
            Category.INCORRECT_TYPE,
            path,
            "expected two non-boolean integers",
        )
    valid = type(value) is list and all(type(item) is str for item in value)
    if valid:
        return tuple(value), None
    return None, _issue(Category.INCORRECT_TYPE, path, "expected string array")


def extract_values(data: Any) -> tuple[dict[Path, Any], list[ConfigIssue]]:
    """Extract typed values and ordered structural issues."""
    values: dict[Path, Any] = {}
    issues: list[ConfigIssue] = []
    if type(data) is not dict:
        return values, [
            _issue(Category.INCORRECT_TYPE, (), "expected JSON object")
        ]
    for section_name, fields in REQUIRED_SECTIONS:
        if section_name not in data:
            issues.append(
                _issue(Category.MISSING_KEY, (section_name,), "missing section")
            )
            continue
        section = data[section_name]
        if type(section) is not dict:
            issues.append(
                _issue(
                    Category.INCORRECT_TYPE,
                    (section_name,),
                    "expected object",
                )
            )
            continue
        for field in fields:
            path = (section_name, field)
            if field not in section:
                issues.append(_issue(Category.MISSING_KEY, path, "missing key"))
                continue
            normalized, error = _normalize(
                section[field], FIELD_KINDS[path], path
            )
            if error:
                issues.append(error)
            else:
                values[path] = normalized
    return values, issues
