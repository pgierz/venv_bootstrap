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

def _source_and_run_bin_in_venv(venv_context, command, shell):
    source_command = " ".join(["source", venv_context.bin_path+"/activate", "&&", " "])
    command = source_command + command
    print(command)
    return subprocess.check_call(command, shell=shell)

def _install_tools(venv_context, config):
    #_run_bin_in_venv(venv_context, ['pip', 'install', 'git+https://github.com/esm-tools/esm_tools'])
    esm_tools_modules = [
        "esm_calendar",
        "esm_database",
        "esm_environment",
        "esm_master",
        "esm_parser",
        "esm_rcfile",
        "esm_runscripts",
        "esm_tools",
        "esm_plugin_manager",
        "esm_version_checker",
    ]
    for tool in esm_tools_modules:
        print(80*"=")
        print("\n\n")
        url = f"git+https://github.com/esm-tools/{tool}"
        user_wants_editable = config["general"].get(f"install_{tool}_editable", False)
        user_wants_branch = config["general"].get(f"install_{tool}_branch")
        if user_wants_editable:
            # Make sure the directory exists:
            src_dir = pathlib.Path(config['general']['experiment_dir'] + f"/src/esm-tools/{tool}")
            src_dir.mkdir(parents=True, exist_ok=True)
            if user_wants_branch:
                branch_command = f" -b {user_wants_branch} "
            else:
                branch_command = ""
            subprocess.check_call(f"git clone {branch_command} {url} {src_dir}")
            _run_bin_in_venv(venv_context, ["pip", "install", "-e", src_dir])
        else:
            if user_wants_branch:
                url += f"@{user_wants_branch}"
            _run_bin_in_venv(venv_context, ["pip", "install", "-U", url])
    print(80*"=")


def _install_required_plugins(venv_context, config):
    required_plugins = ["git+https://github.com/pgierz/venv_bootstrap"]
    for sub_cfg in config.items():
        if isinstance(sub_cfg, dict):
            if "required_plugins" in sub_cfg:
                required_plugins += sub_cfg["required_plugins"]
    for required_plugin in required_plugins:
        _run_bin_in_venv(venv_context, ["pip", "install", required_plugin])




def venv_bootstrap(config):
    """Bootstraps your run into a virtual environment"""
    print(f"Running in venv: {in_virtualenv()}")
    subprocess.check_call("which esm_versions", shell=True)
    subprocess.check_call("esm_versions check", shell=True)
    if not in_virtualenv():
        venv_path = pathlib.Path(config['general']['experiment_dir']).joinpath('.venv')
        venv_context = _venv_create(venv_path)
        _run_python_in_venv(venv_context, ['-m', 'pip', 'install', '-U', 'pip'])
        _install_tools(venv_context, config)
        _install_required_plugins(venv_context, config)
        sys.argv[0] = pathlib.Path(sys.argv[0]).name
        _source_and_run_bin_in_venv(venv_context, " ".join(sys.argv), shell=True)
        print("Exit from venv_bootstrap --> Was not in virtualenv")
        sys.exit(0)
    return config

if __name__ == '__main__':
    venv_bootstrap({})
