"""
test_4010_segments.py

Tests the Pydantic X12 segment models specific to the 4010 specification
"""
from linuxforhealth.x12.v4010.segments import Cr7Segment, Cr5Segment, Cr6Segment


def test_cr5_segment():
    segment_data = {
        "certification_type_code": "I",
        "treatment_period_count": "6",
        "arterial_blood_gas_quantity": "56",
        "oxygen_test_condition_code": "R",
        "oxygen_test_findings_code_1": "1",
    }
    cr5_segment: Cr5Segment = Cr5Segment(**segment_data)
    assert cr5_segment.x12() == "CR5*I*6.00********56.00**R*1~"


def test_cr7_segment():
    segment_data = {
        "discipline_type_code": "PT",
        "total_visits_rendered": "4",
        "total_visits_projected": "12",
    }
    cr7_segment: Cr7Segment = Cr7Segment(**segment_data)
    assert cr7_segment.x12() == "CR7*PT*4*12~"


def test_cr6_segment():
    segment_data = {
        "prognosis_indicator": "4",
        "soc_date": "19941191",
        "date_time_period_format_qualifier": "RD8",
        "certification_period": "19941101-19941231",
        "diagnosis_date": "19941015",
        "skilled_nursing_facility_indicator": "N",
        "medicare_coverage_indicator": "Y",
        "certification_type_indicator": "I",
        "last_visit_date": "19941101",
        "patient_location_code": "A",
    }
    cr6_segment: Cr6Segment = Cr6Segment(**segment_data)
    assert (
        cr6_segment.x12()
        == "CR6*4*19941191*RD8*19941101-19941231*19941015*N*Y*I*****19941101****A~"
    )
