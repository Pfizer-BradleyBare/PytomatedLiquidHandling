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
    """Installs all Venus requirements for plh (libraries, labware, sub-methods)."""
    if not pathlib.Path("C:\\Program Files (x86)\\HAMILTON").exists():
        print(
            "Hamilton Venus software does not appear to be installed. Please install before running this command",
        )
        return

    input(
        "Press <Enter> to continue Venus4 library installation. Otherwise, cancel with <Ctrl+C>",
    )

    from plh.device.HAMILTON import backend

    backend_path = pathlib.Path(backend.__file__).parent
    hamilton_path = pathlib.Path("C:\\Program Files (x86)\\HAMILTON")

    backend_installer_folder = backend_path / "installer"
    backend_labware_folder = backend_path / "labware"
    backend_library_folder = backend_path / "library"
    backend_method_folder = backend_path / "method"

    hamilton_bin_folder = hamilton_path / "Bin" / "plh"
    hamilton_labware_folder = hamilton_path / "LabWare" / "plh"
    hamilton_library_folder = hamilton_path / "Library" / "plh"
    hamilton_methods_folder = hamilton_path / "Methods" / "plh"

    shutil.rmtree(hamilton_bin_folder, ignore_errors=True)
    shutil.rmtree(hamilton_labware_folder, ignore_errors=True)
    shutil.rmtree(hamilton_library_folder, ignore_errors=True)
    shutil.rmtree(hamilton_methods_folder, ignore_errors=True)
    # Clean the folders first

    shutil.copytree(backend_installer_folder, hamilton_bin_folder)
    shutil.copytree(backend_labware_folder, hamilton_labware_folder)
    shutil.copytree(backend_library_folder, hamilton_library_folder)
    shutil.copytree(backend_method_folder, hamilton_methods_folder)
    # copy the content

    (hamilton_methods_folder / "active_layout").mkdir()
    shutil.copyfile(
        hamilton_methods_folder / "blank_layout" / "blank_layout.lay",
        hamilton_methods_folder / "active_layout" / "active_layout.lay",
    )
    shutil.copyfile(
        hamilton_methods_folder / "blank_layout" / "blank_layout.res",
        hamilton_methods_folder / "active_layout" / "active_layout.res",
    )
    # Copy an initial blank layout, to rid of layout related errors.

    for item in hamilton_bin_folder.iterdir():
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
