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
def install_venus() -> None:
    """Installs all Venus libraries required by plh by invoking a set of Hamilton supplied .exe files."""
    if not pathlib.Path("C:\\Program Files (x86)\\HAMILTON").exists():
        print(
            "Hamilton Venus4 software does not appear to be installed. Please install before running this command",
        )
        return

    input(
        "Press <Enter> to continue Venus4 library installation. Otherwise, cancel with <Ctrl+C>",
    )

    from plh.device.HAMILTON import backend

    backend_path = pathlib.Path(backend.__file__)
    hamilton_path = pathlib.Path("C:\\Program Files (x86)\\HAMILTON\\Library")

    backend_installer_folder = backend_path / "installer"
    backend_labware_folder = backend_path / "labware"
    backend_library_folder = backend_path / "library"
    backend_method_folder = backend_path / "method"

    hamilton_bin_folder = hamilton_path / "Bin" / "plh"
    hamilton_labware_folder = hamilton_path / "LabWare" / "plh"
    hamilton_library_folder = hamilton_path / "Library" / "plh"
    hamilton_methods_folder = hamilton_path / "Methods" / "plh"

    hamilton_bin_folder.unlink(missing_ok=True)
    hamilton_labware_folder.unlink(missing_ok=True)
    hamilton_library_folder.unlink(missing_ok=True)
    hamilton_methods_folder.unlink(missing_ok=True)
    # Clean the folders first

    hamilton_bin_folder.mkdir()
    hamilton_labware_folder.mkdir()
    hamilton_library_folder.mkdir()
    hamilton_methods_folder.mkdir()
    # Make the folders

    shutil.copytree(backend_installer_folder, hamilton_bin_folder)
    shutil.copytree(backend_labware_folder, hamilton_labware_folder)
    shutil.copytree(backend_library_folder, hamilton_library_folder)
    shutil.copytree(backend_method_folder, hamilton_methods_folder)

    return

    bin_folder = pathlib.Path(hamilton_bin.__file__).parent

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
                dirs_exist_ok=True,
            )
