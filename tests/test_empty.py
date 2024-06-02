# This file is placed in the Public Domain.
#
#
# pylint: disable=C,R,W1503


"read empty file"


import os
import unittest


from objx.disk   import Workdir, store
from objx.object import Object, cdir, read


class TestEmpty(unittest.TestCase):

    def test_bork(self):
        Workdir.workdir = ".test"
        pth = store("bla")
        cdir(pth)
        with open(pth, "w") as file:
            file.write("")
        obj = Object()
        read(obj, pth)
        self.assertTrue(True)
