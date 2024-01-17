from setuptools import find_packages, setup

setup(
    name="plh",
    version="3.0",
    packages=find_packages(exclude=["Examples"]),
    license="MIT",
    description="Python for labware automation",
    install_requires=[
        "xlwings",
        "pyyaml",
        "flask",
        "networkx",
        "processscheduler",
        "pydantic==2.4.2",
        "pythonnet",
        "redmail",
        "redbox",
        "loguru",
    ],
    url="https://github.com/Pfizer-BradleyBare/PytomatedLiquidHandling.git",
    author="Bradley Bare",
    author_email="Bradley.Bare@pfizer.com",
    include_package_data=True,
)
