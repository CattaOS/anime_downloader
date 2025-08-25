import json
from typing import Any

class FileIO:
    @staticmethod
    def read_json(file_name: str) -> list[Any] | dict[Any, Any]:
        """
        ### Read a json file

        Read json file and convert to dict

        The `file_name` can contain a path

        Args:
            - `file_name`: name of the json file

        Returns:
            - `dict`: dict of json file
        """
        with open(file_name, "r", encoding="UTF-8") as file:
            config = json.loads(file.read())
        return config

    @staticmethod
    def write_json(file_name: str, my_dict: dict[Any, Any]) -> None:
        """
        ### Write a json file

        Write a json file from a given dict

        The `file_name` can contain a path

        Args:
            - `file_name`: name for the json file
            - `my_dict`: dict to be converted in json
        """
        json_string = json.dumps(my_dict)
        with open(file_name, "w") as file:
            file.write(json_string)