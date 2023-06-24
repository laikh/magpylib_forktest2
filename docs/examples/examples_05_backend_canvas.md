---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(examples-backends-canvas)=

# Graphics - Backend, canvas, return_fig

The graphic backend refers to the plotting library that is used for graphic output. Canvas refers to the frame/window/canvas/axes object the graphic output is forwarded to.

## Graphic backend

Magpylib supports several common graphic backends.

```{code-cell} ipython3
from magpylib import SUPPORTED_PLOTTING_BACKENDS

SUPPORTED_PLOTTING_BACKENDS
```

+++ {"user_expressions": []}

The installation default is set to `'auto'`. In this case the backend is dynamically inferred depending on the current running environment (terminal or notebook), the available installed backend libraries and the set canvas:

| environment      | canvas                                            | inferred backend                        |
|------------------|---------------------------------------------------|-----------------------------------------|
| terminal         | `None`                                            | `matplotlib`                            |
| IPython notebook | `None`                                            | `plotly` if installed else `matplotlib` |
| all              | `matplotlib.axes.Axes`                            | `matplotlib`                            |
| all              | `plotly.graph_objects.Figure` (or `FigureWidget`) | `plotly`                                |
| all              | `pyvista.Plotter`                                 | `pyvista`                               |

To explicitly select a graphic backend one can
1. Change the library default with `magpy.defaults.display.backend = 'plotly'`.
2. Set the `backend` kwarg in the `show` function, `show(..., backend='matplotlib')`.

There is a high level of **feature parity**, however, not all graphic features are supported by all backends. In addition, some common Matplotlib syntax (e.g. color `'r'`, linestyle `':'`) is automatically translated to other backends.

The following example demonstrates the currently supported backends:

```{code-cell} ipython3
import magpylib as magpy
import numpy as np
import pyvista as pv

pv.set_jupyter_backend("panel")  # improve rendering in a jupyter notebook

# define sources and paths
loop = magpy.current.Loop(current=1, diameter=1)
loop.position = np.linspace((0, 0, -3), (0, 0, 3), 40)

cylinder = magpy.magnet.Cylinder(
    magnetization=(0, -100, 0), dimension=(1, 2), position=(0, -3, 0)
)
cylinder.rotate_from_angax(np.linspace(0, 300, 40)[1:], "z", anchor=0)

# show the system using different backends
for backend in magpy.SUPPORTED_PLOTTING_BACKENDS:
    print(f"Plotting backend: {backend!r}")
    magpy.show(loop, cylinder, backend=backend)
```

## Output in custom figure

When calling `show`, a figure is automatically generated and displayed. It is also possible to display the `show` output on a given user-defined canvas with the `canvas` kwarg.

In the following example we show how to combine a 2D field plot with the 3D `show` output in **Matplotlib**:

```{code-cell} ipython3
import magpylib as magpy
import matplotlib.pyplot as plt
import numpy as np

# setup matplotlib figure and subplots
fig = plt.figure(figsize=(10, 4))
ax1 = fig.add_subplot(
    121,
)  # 2D-axis
ax2 = fig.add_subplot(122, projection="3d")  # 3D-axis

# define sources and paths
loop = magpy.current.Loop(current=1, diameter=1)
loop.position = np.linspace((0, 0, -3), (0, 0, 3), 40)

cylinder = magpy.magnet.Cylinder(
    magnetization=(0, -100, 0), dimension=(1, 2), position=(0, -3, 0)
)
cylinder.rotate_from_angax(np.linspace(0, 300, 40)[1:], "z", anchor=0)

# compute field and plot in 2D-axis
B = magpy.getB([loop, cylinder], (0, 0, 0), sumup=True)
ax1.plot(B)

# display show() output in 3D-axis
magpy.show(loop, cylinder, canvas=ax2)

# generate figure
plt.tight_layout()
plt.show()
```

A similar example with **Plotly**:

```{code-cell} ipython3
import magpylib as magpy
import numpy as np
import plotly.graph_objects as go

# setup plotly figure and subplots
fig = go.Figure().set_subplots(
    rows=1, cols=2, specs=[[{"type": "xy"}, {"type": "scene"}]]
)

# define sources and paths
loop = magpy.current.Loop(current=1, diameter=1)
loop.position = np.linspace((0, 0, -3), (0, 0, 3), 40)

cylinder = magpy.magnet.Cylinder(
    magnetization=(0, -100, 0), dimension=(1, 2), position=(0, -3, 0)
)
cylinder.rotate_from_angax(np.linspace(0, 300, 40)[1:], "z", anchor=0)

# compute field and plot in 2D-axis
B = magpy.getB([loop, cylinder], (0, 0, 0), sumup=True)
for i, lab in enumerate(["Bx", "By", "Bz"]):
    fig.add_trace(go.Scatter(x=np.linspace(0, 1, 40), y=B[:, i], name=lab))

# display show() output in 3D-axis
temp_fig = go.Figure()
magpy.show(loop, cylinder, canvas=temp_fig, backend="plotly")
fig.add_traces(temp_fig.data, rows=1, cols=2)
fig.layout.scene.update(temp_fig.layout.scene)

# generate figure
fig.show()
```

An example with **Pyvista**:

```{code-cell} ipython3
import magpylib as magpy
import numpy as np
import pyvista as pv

pv.set_jupyter_backend("panel")  # improve rending in a jupyter notebook

# define sources and paths
loop = magpy.current.Loop(current=1, diameter=5)
loop.position = np.linspace((0, 0, -3), (0, 0, 3), 40)

cylinder = magpy.magnet.Cylinder(
    magnetization=(0, -100, 0), dimension=(1, 2), position=(0, -3, 0)
)
cylinder.rotate_from_angax(np.linspace(0, 300, 40)[1:], "z", anchor=0)

# create a pyvista plotting scene with some graphs
pl = pv.Plotter()
line = np.array(
    [(t * np.cos(15 * t), t * np.sin(15 * t), t - 8) for t in np.linspace(3, 5, 200)]
)
pl.add_lines(line, color="black")

# add magpylib.show() output to existing scene
magpy.show(loop, cylinder, backend="pyvista", canvas=pl)

# display scene
pl.camera.position = (50, 10, 10)
pl.set_background("black", top="white")
pl.show()
```

## Return figure

Instead of forwarding a figure to an existing canvas, it is also possible to return the figure object for further manipulation using the `return_fig` command. In the following example this is demonstrated for the pyvista backend.

```{code-cell} ipython3
import magpylib as magpy
import numpy as np
import pyvista as pv

pv.set_jupyter_backend("panel")  # improve rending in a jupyter notebook

# define sources and paths
loop = magpy.current.Loop(current=1, diameter=5)
loop.position = np.linspace((0, 0, -3), (0, 0, 3), 40)

cylinder = magpy.magnet.Cylinder(
    magnetization=(0, -100, 0), dimension=(1, 2), position=(0, -3, 0)
)
cylinder.rotate_from_angax(np.linspace(0, 300, 40)[1:], "z", anchor=0)

# return pyvista scene from magpylib.show()
pl = magpy.show(loop, cylinder, backend="pyvista", return_fig=True)

# add line to the pyvista scene
line = np.array(
    [(t * np.cos(15 * t), t * np.sin(15 * t), t - 8) for t in np.linspace(3, 5, 200)]
)
pl.add_lines(line, color="black")

# display scene
pl.camera.position = (50, 10, 10)
pl.set_background("purple", top="lightgreen")
pl.enable_anti_aliasing("ssaa")
pl.show()
```
