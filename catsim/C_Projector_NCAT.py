# Copyright 2020, General Electric Company. All rights reserved. See https://github.com/xcist/code/blob/master/LICENSE

import numpy as np
from ctypes import *
from numpy.ctypeslib import ndpointer
from catsim.CommonTools import *

def C_Projector_NCAT(cfg, viewId, subViewId):
    ###------- C function and interface
    # in nCAT_main.c: void ncat_projector(double subviewWeight, double *thisView, float *sourcePoints, int nSubSources, 
    #    double *srcHullPoints, int nSrcHullPoints, int *firstDetIndex, int nModulesIn, int *modTypeInds, 
    #    double *Up, double *Right, double *Center, int UNUSED_tvLength)

    fun = cfg.clib.ncat_projector
    fun.argtypes = [c_double, ndpointer(c_double), ndpointer(c_float), c_int, \
        ndpointer(c_double), c_int, ndpointer(c_int), c_int, ndpointer(c_int), \
        ndpointer(c_double), ndpointer(c_double), ndpointer(c_double), c_int]
    fun.restype = None
    
    ###------- Arguments
    det = cfg.detNew
    src = cfg.srcNew
    
    subviewWeight = 1.
    thisView = np.zeros([det.totalNumCells, cfg.spec.nEbin], dtype=np.double) # buffer for C
    sourcePoints = src.samples
    nSubSources = src.nSamples
    srcHullPoints = src.corners.astype(np.double)
    nSrcHullPoints = src.nCorners
    firstDetIndex = det.startIndices
    nModulesIn = det.nMod
    modTypeInds = det.modTypes
    Up = det.vvecs.astype(np.double)
    Right = det.uvecs.astype(np.double)
    Center = det.modCoords.astype(np.double)
    UNUSED_tvLength = cfg.spec.nEbin*det.totalNumCells
    
    ###------- Run C function
    fun(subviewWeight, thisView, sourcePoints, nSubSources, \
        srcHullPoints, nSrcHullPoints, firstDetIndex, nModulesIn, modTypeInds, \
        Up, Right, Center, UNUSED_tvLength)
    
    ###------- Apply transmittance
    cfg.thisSubView *= thisView

    return cfg