# -*- coding: utf-8 -*-
"""Main module."""

import pathlib
import subprocess
import sys
import venv


def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix


def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix

class _EnvBuilder(venv.EnvBuilder):

    def __init__(self, *args, **kwargs):
        self.context = None
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        self.context = context

def _venv_create(venv_path):
    venv_builder = _EnvBuilder(with_pip=True)
    venv_builder.create(venv_path)
    return venv_builder.context

def _run_python_in_venv(venv_context, command):
    command = [venv_context.env_exe] + command
    print(command)
    return subprocess.check_call(command)

def _run_bin_in_venv(venv_context, command):
    command[0] = str(pathlib.Path(venv_context.bin_path).joinpath(command[0]))
    print(command)
    return subprocess.check_call(command)

def _source_and_run_bin_in_venv(venv_context, command, shell_mode):
    source_command = " ".join(["source", venv_context.bin_path+"/activate", "&&", " "])
    command = source_command + command
    print(command)
    return subprocess.check_call(command, shell=shell_mode)

def _main(command=None, shell_mode=False):
    venv_path = pathlib.Path.cwd().joinpath('.venv')
    venv_context = _venv_create(venv_path)
    _run_python_in_venv(venv_context, ['-m', 'pip', 'install', '-U', 'pip'])
    _run_bin_in_venv(venv_context, ['pip', 'install', 'git+https://github.com/esm-tools/esm_tools'])
    if command:
        _source_and_run_bin_in_venv(venv_context, command, shell_mode)



def venv_bootstrap(config):
    """Bootstraps your run into a virtual environment"""
    print(f"Running in venv: {in_virtualenv()}")
    subprocess.check_call("which esm_versions", shell=True)
    subprocess.check_call("esm_versions check", shell=True)
    if not in_virtualenv():
        _main(" ".join(["python"] + sys.argv), shell_mode=True)
        # subprocess.check_call(command, shell=True)
    return config

if __name__ == '__main__':
    venv_bootstrap({})
    print(f"exit from bootstrapper --> in_virtualenv: {in_virtualenv()}")
