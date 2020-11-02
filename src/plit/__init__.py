# -*- coding: utf-8 -*-

"""Importing plotting functionality."""

from .core import subplots, bar, plot, hist
from .templates import pr_curve, prob_hist, acc_vs_cov, calib

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
