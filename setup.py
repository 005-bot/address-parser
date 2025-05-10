from pathlib import Path

from setuptools import find_packages, setup

this_dir = Path(__file__).parent
readme = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="address_parser",
    version="1.0.0",
    author="Aleksandr Soloshenko",
    description="Asynchronous street address normalisation and fuzzy matching",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    python_requires=">=3.11",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "address_parser.data": ["streets.db"],
    },
    install_requires=["aiosqlite>=0.21.0"],
    extras_require={"streets-db": ["overpass", "requests"]},
)
