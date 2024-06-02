# This file is placed in the Public Domain.
#
#
# pylint: disable=C,R,W1503


"read empty file"


import os
import unittest


from objx.object import Object, read


class TestBork(unittest.TestCase):

    def test_bork(self):
        with open("bla", "w") as file:
            file.write("")
        obj = Object()
        read(obj, "bla")
        self.assertTrue(True)
