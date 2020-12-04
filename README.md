## `plit`

`plit` is a [Matplotlib](https://matplotlib.org/) wrapper that automates the
undifferentiated heavy-lifting of writing boilerplate code while maintaining
the power and feel of Matplotlib. 

There are two components to `plit`:
* **Wrappers** around core chart types for standard line, scatter, histograms, and
  bar charts.
* **Templates** that are built from these primatives for specific analytic tasks.

Here is an example chart created with `plit`:

![](figures/calibration.png)

See the [PRFAQ](PRFAQ.md) for more information.

## Install

```
git clone https://github.com/awslabs/plit.git
cd plit
pip install -r requirements.txt
pip install .
```

Note: if you would like to install within a virtual environment, you can use:

```
conda create -n py37 python=3.7
conda activate py37
```

## Quick Start 

The best place to get started is the wrappers. There are three main wrappers
included in `plit`:

* `plot`: for line and scatter charts.
* `hist`: for histograms.
* `bar`: for bar charts.

### Create a line chart 

```
import numpy as np
x = [np.arange(10)]
y = [np.random.random(size=(10,1)) for _ in range(4)]

from plit import plot

plot(x, y, list("ABCD"), 'X', 'Y');
```

### Create a scatter chart

```
from plit import plot

x = [np.random.random(size=(10,1)) for _ in range(4)]
plot(x, y, list("ABCD"), 'X', 'Y', marker_type='o')
```

### Create a histogram

```
from plit import hist

x = [np.random.normal(size=(100,1)), np.random.gamma(shape=1, size=(100,1)) - 2]
hist(x, list("AB"), 'X', title='Histogram', bins=20)
```

### Create a bar chart

```
from plit import bar

x = [f"Group {i+1}"for i in range(6)]
y = [np.random.random(size=(6)) for _ in range(2)]
bar(x, y, list("AB"),'X', 'Y', colors=list("kb"), title='Bar Chart')
```

## Example notebooks 

The best way to go deeper is to look at the examples notebooks:

- [quick-start notebook](notebooks/quick-start.ipynb) gives an overview of core
  functionality including creating core chart types.
- [plit-vs-matplotlib](notebooks/plit-vs-matplotlib.ipynb) shows the difference
  between matplotlib and plit with a simple example.
- [creating-templates-file](notebooks/creating-templates.ipynb) demonstrates
  how to use partial functions to simplify and streamline your visualization
workflow.
- [accuracy-vs-coverage](notebooks/accuracy-vs-coverage.ipynb) shows an illustrative
  example using a template created for visualizing accuracy and coverage.
- [precision-vs-recall](notebooks/precision-recall-curve.ipynb) shows an illustrative
  example using a template created for choosing a threshold using precision and
recall. 
- [softmax-calibration](notebooks/softmax-calibration.ipynb) shows an illustrative
  example using a template created for evaluating the calibration for softmax
output. 
