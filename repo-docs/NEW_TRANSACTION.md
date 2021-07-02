# New Transaction Set Guide

This guide documents the process used to add a new transaction set to LinuxForHealth x12.

## Add Transaction Package

Add a new transaction package to `x12.transactions` for the transaction set. The new transaction package must adhere to
the following convention to support transaction discovery - `x12_[transaction set code]_[implementation version]`.
Within the package add the following modules:

* __init__.py (required to support the new package)
* loops.py
* parsing.py
* segments.py
* transaction_set.py

## Add Segments

Review the transaction specification and determine if all segments within the specification are supported within the
`x12.segments` module. Add new segment models and entries to the `x12.models.X12SegmentName` as necessary. Remember that
segments constraints are generally limited to data type and field length. Specialized validations are implemented within
the transactional loop models.

Next, add specialized segment models to `x12.transactoins.[new transaction package]`as necessary. The specialized models
must extend its base segment model counterpart. 

In the example below, `Loop2000AHlSegment` overrides the `HlSegment` to provide literal, optional, and "choice"/one of constraints. Note
that code tables are implemented as nested enumeration definitions within the model class. The enumerations are nested
rather than defined as a separate type, since the code values are typically not shared between loop contexts.

```python
from enum import Enum
from x12.segments import HlSegment
from typing import Literal, Optional

class Loop2000AHlSegment(HlSegment):
    """
    Loop2000A HL segment adjusted for Information Source usage
    Example:
        HL*1**20*1~
    """

    class HierarchicalLevelCode(str, Enum):
        """
        Code value for HL03
        """

        INFORMATION_SOURCE = "20"

    hierarchical_id_number: Literal["1"]
    hierarchical_parent_id_number: Optional[str]
    hierarchical_level_code: HierarchicalLevelCode
```

## Add Loop Models

Create model classes which extend the `x12.models.X12SegmentGroup` class. Review the specification carefully to ensure
that the loop structure is modeled correctly. Within the loop reference the appropriate "base" segments or transaction
specific segments as necessary.

## Add Transaction Set Model

The transaction set model is defined within the `transaction_set.py` module. The transaction set model must extend 
`x12.models.X12SegmentGroup`.

## Add Transaction Set Parser and Parsing Functions

LinuxForHealth x12 decouples segment parsing from segment iteration/io. To implement a parser create a new class within
the parsing module that extends `x12.parsing.X12SegmentParser`. The new parser must implement the `reset` and `load_model`
methods.

The `reset` method returns the `data_record` dictionary instance attribute to a known starting state when the parser is ready
to start parsing a new record. The `load_model` method loads the `data_record`attribute into the transaction set model. 

Finally each parsing module includes parsing functions which are used to parse the transaction sets segments into the 
parser's `data_record` attribute. Parsing functions use the `match` decorator to identify the segment to parse and any optional 
conditions which must be met. The conditions are optional field equality checks.

```python
from x12.parsing import match
from x12.transactions.x12_270_005010X279A1.parsing import EligibilityInquiryLoops

@match("HL", conditions={"hierarchical_level_code": "20"})
def parse_information_source_hl_segment(segment_data, context, data_record):
    context["current_loop"] = EligibilityInquiryLoops.INFORMATION_SOURCE

    data_record[EligibilityInquiryLoops.INFORMATION_SOURCE].append(
        {"hl_segment": segment_data}
    )
```

