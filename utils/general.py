from colorama import Fore, Style
from enum import Enum
from typing import Generic, TypeVar
import torch
import json
import pandas as pd
from pathlib import Path

from tqdm import tqdm as show_progress

def print_dict(some_dict):
    for key in some_dict:
        print(key, some_dict[key])

def print_section():
    print("*" * 20)

def print_green(some_string):
    print(Fore.GREEN)
    print(some_string)
    print(Style.RESET_ALL)

def colorize_string(color: str, string) -> str:
    return color + string + Style.RESET_ALL

def red(obj_to_color) -> str:
    return colorize_string(Fore.RED, str(obj_to_color))

def green(obj_to_color) -> str:
    return colorize_string(Fore.GREEN, str(obj_to_color))

def blue(obj_to_color) -> str:
    return colorize_string(Fore.BLUE, str(obj_to_color))

def magenta(obj_to_color) -> str:
    return colorize_string(Fore.MAGENTA, str(obj_to_color))

def unsupported_type_error(x):
    return RuntimeError("Unhandled type: {}".format(type(x).__name__))

def die(message):
    raise RuntimeError(message)

def tensor_shape(tensor: torch.Tensor):
    return list(tensor.shape)

class OptionState(Enum):
    Something = 1
    Nothing = 2


T = TypeVar('T')



class Option(Generic[T]):
    def __init__(self, val: T):
        if val is None:
            self.state = OptionState.Nothing
        else:
            self.state = OptionState.Something
            self.value = val

    def get_value(self) -> T:
        if self.state == OptionState.Nothing:
            raise RuntimeError("Trying to access nothing")
        return self.value

    def is_nothing(self) -> bool:
        return self.state == OptionState.Nothing

    def is_something(self) -> bool:
        return self.state == OptionState.Something


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("using device", device)


def pretty_string(obj) -> str:
    return json.dumps(obj=obj, indent=4)


def f1(TP, FP, FN) -> tuple[float, float, float]:
    """
    Given true-positives, false-positives, and false-negatives
    Returns the f1 score, precision, and recall
    """
    if (TP + FP) == 0:
        precision = None
    else:
        precision = TP / (TP + FP)
    if (FN + TP) == 0:
        recall = None
    else:
        recall = TP / (FN + TP)
    if (precision is None) or (recall is None) or ((precision + recall) == 0):
        return 0, 0, 0
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)
        return f1_score, precision, recall


def get_f1_score_from_sets(gold_set: set, predicted_set: set):
    true_positives = len(gold_set.intersection(predicted_set))
    false_positives = len(predicted_set.difference(gold_set))
    false_negatives = len(gold_set.difference(predicted_set))
    return f1(TP=true_positives, FP=false_positives, FN=false_negatives)


def open_make_dirs(file_path, mode):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    return open(file_path, mode)


def create_directory_structure(folder_path: str):
    """
    Creates all the directories on the given `folder_path`.
    Doesn't throw an error if directories already exist.
    Args:
        folder_path: the directory path to create.
    """
    Path(folder_path).mkdir(parents=True, exist_ok=True)



def assert_equals(lhs, rhs, message=""):
    assert lhs == rhs, f"{message} \n LHS: {lhs} \n RHS: {rhs}"


def contained_in(outside: tuple[int,int], inside: tuple[int,int]):
    return (outside[0] <= inside[0]) and \
           (inside[1] <= outside[1])


def create_json_file_with_data(output_file_path: str, data):
    assert output_file_path.endswith('.json')
    with open(output_file_path, 'w') as output_file:
        json.dump(data, output_file)


