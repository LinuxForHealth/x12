# LinuxForHealth x12

![GitHub License](https://img.shields.io/github/license/LinuxForHealth/x12)
![Supported Versions](https://img.shields.io/badge/python%20version-3.8%2C%203.9-blue)
<br>
![Template CI](https://github.com/LinuxForHealth/x12/actions/workflows/continuous-integration.yml/badge.svg)
<br>
![GitHub Issues](https://img.shields.io/github/issues/LinuxForHealth/x12)
![GitHub Forks](https://img.shields.io/github/forks/LinuxForHealth/x12)
![GitHub Stars](https://img.shields.io/github/stars/LinuxForHealth/x12)


LinuxForHealth x12 streams ASC 5010 X12 health care transactions into [Pydantic Models](https://pydantic-docs.helpmanual.io/)  for a pleasant pythonic parsing experience! Integration options include REST endpoints, CLI (command line), or direct access using the Python SDK.

Supported formats include:
* 005010X212 Claim Status
* 005010X221 Claim Payment
* 005010X222 Professional Claim
* 05010X223 Institutional Claim
* 005010X279 Eligibility
* 005010X220 Enrollment and Maintenance

## Quickstart

### Pre-requisites
The LinuxForHealth X12 development environment relies on the following software packages:

- [git](https://git-scm.com) for project version control
- [Python 3.8 or higher](https://www.python.org/downloads/) for runtime/coding support

### Project Setup and Validation
```shell
pip install --upgrade pip setuptools

git clone https://github.com/LinuxForHealth/x12
cd x12

python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip setuptools 
pip install -e .[dev]
pytest
```

### SDK

The X12 SDK provides an `io` package which supports streaming X12 segments or transaction models. Segment
streaming parses each segment into a list containing the fields. Model streaming validates the X12 payload, and returns
one or transaction models from the X12 message.


To stream segments, create a X12SegmentReader instance: 
```python
from linuxforhealth.x12.io import X12SegmentReader

with X12SegmentReader("/home/edi/270.x12") as r:
    # return the segment name and field list
    for segment_name, segment_fields in r.segments():
        print(segment_name)
        print(segment_fields)
```

To stream models, create a X12ModelReader instance:
```python
from linuxforhealth.x12.io import X12ModelReader

with X12ModelReader("/home/edi/270.x12") as r:
    for model in r.models():
        # common model attributes include "header" and "footer"
        print(model.header)
        print(model.footer)
        
        # to convert back to X12
        model.x12()
```

### CLI
The X12 CLI parses a X12 input file and returns either a list of X12 segments, or a list of X12 models based on the provided options.

To view help information
```shell
user@mbp x12 % source venv/bin/activate
(venv) user@mbp x12 % lfhx12 --help
usage: LinuxForHealth X12 [-h] [-s | -m] [-x] [-p] file

The LinuxForHealth X12 CLI parses and validates X12 messages.
Messages are returned in JSON format in either a segment or transactional format.

positional arguments:
  file           The path to a ASC X12 file

optional arguments:
  -h, --help     show this help message and exit
  -s, --segment  Returns X12 segments
  -m, --model    Returns X12 models
  -x, --exclude  Exclude fields set to None in model output
  -p, --pretty   Pretty print output
```

To parse a X12 message into segments with pretty printing enabled
```shell
(venv) user@mbp x12 % lfhx12 -s -p demo-file/demo.270
[
    {
        "ISA00": "ISA",
        "ISA01": "03",
        "ISA02": "9876543210",
<etc, etc>
```

To parse a X12 message into models with pretty printing enabled
```shell
(venv) user@mbp x12 % lfhx12 -m -p demo-file/demo.270
[
    {
        "header": {
            "st_segment": {
                "delimiters": {
                    "element_separator": "*",
                    "repetition_separator": "^",
                    "segment_terminator": "~",
                    "component_separator": ":"
                },
                "segment_name": "ST",
                "transaction_set_identifier_code": "270",
                "transaction_set_control_number": "0001",
                "implementation_convention_reference": "005010X279A1"
            },
            "bht_segment": {
              <etc, etc>
```

In "model" mode, the `-x` option excludes `None` values from output.

### Code Formatting

LinuxForHealth X12 adheres to the [Black Code Style and Convention](https://black.readthedocs.io/en/stable/index.html)

The following command executes the black formatter with default options

```shell
user@mbp x12 % source venv/bin/activate
(venv) user@mbp x12 % black ./src
```

Use the `--help` flag to view all available options for the black code formatter

```shell
(venv) user@mbp x12 % black --help
```

## Building The Project
LinuxForHealth X12 is aligned, to a degree, with the PEP-517 standard. `setup.cfg` stores build metadata/configuration.
`pyproject.toml` contains the build toolchain specification and black formatter configurations.

The commands below creates a source and wheel distribution within a clean build environment.

```shell
python3 -m venv build-venv && source build-venv/bin/activate && pip install --upgrade pip setuptools build wheel twine
python3 -m build --no-isolation
```

## Additional Resources
- [Design Overview](repo-docs/DESIGN.md)
- [New Transaction Support](repo-docs/NEW_TRANSACTION.md)
