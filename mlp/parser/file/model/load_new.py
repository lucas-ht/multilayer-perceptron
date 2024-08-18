"""
This module provides functions to load the model from a pkl file.
"""

from __future__ import annotations
import sys
import logging
from time import perf_counter
from typing import TYPE_CHECKING, Optional, Tuple

import pkl
from pkl.utils import PklError

from . import (
    load_activation,
    load_initializer,
    load_layer,
    load_model,
    load_optimizer,
    load_regularizer,
    load_early_stopping
)

if TYPE_CHECKING:
    from . import (
        Model, Optimizer, EarlyStopping
    )


def load_new_model(path: str) -> Tuple[
        Model,
        int,
        Optimizer,
        Optional[EarlyStopping],
        Optional[int]
    ]:
    """
   Loads the model from a pkl file.

    Args:
        path (str): The path to the configuration file.

    Returns:
        Tuple[
            Model: The model.
            int: The number of epochs.
            Optimizer: The optimizer.
            Optional[EarlyStopping]: The early stopping.
            Optional[int]: The batch size.
        ]
    """

    logging.info('Loading configuration file.')
    start = perf_counter()

    try:
        config = pkl.load(path)

    except PklError as exception:
        logging.error('Cannot load configuration file: %s', exception)
        sys.exit(1)

    end = perf_counter()
    logging.info('Configuration loaded in %.2f seconds.', end - start)

    model = load_model(
        config.model.type,
        config.model
    )

    model.add([
        load_layer(
            layer.type,
            {
                'layer_size': layer.layer_size,
                'activation': load_activation(
                    layer.activation and layer.activation.type,
                    layer.activation
                ),
                'weight_initializer': load_initializer(
                    layer.weight_initializer and layer.weight_initializer.type,
                    layer.weight_initializer
                ),
                'bias_initializer': load_initializer(
                    layer.bias_initializer and layer.bias_initializer.type,
                    layer.bias_initializer
                ),
                'optimizer': load_optimizer(
                    layer.optimizer and layer.optimizer.type,
                    layer.optimizer
                ),
                'regularizer': load_regularizer(
                    layer.regularizer and layer.regularizer.type,
                    layer.regularizer
                ),
                'gradient_clipping': layer.gradient_clipping,
            }
        ) for layer in config.model.layers
    ])

    return (
        model,
        config.epochs,
        load_optimizer(
            config.optimizer and config.optimizer.type,
            config.optimizer
        ),
        load_early_stopping(
            config.early_stopping
        ),
        config.get('batch_size', None)
    )
