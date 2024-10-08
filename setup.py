from setuptools import find_packages, setup

setup(
    name="plh",
    version="3.0",
    packages=find_packages(),
    license="MIT",
    description="Python for labware automation",
    install_requires=[
        "loguru",
        "click",
        "pyyaml",
        "flask",
        "pydantic",  # ==2.4.2",
        "pythonnet",
    ],
    url="https://github.com/Pfizer-BradleyBare/PytomatedLiquidHandling.git",
    author="Bradley Bare",
    author_email="Bradley.Bare@pfizer.com",
    include_package_data=True,
    entry_points="""
        [console_scripts]
        plh=plh.cli:plh
    """,
)
