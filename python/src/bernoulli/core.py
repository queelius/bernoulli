"""Core types for the bernoulli package.

This module defines the Bernoulli[T] generic type, which wraps a value of
type T together with quantified error rates. The full implementation lands
in subsequent plans; this is a placeholder sufficient to make the package
import and the smoke tests pass.
"""

from typing import Generic, TypeVar

T = TypeVar("T")


class Bernoulli(Generic[T]):
    """A value of type T paired with quantified error rates.

    Parameters
    ----------
    value : T
        The wrapped value.

    Notes
    -----
    This is a placeholder. Future plans add error rate parameters,
    composition operators, and the algebra documented in the book.
    """

    def __init__(self, value: T) -> None:
        self.value: T = value
