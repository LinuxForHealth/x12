# LinuxForHealth x12

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

## Quickstart

### Pre-requisites
The LinuxForHealth EDI development environment relies on the following software packages:

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

### CLI
Under Development

### REST API
Under Development

### SDK
Under Development