# Blind HELIX

[![code-style-image]][black]
[![license-image]][mit]

A tool for automatically generating static HELIX Components from library
functions.

## Description

Writing HELIX Components can be time-consuming and before there exists a
critical mass of useful and well-labeled HELIX Components, HELIX is limited in
its dataset generation capabilities. This tool automatically parses symbols or
exports for a given library and generates HELIX Components from each exported
function, making use of link-time optimization for quick and easy program
slicing on the target library. This makes generating a large number of HELIX
Components fairly easy and improves HELIX's dataset generation capabilities.

Note: the generated Components can only be used for static analysis dataset
generation - the library functions identified are not parameterized and are
called with no arguments so the generated binaries will most likely crash.

Currently this supports C libraries.

## Installation

Install Blind HELIX with pip, clone this repository and then (from the root of
the repository) run:

```bash
pip install .
```

## Usage

Blind HELIX includes a number of different parsers for different types of
libraries. As a basic example, to parse the `zlib` library on Linux, run:

```bash
blind-helix parse generic-linux-library zlib \
    --path /usr/lib/x86_64-linux-gnu/libz.a \
    zlib.bhlx
```

This will parse the `zlib` library, identify exported functions, build
Components for each export, test that the generated Components build
successfully (discarding any that fail to build), and finally save the
generated components to a file named `zlib.bhlx`. This file can then be used to
load all of the verified Components which may then be used in HELIX scripts.

```python
import blind_helix

with open("zlib.bhlx", "r") as f:
    components = blind_helix.load(f)

# use `components` as necessary...
```

### VCPKG Support

The `generic-linux-library` parser requires that you specify the path to the
library file. To automatically find the library file, Blind HELIX is integrated
with [Microsoft's VCPKG](https://github.com/microsoft/vcpkg) through the
`vcpkg-linux-library` parser. To parse `zlib` from VCPKG on Linux, simply run:

```bash
blind-helix parse vcpkg-linux-library zlib zlib.bhlx
```

Note: this requires that the `zlib` library is already installed with VCPKG.
See the VCPKG documentation for information on how to install individual
libraries.

### Parsing Many Libraries

It's possible to parse many libraries in parallel using the `parse-many`
command. This command lets you specify all of the libraries you want to parse
by name, control the number of parallel workers for parsing, and captures parse
logging output. For example, to parse a collection of libraries from VCPKG:

```bash
blind-helix parse-many vcpkg-linux-library output/ \
    zlib crc32c protobuf-c cpuinfo mbedtls jansson openjpg
```

### Simple Dataset Generation

Once you have a sizeable collection of components, Blind HELIX also includes a
few very simple, naive dataset generation strategies. For example, to generate
100 randomized combinations of 20 components from a library of Blind HELIX
export files:

```bash
blind-helix dataset random output/ \
    --samples 100 \
    --components 20 \
    /path/to/exports/*.bhlx
```

Note: Blind HELIX is not intended as a dataset generation tool - its main focus
is HELIX Component generation. For more complex dataset generation and better
control over the statistical properties of the generated datasets it's best to
write scripts to generate them yourself.

## Contributing

Pull requests and GitHub issues are welcome.

## Disclaimer

DISTRIBUTION STATEMENT A. Approved for public release: distribution unlimited.

© 2021 Massachusetts Institute of Technology

- Subject to FAR 52.227-11 – Patent Rights – Ownership by the Contractor (May 2014)
- SPDX-License-Identifier: MIT

This material is based upon work supported by the Department of Defense under
Air Force Contract No. FA8721-05-C-0002 and/or FA8702-15-D-0001. Any opinions,
findings, conclusions or recommendations expressed in this material are those
of the author(s) and do not necessarily reflect the views of the Department of
Defense.

[MIT License](LICENSE.txt)

[code-style-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black]: https://github.com/psf/black
[license-image]: https://img.shields.io/github/license/helix-datasets/blind-helix
[mit]: ./LICENSE.txt
