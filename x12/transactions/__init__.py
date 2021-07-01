"""
transactions.py

The transactions module serves as the package root for X12 transaction implementations.
Transaction implementations are stored in separate packages with the following structure

    x12_[transaction_code]_[implementation_version]
    / loops.py -Defines the loop models used within the transaction.
    / parse.py - Defines the segment parsers used to build the transactional loops.
    / segments.py - Contains the overriden/subclassed segments used to support the transactional specification.
    / transaction_set.py - The high level transaction set model which is returned by the model reader
"""
