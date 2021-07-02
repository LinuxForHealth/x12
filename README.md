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
* 005010X217 Services Review
* 005010X218 Premium Payment
* 005010X220 Enrollment and Maintenance
* 005010X221 Claim Payment
* 005010X222 Professional Claim
* 05010X223 Institutional Claim
* 005010X224 Dental Claim
* 005010X279 Eligibility

This project is currently under construction. Please refer to the [LinuxForHealth X12 Issue Board](https://github.com/LinuxForHealth/x12/issues) to review current issues and progress.

## Quickstart

### Pre-requisites
The LinuxForHealth X12 development environment relies on the following software packages:

- [git](https://git-scm.com) for project version control
- [Python 3.8 or higher](https://www.python.org/downloads/) for runtime/coding support
- [Pipenv](https://pipenv.pypa.io) for Python dependency management  

### Project Setup and Validation
```shell
pip install --upgrade pip

git clone https://github.com/LinuxForHealth/x12
cd x12

pipenv sync --dev 
pipenv run pytest
```

### SDK

The X12 SDK provides an `io` package which supports streaming X12 segments or transaction models. Segment
streaming parses each segment into a list containing the fields. Model streaming validates the X12 payload, and returns
one or transaction models from the X12 message.


To stream segments, create a X12SegmentReader instance: 
```python
from x12.io import X12SegmentReader

with X12SegmentReader("/home/edi/270.x12") as r:
    # return the segment name and field list
    for segment_name, segment_fields in r.segments():
        print(segment_name)
        print(segment_fields)
```

To stream models, create a X12ModelReader instance:
```python
from x12.io import X12ModelReader

with X12ModelReader("/home/edi/270.x12") as r:
    for model in r.models():
        # common model properties include "header" and "footer"
        print(model.header)
        print(model.footer)
        
        # to convert back to X12
        model.x12()
```

### CLI
Under Development

### REST API
Under Development


### Additional Resources
- [Design Overview](repo-docs/DESIGN.md)
- [New Transaction Support](repo-docs/NEW_TRANSACTION.md)
