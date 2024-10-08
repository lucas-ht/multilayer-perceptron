"""
Dense layer.
"""

import numpy as np

from .layer import Layer


class DenseLayer(Layer):
    """
    Dense layer.
    """

    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Computes the forward pass of the dense layer.
        """

        if self.weights is None or self.biases is None:
            raise ValueError('Layer not initialized.')

        self.input = x
        self.output = self.activation(
            np.dot(x, self.weights) + self.biases
        )

        return self.output


    def backward(self, gradient: np.ndarray) -> np.ndarray:
        """
        Computes the backward pass of the dense layer.
        """

        gradient = gradient * self.activation.gradient(self.output)

        input_gradient = np.dot(gradient, self.weights.T)
        self.weights_gradient = np.dot(self.input.T, gradient)
        self.biases_gradient = np.sum(gradient, axis=0, keepdims=True)

        if self.gradient_clipping is not None:
            self.clip(self.gradient_clipping)

        if self.regularizer is not None:
            self.weights_gradient += self.regularizer.gradient(self.weights)

        if self.optimizer is not None:
            self.optimize(self.optimizer)

        return input_gradient
