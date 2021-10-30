# -*- coding: utf-8 -*-

"""Helper classes for subplots."""

import csv
import math
import warnings
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageChops


class SimpleMatrixPlotter(object):
    """A simple helper class to fill-in subplot one after another.

    Sample usage using `add()`:

    >>> import pandas as pd
    >>> from plit.subplots import SimpleMatrixPlotter
    >>>
    >>> df = pd.DataFrame({'a': [1,1,1,2,2,2,3,3,3,4,4]})
    >>> gb = df.groupby(by=['a'])
    >>>
    >>> smp = SimpleMatrixPlotter(gb.ngroups)
    >>> for group_name, df_group in gb:
    >>>     ax, _ = smp.add(df_group.plot)
    >>>     assert ax == _
    >>>     ax.set_title(f"Item={group_name}")
    >>> # smp.trim(); plt.tight_layout(); plt.show()  # Uncomment to show the plot.
    >>> smp.savefig("/tmp/testfigure.png")  # After this, figure & axes are gone.

    Alternative usage using `pop()`:

    >>> smp = SimpleMatrixPlotter(gb.ngroups)
    >>> for group_name, df_group in gb:
    >>>     ax = smp.pop()
    >>>     df_group.plot(ax=ax, title=f"Item={group_name}")
    >>> # smp.trim(); plt.tight_layout(); plt.show(); # Uncomment to show the plot.
    >>> smp.savefig("/tmp/testfigure.png")  # After this, figure & axes are gone.

    Attributes:
        i (int): Index of the currently free subplot
    """

    def __init__(
        self,
        figcount,
        ncols: Optional[int] = None,
        figsize=(6.4, 4.8),
        dpi=100,
        **kwargs,
    ):
        """Initialize a ``SimpleMatrixPlotter`` instance.

        Args:
            figcount (int): Total number of subplots.
            ncols (int, optional): Number of columns. Passing None means to set
                to sqrt(figcount) clipped at 5 and 20. Defaults to None.
            figsize (tuple, optional): size per subplot, see ``figsize`` for matplotlib.
                Defaults to (6.4, 4.8).
            dpi (int, optional): dot per inch, see ``dpi`` in matplotlib.
                Defaults to 100.
            kwargs (optional): Keyword argumetns for plt.subplots, but these are
                ignored and will be overriden: ``ncols``, ``nrows``, ``figsize``,
                ``dpi``.
        """
        # Initialize subplots
        if ncols is None:
            ncols = min(max(5, int(math.sqrt(figcount))), 20)
        nrows = figcount // ncols + (figcount % ncols > 0)

        kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in {"nrows", "ncols", "figsize", "dpi"}
        }
        self.fig, _ = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=(figsize[0] * ncols, figsize[1] * nrows),
            dpi=dpi,
            **kwargs,
        )
        self.axes = self.fig.axes  # Cache list of axes returned by self.fig.axes
        self.fig.subplots_adjust(hspace=0.35)
        self._i = 0  # Index of the current free subplot

        # Warn if initial pixels exceed matplotlib limit.
        pixels = np.ceil(self.fig.get_size_inches() * self.fig.dpi).astype("int")
        if (pixels > 2 ** 16).any():
            warnings.warn(
                f"Initial figure is {pixels} pixels, and at least one dimension "
                "exceeds 65536 pixels."
            )

    @property
    def i(self):
        """:int: Index of the earliest unused subplot."""
        return self._i

    @property
    def ncols(self):
        """Return the number of columns."""
        if len(self.axes) < 1:
            return 0

        ax = self.axes[0]
        if hasattr(ax, "get_gridspec"):
            # matplotlib>=3.4.0
            return ax.get_gridspec().ncols
        else:
            return ax.get_geometry()[1]

    @property
    def nrows(self):
        """Return the number of rows."""
        if len(self.axes) < 1:
            return 0

        ax = self.axes[0]
        if hasattr(ax, "get_gridspec"):
            # matplotlib>=3.4.0
            return ax.get_gridspec().nrows
        else:
            return ax.get_geometry()[0]

    @property
    def shape(self):
        """Return a tuple of (rows, cols)."""
        return (self.nrows, self.ncols)

    def add(self, plot_fun, *args, **kwargs) -> Tuple[plt.Axes, Any]:
        """Fill the current free subplot using `plot_fun()`, and set the axes
        and figure as the current ones.

        Args: plot_fun (callable): A function that must accept `ax` keyword
            argument.

        Returns: (plt.Axes, Any): a tuple of (axes, return value of plot_fun).
        """
        ax = self.pop()
        retval = plot_fun(*args, ax=ax, **kwargs)
        return ax, retval

    def pop(self) -> plt.Axes:
        """Get the next axes in this subplot, and set it and its figure as the
        current axes and figure, respectively.

        Returns: plt.Axes: the next axes
        """
        # TODO: extend with new subplots:
        # http://matplotlib.1069221.n5.nabble.com/dynamically-add-subplots-to-figure-td23571.html#a23572
        ax = self.axes[self._i]
        plt.sca(ax)
        plt.figure(self.fig.number)
        self._i += 1
        return ax

    def trim(self):
        """Delete unused subplots."""
        for ax in self.axes[self._i :]:
            self.fig.delaxes(ax)
        self.axes = self.axes[: self._i]

    def savefig(self, *args, **kwargs):
        """Save plotted subplots, then destroy the underlying figure.

        Subsequent operations are undefined and may raise errors.
        """
        self.trim()
        kwargs["bbox_inches"] = "tight"
        self.fig.savefig(*args, **kwargs)
        # Whatever possible ways to release figure
        self.fig.clf()
        plt.close(self.fig)
        del self.fig
        self.fig = None


# NOTE: to simplify the pager implementation, just destroy-old-and-create-new
#       SimpleMatrixPlotter instances. Should it be clear that the overhead of
#       this approach is not acceptable, then reset-and-reuse shall be
#       considered.
#
# As of now, using pager does cap the memory usage (in addition to making sure not
# to hit matplotlib limit of 2^16 pixels per figure dimension). The following
# benchmark to render 10 montages at 100 subplots/montage tops at 392MB RSS,
# when measured on MBP early 2015 model, Mojave 10.14.6, python-3.7.6.
#
# import pandas as pd
# from numpy.random import rand
# from plit.subplots import MontagePager
# mp = MontagePager()
# for i in range(1000):
#     title = f"chart-{i:04d}"
#     pd.Series(rand(6)).plot(ax=mp.pop(title), title=title)
# mp.savefig()
class MontagePager(object):
    """A pager to group and save subplots into multiple montage image files."""

    def __init__(
        self,
        path: Path = Path("."),
        prefix: str = "montage",
        page_size: int = 100,
        savefig_kwargs: Dict[str, Any] = {},
        **kwargs,
    ):
        """Render plots to one or more montages.

        Each montage has at most ``page_size`` subplots. This pager
        automatically saves an existing montage on overflow, which occurs when
        the montage is full and an attempt was made to add a new subplot to it.
        After the existing montage is saved, a new blank montage is created, and
        the new subplot will be added to it. Callers are expected to explicitly
        save the last montage.

        NOTE: if title has multiple lines, individual images are not chopped correctly.
        As such, please make sure title fits in a single line.

        >>> import pandas as pd
        >>> from pathlib import Path
        >>> from numpy.random import rand
        >>> from plit.subplots import MontagePager
        >>>
        >>> mp = MontagePager(Path('output'), savefig_kwargs=dict(transparent=False))
        >>> for i in range(128):
        >>>     title = f"chart-{i:04d}"
        >>>     pd.Series(rand(6)).plot(ax=mp.pop(title), title=title)
        >>> mp.savefig()  # Save the last montage which may be partially filled.

        Args:
            prefix (str, optional): Prefix of output filenames.
                Defaults to "montage".
            page_size (int, optional): Number of subplots per montage.
                Defaults to 100.
            savefig_kwargs (dict, optional): Keyword arguments to
                `SimpleMatrixPlotter.savefig()`, but ``fname`` will be overriden by
                `MontagePager`.
            kwargs: Keyword arguments to instantiate each montage (i.e.,
                `SimpleMatrixPlotter.__init__()`).
        """
        self.path = path
        self.montage_path = path / "montages"
        self.individual_path = path / "individuals"
        # Create directories (issue #15)
        self.montage_path.mkdir(parents=True, exist_ok=True)
        self.individual_path.mkdir(parents=True, exist_ok=True)

        self.prefix = prefix
        self.page_size = page_size
        self.smp_kwargs = kwargs
        self.smp_kwargs["figcount"] = page_size
        self.savefig_kwargs = savefig_kwargs
        self.smp = SimpleMatrixPlotter(**self.smp_kwargs)
        self._i = 0
        self._itemid: List[Any] = []
        self._csv_file = (path / "mappings.csv").open("w")
        self._csvwriter = csv.writer(self._csv_file)
        self._csvwriter.writerow(
            ["individual", "title", "montage", "subplot", "row", "col"]
        )

    def __del__(self):
        self._csv_file.close()

    @property
    def i(self):
        """:int: Sequence number of the current montage (zero-based)."""
        return self._i

    @property
    def filename(self):
        return f"{self.prefix}-{self._i:04d}.png"

    def pop(self, subplot_id: Any = "", **kwargs):
        """Return the next axes, and associate the returned axes with `subplot_id`."""
        if self.smp.i >= self.page_size:
            self.savefig()
            self.smp = SimpleMatrixPlotter(**self.smp_kwargs)
            self._i += 1
        self._itemid.append(subplot_id)
        return self.smp.pop()

    def savefig(self):
        """Save the current montage to a file."""
        # These must be done before smp.savefig() which destroys the underlying figure.
        subplot_cnt = self.smp.i
        bg_rgb = tuple(
            (int(255 * channel) for channel in self.smp.fig.get_facecolor()[:3])
        )

        if subplot_cnt < 1:
            return

        with BytesIO() as buf:
            # Get the image buffer of the bbox-transformed canvas --
            # print_figure() in matplotlib/backend_bases.py.
            #
            # NOTE: methods described in
            # https://stackoverflow.com/questions/4325733/save-a-subplot-in-matplotlib)
            # was tested and found not robust. The best outcome was using `exent
            # = ax.get_tightbbox(...)`, which was still not good enought as the
            # next-row title still creeps into individual subplot image (tested
            # with matplotlib 3.2.1 and 3.3.0).
            self.smp.savefig(buf, format="png", **self.savefig_kwargs)
            buf.seek(0)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", Image.DecompressionBombWarning)
                im = Image.open(buf)
            im.load()

        im.save(self.montage_path / f"{self.prefix}-{self._i:04d}.png")
        self._save_pieces(im, subplot_cnt, bg_rgb)
        self._save_csv()
        im.close()

    def _save_csv(self):
        """Write a row.

        Each line has the following format:

            ["individual", "title", "montage-fname", "subplot-idx", "row", "col"].
        """
        ncols = self.smp.ncols
        mtg_i = self._i
        mtg_fname = self.filename
        for i, itemid in enumerate(self._itemid):
            row, col = divmod(i, ncols)
            s = str(itemid).encode("unicode-escape").decode("utf-8")
            self._csvwriter.writerow(
                (f"{mtg_i:04d}-{i:02d}.png", s, mtg_fname, i, row, col)
            )
        self._itemid.clear()
        self._csv_file.flush()

    def _save_pieces(
        self,
        im: Image.Image,
        subplot_cnt: int,
        bg_rgb: Tuple[float, float, float] = (255, 255, 255),
        debug: bool = False,
    ):
        """Chop to pieces and save, row-wise."""

        def subplot_size():
            true_nrows = (subplot_cnt // self.smp.nrows) + (
                (subplot_cnt % self.smp.ncols) != 0
            )
            true_ncols = min(self.smp.ncols, subplot_cnt)
            h = im.height // true_nrows
            w = im.width // true_ncols
            if debug:
                print(
                    f"im.height={im.height} im.width={im.width}",
                    f"im.subplot_cnt={subplot_cnt}",
                    f"true_nrows={true_nrows} true_ncols={true_ncols} h={h} w={w}",
                )
            return h, w

        subplot_h, subplot_w = subplot_size()

        def fixed_bbox(i):
            """To crop by fix size, but may produce excess border & plot not
            centered."""
            row, col = (i // self.smp.nrows), (i % self.smp.ncols)
            up = row * subplot_h
            left = col * subplot_w
            right = left + subplot_w
            bottom = up + subplot_h
            if debug:
                print(
                    f"fixed_bbox: i={i} row={row} col={col} left={left} up={up} ",
                    f"right={right} bottom={bottom}",
                )
            return left, up, right, bottom

        def tighten(im):
            if self.savefig_kwargs.get("transparent", False):
                bbox = im.getbbox()
            else:
                bg = Image.new("RGB", im.size, bg_rgb)
                diff = ImageChops.difference(im.convert("RGB"), bg)
                bbox = diff.getbbox()

            # Tight crop, but with small pads for a more pleasant view
            cropped = im.crop(pad(*bbox))
            return cropped

        def pad(
            left: float, up: float, right: float, bottom: float, pixels=4
        ) -> Tuple[float, float, float, float]:
            left = min(left - pixels, 0)
            up = min(up - pixels, 0)
            right = min(right + pixels, im.width)
            bottom = min(bottom + pixels, im.height)
            return (left, up, right, bottom)

        subplot_h, subplot_w = subplot_size()
        for i in range(subplot_cnt):
            cropped_fixed = im.crop(fixed_bbox(i))
            cropped_tight = tighten(cropped_fixed)
            cropped_tight.save(self.individual_path / f"{self._i:04d}-{i:02d}.png")
            cropped_tight.close()
            cropped_fixed.close()
