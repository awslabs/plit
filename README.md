## `plit`

`plit` is a Matplotlib wrapper that automates the undifferentiated heavy-lifting
of writing boilerplate code while maintaining the power and feel of Matplotlib. 

## Installation

### Install in your current environment

```
git clone https://github.com/awslabs/plit.git
cd plit
pip3 install -e .
```

### Example of install within a virtual environment

It is recommended to install within a virtual environment. Here is an example
of how to install within a conda environment.

```
git clone https://github.com/awslabs/plit.git
conda create -n py37 python=3.7
conda activate py37
cd plit
pip3 install -e .
```

## Usage 

See the [quick-start notebook](notebooks/quick-start.ipynb).

## FAQ

**Q: What is matplotlib?**

Matplotlib was invented in 2003 as an open-source, python-compatible
alternative to MATPLOT. It is the preeminent data visualization tool in python.
It operates as the base vizualization layer for many other vizualization
libraries, each of which with their own strengths and weaknesses. It is widely
used and liked and disliked.

**Q: Why another data visualization library?**

Matplotlib provides unmatched flexibility for static visualizations, however it
requires a significant amount if boiler-plate code to create basic
visualizations. Indeed, 95% of our time is spent on variations of four
visualizations: Line, Scatter, Bar, Histogram. This is the pain point that `plit`
addresses. `plit` automates the undifferentiated heavy-lifting of writing
boilerplate code while maintaining the power of Matplotlib. 

**Q: What are the goals of `plit`?**

1. *A Matplotlib wrapper so that you don’t have to recreate the “boring
stuff”.* Built-in usage of using the Matplotlib Object Oriented API. `**kwargs`
are fed directly to the underlying Matplotlib API. This means it as not
interactive. Want to make it easy to create your own templates.
2. *Wrappers specifically for line charts, scatter plots, histograms, and bar charts
including common options.* Indeed, 95% of time is spent on variations of
four visualizations: Line, Scatter, Bar, Histogram. Some of the common options
that come out of the box include multiple series, flexible specification of
differing marker types and colors, and mandatory legends. 
3. *Combine charts in arbitrary ways within the same figure grid, or use them on their own.*
4. *Templates for tasks in in analysis/evaluation/interpretation that are common for 
many projects. *For example, calibrating the softmax output from a ML model, or
choosing cutoff thresholds with precision/recall curves. 
5. *Graphs are close to publication quality out of the box.*
This means that have sensible defaults for things like figure size, font
sizes, marker size, DPI, etc....You may want to add your own styling and
customizations.

**Q: What functionality is included in `plit` core wrapper?**

The essence of the core wrapper consists of multi-series functionality for line
charts, scatter plots, histograms, and bar charts including markers, colors,
and legends. Graphs are close to publication quality out of the box via a
sensible default stylesheet. Additionally, `plit` provides a distribution of
statistical and ML-specific data visualizations.

**Q: Where does the name come from?**

The naming choice for `plit` is a wordplay on the common alias for Matplotlib,
plt (its only dependency).

**Q: How can I get involved?**

The first way is just to use it. It is available to use for your next project,
blog post, or white paper. The second way is to provide feedback. Looking for
feedback from Matplotlib users and non Matplotlib users. Want to understand how
it makes your life easier and what challenges or limitations you run into. The
last way is to contribute to it. Submit a snippet of code for a recent
visualization you did along with a small publicly available dataset. 
