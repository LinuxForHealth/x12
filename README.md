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
        # common model attributes include "header" and "footer"
        print(model.header)
        print(model.footer)
        
        # to convert back to X12
        model.x12()
```

Each X12 Transaction Model includes property accessors as a convenience. Supported properties vary per transaction.
```python
from x12.io import X12ModelReader

def test_property_usage(x12_270_subscriber_input):
    """A test case used to exercise property usage"""

    with X12ModelReader(x12_270_subscriber_input) as r:
        transaction_model = [m for m in r.models()][0]

        # the property isn't cached so fetch the subscriber into a variable
        subscriber = transaction_model.subscriber
        subscriber_name = subscriber["loop_2100c"]["nm1_segment"]
        assert subscriber_name["name_last_or_organization_name"] == "DOE"
        assert subscriber_name["name_first"] == "JOHN"
        assert subscriber_name["identification_code"] == "00000000001"

        subscriber_transaction = subscriber["trn_segment"][0]
        assert subscriber_transaction["originating_company_identifier"] == "9800000004"

        info_source_name = transaction_model.information_source["loop_2100a"]["nm1_segment"]
        assert info_source_name["name_last_or_organization_name"] == "PAYER C"
        assert info_source_name["identification_code"] == "12345"
```

### CLI
The X12 CLI utility is implemented as a pipenv script. The script parses a X12 input file and returns either a list of
X12 segments, or a list of X12 models based on the provided options.

To view help information
```shell
tdw@dixons-mbp x12 % pipenv run cli --help
Loading .env environment variables...
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
pipenv run cli -s -p demo-file/demo.270
Loading .env environment variables...
[
    {
        "ISA00": "ISA",
        "ISA01": "03",
        "ISA02": "9876543210",
<etc, etc>
```

To parse a X12 message into models with pretty printing enabled
```shell
tdw@dixons-mbp x12 % pipenv run cli -m -p demo-file/demo.270
Loading .env environment variables...
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

In "model" mode fields that are set to None may be excluded from output using the `-x` option.

### REST API
Under Development


### Additional Resources
- [Design Overview](repo-docs/DESIGN.md)
- [New Transaction Support](repo-docs/NEW_TRANSACTION.md)
