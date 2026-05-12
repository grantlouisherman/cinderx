# Copyright (c) Meta Platforms, Inc. and affiliates.
# pyre-unsafe

import gc
import os
import sys
import unittest

import cinderx
from cinderx.test_support import passUnless, run_in_subprocess, skip_if_ft

_PY_DEBUG_BUILD = hasattr(sys, "gettotalrefcount")
_PY312_BUILD = sys.version_info[:2] == (3, 12)


@skip_if_ft("T251571267: Free threading doesn't support heap immortalization")
@passUnless(cinderx.is_initialized(), "Tests immortalization APIs in CinderX")
class ImmortalizeTests(unittest.TestCase):
    def test_default_not_immortal(self) -> None:
        obj = []
        self.assertFalse(cinderx.is_immortal(obj))

    @unittest.skipUnless(hasattr(os, "fork"), "fork not available on Windows")
    @run_in_subprocess
    def test_is_immortal(self) -> None:
        obj = []
        cinderx.immortalize_heap()
        self.assertTrue(cinderx.is_immortal(obj))

    @unittest.skipUnless(hasattr(os, "fork"), "fork not available on Windows")
    @run_in_subprocess
    def test_post_immortalize(self) -> None:
        cinderx.immortalize_heap()
        obj = []
        self.assertFalse(cinderx.is_immortal(obj))

    @unittest.skipIf(
        _PY_DEBUG_BUILD,
        "Python 3.12 debug builds only allow interned immortal unicode",
    )
    @unittest.skipUnless(hasattr(os, "fork"), "fork not available on Windows")
    @run_in_subprocess
    def test_immortalize_exact_dict_unicode_keys(self) -> None:
        key = "".join(("qe2_", "param"))
        value = object()
        mapping = {key: value}
        holder = [mapping]

        cinderx.immortalize_heap()

        self.assertTrue(cinderx.is_immortal(holder))
        self.assertTrue(cinderx.is_immortal(mapping))
        self.assertTrue(cinderx.is_immortal(key))
        self.assertTrue(cinderx.is_immortal(value))

    @unittest.skipIf(
        _PY_DEBUG_BUILD,
        "Python 3.12 debug builds only allow interned immortal unicode",
    )
    @unittest.skipUnless(hasattr(os, "fork"), "fork not available on Windows")
    @run_in_subprocess
    def test_immortalize_gc_collected_exact_dict_entries(self) -> None:
        key = "".join(("gc_collected_", "param"))
        value = object()
        mapping = {key: value}
        gc.collect()
        self.assertEqual(not _PY312_BUILD, gc.is_tracked(mapping))

        holder = [mapping]
        self.assertEqual(not _PY312_BUILD, gc.is_tracked(mapping))
        cinderx.immortalize_heap()

        self.assertTrue(cinderx.is_immortal(holder))
        self.assertTrue(cinderx.is_immortal(mapping))
        self.assertTrue(cinderx.is_immortal(key))
        self.assertTrue(cinderx.is_immortal(value))

    @unittest.skipIf(
        _PY_DEBUG_BUILD,
        "Python 3.12 debug builds only allow interned immortal unicode",
    )
    @unittest.skipUnless(hasattr(os, "fork"), "fork not available on Windows")
    @run_in_subprocess
    def test_immortalize_nested_exact_dict_entries(self) -> None:
        outer_key = "".join(("outer_", "param"))
        inner_key = "".join(("inner_", "param"))
        inner_value = object()
        inner = {inner_key: inner_value}
        outer = {outer_key: inner}
        holder = [outer]

        cinderx.immortalize_heap()

        self.assertTrue(cinderx.is_immortal(holder))
        self.assertTrue(cinderx.is_immortal(outer))
        self.assertTrue(cinderx.is_immortal(outer_key))
        self.assertTrue(cinderx.is_immortal(inner))
        self.assertTrue(cinderx.is_immortal(inner_key))
        self.assertTrue(cinderx.is_immortal(inner_value))

    @unittest.skipIf(
        _PY_DEBUG_BUILD,
        "Python 3.12 debug builds only allow interned immortal unicode",
    )
    @unittest.skipUnless(hasattr(os, "fork"), "fork not available on Windows")
    @run_in_subprocess
    def test_immortalize_self_referential_exact_dict_entries(self) -> None:
        key = "".join(("self_", "param"))
        value = object()
        self_key = "".join(("self_", "ref"))
        mapping = {key: value}
        mapping[self_key] = mapping
        holder = [mapping]

        cinderx.immortalize_heap()

        self.assertTrue(cinderx.is_immortal(holder))
        self.assertTrue(cinderx.is_immortal(mapping))
        self.assertTrue(cinderx.is_immortal(key))
        self.assertTrue(cinderx.is_immortal(value))
        self.assertTrue(cinderx.is_immortal(self_key))
        self.assertIs(mapping[self_key], mapping)
