import sys
from unittest import mock

import pytest
from mayavi import mlab

import magpylib as magpy


def test_show_with_missing_pyvista():
    """Should raise if pyvista is not installed"""
    src = magpy.magnet.Cuboid((0, 0, 1000), (1, 1, 1))
    with mock.patch.dict(sys.modules, {"pyvista": None}):
        # with pytest.raises(ModuleNotFoundError):
        src.show(return_fig=True, backend="pyvista")


def test_show_with_missing_mayavi():
    """Should raise if mayavi is not installed"""
    src = magpy.magnet.Cuboid((0, 0, 1000), (1, 1, 1))
    mlab.options.offscreen = True
    with mock.patch.dict(sys.modules, {"mayavi": None}):
        # with pytest.raises(ModuleNotFoundError):
        src.show(return_fig=True, backend="mayavi")


def test_dataframe_output_missing_pandas():
    """test if pandas is installed when using dataframe output in `getBH`"""
    src = magpy.magnet.Cuboid((0, 0, 1000), (1, 1, 1))
    with mock.patch.dict(sys.modules, {"pandas": None}):
        with pytest.raises(ModuleNotFoundError):
            src.getB((0, 0, 0), output="dataframe")
