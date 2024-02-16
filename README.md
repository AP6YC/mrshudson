[![mrshudson-header](https://github.com/AP6YC/FileStorage/blob/main/mrshudson/header.png?raw=true)][docs-url]

> Behind every great man there is a patient British landlady who periodically brings tea and unsolicited advice.

A Python scientific project assistant package in the spirit of [DrWatson.jl][drwatson-docs].

[docs-url]: https://github.com/AP6YC/mrshudson
[drwatson-docs]: https://juliadynamics.github.io/DrWatson.jl/dev/
[julia-url]: https://julialang.org/

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Attribution](#attribution)
  - [Authors](#authors)
  - [Assets](#assets)
  - [Fonts](#fonts)

## Overview

`mrshudson` is an assistant module for scientific projects in Python.
It is built in the spirit of the great [DrWatson.jl][drwatson-docs] project for the [Julia][julia-url] programming language.
Just as Dr. John H. Watson assists in the detective work of the great Sherlock Holmes, so too does the landlady of 221B Baker Street Mrs. Martha Louise Hudson provide the facilities, the tea, and the space for the incoherent ramblings and occasional indoor revolver practice of her tenants.

This project aims to accomplish similar goals to the [DrWatson.jl][drwatson-docs] project by virtue of being *scientific project assistant* software:

- **Project Setup**: `mrshudson` provides tools for defining a project layout, initializing a project's directory structure, and accessing these locations with directory functions that point to the correct location no matter where they are accessed from.
- **Naming Simulations** (*TODO*)
- **Saving Tools** (*TODO*)
- **Running and Listing Simulations** (*TODO*)

`mrshudson` also aims to be Pythonic in its namespace management, so each utility is separated into relevant modules encapsulating their functionality:

- `mrshudson.project`: project setup utilities.
- `mrshudson.dirs`: directory functions.

## Installation

`mrshudson` is listed on PyPI, so you can install the latest version from the command line with `pip`:

```sh
pip install mrshudson
```

As always, it is recommended to do so within a virtual environment with a manager such as `conda`, `mamba`, `venv`, etc.

## Usage

Load the module in a script or notebook environment in the usual manner; following the shorthand convention of `tensorflow as tf`, `pandas as pd`, etc., the convention for loading `mrshudson` is as `mrs`.
Afterward, point to the project top simply with its name:

```python
# Import the module
import mrshudson as mrs

# Set the project top
mrs.project.set_projectdir("my_project_name")
```

> NOTE: this assumes that `my_project_name/` is the name of the project top directory and that this function is run at or below this directory.

If you wish, you may initialize a new project with the default layout in your current directory as follows:

```python
mrs.project.initialize_project()
```

You can then point to files within this project structure with their corresponding directory accessor functions, which accept separated arguments for subdirectories and files (as in `pathlib`) and return `pathlib.Path`s:

```python
# Gives <project_top>/subdir/my_file.py
mrs.dirs.projectdir("subdir", "my_file.py)
```

All of the project directory accessors are listed below:

```python
mrs.dirs.projectdir()     # The top of the projec
mrs.dirs.plotsdir()       # The plots directory
mrs.dirs.papersdir()      # The papers directory
mrs.dirs.srcdir()         # The location of the project source files
mrs.dirs.scriptsdir()     # The experiment scripts
mrs.dirs.optsdir()        # Experiment option files
mrs.dirs.modelsdir()      # The location for model files
mrs.dirs.datadir()        # The top data directory
mrs.dirs.datadir_raw()    # Raw data files
mrs.dirs.datadir_pro()    # Processed data files
mrs.dirs.datadir_sims()   # Simulation results
```

For more details, please see the `mrshudson` documentation.

## Attribution

### Authors

- Sasha Petrenko <petrenkos@mst.edu> [@AP6YC](https://github.com/AP6YC)

### Assets

- [Tea icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/tea) ([tea-cup_3352097](https://www.flaticon.com/free-icon/tea-cup_3352097))

### Fonts

- [https://www.fontspace.com/fogle-hunter-font-f23730](https://www.fontspace.com/fogle-hunter-font-f23730)
