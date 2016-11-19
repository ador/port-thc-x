import numpy as np
import outlierdetect.gen_esd as esd

def test_generalizedESD_01():
    x = np.array([float(x) for x in "-1.60 -1.20 \
          0.47 0.54 0.62 0.64 0.90 0.92 0.92 0.93 1.01 1.06 1.30 1.59 \
          3.30".split()])
    # Apply the generalized ESD, max 3 outliers
    r = esd.generalizedESD(x, 3, 0.05)
    # check the outliers
    assert([14, 0, 1] == r[1])

def test_generalizedESD_02():
    x = np.array([float(x) for x in "-1.60 -1.20 \
          0.47 0.54 0.62 0.64 0.90 0.92 0.92 0.93 1.01 1.06 1.30 1.59 \
          3.30".split()])
    # Apply the generalized ESD, max 2 outliers
    r = esd.generalizedESD(x, 2, 0.05)
    # check the outliers
    assert([14, 0] == r[1])

def test_generalizedESD_03():
    x = np.array([float(x) for x in "-10.3 -2.25 -1.68 0.94 1.15 1.20 \
          1.26 1.26 1.34 1.38 1.43 1.49 1.49 1.49 1.50 1.50 1.53 1.55 \
          1.55 1.56 1.58 1.65 1.69 1.70 1.76 1.77 1.81 1.91 1.94 1.96 \
          1.99 2.06 2.09 2.10 2.14 2.15 2.23 2.24 2.26 2.35 2.37 2.40 \
          2.47 2.54 2.62 2.64 2.90 2.92 2.92 2.93 3.21 3.26 3.30 3.59 \
          3.68 4.30 4.64 5.34 5.92 16.01".split()])

    r = esd.generalizedESD(x, 10, 0.05)
    # check the outliers
    assert([59, 0, 1, 2, 58, 57] == r[1])

