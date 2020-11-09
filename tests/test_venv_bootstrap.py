#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `venv_bootstrap` package."""


import unittest
from click.testing import CliRunner

from venv_bootstrap import venv_bootstrap
from venv_bootstrap import cli


class TestVenv_bootstrap(unittest.TestCase):
    """Tests for `venv_bootstrap` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'venv_bootstrap.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
