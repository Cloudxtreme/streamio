"""Unit Test(s)"""


from time import time
from json import dumps
from itertools import chain
from operator import itemgetter
from random import randint, sample, seed

try:
    from collections import OrderedDict as odict
except ImportError:  # Python 2.6
    # Taken from: https://raw.github.com/bluedynamics/odict/master/src/odict/pyodict.py
    from .odict import odict  # noqa


from streamio import csvstream, csvdictstream, jsonstream, merge, mergesort, minmax


def test__jsonstream1(tmpdir):
    seed(time())
    xs = [sample(range(100), 4) for _ in range(4)]

    with tmpdir.join("test.json").open("w") as f:
        for x in xs:
            f.write("{0:s}\n".format(dumps(x)))

    assert list(jsonstream(tmpdir.join("test.json"))) == xs


def test__jsonstream2(tmpdir):
    seed(time())
    xs = [sample(range(100), 4) for _ in range(4)]

    with tmpdir.join("test.json").open("w") as f:
        for x in xs:
            f.write("{0:s}\n".format(dumps(x)))

    assert list(jsonstream(tmpdir.join("test.json").open("r"))) == xs


def test__jsonstream3(tmpdir):
    seed(time())
    xs = [sample(range(100), 4) for _ in range(4)]

    with tmpdir.join("test.json").open("w") as f:
        for x in xs:
            f.write("{0:s}\n".format(dumps(x)))

    assert list(jsonstream(str(tmpdir.join("test.json")))) == xs


def test__csvstream1(tmpdir):
    seed(time())
    xs = [map(str, sample(range(100), 3)) for _ in range(4)]

    with tmpdir.join("test.csv").open("w") as f:
        f.write("\n".join([",".join(x) for x in xs]))

    assert list(csvstream(tmpdir.join("test.csv"))) == xs


def test__csvstream2(tmpdir):
    seed(time())
    xs = [map(str, sample(range(100), 3)) for _ in range(4)]

    with tmpdir.join("test.csv").open("w") as f:
        f.write("\n".join([",".join(x) for x in xs]))

    assert list(csvstream(tmpdir.join("test.csv").open("r"))) == xs


def test__csvstream3(tmpdir):
    seed(time())
    xs = [map(str, sample(range(100), 3)) for _ in range(4)]

    with tmpdir.join("test.csv").open("w") as f:
        f.write("\n".join([",".join(x) for x in xs]))

    assert list(csvstream(str(tmpdir.join("test.csv")))) == xs


def test__csvdictstream1(tmpdir):
    fields = ["a", "b", "c"]

    seed(time())
    xs = [odict(zip(fields, map(str, sample(range(100), 3)))) for _ in range(4)]

    with tmpdir.join("test.csv").open("w") as f:
        f.write("{0:s}\n".format(",".join(fields)))
        f.write("\n".join([",".join(x.values()) for x in xs]))

    assert list(csvdictstream(tmpdir.join("test.csv"))) == xs


def test__merge1():
    seed(time())
    xs = [sample(range(100), 4) for _ in range(4)]
    ys = (sorted(x) for x in xs)
    assert list(merge(*ys)) == sorted(chain(*xs))


def test__merge2():
    seed(time())
    xs = [sample(range(100), 5) for _ in range(4)]
    ys = (sorted(x) for x in xs)
    assert list(merge(*ys)) == sorted(chain(*xs))


def test__merge3():
    seed(time())
    xs = [sample(range(100), 5) for _ in range(4)]
    xs.append([])
    ys = (sorted(x) for x in xs)
    assert list(merge(*ys)) == sorted(chain(*xs))


def test__merge4():
    seed(time())
    xs = [sample(range(100), randint(0, 100)) for _ in range(randint(0, 100))]
    ys = (sorted(x) for x in xs)
    assert list(merge(*ys)) == sorted(chain(*xs))


def test__mergesort1(tmpdir):
    seed(time())
    xs = [sample(range(100), 4) for _ in range(10000)]

    with tmpdir.join("test.json").open("w") as f:
        for x in xs:
            f.write("{0:s}\n".format(dumps(x)))

    mergesort(tmpdir.join("test.json"), maxitems=1000)

    assert list(jsonstream(tmpdir.join("test.json"))) == sorted(xs)


def test__mergesort2(tmpdir):
    seed(time())
    xs = [sample(range(100), 4) for _ in range(10000)]

    with tmpdir.join("test.json").open("w") as f:
        for x in xs:
            f.write("{0:s}\n".format(dumps(x)))

    key = itemgetter(0, 1, 2, 3)
    mergesort(tmpdir.join("test.json"), key=key, maxitems=1000)

    assert list(jsonstream(tmpdir.join("test.json"))) == sorted(xs, key=key)


def test__mergesort3(tmpdir):
    seed(time())
    xs = [randint(0, 1000000) for _ in range(1000000)]

    with tmpdir.join("test.json").open("w") as f:
        for x in xs:
            f.write("{0:s}\n".format(dumps(x)))

    mergesort(tmpdir.join("test.json"), maxitems=10000)

    assert list(jsonstream(tmpdir.join("test.json"))) == sorted(xs)


def test__minmax():
    seed(time())
    xs = [randint(0, 100) for _ in range(100)]

    _min, _max = minmax(xs)
    assert _min == min(xs)
    assert _max == max(xs)
