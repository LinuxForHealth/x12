"""
test_segments.py

Tests the Pydantic X12 segment models
"""
from x12.segments import *
from decimal import Decimal
from x12.models import X12Delimiters


def test_aaa_segment():
    segment_data = {
        "response_code": "Y",
        "reject_reason_code": "42",
        "follow_up_action_code": "Y",
    }
    aaa_segment: AaaSegment = AaaSegment(**segment_data)
    assert aaa_segment.x12() == "AAA*Y**42*Y~"


def test_amt_segment():
    segment_data = {"amount_qualifier_code": "R", "monetary_amount": Decimal("37.5")}
    amt_segment: AmtSegment = AmtSegment(**segment_data)
    assert amt_segment.x12() == "AMT*R*37.50~"


def test_bht_segment():
    segment_data = {
        "hierarchical_structure_code": "0022",
        "transaction_set_purpose_code": "01",
        "submitter_transactional_identifier": "1c257041a955432091b0c073d788d29a",
        "transaction_set_creation_date": "19980101",
        "transaction_set_creation_time": "1400",
        "transaction_type_code": "RT",
    }

    bht_segment: BhtSegment = BhtSegment(**segment_data)
    assert (
        bht_segment.x12()
        == "BHT*0022*01*1c257041a955432091b0c073d788d29a*19980101*1400*RT~"
    )


def test_dmg_segment():
    segment_data = {
        "date_time_period_format_qualifier": "D8",
        "date_time_period": "19430917",
        "gender_code": "M",
    }

    dmg_segment: DmgSegment = DmgSegment(**segment_data)
    assert dmg_segment.x12() == "DMG*D8*19430917*M~"


def test_dtp_segment_date_period():
    segment_data = {
        "date_time_qualifier": "291",
        "date_time_period_format_qualifier": "D8",
        "date_time_period": "20051015",
    }

    dtp_segment: DtpSegment = DtpSegment(**segment_data)
    assert dtp_segment.x12() == "DTP*291*D8*20051015~"


def test_dtp_segment_date_range():
    segment_data = {
        "date_time_qualifier": "291",
        "date_time_period_format_qualifier": "RD8",
        "date_time_period": "20051015-20051201",
    }

    dtp_segment: DtpSegment = DtpSegment(**segment_data)
    assert dtp_segment.x12() == "DTP*291*RD8*20051015-20051201~"


def test_eb_segment():
    segment_data = {
        "eligibility_benefit_information": "B",
        "service_type_code": [
            "1",
            "33",
            "35",
            "47",
            "86",
            "88",
            "98",
            "AL",
            "MH",
            "UC",
        ],
        "insurance_type_code": "HM",
        "plan_coverage_description": "GOLD 123 PLAN",
        "time_period_qualifier": "27",
        "benefit_amount": "10.00",
        "inplan_network_indicator": "Y",
    }

    eb_segment: EbSegment = EbSegment(**segment_data)
    assert (
        eb_segment.x12()
        == "EB*B**1^33^35^47^86^88^98^AL^MH^UC*HM*GOLD 123 PLAN*27*10.00*****Y~"
    )


def test_eq_segment():
    segment_data = {
        "service_type_code": ["98", "34", "44", "81", "A0", "A3"],
        "coverage_level_code": "FAM",
    }

    eq_segment: EqSegment = EqSegment(**segment_data)
    assert eq_segment.x12() == "EQ*98^34^44^81^A0^A3**FAM~"


def test_ge_segment():
    segment_data = {
        "number_of_transaction_sets_included": 1,
        "group_control_number": "1",
    }

    ge_segment: GeSegment = GeSegment(**segment_data)
    assert ge_segment.x12() == "GE*1*1~"


def test_gs_segment():
    segment_data = {
        "functional_identifier_code": "HS",
        "application_sender_code": "000000005",
        "application_receiver_code": "54321",
        "functional_group_creation_date": "20131031",
        "functional_group_creation_time": "1147",
        "group_control_number": "1",
        "responsible_agency_code": "X",
        "version_identifier_code": "005010X279A",
    }

    gs_segment: GsSegment = GsSegment(**segment_data)
    assert gs_segment.x12() == "GS*HS*000000005*54321*20131031*1147*1*X*005010X279A~"


def test_hi_segment():
    segment_data = {
        "health_care_code_1": ["BK", "8901"],
        "health_care_code_2": ["BF", "87200"],
        "health_care_code_3": ["BF", "5559"],
    }
    hi_segment: HiSegment = HiSegment(**segment_data)
    assert hi_segment.x12() == "HI*BK:8901*BF:87200*BF:5559~"


def test_hl_segment():
    segment_data = {
        "hierarchical_id_number": "3",
        "hierarchical_parent_id_number": "2",
        "hierarchical_level_code": "22",
        "hierarchical_child_code": "0",
    }

    hl_segment: HlSegment = HlSegment(**segment_data)
    assert hl_segment.x12() == "HL*3*2*22*0~"


def test_hsd_segment():
    segment_data = {
        "quantity_qualifier": "VS",
        "quantity": 12.00,
        "measurement_code": "WK",
        "sample_selection_modulus": 3.00,
        "time_period_qualifier": "34",
        "period_count": 1.00,
    }
    hsd_segment: HsdSegment = HsdSegment(**segment_data)
    assert hsd_segment.x12() == "HSD*VS*12.00*WK*3.00*34*1.00~"


def test_iea_segment():
    segment_data = {
        "number_of_included_functional_groups": 1,
        "interchange_control_number": "000000907",
    }

    iea_segment: IeaSegment = IeaSegment(**segment_data)
    assert iea_segment.x12() == "IEA*1*000000907~"


def test_iii_segment():
    segment_data = {"code_list_qualifier_code": "ZZ", "industry_code": "21"}
    iii_segment: IiiSegment = IiiSegment(**segment_data)
    assert iii_segment.x12() == "III*ZZ*21~"


def test_ins_segment():
    segment_data = {
        "member_indicator": "Y",
        "individual_relationship_code": "18",
        "maintenance_type_code": "021",
        "maintenance_reason_code": "28",
        "benefit_status_code": "A",
        "employment_status_code": "FT",
    }
    ins_segment: InsSegment = InsSegment(**segment_data)
    assert ins_segment.x12() == "INS*Y*18*021*28*A***FT~"


def test_isa_segment():
    segment_data = {
        "authorization_information_qualifier": "03",
        "authorization_information": "9876543210",
        "security_information_qualifier": "01",
        "security_information": "9876543210",
        "interchange_sender_qualifier": "30",
        "interchange_sender_id": "000000005      ",
        "interchange_receiver_qualifier": "30",
        "interchange_receiver_id": "12345          ",
        "interchange_date": "131031",
        "interchange_time": "1147",
        "repetition_separator": "^",
        "interchange_control_version_number": "00501",
        "interchange_control_number": "000000907",
        "acknowledgment_requested": "1",
        "interchange_usage_indicator": "T",
        "component_element_separator": ":",
    }

    isa_segment: IsaSegment = IsaSegment(**segment_data)
    assert (
        isa_segment.x12()
        == "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~"
    )


def test_le_segment():
    segment_data = {"loop_id_code": "2120"}
    le_segment: LeSegment = LeSegment(**segment_data)
    assert le_segment.x12() == "LE*2120~"


def test_ls_segment():
    segment_data = {"loop_id_code": "2120"}
    ls_segment: LsSegment = LsSegment(**segment_data)
    assert ls_segment.x12() == "LS*2120~"


def test_msg_segment():
    segment_data = {"free_form_text": "this is free form text"}
    msg_segment: MsgSegment = MsgSegment(**segment_data)
    assert msg_segment.x12() == "MSG*this is free form text~"


def test_n3_segment():
    segment_data = {
        "address_information_1": "201 PARK AVENUE",
        "address_information_2": "SUITE 300",
    }
    n3_segment: N3Segment = N3Segment(**segment_data)
    assert n3_segment.x12() == "N3*201 PARK AVENUE*SUITE 300~"


def test_n4_segment():
    segment_data = {
        "city_name": "KANSAS CITY",
        "state_province_code": "MO",
        "postal_code": "64108",
    }
    n4_segment: N4Segment = N4Segment(**segment_data)
    assert n4_segment.x12() == "N4*KANSAS CITY*MO*64108~"


def test_nm1_segment():
    segment_data = {
        "entity_identifier_code": "PR",
        "entity_type_qualifier": "2",
        "name_last_or_organization_name": "ACME",
        "identification_code_qualifier": "PI",
        "identification_code": "12345",
    }
    nm1_segment: Nm1Segment = Nm1Segment(**segment_data)
    assert nm1_segment.x12() == "NM1*PR*2*ACME*****PI*12345~"


def test_prv_segment():
    segment_data = {
        "provider_code": "RF",
        "reference_identification_qualifier": "PXC",
        "reference_identification": "207Q00000X",
    }
    prv_segment: PrvSegment = PrvSegment(**segment_data)
    assert prv_segment.x12() == "PRV*RF*PXC*207Q00000X~"


def test_ref_segment():
    segment_data = {
        "reference_identification_qualifier": "EO",
        "reference_identification": "477563928",
    }
    ref_segment: RefSegment = RefSegment(**segment_data)
    assert ref_segment.x12() == "REF*EO*477563928~"


def test_se_segment():
    segment_data = {
        "transaction_segment_count": 17,
        "transaction_set_control_number": "0001",
    }

    se_segment: SeSegment = SeSegment(**segment_data)
    assert se_segment.x12() == "SE*17*0001~"


def test_st_segment():
    segment_data = {
        "transaction_set_identifier_code": "270",
        "transaction_set_control_number": "0001",
        "implementation_convention_reference": "005010X279A1",
    }

    st_segment: StSegment = StSegment(**segment_data)
    assert st_segment.x12() == "ST*270*0001*005010X279A1~"


def test_trn_segment():
    segment_data = {
        "trace_type_code": "1",
        "reference_identification_1": "98175-012547",
        "originating_company_identifier": "8877281234",
        "reference_identification_2": "RADIOLOGY",
    }

    trn_segment: TrnSegment = TrnSegment(**segment_data)
    assert trn_segment.x12() == "TRN*1*98175-012547*8877281234*RADIOLOGY~"


def test_segment_lookup():
    """Basic validations to ensure that the segment lookup loads"""

    assert len(SEGMENT_LOOKUP) > 0
    assert "GE" in SEGMENT_LOOKUP
    assert "GS" in SEGMENT_LOOKUP
    assert "IEA" in SEGMENT_LOOKUP
    assert "ISA" in SEGMENT_LOOKUP
    assert "ST" in SEGMENT_LOOKUP
    assert "SE" in SEGMENT_LOOKUP


def test_x12_with_custom_delimiters():
    """tests x12 generation where custom delimiters are used"""
    x12_delimiters: X12Delimiters = X12Delimiters(
        element_separator="|", segment_terminator="?"
    )

    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "trace_type_code": "1",
        "reference_identification_1": "98175-012547",
        "originating_company_identifier": "8877281234",
        "reference_identification_2": "RADIOLOGY",
    }

    trn_segment: TrnSegment = TrnSegment(**segment_data)
    assert trn_segment.x12() == "TRN|1|98175-012547|8877281234|RADIOLOGY?"
