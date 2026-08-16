"""Authoritative Stage 1 configuration constraints."""

BOARD_FIELDS = (
    "grid_size",
    "num_agents",
    "thief_start",
    "cop_start",
    "axis_origin_corner",
    "axis_start_index",
)
MOVEMENT_FIELDS = (
    "move_set",
    "max_barriers",
    "max_moves",
    "survival_threshold",
)
SCORING_FIELDS = (
    "capture_cop",
    "capture_thief",
    "survival_cop",
    "survival_thief",
    "technical_loss",
)
REQUIRED_SECTIONS = (
    ("board_and_agents", BOARD_FIELDS),
    ("movement_and_barriers", MOVEMENT_FIELDS),
    ("scoring", SCORING_FIELDS),
)
FIELD_KINDS = {
    ("board_and_agents", "grid_size"): "int",
    ("board_and_agents", "num_agents"): "int",
    ("board_and_agents", "thief_start"): "coordinate",
    ("board_and_agents", "cop_start"): "coordinate",
    ("board_and_agents", "axis_origin_corner"): "string",
    ("board_and_agents", "axis_start_index"): "int",
    ("movement_and_barriers", "move_set"): "string_tuple",
    ("movement_and_barriers", "max_barriers"): "int",
    ("movement_and_barriers", "max_moves"): "int",
    ("movement_and_barriers", "survival_threshold"): "int",
    ("scoring", "capture_cop"): "int",
    ("scoring", "capture_thief"): "int",
    ("scoring", "survival_cop"): "int",
    ("scoring", "survival_thief"): "int",
    ("scoring", "technical_loss"): "int",
}
FIXED_VALUES = (
    (("board_and_agents", "num_agents"), 2),
    (("movement_and_barriers", "move_set"), ("N", "S", "E", "W", "STAY")),
    (("scoring", "capture_cop"), 20),
    (("scoring", "capture_thief"), 5),
    (("scoring", "survival_cop"), 5),
    (("scoring", "survival_thief"), 10),
    (("scoring", "technical_loss"), 0),
)
MINIMUM_VALUES = (
    (("board_and_agents", "grid_size"), 7),
    (("movement_and_barriers", "max_barriers"), 14),
    (("movement_and_barriers", "max_moves"), 35),
    (("movement_and_barriers", "survival_threshold"), 35),
)
