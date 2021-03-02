# plit

`plit` is a [Matplotlib](https://matplotlib.org/) wrapper that automates the
undifferentiated heavy-lifting of writing boilerplate code while maintaining
the power and feel of Matplotlib. 

![](https://img.shields.io/badge/License-Apache%202.0-blue.svg) 
![](https://readthedocs.org/projects/plit/badge/?version=latest)
![](https://img.shields.io/badge/code_style-black-000000.svg)
<!-- ![](https://img.shields.io/github/v/release/awslabs/plit.svg) -->

There are two components to `plit`:
* **Wrappers** around core chart types for standard line, scatter, histograms, and
  bar charts.
* **Templates** that are built from these primatives for specific analytic tasks.

Here is an example chart created with `plit`:

![](https://github.com/awslabs/plit/raw/main/figures/calibration.png)

See the [PRFAQ](PRFAQ.md) for more information.

# Install

```Python
git clone https://github.com/awslabs/plit.git
cd plit
pip install -r requirements.txt
pip install .
```

# Quick Start 

The best place to get started is the wrappers. There are three main wrappers
included in `plit`. The naming is consistent with matplotlib. They work with
multi-series by default.

* `plot`: for line and scatter charts.
* `hist`: for histograms.
* `bar`: for bar charts.

## Create a line chart 

Create a line and scatter chart using the `plot` function.

```Python
import numpy as np
x = [np.arange(10)]
y = [np.random.random(size=(10,1)) for _ in range(4)]

from plit import plot

plot(x, y, list("ABCD"), 'X', 'Y');
```

## Create a scatter chart

By simply changing the `marker_type='o'` you switch from line to scatter chart.

```Python
from plit import plot

x = [np.random.random(size=(10,1)) for _ in range(4)]
plot(x, y, list("ABCD"), 'X', 'Y', marker_type='o')
```

## Create a histogram

Create a histogram using the `hist` function.

```Python
from plit import hist

x = [np.random.normal(size=(100,1)), np.random.gamma(shape=1, size=(100,1)) - 2]
hist(x, list("AB"), 'X', title='Histogram', bins=20)
```

## Create a bar chart

Create a grouped bar chart with the `bar` function.

```Python
from plit import bar

x = [f"Group {i+1}"for i in range(6)]
y = [np.random.random(size=(6)) for _ in range(2)]
bar(x, y, list("AB"),'X', 'Y', colors=list("kb"), title='Bar Chart')
```

## Example notebooks 

The best way to go deeper is to look at the examples notebooks:

- [quick-start notebook](https://github.com/awslabs/plit/blob/main/notebooks/quick-start.ipynb) gives an overview of core
  functionality including creating core chart types.
- [plit-vs-matplotlib](https://github.com/awslabs/plit/blob/main/notebooks/plit-vs-matplotlib.ipynb) shows the difference
  between matplotlib and plit with a simple example.
- [creating-templates-file](https://github.com/awslabs/plit/blob/main/notebooks/creating-templates.ipynb) demonstrates
  how to use partial functions to simplify and streamline your visualization
workflow.
- [accuracy-vs-coverage](https://github.com/awslabs/plit/blob/main/notebooks/accuracy-vs-coverage.ipynb) shows an illustrative
  example using a template created for visualizing accuracy and coverage.
- [precision-vs-recall](https://github.com/awslabs/plit/blob/main/notebooks/precision-recall-curve.ipynb) shows an illustrative
  example using a template created for choosing a threshold using precision and
recall. 
- [softmax-calibration](https://github.com/awslabs/plit/blob/main/notebooks/softmax-calibration.ipynb) shows an illustrative
  example using a template created for evaluating the calibration for softmax
output. 
