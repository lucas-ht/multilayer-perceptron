"""
This module contains the dataset splitting function.
"""

import os

from sklearn.model_selection import train_test_split

from .parser.file import load_dataset, save_dataset


def split(dataset_path: str, test_size: float, out_dir: str) -> None:
    """
    Splits the dataset into training and test sets.

    Args:
        dataset (str): The dataset to split.
        test_size: (float) The size of the test set.
        out_dir (str): The output directory.
    """

    dataset = load_dataset(dataset_path)
    train, test = train_test_split(dataset, test_size=test_size)

    save_dataset(train,  os.path.join(out_dir, 'train.csv'))
    save_dataset(test,  os.path.join(out_dir, 'test.csv'))
