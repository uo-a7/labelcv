from pathlib import Path
import shutil

import yaml

from labelme.logger import logger


here = Path(__file__).parent


def update_dict(target_dict, new_dict, validate_item=None):
    for key, value in new_dict.items():
        if validate_item:
            validate_item(key, value)
        if key not in target_dict:
            logger.warn("Skipping unexpected key in config: {}".format(key))
            continue
        if isinstance(target_dict[key], dict) and isinstance(value, dict):
            update_dict(target_dict[key], value, validate_item=validate_item)
        else:
            target_dict[key] = value


# -----------------------------------------------------------------------------


def get_config():
    default_config_file = here.joinpath("default_config.yaml").as_posix()
    with open(default_config_file, 'r') as f:
        config = yaml.safe_load(f)

    # save default config to ~/.labelmerc
    user_config_file = Path.home().joinpath(".labelmerc").as_posix()
    if not Path(user_config_file).exists():
        logger.info("Copy config file from {} to {}".format(default_config_file, user_config_file))
        shutil.copy(default_config_file, user_config_file)

    with open(user_config_file, 'r') as f:
        logger.info("Loading config file from: {}".format(user_config_file))
        config_from_yaml = yaml.safe_load(f)

    update_dict(config, config_from_yaml, validate_item=validate_config_item)

    return config


def validate_config_item(key, value):
    if key == "validate_label" and value not in [None, "exact"]:
        raise ValueError(
            "Unexpected value for config key 'validate_label': {}".format(
                value
            )
        )
    if key == "shape_color" and value not in [None, "auto", "manual"]:
        raise ValueError(
            "Unexpected value for config key 'shape_color': {}".format(value)
        )
    if key == "labels" and value is not None and len(value) != len(set(value)):
        raise ValueError(
            "Duplicates are detected for config key 'labels': {}".format(value)
        )


# def get_config(config_file_or_yaml=None, config_from_args=None):
#     # 1. default config
#     config = get_default_config()
#
#     # 2. specified as file or yaml
#     if config_file_or_yaml is not None:
#         config_from_yaml = yaml.safe_load(config_file_or_yaml)
#         if not isinstance(config_from_yaml, dict):
#             with open(config_from_yaml) as f:
#                 logger.info(
#                     "Loading config file from: {}".format(config_from_yaml)
#                 )
#                 config_from_yaml = yaml.safe_load(f)
#         update_dict(
#             config, config_from_yaml, validate_item=validate_config_item
#         )
#
#     # 3. command line argument or specified config file
#     if config_from_args is not None:
#         update_dict(
#             config, config_from_args, validate_item=validate_config_item
#         )
#
#     return config
