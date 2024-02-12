"""Command Line Interface (cli) for plh.
"""

import pathlib
import shutil
import subprocess

import click


@click.group()
def plh() -> None:
    """Main entry point for cli functions."""


@plh.command()
def install_venus_dependencies() -> None:
    """This command installs all Venus libraries required by plh by invoking a set of Hamilton supplied .exe files."""
    if not pathlib.Path("C:\\Program Files (x86)\\HAMILTON").exists():
        print(
            "Hamilton Venus4 software does not appear to be installed. Please install before running this command",
        )
        return

    input(
        "Press <Enter> to continue Venus4 library installation. Otherwise, cancel with <Ctrl+C>",
    )

    from plh.driver.HAMILTON.backend import bin as HAMILTON_bin

    bin_folder = pathlib.Path(HAMILTON_bin.__file__).parent

    for item in bin_folder.iterdir():
        if item.is_file() and item.suffix == ".exe":
            process = subprocess.Popen(
                [  # noqa:S603
                    item,
                ],
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )

            while process.poll() is None:
                ...
            # Wait for completion
        # run file if .exe (installs libraries)

        if item.is_dir():
            shutil.copytree(
                src=item,
                dst="C:\\Program Files (x86)\\HAMILTON\\Library",
                dirs_exist_ok=False,
            )
