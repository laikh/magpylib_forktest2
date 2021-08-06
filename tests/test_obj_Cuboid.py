import pickle
import os
import numpy as np
import magpylib as magpy
from magpylib.magnet import Cuboid
from magpylib._lib.obj_classes.class_Sensor import Sensor

# """data generation for test_Cuboid()"""

# N = 100

# mags = (np.random.rand(N,3)-0.5)*1000
# dims = (np.random.rand(N,3)-0.5)*5
# posos = (np.random.rand(N,333,3)-0.5)*10 #readout at 333 positions

# angs =  (np.random.rand(N,18)-0.5)*2*10 # each step rote by max 10 deg
# axs =   (np.random.rand(N,18,3)-0.5)
# anchs = (np.random.rand(N,18,3)-0.5)*5.5
# movs =  (np.random.rand(N,18,3)-0.5)*0.5

# B = []
# for mag,dim,ang,ax,anch,mov,poso in zip(mags,dims,angs,axs,anchs,movs,posos):
#     pm = Cuboid(mag,dim)

#     # 18 subsequent operations
#     for a,aa,aaa,mv in zip(ang,ax,anch,mov):
#         pm.move(mv).rotate_from_angax(a,aa,aaa)

#     B += [pm.getB(poso)]
# B = np.array(B)

# inp = [mags,dims,posos,angs,axs,anchs,movs,B]

# pickle.dump(inp,open(os.path.abspath('./../'testdata_Cuboid.p', 'wb'))


def test_Cuboid_basics():
    """ test Cuboid fundamentals, test against magpylib2 fields
    """
    # data generated below
    data = pickle.load(open(os.path.abspath('./tests/testdata/testdata_Cuboid.p'), 'rb'))
    mags,dims,posos,angs,axs,anchs,movs,B = data

    btest = []
    for mag,dim,ang,ax,anch,mov,poso in zip(mags,dims,angs,axs,anchs,movs,posos):
        pm = Cuboid(mag,dim)

        # 18 subsequent operations
        for a,aa,aaa,mv in zip(ang,ax,anch,mov):
            pm.move(mv).rotate_from_angax(a,aa,aaa)

        btest += [pm.getB(poso)]
    btest = np.array(btest)

    assert np.allclose(B, btest), "test_Cuboid failed big time"


def test_Cuboid_add():
    """ testing __add__
    """
    src1 = Cuboid((1,2,3),(1,2,3))
    src2 = Cuboid((1,2,3),(1,2,3))
    col = src1 + src2
    assert isinstance(col,magpy.Collection), 'adding cuboides fail'


def test_Cuboid_squeeze():
    """ testing squeeze output
    """
    src1 = Cuboid((1,1,1),(1,1,1))
    sensor = Sensor(pixel=[(1,2,3),(1,2,3)])
    B = src1.getB(sensor)
    assert B.shape==(2,3)
    H = src1.getH(sensor)
    assert H.shape==(2,3)

    B = src1.getB(sensor,squeeze=False)
    assert B.shape==(1,1,1,2,3)
    H = src1.getH(sensor,squeeze=False)
    assert H.shape==(1,1,1,2,3)


def test_repr_cuboid():
    """ test __repr__
    """
    pm1 = Cuboid((1,2,3),(1,2,3))
    assert pm1.__repr__()[:6] == 'Cuboid', 'Cuboid repr failed'