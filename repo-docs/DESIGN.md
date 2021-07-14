# LinuxForHealth x12 Design Overview

LinuxForHealth x12 parses and validates ASC X12 health care transactions. At the core of the x12 application is
its data model. The data model aligns with the ASC X12 specifications and supports its primary concepts including
fields, segments, loops, and transactions.

## ASC X12 Overview

Segments, loops, and transaction sets are concepts which provide higher levels of grouping within the ASC X12 specification.
Segments are the lowest order of grouping, while transaction sets provide the highest level.

Segments consist of fields.
Loops consist of segments.
Transaction sets consist of loops.

### ASC X12 Fields and Data Types
A field represents a single data attribute with a scalar type. The table below illustrates how LinuxForHealth x12 maps
ASC X12 data types to Python's type system.

| ASC X12 Data Type | Python Type   |
| ----------------- | ------------- |
| Numeric           | int           |
| Decimal           | Decimal       |
| ID                | str           |
| String            | str           |
| Date              | datetime.date |
| Time              | datetime.time |
| Binary            | byte[]        |

### ASC X12 Segments
Segments group a collection of fields into a logical record. For example, the `NM1` segment is a grouping of
fields used to identify an "entity's" name.

```shell
NM1*PR*2*PAYER C*****PI*12345~
```

### ASC X12 Loops

Loops are an organizational grouping within the specification that are not expressed within the X12 message payload.
The specification uses loops to build a higher level record, such as a subscriber or dependent. This higher level
grouping typically adds additional validation constraints to each segment. A segment in one loop typically utilizes
different field constraints than it does in another. 

For example, the `HL` segment's hierarchical level code field, or `HL03`, is used within the Eligibility (270) transaction
to specify the beginning of a new hierarchical record. The permitted values for the `HL03` field differ based on which
loop the segment is in.

* The Information Source Loop/Loop 2000A sets `HL03` to `20`
* The Information Receiver Loop/Loop 2000B sets `HL03` to `21`
* The Subscriber Loop/Loop 2000C sets `HL03` to `22`
* The Dependent Loop/Loop 2000C sets `HL03` to `23`

Finally, the segments below represent an "Information Receiver" loop within the Eligibility (270) transaction. The loop
boundaries are inferred using the transaction set segments.

```shell
HL*2*1*21*1~
NM1*1P*1*DOE*JOHN****XX*1467857193~
REF*4A*000111222~
N3*123 MAIN ST.*SUITE 42~
N4*SAN MATEO*CA*94401~
```

### ASC X12 Transaction Set

The transaction set is the highest level of grouping, and represents a single unit of work. The following X12 message
is a single transaction set.

```shell
ST*270*0001*005010X279A1~
BHT*0022*13*10001234*20131031*1147~
HL*1**20*1~
NM1*PR*2*PAYER C*****PI*12345~
HL*2*1*21*1~
NM1*1P*1*DOE*JOHN****XX*1467857193~
REF*4A*000111222~
N3*123 MAIN ST.*SUITE 42~
N4*SAN MATEO*CA*94401~
HL*3*2*22*0~
TRN*1*930000000000*9800000004*PD~
NM1*IL*1*DOE*JOHN****MI*00000000001~
REF*6P*0123456789~
DMG*D8*19700101~
DTP*291*D8*20131031~
EQ*1~
SE*17*0001~
```

### ASC X12 Control Envelope

The x12 specification requires transaction sets to be nestled within an "envelope" for transmission. In this case the
"envelope" is simply additional segments which contain metadata regarding the message transmission and recipients.
The `ISA`, `GS`, `GE`. and `IEA` segments  are the control segments used to contain the message. The `ISA` and `IEA` are
the opening control header and footer segments, while the `GS` and `GE` segments serve as the functional group header
and footer statements. 

In general terms, the `ISA` and `IEA` segments identify the parties involved in the message exchange. The `GS` and `GE`
segments identify the transaction type within the message payload. The control segments also support checksums (of sorts),
security metadata, and timestamps. 

### ASC X12 File Format

The X12 file format is a simple text based delimited format which dates back to 1979. The initial segment in a X12 
payload, the `ISA` segment, is a fixed length segment used to define the delimiters used in the transmission.

```shell
ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~
```

| Field Type             | Position (Zero Based) | General Industry Default |
| ---------------------- | --------------------- | ------------------------ |
| element separator      | 3                     | *                        |
| repetition character   | 82                    | ^                        |
| component separator    | 104                   | :                        |
| segment terminator     | 105                   | ~                        |

## LinuxForHealth x12 Data Model

The LinuxForHealth x12 data models extend [pydantic](https://pydantic-docs.helpmanual.io/usage/models) 's BaseModel
implementation. 

The LinuxForHealth x12 data model aligns with the ASC X12 specification and includes:

* [Base models](./x12/models.py) in `x12.models` to support X12 segments and groupings (loops and transactions).
* [Segment models](./x12/segments.py) include all X12 segments used by ASC X12 Health Care transactions.

The segment models define the fields used within a segment, but not the allowable values for a field, or if a field is
optional. These specifications are enforced at the "loop level" within a transaction. The LinuxForHealth x12 
transaction models reside within the `x12.transactions` package. Transaction implementations follow a standard naming
convention of `x12_[transaction code]_[implementation_version]`.

The contents of a transaction package include:

![transaction-package.png](transaction-package.png)

* loops.py - Loop data model implementations.
* parsing.py - Parsing functions used to create loop records within the transactional data model.
* segments.py - Segment subclasses used to enforce loop context validation constraints.
* transaction_set.py - The transaction set model.

### Data Model Hierarchy

X12Segment is the base model class for X12 segments. It includes a `x12` method which transforms the segment to a valid
x12 string.

```python
import abc
from pydantic import BaseModel

class X12Segment(abc.ABC, BaseModel):
    """
    X12BaseSegment serves as the abstract base class for all X12 segment models.
    """

    delimiters: X12Delimiters = X12Delimiters()
    segment_name: X12SegmentName

    class Config:
        """
        Default configuration for X12 Models
        """

        use_enum_values = True

    def x12(self) -> str:
        """
        :return: the X12 representation of the model instance
        """
        x12_values = []
        for k, v in self.dict(exclude={"delimiters"}).items():
            # evaluate fields
    
        x12_str = self.delimiters.element_separator.join(x12_values).rstrip(
        self.delimiters.element_separator
        )
        return x12_str + self.delimiters.segment_terminator


```

The X12SegmentGroup model is the base model used to model a X12 loop or transaction set. The X12SegmentGroup also includes
a `x12` method which generates valid x12 from its contained segments.

```python
import abc
from pydantic import BaseModel
from typing import List

class X12SegmentGroup(abc.ABC, BaseModel):
    """
    Abstract base class for a model, typically a loop or transaction, which groups x12 segments.
    """

    def x12(self, use_new_lines=True) -> str:
        """
        :return: Generates a X12 representation of the loop using its segments.
        """
        x12_segments: List[str] = []
        fields = [f for f in self.__fields__.values() if hasattr(f.type_, "x12")]

        for f in fields:
            # process fields
        join_char: str = "\n" if use_new_lines else ""
        return join_char.join(x12_segments)
```
