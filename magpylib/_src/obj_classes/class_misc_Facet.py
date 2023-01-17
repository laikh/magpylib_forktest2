"""Magnet Facet class code
"""

import numpy as np
from magpylib._src.obj_classes.class_BaseExcitations import BaseMagnet
from magpylib._src.fields.field_BH_facet import facet_field_from_obj
from magpylib._src.input_checks import check_format_input_vector
from magpylib._src.display.traces_generic import make_Facet


class Facet(BaseMagnet):
    """Triangular facet(s) with homogeneous surface charge.

    Can be used as `sources` input for magnetic field computation.

    When `position=(0,0,0)` and `orientation=None` the local object coordinates of the
    Facet vertices coincide with the global coordinate system. The geometric
    center of the Facet is determined by its vertices and is not necessarily located
    in the origin of the local coordinate system.

    Parameters
    ----------
    magnetization: array_like, shape (3,), default=`None`
        Magnetization vector (mu0*M, remanence field) in units of [mT] given in
        the local object coordinates (rotates with object). The homogeneous surface
        charge of each facet is given by the projection of the magnetization on the
        facet normal vector.

    vertices: ndarray, shape (3,3) or (n,3,3)
        Triangular facets are defined through triples of vertices in the local object
        coordinates. Multiple facets, each with dimension (3,3) can be combined in a single
        Facet object.

    position: array_like, shape (3,) or (m,3)
        Object position(s) in the global coordinates in units of [mm]. For m>1, the
        `position` and `orientation` attributes together represent an object path.

    barycenter: array_like, shape (3,)
        Read only property that returns the geometric barycenter (=center of mass)
        of the object.

    orientation: scipy `Rotation` object with length 1 or m, default=`None`
        Object orientation(s) in the global coordinates. `None` corresponds to
        a unit-rotation. For m>1, the `position` and `orientation` attributes
        together represent an object path.

    parent: `Collection` object or `None`
        The object is a child of it's parent collection.

    style: dict
        Object style inputs must be in dictionary form, e.g. `{'color':'red'}` or
        using style underscore magic, e.g. `style_color='red'`.

    Returns
    -------
    magnet source: `Facet` object

    Examples
    --------
    `Facet` objects are magnetic field sources. Below we compute the H-field [kA/m] of a
    facet object with magnetization (100,200,300) in units of [mT] dimensions defined
    through the vertices (0,0,0), (1,0,0) and (0,1,0) in units of [mm] at the
    observer position (1,1,1) given in units of [mm]:

    >>> import magpylib as magpy
    >>> verts = [(0,0,0), (1,0,0), (0,1,0)]
    >>> src = magpy.misc.Facet(magnetization=(100,200,300), vertices=verts)
    >>> H = src.getH((1,1,1))
    >>> print(H)
    [2.24851814 2.24851814 3.49105683]

    We rotate the source object, and compute the B-field, this time at a set of observer positions:

    >>> src.rotate_from_angax(45, 'x')
    >>> B = src.getB([(1,1,1), (2,2,2), (3,3,3)])
    >>> print(B)
    [[3.94659011 4.21772671 4.21772671] 
    [0.73745776 0.77325648 0.77325648] 
    [0.30049474 0.31043974 0.31043974]]

    The same result is obtained when the rotated source moves along a path away from an
    observer at position (1,1,1). Here we use a `Sensor` object as observer.

    >>> sens = magpy.Sensor(position=(1,1,1))
    >>> src.move([(-1,-1,-1), (-2,-2,-2)])
    >>> B = src.getB(sens)
    >>> print(B)
    [[3.94659011 4.21772671 4.21772671] 
    [0.73745776 0.77325648 0.77325648] 
    [0.30049474 0.31043974 0.31043974]]


    """

    _field_func = staticmethod(facet_field_from_obj)
    _field_func_kwargs_ndim = {"magnetization": 2, "vertices": 3}
    _draw_func = make_Facet

    def __init__(
        self,
        magnetization=None,
        vertices=None,
        position=(0, 0, 0),
        orientation=None,
        style=None,
        **kwargs,
    ):

        self.vertices = vertices

        # init inheritance
        super().__init__(position, orientation, magnetization, style, **kwargs)

    # property getters and setters
    @property
    def vertices(self):
        """Object faces"""
        return self._vertices

    @vertices.setter
    def vertices(self, val):
        """Set face vertices (a,b,c), shape (3,3) or (n,3,3), [mm]."""
        self._vertices = check_format_input_vector(
            val,
            dims=(2,3),
            shape_m1=3,
            sig_name="Facet.vertices",
            sig_type="array_like (list, tuple, ndarray) of shape (3,3) or (n,3,3)",
            reshape=(-1,3,3),
            allow_None=True,
        )

    @property
    def _barycenter(self):
        """Object barycenter."""
        return self._get_barycenter(self._position, self._orientation, self._vertices)

    @property
    def barycenter(self):
        """Object barycenter."""
        return np.squeeze(self._barycenter)

    @staticmethod
    def _get_barycenter(position, orientation, vertices):
        """Returns the barycenter of a facet object."""
        centroid = np.mean(vertices, axis=(0,1))
        barycenter = orientation.apply(centroid) + position
        return barycenter
