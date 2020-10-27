# -*- coding: utf-8 -*-

"""Templates for common tasks in ML and statistics."""

import numpy as np
from functools import partial
from .core import plot, bar, hist
import math

prob_hist = partial(
    hist,
    ylab="Observation Count (Valid)",
    xlab="Probability Bucket",
    bins=np.arange(0, 1.01, 0.05),
)
prob_hist.__doc__ = """Histogram for charting probabilities."""

pr_curve = partial(
    plot,
    labels=["Recall", "Precision"],
    xlab="Threshold Cutoff for Positive Class",
    ylab="Precision or Recall",
    title="Choosing a Threshold",
    markers=["g-", "g--", "b-", "b--", "r-", "r--"],
    pct_ticks=(False, True),
    grid=True,
)
pr_curve.__doc__ = """Dashed line chart for charting precision and recall curve."""


acc_vs_cov = partial(
    plot,
    xlab="Document Coverage",
    ylab="Document Accuracy",
    grid=True,
    markers=["k--", "ko-", "ks-"],
    xticks=np.arange(0, 1.05, 0.1),
    markersize=8,
    title="Accuracy vs. Document Coverage",
    pct_ticks=(True, True),
)

pr_curve.__doc__ = """Dashed line chart for accuracy and coverage."""

expected = [0.55, 0.65, 0.75, 0.85, 0.95]
grp_labels = [f"{10*math.floor(10*i)}-{10+10*math.floor(10*i)}%" for i in expected]
calib = partial(
    bar,
    x=grp_labels,
    xlab="Probability Bucket",
    ylab="Accuracy",
    ylim=[0.4, 1],
    grid=True,
    alpha=0.8,
    pct_ticks=True,
)

pr_curve.__doc__ = """For assessing model calibration."""
