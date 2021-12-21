"""
test_5010_segments.py

Tests the Pydantic X12 segment models
"""
from linuxforhealth.x12.v5010.segments import *
from decimal import Decimal
from linuxforhealth.x12.models import X12Delimiters


def test_aaa_segment():
    segment_data = {
        "response_code": "Y",
        "reject_reason_code": "42",
        "follow_up_action_code": "Y",
    }
    aaa_segment: AaaSegment = AaaSegment(**segment_data)
    assert aaa_segment.x12() == "AAA*Y**42*Y~"


def test_act_segment():
    segment_data = {
        "tpa_account_number": "1234",
        "tpa_account_number_2": "23498765",
    }
    act_segment: ActSegment = ActSegment(**segment_data)
    assert act_segment.x12() == "ACT*1234*****23498765~"


def test_amt_segment():
    segment_data = {"amount_qualifier_code": "R", "monetary_amount": Decimal("37.5")}
    amt_segment: AmtSegment = AmtSegment(**segment_data)
    assert amt_segment.x12() == "AMT*R*37.50~"


def test_bgn_segment():
    segment_data = {
        "transaction_set_purpose_code": "00",
        "transaction_set_reference_number": "12456",
        "transaction_set_creation_date": "20131020",
        "transaction_set_creation_time": "1200",
        "action_code": "2",
    }

    bgn_segment: BgnSegment = BgnSegment(**segment_data)
    assert bgn_segment.x12() == "BGN*00*12456*20131020*1200****2~"


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


def test_bpr_segment():
    segment_data = {
        "transaction_handling_code": "C",
        "total_actual_provider_payment_amount": "150000.00",
        "credit_debit_flag_code": "C",
        "payment_method_code": "ACH",
        "payment_format_code": "CTX",
        "sender_dfi_qualifier": "01",
        "sender_dfi_id": "999999992",
        "sender_account_qualifier": "DA",
        "sender_account_number": "123456",
        "payer_identifier": "1512345678",
        "sender_supplemental_code": "999999999",
        "receiver_dfi_qualifier": "01",
        "receiver_bank_id_number": "999988880",
        "receiver_account_qualifier": "DA",
        "receiver_account_number": "98765",
        "eft_effective_date": "20030901",
    }
    bpr_segment: BprSegment = BprSegment(**segment_data)
    assert (
        bpr_segment.x12()
        == "BPR*C*150000.00*C*ACH*CTX*01*999999992*DA*123456*1512345678*999999999*01*999988880*DA*98765*20030901~"
    )


def test_cas_segment():
    segment_data = {
        "adjustment_group_code": "PR",
        "adjustment_reason_code_1": "1",
        "monetary_amount_1": "7.93",
    }

    cas_segment: CasSegment = CasSegment(**segment_data)
    assert cas_segment.x12() == "CAS*PR*1*7.93~"


def test_clm_segment():
    segment_data = {
        "patient_control_number": "26463774",
        "total_claim_charge_amount": "100.00",
        "health_care_service_location_information": "11:B:1",
        "provider_or_supplier_signature_indicator": "Y",
        "provider_accept_assignment_code": "A",
        "benefit_assignment_certification_indicator": "Y",
        "release_of_information_code": "I",
    }

    clm_segment: ClmSegment = ClmSegment(**segment_data)
    assert clm_segment.x12() == "CLM*26463774*100.00***11:B:1*Y*A*Y*I~"


def test_clp_segment():
    segment_data = {
        "patient_control_number": "7722337",
        "claim_status_code": "1",
        "total_claim_charge_amount": "211366.97",
        "claim_payment_amount": "138018.40",
        "claim_filing_indicator_code": "12",
        "payer_claim_control_number": "119932404007801",
    }
    clp_segment: ClpSegment = ClpSegment(**segment_data)
    assert clp_segment.x12() == "CLP*7722337*1*211366.97*138018.40**12*119932404007801~"


def test_cl1_segment():
    segment_data = {
        "admission_type_code": "1",
        "admission_source_code": "7",
        "patient_status_code": "30",
    }

    cl1_segment: Cl1Segment = Cl1Segment(**segment_data)
    assert cl1_segment.x12() == "CL1*1*7*30~"


def test_cn1_segment():
    segment_data = {"contract_type_code": "02", "contract_amount": "550"}

    cn1_segment: Cn1Segment = Cn1Segment(**segment_data)
    assert cn1_segment.x12() == "CN1*02*550.00~"


def test_crc_segment():
    segment_data = {
        "code_category": "E1",
        "certification_condition_indicator": "Y",
        "condition_code_1": "L1",
    }
    crc_segment: CrcSegment = CrcSegment(**segment_data)
    assert crc_segment.x12() == "CRC*E1*Y*L1~"


def test_cr1_segment():
    segment_data = {
        "weight_measurement_code": "LB",
        "patient_weight": "140",
        "ambulance_transport_reason_code": "A",
        "mileage_measurement_code": "DH",
        "transport_distance": "12.0",
        "stretcher_purpose_description": "UNCONSCIOUS",
    }

    cr1_segment: Cr1Segment = Cr1Segment(**segment_data)
    assert cr1_segment.x12() == "CR1*LB*140.00**A*DH*12.00****UNCONSCIOUS~"


def test_cr2_segment():
    segment_data = {"patient_condition_code": "M"}
    cr2_segment: Cr2Segment = Cr2Segment(**segment_data)
    assert cr2_segment.x12() == "CR2********M~"


def test_cr3_segment():
    segment_data = {
        "certification_type_code": "I",
        "unit_basis_measurement_code": "MO",
        "durable_medical_equipment_duration": "6.00",
    }
    cr3_segment: Cr3Segment = Cr3Segment(**segment_data)
    assert cr3_segment.x12() == "CR3*I*MO*6.00~"


def test_ctp_segment():
    segment_data = {"quantity": "2.00", "composite_unit_of_measure": "UN"}
    ctp_segment: CtpSegment = CtpSegment(**segment_data)
    assert ctp_segment.x12() == "CTP****2.00*UN~"


def test_cur_segment():
    segment_data = {"entity_identifier_code": "85", "currency_code": "USD"}

    cur_segment: CurSegment = CurSegment(**segment_data)
    assert cur_segment.x12() == "CUR*85*USD~"


def test_dmg_segment():
    segment_data = {
        "date_time_period_format_qualifier": "D8",
        "date_time_period": "19430917",
        "gender_code": "M",
    }

    dmg_segment: DmgSegment = DmgSegment(**segment_data)
    assert dmg_segment.x12() == "DMG*D8*19430917*M~"


def test_dsb_segment():
    segment_data = {
        "disability_type_code": "2",
        "product_service_id_qualifier": "DX",
        "diagnosis_code": "585",
    }
    dsb_segment: DsbSegment = DsbSegment(**segment_data)
    assert dsb_segment.x12() == "DSB*2******DX*585~"


def test_dtm_segment():
    segment_data = {"date_time_qualifier": "405", "production_date": "20020317"}
    dtm_segment: DtmSegment = DtmSegment(**segment_data)
    assert dtm_segment.x12() == "DTM*405*20020317~"


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


def test_ec_segment():
    segment_data = {
        "employment_class_code_1": "04",
        "employment_class_code_2": "06",
        "employment_class_code_3": "07",
    }
    ec_segment: EcSegment = EcSegment(**segment_data)
    assert ec_segment.x12() == "EC*04*06*07~"


def test_eq_segment():
    segment_data = {
        "service_type_code": ["98", "34", "44", "81", "A0", "A3"],
        "coverage_level_code": "FAM",
    }

    eq_segment: EqSegment = EqSegment(**segment_data)
    assert eq_segment.x12() == "EQ*98^34^44^81^A0^A3**FAM~"


def test_frm_segment():
    segment_data = {"question_number_letter": "12", "question_response_1": "N"}

    frm_segment: FrmSegment = FrmSegment(**segment_data)
    assert frm_segment.x12() == "FRM*12*N~"


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


def test_hcp_segment():
    segment_data = {
        "pricing_methodology": "03",
        "repriced_allowed_amount": "100.00",
        "repriced_saving_amount": "10.00",
        "repricing_organization_identifier": "RPO12345",
    }
    hcp_segment: HcpSegment = HcpSegment(**segment_data)
    assert hcp_segment.x12() == "HCP*03*100.00*10.00*RPO12345~"


def test_hd_segment():
    segment_data = {
        "maintenance_type_code": "021",
        "insurance_line_code": "HLT",
        "plan_coverage_description": "PLAN A BCD",
        "coverage_line_code": "FAM",
    }
    hd_segment: HdSegment = HdSegment(**segment_data)
    assert hd_segment.x12() == "HD*021**HLT*PLAN A BCD*FAM~"


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


def test_hlh_segment():
    segment_data = {
        "health_related_code": "X",
        "member_height": "74.00",
        "member_weight": "210.00",
    }

    hlh_segment: HlhSegment = HlhSegment(**segment_data)
    assert hlh_segment.x12() == "HLH*X*74.00*210.00~"


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


def test_icm_segment():
    segment_data = {"frequency_code": "1", "wage_amount": "800", "weekly_hours": "40"}
    icm_segment: IcmSegment = IcmSegment(**segment_data)
    assert icm_segment.x12() == "ICM*1*800.00*40.00~"


def test_idc_segment():
    segment_data = {
        "plan_coverage_description": "12345",
        "identification_card_type_code": "H",
    }
    idc_segment: IdcSegment = IdcSegment(**segment_data)
    assert idc_segment.x12() == "IDC*12345*H~"


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


def test_k3_segment():
    segment_data = {"fixed_format_information": "STATE DATA REQUIREMENT"}
    k3_segment: K3Segment = K3Segment(**segment_data)
    assert k3_segment.x12() == "K3*STATE DATA REQUIREMENT~"


def test_le_segment():
    segment_data = {"loop_id_code": "2120"}
    le_segment: LeSegment = LeSegment(**segment_data)
    assert le_segment.x12() == "LE*2120~"


def test_lin_segment():
    segment_data = {
        "product_service_id_qualifier": "N4",
        "national_drug_code_universal_product_number": "01234567891",
    }
    lin_segment: LinSegment = LinSegment(**segment_data)
    assert lin_segment.x12() == "LIN**N4*01234567891~"


def test_lq_segment():
    segment_data = {"code_list_qualifier_code": "UT", "form_identifier": "1.02"}
    lq_segment: LqSegment = LqSegment(**segment_data)
    assert lq_segment.x12() == "LQ*UT*1.02~"


def test_ls_segment():
    segment_data = {"loop_id_code": "2120"}
    ls_segment: LsSegment = LsSegment(**segment_data)
    assert ls_segment.x12() == "LS*2120~"


def test_lui_segment():
    segment_data = {
        "identification_code_qualifier": "LD",
        "identification_code": "123",
        "language_use_indicator": "8",
    }
    lui_segment: LuiSegment = LuiSegment(**segment_data)
    assert lui_segment.x12() == "LUI*LD*123**8~"


def test_lx_segment():
    segment_data = {"assigned_number": 1}
    lx_segment: LxSegment = LxSegment(**segment_data)
    assert lx_segment.x12() == "LX*1~"


def test_mea_segment():
    segment_data = {
        "measurement_reference_id_code": "TR",
        "measurement_qualifier": "R1",
        "measurement_value": "113.40",
    }
    mea_segment: MeaSegment = MeaSegment(**segment_data)
    assert mea_segment.x12() == "MEA*TR*R1*113.40~"


def test_mia_segment():
    segment_data = {"covered_days_visit_count": "0", "claim_drg_amount": "138018.40"}
    mia_segment: MiaSegment = MiaSegment(**segment_data)
    assert mia_segment.x12() == "MIA*0***138018.40~"


def test_moa_segment():
    segment_data = {"claim_payment_remark_code_1": "A4"}
    moa_segment: MoaSegment = MoaSegment(**segment_data)
    assert moa_segment.x12() == "MOA***A4~"


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


def test_nte_segment():
    segment_data = {
        "note_reference_code": "ADD",
        "description": "SURGERY WAS UNUSUALLY LONG BECAUSE [FILL IN REASON]",
    }
    nte_segment: NteSegment = NteSegment(**segment_data)
    assert (
        nte_segment.x12()
        == "NTE*ADD*SURGERY WAS UNUSUALLY LONG BECAUSE [FILL IN REASON]~"
    )


def test_oi_segment():
    segment_data = {
        "benefits_assignment_certification": "Y",
        "patient_signature_source_code": "P",
        "release_of_information_code": "Y",
    }

    oi_segment: OiSegment = OiSegment(**segment_data)
    assert oi_segment.x12() == "OI***Y*P**Y~"


def test_pat_segment():
    segment_data = {
        "unit_basis_measurement_code": "01",
        "patient_weight": "146.00",
    }
    pat_segment: PatSegment = PatSegment(**segment_data)
    assert pat_segment.x12() == "PAT*******01*146.00~"


def test_pla_segment():
    segment_data = {
        "action_code": "2",
        "entity_identifier_code": "1P",
        "date": "19970628",
        "maintenance_reason_code": "AI",
    }
    pla_segment: PlaSegment = PlaSegment(**segment_data)
    assert pla_segment.x12() == "PLA*2*1P*19970628**AI~"


def test_plb_segment():
    segment_data = {
        "provider_identifier": "1234567890",
        "fiscal_period_date": "20000930",
        "adjustment_reason_code_1": "CV:9876514",
        "provider_adjustment_amount_1": "-1.27",
    }
    plb_segment: PlbSegment = PlbSegment(**segment_data)
    assert plb_segment.x12() == "PLB*1234567890*20000930*CV:9876514*-1.27~"


def test_prv_segment():
    segment_data = {
        "provider_code": "RF",
        "reference_identification_qualifier": "PXC",
        "reference_identification": "207Q00000X",
    }
    prv_segment: PrvSegment = PrvSegment(**segment_data)
    assert prv_segment.x12() == "PRV*RF*PXC*207Q00000X~"


def test_ps1_segment():
    segment_data = {
        "purchased_service_provider_identifier": "PN222222",
        "purchased_service_charge_amount": "110.00",
    }
    ps1_segment: Ps1Segment = Ps1Segment(**segment_data)
    assert ps1_segment.x12() == "PS1*PN222222*110.00~"


def test_pwk_segment():
    segment_data = {
        "segment_name": "PWK",
        "report_type_code": "OZ",
        "report_transmission_code": "BM",
        "identification_code_qualifier": "AC",
        "identification_code": "DMN0012",
    }

    pwk_segment: PwkSegment = PwkSegment(**segment_data)
    assert pwk_segment.x12() == "PWK*OZ*BM***AC*DMN0012~"


def test_qty_segment():
    segment_data = {"quantity_qualifier": "PT", "quantity": "2.00"}
    qty_segment: QtySegment = QtySegment(**segment_data)
    assert qty_segment.x12() == "QTY*PT*2.00~"


def test_rdm_segment():
    segment_data = {"report_transmission_code": "BM", "name": "JANE DOE"}
    rdm_segment: RdmSegment = RdmSegment(**segment_data)
    assert rdm_segment.x12() == "RDM*BM*JANE DOE~"


def test_ref_segment():
    segment_data = {
        "reference_identification_qualifier": "EO",
        "reference_identification": "477563928",
    }
    ref_segment: RefSegment = RefSegment(**segment_data)
    assert ref_segment.x12() == "REF*EO*477563928~"


def test_sbr_segment():
    segment_data = {
        "payer_responsibility_code": "P",
        "group_policy_number": "2222-SJ",
        "claim_filing_indicator_code": "CI",
    }
    sbr_segment: SbrSegment = SbrSegment(**segment_data)
    assert sbr_segment.x12() == "SBR*P**2222-SJ******CI~"


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


def test_stc_segment():
    segment_data = {
        "health_care_claim_status_1": "E0:24:41",
        "status_effective_date": "20050830",
    }

    stc_segment: StcSegment = StcSegment(**segment_data)
    assert stc_segment.x12() == "STC*E0:24:41*20050830~"


def test_svc_segment():
    segment_data = {
        "composite_medical_procedure_identifier_1": "HC:99214",
        "line_item_charge_amount": "100.00",
        "line_item_provider_payment_amount": "80.00",
    }
    svc_segment: SvcSegment = SvcSegment(**segment_data)
    assert svc_segment.x12() == "SVC*HC:99214*100.00*80.00~"


def test_sv1_segment():
    segment_data = {
        "product_service_id_qualifier": "HC:99213",
        "line_item_charge_amount": "40.00",
        "unit_basis_measurement_code": "UN",
        "service_unit_count": "1.00",
        "composite_diagnosis_code_pointer": "1",
    }
    sv1_segment: Sv1Segment = Sv1Segment(**segment_data)
    assert sv1_segment.x12() == "SV1*HC:99213*40.00*UN*1.00***1~"


def test_sv2_segment():
    segment_data = {
        "service_line_revenue_code": "0120",
        "line_item_charge_amount": "1500.00",
        "measurement_code": "DA",
        "service_unit_count": "5.00",
    }
    sv2_segment: Sv2Segment = Sv2Segment(**segment_data)
    assert sv2_segment.x12() == "SV2*0120**1500.00*DA*5.00~"


def test_sv5_segment():
    segment_data = {
        "product_service_id_qualifier": "HC:A4631",
        "unit_basis_measurement_code": "DA",
        "length_of_medical_necessity": "30.00",
        "dme_rental_price": "50.00",
        "dme_purchase_price": "5000.00",
        "rental_unit_price_indicator": "4",
    }
    sv5_segment: Sv5Segment = Sv5Segment(**segment_data)
    assert sv5_segment.x12() == "SV5*HC:A4631*DA*30.00*50.00*5000.00*4~"


def test_svd_segment():
    segment_data = {
        "other_payer_primary_identifier": "43",
        "service_line_paid_amount": "55.00",
        "composite_medical_procedure_identifier": "HC:84550",
        "paid_service_count": "3.00",
    }
    svd_segment: SvdSegment = SvdSegment(**segment_data)
    assert svd_segment.x12() == "SVD*43*55.00*HC:84550**3.00~"


def test_trn_segment():
    segment_data = {
        "trace_type_code": "1",
        "reference_identification_1": "98175-012547",
        "originating_company_identifier": "8877281234",
        "reference_identification_2": "RADIOLOGY",
    }

    trn_segment: TrnSegment = TrnSegment(**segment_data)
    assert trn_segment.x12() == "TRN*1*98175-012547*8877281234*RADIOLOGY~"


def test_ts2_segment():
    segment_data = {
        "total_drg_amount": "59786.00",
        "total_federal_specific_amount": "55375.77",
    }
    ts2_segment: Ts2Segment = Ts2Segment(**segment_data)
    assert ts2_segment.x12() == "TS2*59786.00*55375.77~"


def test_ts3_segment():
    segment_data = {
        "provider_identifier": "123456",
        "facility_type_code": "11",
        "fiscal_period_date": "20021031",
        "total_claim_count": "10",
        "total_claim_charge_amount": "130957.66",
    }
    ts3_segment: Ts3Segment = Ts3Segment(**segment_data)
    assert ts3_segment.x12() == "TS3*123456*11*20021031*10*130957.66~"


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
