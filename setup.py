from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="PyTrains",
    version="0.0.7",
    description="Get realtime UK trains information through a simple Python API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="w-henderson",
    url="https://github.com/w-henderson/PyTrains",
    project_urls={"Source": "https://github.com/w-henderson/PyTrains"},
    license="GPL-3.0",
    keywords=["trains", "train times", "uk", "cli", "timetable"],
    packages=["pytrains"],
    package_dir={"": "."},
    entry_points={"console_scripts": ["pytrains = pytrains.cli:main"]},
    zip_safe=False,
    install_requires=[
        "requests",
        "colorama",
    ],
    extras_require={
        "tests": ["pytest"],
    },
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True
)