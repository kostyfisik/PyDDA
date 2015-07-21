import numpy


def power_function(pow): return lambda x: numpy.power(x, pow)


def load_dipole_file(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    dipoles = []
    for line in lines:
        dipole = []
        for d in line.split(','):
            dipole.append(float(d))
        dipoles.append(dipole)
    return numpy.asarray(dipoles)


def col3to1(threecol):
    # input vector   [v1x
    #                 v1y
    #                 v1z
    #                  .
    #                  .
    #                  .
    #                 vNx
    #                 vNy
    #                 vNz]
    #
    # output   [v1x v1y v1z
    #            .   .   .
    #            .   .   .
    #            .   .   .
    #           vNx vNy vNz]
    #


    #dummy, N = threecol.shape

    #onecol = numpy.zeros(3*N, dtype=numpy.complex64)
    #ind = numpy.multiply(range(2, N), 3)
    #onecol[ind-2] = threecol[:, ]
    #onecol[ind-1] = threecol[:, 2]
    #onecol[ind] = threecol[:, 3]

    n, m = threecol.shape
    onecol = numpy.reshape(threecol, n*m)

    return onecol


def rtp2xyz(r, theta, phi):
    # rtp2xyz.m
    # Coordinate transformation from spherical to cartesian
    # theta is the polar angle, measured from the +z axis,
    # and varies from 0 to pi
    # phi is the azimuthal angle, measured from the +x axis, increasing
    # towards the +y axis, varying from 0 to 2*pi
    #
    # Usage:
    # [x,y,z] = rtp2xyz(r,theta,phi);
    # where x, y, z, r, theta, phi are all scalars or
    # equal-length vectors
    # or
    # x = rtp2xyz(r);
    # where x = [ x y z ] and r = [ r theta phi ]
    #
    # Angles are in radians
    #
    # PACKAGE INFO

    #if nargin == 1
    #   theta = r(:,2);
    #   phi = r(:,3);
    #   r = r(:,1);
    #end

    z = r * numpy.cos(theta)
    xy = r * numpy.sin(theta)

    x = xy * numpy.cos(phi)
    y = xy * numpy.sin(phi)

    #if nargout == 1
    #   x = x(:);
    #  y = y(:);
    #  z = z(:);
    #  x = [ x y z ];

    return x, y, z


def threewide(a):
    # threewide.m - converts an input vector (either row or column
    #               vector) into a column vector repeated in
    #               three columns.
    # Usage:
    # wide_vector = threewide(original_vector);
    #
    # You might find this useful for multiplying a vector of scalars
    # with a column vector of 3-vectors.
    #
    # PACKAGE INFO

    a = numpy.reshape(a, [-1])
    wide_vector = numpy.asarray([a, a, a]).T #Flaky.

    return wide_vector


def matchsize(A, B, C = None):
    # matchsize.m - checks that all vector inputs have the same
    #     number of rows, and expands single-row inputs by repetition
    #     to match the input row number.
    #
    # Usage:
    # [A,B] = matchsize(A,B)
    # [A,B,C] = matchsize(A,B,C)
    #
    # Either 2 or 3 input vectors/scalars are allowed.
    #
    # PACKAGE INFO

    An = A.size
    Bn = B.size
    NoC = False
    if C is None:
        Cn = 1
        C = [0]
        NoC = True
    else:
        Cn = C.size

    nmax = numpy.maximum(An, Bn)
    namx = numpy.maximum(nmax, Cn)

    if An < nmax:
        if An == 1:
            A = numpy.ones([nmax]) * A
        else:
            raise Exception('Number of rows in inputs must be one or equal.')

    if Bn < nmax:
        if Bn == 1:
            B = numpy.ones([nmax]) * B
        else:
            raise Exception('Number of rows in inputs must be one or equal.')

    if Cn < nmax and not NoC:
        if Cn == 1:
            C = numpy.ones([nmax]) * C
        else:
            raise Exception('Number of rows in inputs must be one or equal.')
    if NoC:
        return A, B
    else:
        return A, B, C