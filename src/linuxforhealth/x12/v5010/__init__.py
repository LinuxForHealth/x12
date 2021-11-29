"""
v5010.py

The v5010 module serves as the package root for X12 "5010" transaction implementations.
Transaction implementations are stored in separate packages with the following structure:

    x12_[transaction_code]_[implementation_version]
    / loops.py - Transaction Loop Domain Models
    / parsing.py - Transaction Set Parser Implementation and Loop Parser Functions
    / segments.py - Specialized Segments for Loop Domain Models
    / transaction_set.py - Transaction Set Domain Model
"""
