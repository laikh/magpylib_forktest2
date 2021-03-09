""" Display function codes"""

import numpy as np
import matplotlib.pyplot as plt
from magpylib._lib.utility import format_obj_input, test_path_format
from magpylib._lib.display.mpl_draw import (draw_directs, draw_faces, draw_markers, draw_path,
    draw_sensors)
from magpylib._lib.display.disp_utility import faces_box, faces_cylinder, system_size
from magpylib import _lib

def display(
        *objects,
        markers=[(0,0,0)],
        axis=None,
        direc=False,
        show_path=True):
    """ Display objects and paths graphically using matplotlib.

    Parameters
    ----------
    objects: sources, collections or sensors
        Show a 3D reprensation of given objects in matplotlib.

    markers: array_like, shape (N,3), default=[(0,0,0)]
        Mark positions in graphic output. Default value puts a marker
        in the origin.

    axis: pyplot.axis, default=None
        Display graphical output in a given pyplot axis (must be 3D).

    direc: bool, default=False
        Set True to plot magnetization and current directions

    show_path: bool/string, default=True
        Set True to plot object paths. Set to 'all' to plot an object
        represenation at each path position.

    Returns
    -------
    no return
    """
    # pylint: disable=protected-access
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=dangerous-default-value

    Box = _lib.obj_classes.Box
    Cylinder = _lib.obj_classes.Cylinder
    Sensor = _lib.obj_classes.Sensor

    # create or set plotting axis
    if axis is None:
        fig = plt.figure(dpi=80, figsize=(8,8))
        ax = fig.gca(projection='3d')
        generate_output = True
    else:
        ax = axis
        generate_output = False

    # load color map
    cmap = plt.cm.get_cmap('hsv')

    # flatten input
    obj_list = format_obj_input(objects)

    # test if every individual obj_path is good
    test_path_format(obj_list)

    # draw objects --------------------------------------------------
    faced_objects = [obj for obj in obj_list if isinstance(obj, (
        Box,
        Cylinder
        ))]
    face_points = [] # collect vertices for system size evaluation

    for i, obj in enumerate(faced_objects):
        col = cmap(i/len(faced_objects))

        if isinstance(obj, Box):
            faces = faces_box(obj,show_path)
            lw = 0.5
            face_points += draw_faces(faces, col, lw, ax)

        elif isinstance(obj, Cylinder):
            faces = faces_cylinder(obj,show_path)
            lw = 0.25
            face_points += draw_faces(faces, col, lw, ax)

    sensors = [obj for obj in obj_list if isinstance(obj, Sensor)]
    pix_points = draw_sensors(sensors, ax)

    # path ------------------------------------------------------
    path_points = []
    if show_path or (show_path=='all'):
        for i, obj in enumerate(faced_objects):
            col = cmap(i/len(faced_objects))
            path_points += draw_path(obj, col, ax)

        for sens in sensors:
            path_points += draw_path(sens, '.6', ax)

    # markers -------------------------------------------------------
    if markers:
        markers = np.array(markers)
        draw_markers(markers, ax)

    # directs -------------------------------------------------------
    if direc:
        draw_directs(faced_objects, cmap, ax)

    # determine system size
    limx0, limx1, limy0, limy1, limz0, limz1 = system_size(
        face_points, pix_points, markers, path_points)

    # plot styling --------------------------------------------------
    ax.set(
        xlabel = 'x [mm]',
        ylabel = 'y [mm]',
        zlabel = 'z [mm]',
        xlim=(limx0, limx1),
        ylim=(limy0, limy1),
        zlim=(limz0, limz1)
        )

    # generate output ------------------------------------------------
    if generate_output:
        plt.show()
