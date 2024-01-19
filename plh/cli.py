import pathlib
import shutil
import subprocess

import click


@click.command()
def plh_help() -> None:
    print(
        """
The following commands are available:
    plh-install-hamilton-venus4-files | Installs all Venus4 libraries required by the Hamilton base methods in plh.
    """,
    )


@click.command()
def install_hamilton_venus4_files() -> None:
    if not pathlib.Path("C:\\Program Files (x86)\\HAMILTON").exists():
        print(
            "Hamilton Venus4 software does not appear to be installed. Please install before running this command",
        )
        return

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
