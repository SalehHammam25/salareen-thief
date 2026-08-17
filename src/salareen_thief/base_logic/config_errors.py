"""Deterministic configuration error descriptions."""

from dataclasses import dataclass
from enum import StrEnum


class ConfigErrorCategory(StrEnum):
    FILE_NOT_FOUND = "file_not_found"
    FILE_READ_ERROR = "file_read_error"
    MALFORMED_JSON = "malformed_json"
    DUPLICATE_KEY = "duplicate_key"
    MISSING_KEY = "missing_key"
    INCORRECT_TYPE = "incorrect_type"
    BELOW_MINIMUM = "below_minimum"
    FIXED_VALUE_DEVIATION = "fixed_value_deviation"
    RELATIONSHIP_MISMATCH = "relationship_mismatch"
    OUT_OF_BOUNDS = "out_of_bounds"


@dataclass(frozen=True, slots=True)
class ConfigIssue:
    category: ConfigErrorCategory
    path: tuple[str | int, ...]
    message: str
