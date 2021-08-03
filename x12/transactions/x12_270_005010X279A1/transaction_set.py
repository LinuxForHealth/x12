"""
transaction_set.py

Defines the Eligibility 270 005010X279A1 transaction set model.
"""

from typing import List, Dict, Union

from x12.models import X12SegmentGroup

from .loops import Footer, Header, Loop2000A


class EligibilityInquiry(X12SegmentGroup):
    """ """

    header: Header
    loop_2000a: List[Loop2000A]
    footer: Footer

    @property
    def information_source(self, return_first=True) -> Union[List, Dict]:
        """
        Returns Information Source Loops 2000A and 2100A within a single "record" (dictionary).

        :param return_first: Indicates if the first result is returned. When set to False all results are returned.
        :returns: Dictionary if return_first = True, otherwise returns a List
        """
        result = [
            info_source.dict(exclude={"loop_2000b"}) for info_source in self.loop_2000a
        ]
        return result[0] if return_first else result

    @property
    def information_receiver(self, return_first=True) -> Union[List, Dict]:
        """
        Returns Information Receiver Loops 2000B and 2100B within a single "record" (dictionary).

        :param return_first: Indicates if the first result is returned. When set to False all results are returned.
        :returns: Dictionary if return_first = True, otherwise returns a List
        """
        result = []

        for info_source in self.loop_2000a:
            for info_receiver in info_source.loop_2000b:
                result.append(info_receiver.dict(exclude={"loop_2000c"}))
        return result[0] if return_first else result

    @property
    def subscriber(self, return_first=True) -> Union[List, Dict]:
        """
        Returns Subscriber Loops 2000C, 2100C, and 2110C within a single "record" (dictionary).

        :param return_first: Indicates if the first result is returned. When set to False all results are returned.
        :returns: Dictionary if return_first = True, otherwise returns a List
        """
        result = []

        for info_source in self.loop_2000a:
            for info_receiver in info_source.loop_2000b:
                for subscriber in info_receiver.loop_2000c:
                    result.append(subscriber.dict(exclude={"loop_2000d"}))
        return result[0] if return_first else result

    @property
    def dependent(self, return_first=True) -> Union[List, Dict]:
        """
        Returns Dependent Loops 2000D, 2100D, and 2110D within a single "record" (dictionary).

        :param return_first: Indicates if the first result is returned. When set to False all results are returned.
        :returns: Dictionary or List if a dependent is present, based on `return_first`. If no dependent is present, returns None.
        """
        result = []

        for info_source in self.loop_2000a:
            for info_receiver in info_source.loop_2000b:
                for subscriber in info_receiver.loop_2000c:
                    if subscriber.loop_2000d:
                        for dependent in subscriber.loop_2000d:
                            result.append(dependent.dict())

        if return_first:
            return result[0] if result else None
        else:
            return result if len(result) else None
