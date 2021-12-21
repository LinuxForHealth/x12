"""
segments.py

The segments module contains models for ALL ASC X12 5010 segments used within health care transactions.
The segments defined within this module serve as "base models" for transactional use, where a segment subclass is defined
and overriden as necessary to support a transaction's specific validation and usage constraints.
"""

import datetime
from enum import Enum
from typing import Dict, List, Literal, Optional, Tuple, Union
from decimal import Decimal

from pydantic import Field, PositiveInt, condecimal, validator, root_validator, conint

from linuxforhealth.x12.models import X12Segment, X12SegmentName
from linuxforhealth.x12.support import (
    parse_x12_date,
    parse_interchange_date,
    field_validator,
)
from linuxforhealth.x12.validators import validate_date_field


class AaaSegment(X12Segment):
    """
    Request validation.
    Example:
        AAA*Y**42*Y~
    """

    class ResponseCode(str, Enum):
        """
        AAA01 code values
        """

        NO = "N"
        YES = "Y"

    segment_name: X12SegmentName = X12SegmentName.AAA
    response_code: ResponseCode
    agency_qualifier_code: Optional[str] = Field(max_length=2)
    reject_reason_code: str = Field(min_length=2, max_length=2)
    follow_up_action_code: str = Field(min_length=1, max_length=1)


class ActSegment(X12Segment):
    """
    Account Identification
    Example:
        ACT*1234*****23498765~
    """

    segment_name: X12SegmentName = X12SegmentName.ACT
    tpa_account_number: str = Field(min_length=1, max_length=35)
    name: Optional[str] = Field(max_length=60)
    identification_code_qualifier: Optional[str] = Field(max_length=2)
    identification_code: Optional[str] = Field(max_length=80)
    account_number_qualifier: Optional[str] = Field(max_length=3)
    tpa_account_number_2: Optional[str] = Field(min_length=1, max_length=35)
    description: Optional[str] = Field(max_length=80)
    payment_method_type_code: Optional[str] = Field(max_length=2)
    benefit_status_code: Optional[str] = Field(max_length=1)


class AmtSegment(X12Segment):
    """
    Monetary Amount Information.
    Example:
        AMT*R*37.5~
    """

    segment_name: X12SegmentName = X12SegmentName.AMT
    amount_qualifier_code: str = Field(min_length=1, max_length=3)
    monetary_amount: Decimal
    credit_debit_flag_code: Optional[str] = Field(min_length=0, max_length=1)


class BgnSegment(X12Segment):
    """
    Beginning Segment
    Example:
        BGN*00*12456*20131020*1200****2~
    """

    class TransactionSetPurposeCode(str, Enum):
        """
        Code values for BGN01
        """

        ORIGINAL = "00"
        RESUBMISSION = "15"
        INFORMATION_COPY = "22"

    class TimeZoneCode(str, Enum):
        """
        Code values for BGN05
        """

        ISO_PS01 = "01"
        ISO_PS02 = "02"
        ISO_PS03 = "03"
        ISO_PS04 = "04"
        ISO_PS05 = "05"
        ISO_PS06 = "06"
        ISO_PS07 = "07"
        ISO_PS08 = "08"
        ISO_PS09 = "09"
        ISO_PS10 = "10"
        ISO_PS11 = "11"
        ISO_PS12 = "12"
        ISO_PS13 = "13"
        ISO_PS14 = "14"
        ISO_PS15 = "15"
        ISO_PS16 = "16"
        ISO_PS17 = "17"
        ISO_PS18 = "18"
        ISO_PS19 = "19"
        ISO_PS20 = "20"
        ISO_PS21 = "21"
        ISO_PS22 = "22"
        ISO_PS23 = "23"
        ISO_PS24 = "24"
        ALASKA_DAYLIGHT_TIME = "AD"
        ALASKA_STANDARD_TIME = "AS"
        ALASKA_TIME = "AT"
        CENTRAL_DAYLIGHT_TIME = "CD"
        CENTRAL_STANDARD_TIME = "CS"
        CENTRAL_TIME = "CT"
        EASTERN_DAYLIGHT_TIME = "ED"
        EASTERN_STANDARD_TIME = "ES"
        EASTERN_TIME = "ET"
        GREENWICH_MEAN_TIME = "GM"
        HAWAII_ALEUTIAN_DAYLIGHT_TIME = "HD"
        HAWAII_ALEUTIAN_STANDARD_TIME = "HS"
        HAWAII_ALEUTIAN_TIME = "HT"
        LOCAL_TIME = "LT"
        MOUNTAIN_DAYLIGHT_TIME = "MD"
        MOUNTAIN_STANDARD_TIME = "MS"
        MOUNTAIN_TIME = "MT"
        NEWFOUNDLAND_DAYLIGHT_TIME = "ND"
        NEWFOUNDLAND_STANDARD_TIME = "NS"
        NEWFOUNDLAND_TIME = "NT"
        PACIFIC_DAYLIGHT_TIME = "PD"
        PACIFIC_STANDARD_TIME = "PS"
        PACIFIC_TIME = "PT"
        ATLANTIC_DAYLIGHT_TIME = "TD"
        ATLANTIC_STANDARD_TIME = "TT"
        UNIVERSAL_TIME_COORDINATE = "UT"

    class ActionCode(str, Enum):
        """
        Code values for BGN08
        """

        CHANGE = "2"
        VERIFY = "4"
        REPLACE = "RX"

    segment_name: X12SegmentName = X12SegmentName.BGN
    transaction_set_purpose_code: TransactionSetPurposeCode
    transaction_set_reference_number: str = Field(min_length=1, max_length=50)
    transaction_set_creation_date: Union[str, datetime.date]
    transaction_set_creation_time: Union[str, datetime.time]
    time_zone_code: Optional[TimeZoneCode]
    original_transaction_set_reference_number: Optional[str] = Field(
        min_length=1, max_length=50
    )
    transaction_type_code: Optional[str] = Field(min_length=2, max_length=2)
    action_code: ActionCode
    security_level_code: Optional[str] = Field(min_length=2, max_length=2)


class BhtSegment(X12Segment):
    """
    Defines the business application purpose and supporting reference data for the transaction.
    Example:
        BHT*0022*01**19980101*1400*RT~
    """

    segment_name: X12SegmentName = X12SegmentName.BHT
    hierarchical_structure_code: str = Field(min_length=4, max_length=4)
    transaction_set_purpose_code: str = Field(min_length=2, max_length=2)
    submitter_transactional_identifier: str = Field(min_length=1, max_length=50)
    transaction_set_creation_date: Union[str, datetime.date]
    transaction_set_creation_time: str
    transaction_type_code: str = Field(min_length=2, max_length=2)

    _validate_transaction_date = field_validator("transaction_set_creation_date")(
        parse_x12_date
    )


class BprSegment(X12Segment):
    """
    Financial Information
    Example:
        BPR*C*150000*C*ACH*CTX*01*999999992*DA*123456*1512345678*999999999*01*999988880*DA*98765*20030901~
    """

    class TransactionHandlingCode(str, Enum):
        """
        Code values for BPR01
        """

        PAYMENT_ACCOMPANIES_REMITTANCE_ADVICE = "C"
        MAKE_PAYMENT_ONLY = "D"
        NOTIFICATION_ONLY = "H"
        REMITTANCE_INFORMATION_ONLY = "I"
        PRENOTIFICATION_FUTURE_TRANSFERS = "P"
        SPLIT_PAYMENT_REMITTANCE = "U"
        HANDLING_PARTY_OPTION_TO_SPLIT_PAYMENT_REMITTANCE = "X"

    class CreditDebitFlagCode(str, Enum):
        """
        Code values for BPR03
        """

        CREDIT = "C"
        DEBIT = "D"

    class PaymentMethodCode(str, Enum):
        """
        Code values for BPR04
        """

        AUTOMATED_CLEARING_HOUSE = "ACH"
        FINANCIAL_INSTITUTION_OPTION = "BOP"
        CHECK = "CHK"
        FEDERAL_RESERVE_WIRE_TRANSFER = "FWT"
        NON_PAYMENT_DATA = "NON"

    class PaymentFormatCode(str, Enum):
        """
        Code values for BPR05
        """

        CASH_DISBURSEMENT_PLUS_ADDENDA = "CCP"
        CORPORATE_TAX_EXCHANGE = "CTX"

    class FinancialInstitutionIdQualifier(str, Enum):
        """
        Code values for BPR06
        """

        ABA_TRANSIT_ROUTING_NUMBER = "01"
        CANADIAN_BANK_BRANCH_INSTITUTION_NUMBER = "04"

    class DfiIdentificationQualifier(str, Enum):
        """
        Code values for BPR12
        """

        ABA_TRANSIT_ROUTING_NUMBER = "01"
        CANADIAN_BANK_BRANCH_INSTITUTION_NUMBER = "04"

    class AccountNumberQualifier(str, Enum):
        """
        Code values for BPR14
        """

        DEMAND_DEPOSIT = "DA"
        SAVINGS = "SG"

    segment_name: X12SegmentName = X12SegmentName.BPR
    transaction_handling_code: TransactionHandlingCode
    total_actual_provider_payment_amount: Decimal
    credit_debit_flag_code: CreditDebitFlagCode
    payment_method_code: PaymentMethodCode
    payment_format_code: Optional[PaymentFormatCode]
    sender_dfi_qualifier: Optional[FinancialInstitutionIdQualifier]
    sender_dfi_id: Optional[str] = Field(max_length=12)
    sender_account_qualifier: Optional[Literal["DA"]]
    sender_account_number: Optional[str] = Field(max_length=35)
    payer_identifier: Optional[str] = Field(max_length=10)
    sender_supplemental_code: Optional[str] = Field(max_length=9)
    receiver_dfi_qualifier: Optional[FinancialInstitutionIdQualifier]
    receiver_bank_id_number: Optional[str] = Field(max_length=12)
    receiver_account_qualifier: Optional[AccountNumberQualifier]
    receiver_account_number: Optional[str] = Field(max_length=35)
    eft_effective_date: Optional[Union[str, datetime.date]]

    _validate_x12_date = field_validator("eft_effective_date")(validate_date_field)

    @validator("payment_format_code")
    def validate_payment_format_code(cls, v, values):
        """
        Validates that the payment format code is present for ACH transactions
        """
        is_ach = values.get("payment_method_code") == "ACH"
        if is_ach and not v:
            raise ValueError("payment_format_code is required for ACH transactions")
        return v

    @root_validator(pre=True)
    def validate_electronic_payment_fields(cls, values):
        """
        Validates the required fields for electronic transactions
        """
        payment_code = values.get("payment_method_code")

        if payment_code not in ("ACH", "BOP", "FTW"):
            return values

        for f in (
            "sender_dfi_qualifier",
            "sender_dfi_id",
            "sender_account_qualifier",
            "sender_account_number",
            "payer_identifier",
            "receiver_dfi_qualifier",
            "receiver_bank_id_number",
            "receiver_account_qualifier",
            "receiver_account_number",
        ):

            if not values.get(f):
                raise ValueError(f"{f} is required for electronic transactions")

        return values


class CasSegment(X12Segment):
    """
    Claim level adjustments
    Example:
        CAS*PR*1*7.93~
    """

    class ClaimAdjustmentGroupCode(str, Enum):
        """
        Code values for CAS01
        """

        CONTRACTUAL_OBLIGATIONS = "CO"
        CORRECTION_AND_REVERSALS = "CR"
        OTHER_ADJUSTMENTS = "OA"
        PAYER_INITIATED_REDUCTIONS = "PI"
        PATIENT_RESPONSIBILITY = "PR"

    segment_name: X12SegmentName = X12SegmentName.CAS
    adjustment_group_code: ClaimAdjustmentGroupCode

    adjustment_reason_code_1: str = Field(min_length=1, max_length=5)
    monetary_amount_1: Decimal
    quantity_1: Optional[Decimal]

    adjustment_reason_code_2: Optional[str] = Field(max_length=5)
    monetary_amount_2: Optional[Decimal]
    quantity_2: Optional[Decimal]

    adjustment_reason_code_3: Optional[str] = Field(max_length=12)
    monetary_amount_3: Optional[Decimal]
    quantity_3: Optional[Decimal]

    adjustment_reason_code_4: Optional[str] = Field(max_length=12)
    monetary_amount_4: Optional[Decimal]
    quantity_4: Optional[Decimal]

    adjustment_reason_code_5: Optional[str] = Field(max_length=12)
    monetary_amount_5: Optional[Decimal]
    quantity_5: Optional[Decimal]

    adjustment_reason_code_6: Optional[str] = Field(max_length=12)
    monetary_amount_6: Optional[Decimal]
    quantity_6: Optional[Decimal]

    @root_validator
    def validate_adjustments(cls, values):
        """
        Validates that an adjustment "set" has a reason code, amount, and quantity.

        :param values: The raw, unvalidated transaction data.
        """
        for i in range(1, 7, 1):
            adjustment_fields: Tuple = (
                values.get(f"adjustment_reason_code_{i}"),
                values.get(f"monetary_amount_{i}"),
            )

            if any(adjustment_fields) and not all(adjustment_fields):
                raise ValueError(
                    f"Adjustment set {i} is required to have a reason code, amount, and quantity"
                )

        return values


class ClmSegment(X12Segment):
    """
    Claim Information Segment
    Example:
        CLM*26463774*100***11:B:1*Y*A*Y*I~
    """

    class ProviderOrSupplierSignatureIndicator(str, Enum):
        """
        Code values for CLM06
        """

        NO = "N"
        YES = "Y"

    class ProviderAcceptAssignmentCode(str, Enum):
        """
        Code values for CLM07
        """

        ASSIGNED = "A"
        ASSIGNMENT_ACCEPTED_CLINICAL_LAB_ONLY = "B"
        NOT_ASSIGNED = "C"

    class BenefitsAssignmentCertificationIndicator(str, Enum):
        """
        Code values for CLM08
        """

        NO = "N"
        NOT_APPLICABLE = "W"
        YES = "Y"

    class ReleaseOfInformationCode(str, Enum):
        """
        Code values for CLM09
        """

        INFORMED_CONSENT_NO_SIGNATURE = "I"
        SIGNED_STATEMENT = "Y"

    class DelayReasonCode(str, Enum):
        """
        Code values for CLM20
        """

        PROOF_OF_ELIGIBILITY_UNKNOWN_UNAVAILABLE = "1"
        LITIGATION = "2"
        AUTHORIZATION_DELAYS = "3"
        DELAY_IN_CERTIFYING_PROVIDER = "4"
        DELAY_IN_SUPPLYING_BILLING_FORMS = "5"
        DELAY_IN_DELIVERY_OF_CUSTOM_APPLIANCES = "6"
        THIRD_PARTY_PROCESSING_DELAY = "7"
        DELAY_IN_ELIGIBILITY_DETERMINATION = "8"
        ORIGINAL_CLAIM_REJECTED_DENIED_UNRELATED_TO_BILLING = "9"
        ADMINISTRATION_DELAY_PRIOR_APPROVAL = "10"
        OTHER = "11"
        NATURAL_DISASTER = "15"

    segment_name: X12SegmentName = X12SegmentName.CLM
    patient_control_number: str = Field(min_length=1, max_length=38)
    total_claim_charge_amount: Decimal = Decimal("0.00")
    claim_filing_indicator_code: Optional[str] = Field(min_length=1, max_length=2)
    non_institutional_claim_type_code: Optional[str] = Field(min_length=1, max_length=2)
    health_care_service_location_information: str = Field(is_component=True)
    provider_or_supplier_signature_indicator: Optional[str] = Field(max_length=1)
    provider_accept_assignment_code: ProviderAcceptAssignmentCode
    benefit_assignment_certification_indicator: BenefitsAssignmentCertificationIndicator
    release_of_information_code: ReleaseOfInformationCode
    patient_signature_source_code: Optional[str] = Field(max_length=1)
    related_causes_code: Optional[str] = Field(is_component=True)
    special_program_code: Optional[str] = Field(max_length=3)
    yes_no_condition_response_code_1: Optional[str] = Field(max_length=1)
    level_of_service_code: Optional[str] = Field(max_length=3)
    yes_no_condition_response_code_2: Optional[str] = Field(max_length=1)
    provider_agreement_code: Optional[str] = Field(max_length=1)
    claim_status_code: Optional[str] = Field(max_length=2)
    yes_no_condition_response_code_3: Optional[str] = Field(max_length=1)
    claim_submission_reason_code: Optional[str] = Field(max_length=2)
    delay_reason_code: Optional[DelayReasonCode] = Field(max_length=2)


class ClpSegment(X12Segment):
    """
    Claim Payment
    Example:
        CLP*7722337*1*211366.97*138018.40**12*119932404007801~

    """

    class ClaimStatusCode(str, Enum):
        """
        Code values for CLP02
        """

        PROCESSED_AS_PRIMARY = "1"
        PROCESSED_AS_SECONDARY = "2"
        PROCESSED_AS_TERTIARY = "3"
        DENIED = "4"
        PROCESSED_AS_PRIMARY_FORWARDED = "19"
        PROCESSED_AS_SECONDARY_FORWARDED = "20"
        PROCESSED_AS_TERTIARY_FORWARDED = "21"
        REVERSAL_PREVIOUS_PAYMENT = "22"
        NOT_OUR_CLAIM_FORWARDED = "23"
        PREDETERMINATION_PRICING_NO_PAYMENT = "25"

    class ClaimFilingIndicatorCode(str, Enum):
        """
        Code values for CLP06
        """

        PPO = "12"
        POS = "13"
        EPO = "14"
        INDEMNITY_INSURANCE = "15"
        HMO_MEDICARE_RISK = "16"
        DENTAL_MAINTENANCE_ORGANIZATION = "17"
        AUTOMOBILE_MEDICAL = "AM"
        CHAMPUS = "CH"
        DISABILITY = "DS"
        HMO = "HM"
        LIABILITY_MEDICAL = "LM"
        MEDICARE_PART_A = "MA"
        MEDICARE_PART_B = "MB"
        MEDICAID = "MC"
        OTHER_FEDERAL_PROGRAM = "OF"
        TITLE_V = "TV"
        VETERANS_AFFAIRS_PLAN = "VA"
        WORKERS_COMPENSATION_HEALTH_CLAIM = "WC"
        MUTUALLY_DEFINED = "ZZ"

    segment_name: X12SegmentName = X12SegmentName.CLP
    patient_control_number: str = Field(min_length=1, max_length=38)
    claim_status_code: ClaimStatusCode
    total_claim_charge_amount: Decimal
    claim_payment_amount: Decimal
    patient_responsibility_amount: Optional[Decimal]
    claim_filing_indicator_code: ClaimFilingIndicatorCode
    payer_claim_control_number: Optional[str] = Field(max_length=50)
    facility_type_code: Optional[str] = Field(max_length=2)
    claim_frequency_type_code: Optional[str] = Field(max_length=1)
    patient_status_code: Optional[str] = Field(max_length=2)
    drg_code: Optional[str] = Field(max_length=4)
    drg_weight: Optional[condecimal(gt=Decimal("0.0"))]
    discharge_fraction: Optional[condecimal(ge=Decimal("0.0"))]
    condition_response_code: Optional[str] = Field(max_length=1)


class Cl1Segment(X12Segment):
    """
    Institutional Claim Code
    Example:
        CL1*1*7*30~
    """

    segment_name: X12SegmentName = X12SegmentName.CL1
    admission_type_code: str = Field(min_length=1, max_length=1)
    admission_source_code: Optional[str] = Field(max_length=1)
    patient_status_code: str = Field(min_length=1, max_length=2)
    nursing_home_residential_status_code: Optional[str] = Field(max_length=1)


class Cn1Segment(X12Segment):
    """
    Contract information.
    Example:
        CN1*02*550~
    """

    segment_name: X12SegmentName = X12SegmentName.CN1
    contract_type_code: str = Field(min_length=2, max_length=2)
    contract_amount: Optional[Decimal]
    contract_percentage: Optional[Decimal]
    contract_code: Optional[str] = Field(max_length=50)
    terms_discount_percentage: Optional[Decimal]
    contract_version_identifier: Optional[str] = Field(max_length=30)


class CobSegment(X12Segment):
    """
    Coordination of Benefits
    Example:
        COB*P*XYZ123*1~
    """

    class PayerResponsibilitySequenceCode(str, Enum):
        """
        Code values for COB01
        """

        PRIMARY = "P"
        SECONDARY = "S"
        TERTIARY = "T"
        UNKNOWN = "U"

    class CoordinationOfBenefitsCode(str, Enum):
        """
        Code values for COB03
        """

        COORDINATION_OF_BENEFITS = "1"
        UNKNOWN = "5"
        NO_COORDINATION_OF_BENEFITS = "6"

    class ServiceTypeCode(str, Enum):
        """
        Code values for COB04
        """

        MEDICAL_CARE = "1"
        DENTAL_CARE = "35"
        HOSPITAL_INPATIENT = "48"
        HOSPITAL_OUTPATIENT = "50"
        LONG_TERM_CARE = "54"
        FREE_STANDING_PRESCRIPTION_DRUG = "89"
        MAIL_ORDER_PRESCRIPTION_DRUG = "90"
        PSYCHIATRIC = "A4"
        SKILLED_NURSING_CARE = "AG"
        VISION = "AL"
        PARTIAL_HOSPITALIZATION_PSYCHIATRIC = "BB"

    segment_name: X12SegmentName = X12SegmentName.COB
    payer_responsibility_sequence_code: PayerResponsibilitySequenceCode
    group_policy_number: Optional[str] = Field(min_length=1, max_length=50)
    coordination_of_benefits_code: CoordinationOfBenefitsCode
    service_type_code: Optional[ServiceTypeCode]


class CrcSegment(X12Segment):
    """
    Conditions Indicator
    Example:
        CRC*E1*Y*L1~
    """

    segment_name: X12SegmentName = X12SegmentName.CRC
    code_category: str = Field(min_length=2, max_length=2)
    certification_condition_indicator: str = Field(min_length=1, max_length=1)
    condition_code_1: str = Field(min_length=2, max_length=3)
    condition_code_2: Optional[str] = Field(max_length=3)
    condition_code_3: Optional[str] = Field(max_length=3)
    condition_code_4: Optional[str] = Field(max_length=3)
    condition_code_5: Optional[str] = Field(max_length=3)


class Cr1Segment(X12Segment):
    """
    Ambulance Transport Information
    Example:
        CR1*LB*140**A*DH*12****UNCONSCIOUS~
    """

    class AmbulanceTransportReasonCode(str, Enum):
        """
        Code values for CR104
        """

        PATIENT_TRANSPORTED_CARE_OF_SYMPTOMS = "A"
        PATIENT_TRANSPORTED_FOR_PHYSICIAN = "B"
        PATIENT_TRANSPORTED_FOR_FAMILY = "C"
        PATIENT_TRANSPORTED_FOR_SPECIALIST = "D"
        PATIENT_TRANSPORTED_FOR_REHABILITATION = "E"

    segment_name: X12SegmentName = X12SegmentName.CR1
    weight_measurement_code: Optional[Literal["LB"]]
    patient_weight: Optional[Decimal]
    ambulance_transport_code: Optional[str] = Field(max_length=1)
    ambulance_transport_reason_code: AmbulanceTransportReasonCode
    mileage_measurement_code: Literal["DH"]
    transport_distance: Decimal
    address_information_1: Optional[str] = Field(max_length=55)
    address_information_2: Optional[str] = Field(max_length=55)
    round_trip_purpose_description: Optional[str] = Field(max_length=80)
    stretcher_purpose_description: Optional[str] = Field(max_length=80)


class Cr2Segment(X12Segment):
    """
    Chiropractic Certification
    Example:
        CR2********M~
    """

    class PatientConditionCode(str, Enum):
        """
        Code values for CR208
        """

        ACUTE_CONDITION = "A"
        CHRONIC_CONDITION = "C"
        NON_ACUTE = "D"
        NON_LIFE_THREATENING = "E"
        ROUTINE = "F"
        SYMPTOMATIC = "G"
        ACUTE_MANIFESTATION_OF_CHRONIC_CONDITION = "M"

    segment_name: X12SegmentName = X12SegmentName.CR2
    count: Optional[str] = Field(max_length=9)
    quantity: Optional[Decimal]
    subluxation_level_code_1: Optional[str] = Field(max_length=3)
    subluxation_level_code_2: Optional[str] = Field(max_length=3)
    unit_basis_measurement_code: Optional[str] = Field(max_length=2)
    quantity_1: Optional[Decimal]
    quantity_2: Optional[Decimal]
    patient_condition_code: PatientConditionCode
    patient_condition_description_1: Optional[str] = Field(max_length=80)
    patient_condition_description_2: Optional[str] = Field(max_length=80)
    yes_no_condition_response_code: Optional[str]


class Cr3Segment(X12Segment):
    """
    Durable Medical Equipment Certification
    Example:
        CR3*I*MO*6.00~
    """

    class CertificationTypeCode(str, Enum):
        """
        Code values for CR301
        """

        INITIAL = "I"
        RENEWAL = "R"
        REVISED = "S"

    segment_name: X12SegmentName = X12SegmentName.CR3
    certification_type_code: CertificationTypeCode
    unit_basis_measurement_code: Literal["MO"]
    durable_medical_equipment_duration: condecimal(gt=Decimal("0.0"))
    insulin_dependent_code: Optional[str] = Field(max_length=1)
    description: Optional[str] = Field(max_length=80)


class CtpSegment(X12Segment):
    """
    Pricing Information
    Example:
        CTP****2.00*UN~
    """

    segment_name: X12SegmentName = X12SegmentName.CTP
    class_of_trade_code: Optional[str] = Field(max_length=2)
    price_identifier_code: Optional[str] = Field(max_length=3)
    unit_price: Optional[Decimal]
    quantity: Decimal
    composite_unit_of_measure: str = Field(is_component=True)


class CurSegment(X12Segment):
    """
    Foreign Currency Information
    Example:
        CUR*85*USD~
    """

    segment_name: X12SegmentName = X12SegmentName.CUR
    entity_identifier_code: str = Field(min_length=2, max_length=3)
    currency_code: str = Field(min_length=3, max_length=3)


class DmgSegment(X12Segment):
    """
    Demographic Information (birthdate, gender).
    Example:
        DMG*D8*19430917*M~
    """

    class GenderCode(str, Enum):
        """
        Code value for DMG03
        """

        FEMALE = "F"
        MALE = "M"

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code value for DMG01
        """

        SPECIFIC_DATE = "D8"

    segment_name: X12SegmentName = X12SegmentName.DMG
    date_time_period_format_qualifier: Optional[DateTimePeriodFormatQualifier]
    date_time_period: Optional[Union[str, datetime.date]]
    gender_code: Optional[GenderCode]
    marital_status_code: Optional[str] = Field(max_length=1)
    race_or_ethnicity: Optional[str]
    citizenship_stats_code: Optional[str] = Field(max_length=2)
    country_code: Optional[str] = Field(max_length=3)
    basis_of_verification_code: Optional[str] = Field(max_length=2)
    quantity: Optional[Decimal]
    code_list_qualifier_code: Optional[Literal["REC"]]
    race_or_ethnicity_code: Optional[str] = Field(max_length=30)

    _validate_x12_date = field_validator("date_time_period")(validate_date_field)

    @root_validator
    def validate_date_time_fields(cls, values):
        """
        Validates that both a date_time_period_format_qualifier and date_time_period are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        date_fields: Tuple = values.get(
            "date_time_period_format_qualifier"
        ), values.get("date_time_period")

        if any(date_fields) and not all(date_fields):
            raise ValueError(
                "DMG Segment requires both a date_time_period_format_qualifier and date time period if one or the other is present"
            )

        return values


class DsbSegment(X12Segment):
    """
    Disability Information
    Example:
        DSB*2******DX*585~
    """

    class DisabilityTypeCode(str, Enum):
        """
        Code values for DSB01
        """

        SHORT_TERM_DISABILITY = "1"
        LONG_TERM_DISABILITY = "2"
        PERMANENT_TOTAL_DISABILITY = "3"
        NO_DISABILITY = "4"

    class ProductServiceIdQualifier(str, Enum):
        """
        Code values for DSB07
        """

        ICD_9_DIAGNOSIS = "DX"
        MUTUALLY_DEFINED = "ZZ"

    segment_name: X12SegmentName = X12SegmentName.DSB
    disability_type_code: DisabilityTypeCode
    quantity: Optional[Decimal]
    occupation_code: Optional[str] = Field(min_length=4, max_length=6)
    work_intensity_code: Optional[str] = Field(min_length=1, max_length=1)
    product_option_code: Optional[str] = Field(min_length=1, max_length=2)
    monetary_amount: Optional[Decimal]
    product_service_id_qualifier: Optional[ProductServiceIdQualifier]
    diagnosis_code: Optional[str] = Field(min_length=1, max_length=15)


class DtmSegment(X12Segment):
    """
    Production Date
    Example:
        DTM*405*20020317~
    """

    segment_name: X12SegmentName = X12SegmentName.DTM
    date_time_qualifier: str = Field(min_length=3, max_length=3)
    production_date: Union[str, datetime.date]

    _validate_x12_date = field_validator("production_date")(validate_date_field)


class DtpSegment(X12Segment):
    """
    Date or Time Period
    Example:
        DTP*291*D8*20051015~
    """

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code values for DTP02
        """

        SPECIFIC_DATE = "D8"
        DATE_RANGE = "RD8"

    segment_name: X12SegmentName = X12SegmentName.DTP
    date_time_qualifier: str = Field(min_length=3, max_length=3)
    date_time_period_format_qualifier: DateTimePeriodFormatQualifier
    date_time_period: Union[str, datetime.date]

    _validate_x12_date = field_validator("date_time_period")(validate_date_field)


class EbSegment(X12Segment):
    """
    Eligibility Benefit Information
    Example:
        EB*B**1^33^35^47^86^88^98^AL^MH^UC*HM*GOLD 123 PLAN*27*10*****Y~
    """

    class EligibilityBenefitInformationCode(str, Enum):
        """
        Code values for EB01
        """

        ACTIVE_COVERAGE = "1"
        ACTIVE_FULL_RISK_CAPITATION = "2"
        ACTIVE_SERVICES_CAPITATED = "3"
        ACTIVE_SERVICES_CAPITATED_TO_PRIMARY_CARE = "4"
        ACTIVE_PENDING_INVESTIGATION = "5"
        INACTIVE = "6"
        INACTIVE_PENDING_ELIGIBILITY_UPDATE = "7"
        INACTIVE_PENDING_INVESTIGATION = "8"
        CO_INSURANCE = "A"
        CO_PAYMENT = "B"
        DEDUCTIBLE = "C"
        COVERAGE_BASIS = "CB"
        BENEFIT_DESCRIPTION = "D"
        EXCLUSIONS = "E"
        LIMITATIONS = "F"
        OUT_OF_POCKET_STOP_LOSS = "G"
        UNLIMITED = "H"
        NON_COVERED = "I"
        COST_CONTAINMENT = "J"
        REVERSE = "K"
        PRIMARY_CARE_PROVIDER = "L"
        PRE_EXISTING_CONDITION = "M"
        MANAGED_CARE_COORDINATOR = "MC"
        SERVICES_RESTRICTED_TO_FOLLOWING_PROVIDER = "N"
        NOT_DEEMED_A_MEDICAL_NECESSITY = "O"
        BENEFIT_DISCLAIMER = "P"
        SECOND_SURGICAL_OPINION_REQUIRED = "Q"
        OTHER_OR_ADDITIONAL_PAYOR = "R"
        PRIOR_YEAR_HISTORY = "S"
        CARD_REPORTED_LOST_STOLEN = "T"
        CONTACT_FOLLOWING_FOR_BENEFIT_INFO = "U"
        CANNOT_PROCESS = "V"
        OTHER_SOURCE_OF_DATA = "W"
        HEALTH_CARE_FACILITY = "X"
        SPEND_DOWN = "Y"

    class CoverageLevelCode(str, Enum):
        """
        Code values for EB02
        """

        CHILDREN_ONLY = "CHD"
        DEPENDENTS_ONLY = "DEP"
        EMPLOYEE_AND_CHILDREN = "ECH"
        EMPLOYEE_ONLY = "EMP"
        EMPLOYEE_AND_SPOUSE = "ESP"
        FAMILY = "FAM"
        INDIVIDUAL = "IND"
        SPOUSE_AND_CHILDREN = "SPC"
        SPOUSE_ONLY = "SPO"

    class ServiceTypeCode(str, Enum):
        """
        Code values for EB03
        """

        MEDICAL_CARE = "1"
        SURGICAL = "2"
        CONSULTATION = "3"
        DIAGNOSTIC_X_RAY = "4"
        DIAGNOSTIC_LAB = "5"
        RADIATION_THERAPY = "6"
        ANESTHESIA = "7"
        SURGICAL_ASSISTANCE = "8"
        OTHER_MEDICAL = "9"
        BLOOD_CHARGES = "10"
        USED_DURABLE_MEDICAL_EQUIPMENT = "11"
        DURABLE_MEDICAL_EQUIPMENT_PURCHASE = "12"
        AMBULATORY_SERVICE_CENTER_FACILITY = "13"
        RENAL_SUPPLIES_IN_THE_HOME = "14"
        ALTERNATE_METHOD_DIALYSIS = "15"
        CHRONIC_RENAL_DISEASE_EQUIPMENT = "16"
        PRE_ADMISSION_TESTING = "17"
        DURABLE_MEDICAL_EQUIPMENT_RENTAL = "18"
        PNEUMONIA_VACCINE = "19"
        SECOND_SURGICAL_OPINION = "20"
        THIRD_SURGICAL_OPINION = "21"
        SOCIAL_WORK = "22"
        DIAGNOSTIC_DENTAL = "23"
        PERIODONTICS = "24"
        RESTORATIVE = "25"
        ENDODONTICS = "26"
        MAXILLOFACIAL_PROSTHETICS = "27"
        ADJUNCTIVE_DENTAL_SERVICES = "28"
        HEALTH_BENEFIT_PLAN_COVERAGE = "30"
        PLAN_WAITING_PERIOD = "32"
        CHIROPRACTIC = "33"
        CHIROPRACTIC_OFFICE_VISITS = "34"
        DENTAL_CARE = "35"
        DENTAL_CROWNS = "36"
        DENTAL_ACCIDENT = "37"
        ORTHODONTICS = "38"
        PROSTHODONTICS = "39"
        ORAL_SURGERY = "40"
        ROUTINE_PREVENTIVE_DENTAL = "41"
        HOME_HEALTH_CARE = "42"
        HOME_HEALTH_PRESCRIPTIONS = "43"
        HOME_HEALTH_VISITS = "44"
        HOSPICE = "45"
        RESPITE_CARE = "46"
        HOSPITAL = "47"
        HOSPITAL_INPATIENT = "48"
        HOSPITAL_ROOM_AND_BOARD = "49"
        HOSPITAL_OUTPATIENT = "50"
        HOSPITAL_EMERGENCY_ACCIDENT = "51"
        HOSPITAL_EMERGENCY_MEDICAL = "52"
        HOSPITAL_AMBULATORY_SURGICAL = "53"
        LONG_TERM_CARE = "54"
        MAJOR_MEDICAL = "55"
        MEDICALLY_RELATED_TRANSPORTATION = "56"
        AIR_TRANSPORTATION = "57"
        CABULANCE = "58"
        LICENSED_AMBULANCE = "59"
        GENERAL_BENEFITS = "60"
        INVITRO_FERTILIZATION = "61"
        MRI_CAT_SCAN = "62"
        DONOR_PROCEDURE = "63"
        ACUPUNCTURE = "64"
        NEWBORN_CARE = "65"
        PATHOLOGY = "66"
        SMOKING_CESSATION = "67"
        WELL_BABY_CARE = "68"
        MATERNITY = "69"
        TRANSPLANTS = "70"
        AUDIOLOGY_EXAM = "71"
        INHALATION_THERAPY = "72"
        DIAGNOSTIC_MEDICAL = "73"
        PRIVATE_DUTY_NURSING = "74"
        PROSTHETIC_DEVICE = "75"
        DIALYSIS = "76"
        OTOLOGICAL_EXAM = "77"
        CHEMOTHERAPY = "78"
        ALLERGY_TESTING = "79"
        IMMUNIZATIONS = "80"
        ROUTINE_PHYSICAL = "81"
        FAMILY_PLANNING = "82"
        INFERTILITY = "83"
        ABORTION = "84"
        AIDS = "85"
        EMERGENCY_SERVICES = "86"
        CANCER = "87"
        PHARMACY = "88"
        FREE_STANDING_PRESCRIPTION_DRUG = "89"
        MAIL_ORDER_PRESCRIPTION_DRUG = "90"
        BRAND_NAME_PRESCRIPTION_DRUG = "91"
        GENERIC_PRESCRIPTION_DRUG = "92"
        PDDIATRY = "93"
        PDDIATRY_NURSING_HOME_VISITS = "94"
        PROFESSIONAL_PHYSICIAN = "96"
        ANESTHESIOLOGIST = "97"
        PROFESSIONAL_PHYSICIAN_VISIT_OFFICE = "98"
        PROFESSIONAL_PHYSICIAN_VISIT_INPATIENT = "99"
        PROFESSIONAL_PHYSICIAN_VISIT_OUTPATIENT = "99"
        PROFESSIONAL_PHYSICIAN_VISIT_NURSING_HOME = "A1"
        PROFESSIONAL_PHYSICIAN_VISIT_SKILLED_NURSING_FACILITY = "A2"
        PROFESSIONAL_PHYSICIAN_VISIT_HOME_PSYCHIATRIC = "A3"
        PSYCHIATRIC_ROOM_AND_BOARD = "A4"
        PSYCHOTHERAPY = "A5"
        PSYCHIATRIC_INPATIENT = "A6"
        PSYCHIATRIC_OUTPATIENT = "A7"
        REHABILITATION = "A9"
        REHABILITATION_ROOM_AND_BOARD = "AA"
        REHABILITATION_INPATIENT = "AB"
        REHABILITATION_OUTPATIENT = "AC"
        OCCUPATIONAL_THERAPY = "AD"
        PHYSICAL_MEDICINE = "AE"
        SPEECH_THERAPY = "AF"
        SKILLED_NURSING_CARE = "AG"
        SKILLED_NURSING_CARE_ROOM_AND_BOARD = "AH"
        SUBSTANCE_ABUSE = "AI"
        ALCOHOLISM = "AJ"
        DRUG_ADDICTION = "AK"
        VISION_OPTOMETRY = "AL"
        FRAMES = "AM"
        ROUTINE_VISION_EXAM = "AN"
        LENSES = "AO"
        NONMEDICALLY_NECESSARY_PHYSICAL = "AQ"
        EXPERIMENTAL_DRUG_THERAPY = "AR"
        BURN_CARE = "B1"
        BRAND_NAME_PRESCRIPTION_DRUG_FORMULARY = "B2"
        BRAND_NAME_PRESCRIPTION_DRUG_NON_FORMULARY = "B3"
        INDEPENDENT_MEDICAL_EVALUATION = "BA"
        PARTIAL_HOSPITALIZATION_PSYCHIATRIC = "BB"
        DAY_CARE_PSYCHIATRIC = "BC"
        COGNITIVE_THERAPY = "BD"
        MASSAGE_THERAPY = "BE"
        PULMONARY_REHABILITATION = "BF"
        CARDIAC_REHABILITATION = "BG"
        PEDIATRIC = "BH"
        NURSERY = "BI"
        SKIN = "BJ"
        ORTHOPEDIC = "BK"
        CARDIAC = "BL"
        LYMPHATIC = "BM"
        GASTROINTESTINAL = "BN"
        ENDOCRINE = "BP"
        NEUROLOGY = "BQ"
        EYE = "BR"
        INVASIVE_PROCEDURE = "BS"
        GYNECOLOGICAL = "BT"
        OBSTETRICAL = "BU"
        OBSTETRICAL_GYNECOLOGICAL = "BV"
        MAIL_ORDER_PRESCRIPTION_DRUG_BRAND_NAME = "BW"
        MAIL_ORDER_PRESCRIPTION_DRUG_GENERIC = "BX"
        PHYSICIAN_VISIT_OFFICE_SICK = "BY"
        PHYSICIAN_VISIT_OFFICE_WELL = "BZ"
        CORONARY_CARE = "C1"
        PRIVATE_DUTY_NURSING_INPATIENT = "CA"
        PRIVATE_DUTY_NURSING_HOME = "CB"
        SURGICAL_BENEFITS_PROFESSIONAL_PHYSICIAN = "CC"
        SURGICAL_BENEFITS_FACILITY = "CD"
        MENTAL_HEALTH_PROVIDER_INPATIENT = "CE"
        MENTAL_HEALTH_PROVIDER_OUTPATIENT = "CF"
        MENTAL_HEALTH_FACILITY_INPATIENT = "CG"
        MENTAL_HEALTH_FACILITY_OUTPATIENT = "CH"
        SUBSTANCE_ABUSE_FACILITY_INPATIENT = "C1"
        SUBSTANCE_ABUSE_FACILITY_OUTPATIENT = "C2"
        SCREENING_X_RAY = "CK"
        SCREENING_LABORATORY = "CL"
        MAMMOGRAM_HIGH_RISK_PATIENT = "CM"
        MAMMOGRAM_LOW_RISK_PATIENT = "CN"
        FLU_VACCINATION = "CO"
        EYEWEAR_AND_EYEWEAR_ACCESSORIES = "CP"
        CASE_MANAGEMENT = "CQ"
        DERMATOLOGY = "DG"
        DURABLE_MEDICAL_EQUIPMENT = "DM"
        DIABETIC_SUPPLIES = "DS"
        GENERIC_PRESCRIPTION_DRUG_FORMULARY = "GF"
        GENERIC_PRESCRIPTION_DRUG_NON_FORMULARY = "GN"
        ALLERGY = "GY"
        INTENSIVE_CARE = "IC"
        MENTAL_HEALTH = "MH"
        NEONATAL_INTENSIVE_CARE = "NI"
        ONCOLOGY = "ON"
        PHYSICAL_THERAPY = "PT"
        PULMONARY = "PU"
        RENAL = "RN"
        RESIDENTIAL_PSYCHIATRIC_TREATMENT = "RT"
        TRANSITIONAL_CARE = "TC"
        TRANSITION_NURSERY_CARE = "TN"
        URGENT_CARE = "UC"

    class InsuranceTypeCode(str, Enum):
        """
        code values for EB04
        """

        MEDICARE_SECONDARY_EMPLOYER_GROUP_PRIMARY = "12"
        MEDICARE_SECONDARY_END_STAGE_RENAL_DISEASE = "13"
        MEDICARE_SECONDARY_AUTO_PRIMARY = "14"
        MEDICARE_SECONDARY_WORKERS_COMP = "15"
        MEDICARE_SECONDARY_PUBLIC_HEALTH_SERVICE = "16"
        MEDICARE_SECONDARY_BLACK_LUNG = "41"
        MEDICARE_SECONDARY_VETERANS_ADMIN = "42"
        MEDICARE_SECONDARY_DISABLED_BENEFICIARY = "43"
        MEDICARE_SECONDARY_OTHER_LIABILITY = "47"
        AUTO_INSURANCE_POLICY = "AP"
        COMMERCIAL = "C1"
        COBRA = "CO"
        MEDICARE_CONDITIONALLY_PRIMARY = "CP"
        DISABILITY = "D"
        DISABILITY_BENEFITS = "DB"
        EXCLUSIVE_PROVIDER_ORGANIZATION = "EP"
        FAMILY_OR_FRIENDS = "FF"
        GROUP_POLICY = "GP"
        HMO = "HM"
        HMO_MEDICARE_RISK = "HN"
        SPECIAL_LOW_INCOME_MEDICARE_BENEFICIARY = "HS"
        INDEMNITY = "IN"
        INDIVIDUAL_POLICY = "IP"
        LONG_TERM_CARE = "LC"
        LONG_TERM_POLICY = "LD"
        LIFE_INSURANCE = "LI"
        LITIGATION = "LT"
        MEDICARE_PART_A = "MA"
        MEDICARE_PART_B = "MB"
        MEDICAID = "MC"
        MEDIGAP_PART_A = "MH"
        MEDIGAP_PART_B = "MI"
        MEDICARE_PRIMARY = "MP"
        OTHER = "OT"
        PROPERTY_INSURANCE_PERSONAL = "PE"
        PERSONAL = "PL"
        PERSONAL_PAYMENT_CASH = "PP"
        PREERRED_PROVIDER_ORGANIZATION = "PR"
        POINT_OF_SERVICE = "POS"
        QUALIFIED_MEDICARE_BENEFICIARY = "QM"
        PROPERTY_INSURANCE_REAL = "RP"
        SUPPLEMENTAL_POLICY = "SP"
        TEFRA = "TF"
        WORKERS_COMPENSATION = "WC"
        WRAP_UP_POLICY = "WU"

    class TimePeriodQualifier(str, Enum):
        """
        Code values for EB06
        """

        HOUR = "6"
        DAY = "7"
        TWENTY_FOUR_HOURS = "13"
        YEARS = "21"
        SERVICE_YEAR = "22"
        CALENDAR_YEAR = "23"
        YEAR_TO_DATE = "24"
        CONTRACT = "25"
        EPISODE = "26"
        VISIT = "27"
        OUTLIER = "28"
        REMAINING = "29"
        EXCEEDED = "30"
        NOT_EXCEEDED = "31"
        LIFETIME = "32"
        LIFETIME_REMAINING = "33"
        MONTH = "34"
        WEEK = "35"
        ADMISSION = "36"

    class QuantityQualifier(str, Enum):
        """
        Code valus for EB09
        """

        MINIMUM = "8H"
        QUANTITY_USED = "99"
        COVERED_ACTUAL = "CA"
        COVERED_ESTIMATED = "CE"
        NUMBER_OF_COINSURANCE_DAYS = "D3"
        DEDUCTIBLE_BLOOD_UNITS = "D8"
        DAYS = "DY"
        HOURS = "HS"
        LIFETIME_RESERVE_ACTUAL = "LA"
        LIFETIME_RESERVE_ESTIMATED = "LE"
        MAXIMUM = "M2"
        MONTH = "MN"
        NUMBER_OF_SERVICES_OR_PROCEDURES = "P6"
        QUANTITY_APPROVED = "QA"
        AGE_HIGH_VALUE = "S7"
        AGE_LOW_VALUE = "S8"
        VISITS = "VS"
        YEARS = "YY"

    class AuthorizationCertificationIndicator(str, Enum):
        """
        Code values for EB11
        """

        NO = "N"
        UNKNOWN = "U"
        YES = "Y"

    class InPlanNetworkIndicator(str, Enum):
        """
        Code values for EB12
        """

        NO = "N"
        UNKNOWN = "U"
        NOT_APPLICABLE = "W"
        YES = "Y"

    segment_name: X12SegmentName = X12SegmentName.EB
    eligibility_benefit_information: EligibilityBenefitInformationCode
    coverage_level_code: Optional[CoverageLevelCode]
    service_type_code: Optional[List[ServiceTypeCode]]
    insurance_type_code: Optional[InsuranceTypeCode]
    plan_coverage_description: Optional[str]
    time_period_qualifier: Optional[TimePeriodQualifier]
    benefit_amount: Optional[Decimal]
    benefit_percent: Optional[Decimal]
    quantity_qualifier: Optional[Decimal]
    quantity: Optional[Decimal]
    authorization_certification_indicator: Optional[AuthorizationCertificationIndicator]
    inplan_network_indicator: Optional[InPlanNetworkIndicator]
    procedure_identifier: Optional[List[str]] = Field(is_component=True)
    diagnosis_code_pointer: Optional[List[str]] = Field(is_component=True)

    @root_validator
    def validate_quantity(cls, values):
        """
        Validates that both a quantity_qualifier and quantity are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        quantity_fields: Tuple = values.get("quantity_qualifier"), values.get(
            "quantity"
        )

        if any(quantity_fields) and not all(quantity_fields):
            raise ValueError("Quantity requires the quantity identifier and value.")

        return values


class EcSegment(X12Segment):
    """
    Employment Class
    Example:
        EC*04*06*07~
    """

    class EmploymentClassCode(str, Enum):
        """
        Code values for EC01, EC02, and EC03
        """

        UNION = "01"
        NON_UNION = "02"
        EXECUTIVE = "03"
        NON_EXECUTIVE = "04"
        MANAGEMENT = "05"
        NON_MANAGEMENT = "06"
        HOURLY = "07"
        SALARIED = "08"
        ADMINISTRATIVE = "09"
        NON_ADMINISTRATIVE = "10"
        EXEMPT = "11"
        NON_EXEMPT = "12"
        HIGHLY_COMPENSATED = "17"
        KEY_EMPLOYEE = "18"
        BARGAINING = "19"
        NON_BARGAINING = "20"
        OWNER = "21"
        PRESIDENT = "22"
        VICE_PRESIDENT = "23"

    segment_name: X12SegmentName = X12SegmentName.EC
    employment_class_code_1: EmploymentClassCode
    employment_class_code_2: Optional[EmploymentClassCode]
    employment_class_code_3: Optional[EmploymentClassCode]


class EqSegment(X12Segment):
    """
    Eligibility Inquiry Segment
    Example:
        EQ*98^34^44^81^A0^A3**FAM~
    """

    segment_name: X12SegmentName = X12SegmentName.EQ
    service_type_code: Optional[List[str]]
    medical_procedure_id: Optional[List[str]] = Field(is_component=True)
    coverage_level_code: Optional[str] = Field(max_length=3)
    insurance_type_code: Optional[str] = Field(max_length=3)
    diagnosis_code_pointer: Optional[List[str]] = Field(is_component=True)

    @root_validator
    def validate_type_and_procedure_code(cls, values):
        """
        Validates that the EQ segment contains a service type code or a medical procedure id

        :param values: The raw, unvalidated transaction data.
        """
        reference_fields: Tuple = values.get("service_type_code"), values.get(
            "medical_procedure_id"
        )

        if not any(reference_fields):
            raise ValueError(
                "Service Type Code or Medical Procedure is required for EQ segment"
            )

        return values


class FrmSegment(X12Segment):
    """
    Supporting documentation segment
    Example:
        FRM*12*N~
    """

    class QuestionResponse(str, Enum):
        """
        Code values for FRM02
        """

        NO = "N"
        NOT_APPLICABLE = "W"
        YES = "Y"

    segment_name: X12SegmentName = X12SegmentName.FRM
    question_number_letter: str = Field(min_length=1, max_length=20)
    question_response_1: Optional[QuestionResponse]
    question_response_2: Optional[str] = Field(max_length=50)
    question_response_3: Optional[Union[str, datetime.date]]
    question_response_4: Optional[Decimal]

    _validate_question_response_3 = field_validator("question_response_3")(
        parse_x12_date
    )


class GeSegment(X12Segment):
    """
    Defines a functional header for the message and is an EDI control segment.
    Example:
        GE*1*1~
    """

    segment_name: X12SegmentName = X12SegmentName.GE
    number_of_transaction_sets_included: PositiveInt
    group_control_number: str = Field(min_length=1, max_length=9)


class GsSegment(X12Segment):
    """
    Defines a functional header for the message and is an EDI control segment.
    Example:
        GS*HS*000000005*54321*20131031*1147*1*X*005010X279A~
    """

    segment_name: X12SegmentName = X12SegmentName.GS
    functional_identifier_code: str = Field(min_length=2, max_length=2)
    application_sender_code: str = Field(min_length=2, max_length=15)
    application_receiver_code: str = Field(min_length=2, max_length=15)
    functional_group_creation_date: Union[str, datetime.date]
    functional_group_creation_time: str
    group_control_number: str = Field(min_length=1, max_length=9)
    responsible_agency_code: Literal["X"]
    version_identifier_code: str = Field(min_length=1, max_length=12)

    _validate_creation_date = field_validator("functional_group_creation_date")(
        parse_x12_date
    )


class HcpSegment(X12Segment):
    """
    Health Care Pricing
    Example:
        HCP*03*100*10*RPO12345~
    """

    class PricingMethodology(str, Enum):
        """
        Code values for HCP01
        """

        ZERO_PRICING_NOT_COVERED = "00"
        PRICED_AS_BILLED_100_PERCENT = "01"
        PRICED_AT_STANDARD_FEE_SCHEDULE = "02"
        PRICED_AT_CONTRACTUAL_PERCENTAGE = "03"
        BUNDLED_PRICING = "04"
        PEER_REVIEW_PRICING = "05"
        FLAT_RATE_PRICING = "07"
        COMBINATION_PRICING = "08"
        MATERNITY_PRICING = "09"
        OTHER_PRICING = "10"
        LOWER_OF_COST = "11"
        RATIO_OF_COST = "12"
        COST_REIMBURSED = "13"
        ADJUSTMENT_PRICING = "14"

    class RejectReasonCode(str, Enum):
        """
        Code values for HCP13
        """

        CANNOT_IDENTIFY_PROVIDER_AS_TPO = "T1"
        CANNOT_IDENTIFY_PAYER_AS_TPO = "T2"
        CANNOT_IDENTIFY_INSURED_AS_TPO = "T3"
        PAYER_NAME_OR_IDENTIFIER_MISSING = "T4"
        CERTIFICATION_INFORMATION_MISSING = "T5"
        CLAIM_DOES_NOT_CONTAIN_INFO_FOR_REPRICING = "T6"

    class PolicyComplianceCode(str, Enum):
        """
        Code values for HCP14
        """

        PROCEDURE_FOLLOWED = "1"
        NOT_FOLLOWED_CALL_NOT_MADE = "2"
        NOT_MEDICALLY_NECESSARY = "3"
        NOT_FOLLOWED_OTHER = "4"
        EMERGENCY_ADMIT_NON_NETWORK_HOSPITAL = "5"

    class ExceptionCode(str, Enum):
        """
        Code values for HCP15
        """

        NON_NETWORK_PROFESSIONAL_PROVIDER_IN_NETWORK_HOSPITAL = "1"
        EMERGENCY_CARE = "2"
        SERVICES_SPECIALIST_NOT_IN_NETWORK = "3"
        OUT_OF_SERVICE_AREA = "4"
        STATE_MANDATES = "5"
        OTHER = "6"

    segment_name: X12SegmentName = X12SegmentName.HCP
    pricing_methodology: PricingMethodology
    repriced_allowed_amount: Decimal
    repriced_saving_amount: Optional[Decimal]
    repricing_organization_identifier: Optional[str] = Field(max_length=50)
    per_diem_flat_rate_amount: Optional[Decimal]
    repriced_apg_code: Optional[str] = Field(max_length=50)
    repriced_apg_amount: Optional[Decimal]
    product_service_id_1: Optional[str] = Field(max_length=48)
    product_service_id_1_qualifier: Optional[str] = Field(max_length=2)
    product_service_id_2: Optional[str] = Field(max_length=48)
    unit_basis_measurement_code: Optional[str] = Field(max_length=2)
    quantity: Optional[Decimal]
    reject_reason_code: Optional[RejectReasonCode]
    policy_compliance_code: Optional[PolicyComplianceCode]
    exception_code: Optional[ExceptionCode]


class HdSegment(X12Segment):
    """
    Health coverage
    Example:
        HD*021**HLT*PLAN A BCD*FAM~
    """

    class MaintenanceTypeCode(str, Enum):
        """
        Code values for HD01
        """

        CHANGE = "001"
        DELETE = "002"
        ADDITION = "021"
        CANCELLATION_OR_TERMINATION = "024"
        REINSTATEMENT = "025"
        CORRECTION = "026"
        AUDIT_OR_COMPARE = "030"
        EMPLOYEE_INFORMATION_NOT_APPLICABLE = "032"

    class InsuranceLineCode(str, Enum):
        """
        Code values for HD03
        """

        PREVENTATIVE_CARE_WELLNESS = "AG"
        TWENTY_FOUR_HOUR_CARE_RISK = "AH"
        MEDICARE_RISK = "AJ"
        MENTAL_HEALTH = "AK"
        DENTAL_CAPITATION = "DCP"
        DENTAL = "DEN"
        EXCLUSIVE_PROVIDER_ORGANIZATION = "EPO"
        FACILITY = "FAC"
        HEARING = "HE"
        HEALTH = "HLT"
        HEALTH_MAINTEANCE_ORGANIZATION = "HMO"
        LONG_TERM_CARE = "LTC"
        LONG_TERM_DISABILITY = "LTD"
        MAJOR_MEDICAL = "MM"
        MAIL_ORDER_DRUG = "MOD"
        PRESCRIPTION_DRUG = "PDG"
        POINT_OF_SERVICE = "POS"
        PREFERRED_PROVIDER_ORGANIZATION = "PPO"
        PRACTITIONERS = "PRA"
        SHORT_TERM_DISABILITY = "STD"
        UTILIZATION_REVIEW = "UR"
        VISION = "VIS"

    class CoverageLineCode(str, Enum):
        """
        Code values for HD05
        """

        CHILDREN_ONLY = "CHD"
        DEPENDENTS_ONLY = "DEP"
        EMPLOYEE_ONE_DEPENDENT = "E1D"
        EMPLOYEE_TWO_DEPENDENT = "E2D"
        EMPLOYEE_THREE_DEPENDENT = "E3D"
        EMPLOYEE_ONE_OR_MORE_DEPENDENTS = "E5D"
        EMPLOYEE_TWO_OR_MORE_DEPENDENTS = "E6D"
        EMPLOYEE_THREE_OR_MORE_DEPENDENTS = "E7D"
        EMPLOYEE_FOUR_OR_MORE_DEPENDENTS = "E8D"
        EMPLOYEE_FIVE_OR_MORE_DEPENDENTS = "E9D"
        EMPLOYEE_AND_CHILDREN = "ECH"
        EMPLOYEE_ONLY = "EMP"
        EMPLOYEE_AND_SPOUSE = "ESP"
        FAMILY = "FAM"
        INDIVIDUAL = "IND"
        SPOUSE_AND_CHILDREN = "SPC"
        SPOUSE_ONLY = "SPO"
        TWO_PARTY = "TWO"

    class LateEnrollmentIndicator(str, Enum):
        """
        Code values for HD09
        """

        NO = "N"
        YES = "Y"

    segment_name: X12SegmentName = X12SegmentName.HD
    maintenance_type_code: MaintenanceTypeCode
    maintenance_reason_code: Optional[str] = Field(min_length=2, max_length=3)
    insurance_line_code: InsuranceLineCode
    plan_coverage_description: Optional[str] = Field(min_length=1, max_length=50)
    coverage_line_code: Optional[CoverageLineCode]
    count_1: Optional[int]
    count_2: Optional[int]
    underwriting_decision_code: Optional[str] = Field(min_length=1, max_length=1)
    late_enrollment_indicator: Optional[LateEnrollmentIndicator]
    drug_house_code: Optional[str] = Field(min_length=2, max_length=3)
    yes_no_condition_response_code: Optional[str] = Field(min_length=1, max_length=1)


class HiSegment(X12Segment):
    """
    Health Care Information/Diagnostic Codes
    Example:
         HI*BK:8901*BF:87200*BF:5559~
    """

    segment_name: X12SegmentName = X12SegmentName.HI
    health_care_code_1: List = Field(is_component=True)
    health_care_code_2: Optional[List] = Field(is_component=True)
    health_care_code_3: Optional[List] = Field(is_component=True)
    health_care_code_4: Optional[List] = Field(is_component=True)
    health_care_code_5: Optional[List] = Field(is_component=True)
    health_care_code_6: Optional[List] = Field(is_component=True)
    health_care_code_7: Optional[List] = Field(is_component=True)
    health_care_code_8: Optional[List] = Field(is_component=True)


class HlSegment(X12Segment):
    """
    Defines a hierarchical organization used to relate one grouping of segments to another
    Example:
        HL*3*2*22*1~
    """

    segment_name: X12SegmentName = X12SegmentName.HL
    hierarchical_id_number: str = Field(min_length=1, max_length=12)
    hierarchical_parent_id_number: str = Field(min_length=1, max_length=12)
    hierarchical_level_code: str = Field(min_length=1, max_length=2)
    hierarchical_child_code: str = Field(min_length=1, max_length=1, regex="^0|1$")


class HlhSegment(X12Segment):
    """
    Member Health Information
    Example:
        HLH*X*74*210~
    """

    class HealthRelatedCode(str, Enum):
        """
        Code values for HLH01
        """

        NONE = "N"
        SUBSTANCE_ABUSE = "S"
        TOBACCO_USE = "T"
        UNKNOWN = "U"
        TOBACCO_USE_AND_SUBSTANCE_ABUSE = "X"

    segment_name: X12SegmentName = X12SegmentName.HLH
    health_related_code: HealthRelatedCode
    member_height: Optional[Decimal]
    member_weight: Optional[Decimal]


class HsdSegment(X12Segment):
    """
    Health Care Services Delivery
    Example:
        HSD*VS*12*WK*3*34*1~
    """

    class QuantityQualifier(str, Enum):
        """
        HSD01 code values
        """

        DAYS = "DY"
        UNITS = "FL"
        HOURS = "HS"
        MONTH = "MN"
        VISITS = "VS"

    class MeasurementCode(str, Enum):
        """
        HSD03 code values
        """

        DAYS = "DA"
        MONTHS = "MO"
        VISIT = "VS"
        WEEK = "WK"
        YEARS = "YR"

    class TimePeriodQualifier(str, Enum):
        """
        HD05 code values
        """

        HOURS = "6"
        DAY = "7"
        YEARS = "21"
        SERVICE_YEAR = "22"
        CALENDAR_YEAR = "23"
        YEAR_TO_DATE = "24"
        CONTRACT = "25"
        EPISODE = "26"
        VISIT = "27"
        OUTLIER = "28"
        REMAINING = "29"
        EXCEEDED = "30"
        NOT_EXCEEDED = "31"
        LIFETIME = "32"
        LIFETIME_RECURRING = "33"
        MONTH = "34"
        WEEK = "35"

    class DeliveryFrequencyCode(str, Enum):
        """
        HSD07 code values
        """

        FIRST_WEEK_OF_MONTH = "1"
        SECOND_WEEK_OF_MONTH = "2"
        THIRD_WEEK_OF_MONTH = "3"
        FOURTH_WEEK_OF_MONTH = "4"
        FIFTH_WEEK_OF_MONTH = "5"
        FIRST_AND_THIRD_WEEKS_OF_MONTH = "6"
        SECOND_AND_FOURTH_WEEKS_OF_MONTH = "7"
        FIRST_WORKING_DAY_OF_PERIOD = "8"
        LAST_WORKING_DAY_OF_PERIOD = "9"
        MONDAY_TO_FRIDAY = "A"
        MONDAY_TO_SATURDAY = "B"
        MONDAY_TO_SUNDAY = "C"
        MONDAY = "D"
        TUESDAY = "E"
        WEDNESDAY = "F"
        THURSDAY = "G"
        FRIDAY = "H"
        SATURDAY = "J"
        SUNDAY = "K"
        MONDAY_TO_THURSDAY = "L"
        IMMEDIATELY = "M"
        AS_DIRECTED = "N"
        DAILY_MON_TO_FRI = "O"
        HALF_MON_HALF_THURS = "P"
        HALF_TUES_HALF_THURS = "Q"
        HALF_WED_HALF_FRIDAY = "R"
        ONCE_ANYTIME_MON_TO_FRI = "S"
        TUESDAY_TO_FRIDAY = "SG"
        MONDAY_TUESDAY_THURSDAY = "SL"
        MONDAY_TUESDAY_FRIDAY = "SP"
        WEDNESDAY_THURSDAY = "SX"
        MONDAY_WEDNESDAY_THURSDAY = "SY"
        TUESDAY_THURSDAY_FRIDAY = "SZ"
        HALF_TUESDAY_HALF_FRIDAY = "T"
        HALF_MONDAY_HALF_WEDNESDAY = "U"
        THIRD_MONDAY_THIRD_WEDNESDAY_THIRD_FRIDAY = "V"
        WHENEVER_NECESSARY = "W"
        HALF_BY_WEDNESDAY_BALANCE_BY_FRIDAY = "X"
        NONE_CANCEL_PREVIOUS_PATTERN = "Y"

    class DeliveryPatternTimeCode(str, Enum):
        """
        HSD08 code values
        """

        FIRST_SHIFT = "A"
        SECOND_SHIFT = "B"
        THIRD_SHIFT = "C"
        AM = "D"
        PM = "E"
        AS_DIRECTED = "F"
        ANY_SHIFT = "G"
        NONE_CANCEL_PREVIOUS_PATTERN = "Y"

    segment_name: X12SegmentName = X12SegmentName.HSD
    quantity_qualifier: Optional[QuantityQualifier]
    quantity: Optional[Decimal]
    measurement_code: Optional[MeasurementCode]
    sample_selection_modulus: Optional[Decimal]
    time_period_qualifier: Optional[TimePeriodQualifier]
    period_count: Optional[Decimal]
    delivery_frequency_code: Optional[DeliveryFrequencyCode]
    delivery_pattern_time_code: Optional[DeliveryPatternTimeCode]

    @root_validator
    def validate_quantity(cls, values):
        """
        Validates that quantity values are conveyed with a qualifier and value.

        :param values: The raw, unvalidated transaction data.
        """
        quantity_fields: Tuple = values.get("quantity_qualifier"), values.get(
            "quantity"
        )

        if not any(quantity_fields):
            raise ValueError("Quantity requires a qualifier and value")

        return values

    @root_validator
    def validate_periods(cls, values):
        """
        Validates that time periods are conveyed correctly
        """
        if values.get("period_count") and not values.get("time_period_qualifier"):
            raise ValueError("Period requires a qualifier and value")
        return values


class IcmSegment(X12Segment):
    """
    Member Income
    Example:
        ICM*1*425.25*40.00~
    """

    class FrequencyCode(str, Enum):
        """
        Code values for ICM01
        """

        WEEKLY = "1"
        BIWEEKLY = "2"
        SEMIMONTHLY = "3"
        MONTHLY = "4"
        DAILY = "6"
        ANNUAL = "7"
        TWO_CALENDAR_MONTHS = "8"
        LUMP_SUM_SEPARATION_ALLOWANCE = "9"
        YEAR_TO_DATE = "B"
        SINGLE = "C"
        HOURLY = "H"
        QUARTERLY = "Q"
        SEMI_ANNUAL = "S"
        UNKNOWN = "U"

    segment_name: X12SegmentName = X12SegmentName.ICM
    frequency_code: FrequencyCode
    wage_amount: Decimal
    weekly_hours: Optional[Decimal]
    location_identifier: Optional[str] = Field(max_length=30)
    salary_grade_code: Optional[str] = Field(max_length=5)
    currency_code: Optional[str]


class IdcSegment(X12Segment):
    """
    Identification Card
    Example:
        IDC*12345*H~
    """

    class IdentificationCardTypeCode(str, Enum):
        """
        Code values for IDC02
        """

        DENTAL_INSURANCE = "D"
        HEALTH_INSURANCE = "H"
        PRESCRIPTION_DRUG_SERVICE_DRUG_INSURANCE = "P"

    class ActionCode(str, Enum):
        """
        Code values for IDC04
        """

        ADD = "1"
        CHANGE = "2"
        REPLACE = "RX"

    segment_name: X12SegmentName = X12SegmentName.IDC
    plan_coverage_description: str = Field(min_length=1, max_length=50)
    identification_card_type_code: IdentificationCardTypeCode
    identification_card_count: Optional[int] = conint(gt=0)
    action_code: Optional[ActionCode]


class IeaSegment(X12Segment):
    """
    Defines the interchange footer and is an EDI control segment.
    Example:
        IEA*1*000000907~
    """

    segment_name: X12SegmentName = X12SegmentName.IEA
    number_of_included_functional_groups: PositiveInt
    interchange_control_number: str = Field(min_length=9, max_length=9)


class IiiSegment(X12Segment):
    """
    Additional Inquiry Information
    Example:
        III*ZZ*21~
    """

    class CodeListQualifierCode(str, Enum):
        """
        Code values for III01
        """

        NCCI_NATURE_OF_INJURY_CODE = "GR"
        NATURE_OF_INJURY_CODE = "NI"
        MUTUALLY_DEFINED = "ZZ"

    segment_name: X12SegmentName = X12SegmentName.III
    code_list_qualifier_code: Optional[CodeListQualifierCode]
    industry_code: Optional[str] = Field(max_length=30)
    code_category: Optional[Literal["44"]]
    injured_body_part_name: Optional[str] = Field(max_length=264)

    @root_validator
    def validate_industry_code(cls, values):
        """
        Validates that an industry code is conveyed with a qualifier and value, if sent at all.

        :param values: The validated model values.
        """
        industry_codes = values.get("code_list_qualifier_code"), values.get(
            "industry_code"
        )
        if any(industry_codes) and not all(industry_codes):
            raise ValueError("Industry codes require a qualifier and value")
        return values

    @root_validator
    def validate_nature_of_injury(cls, values):
        """
        Validates the nature of injury if present

        :param values: The validated model values
        """
        if values.get("code_category") and not values.get("injured_body_part_name"):
            raise ValueError(
                "Nature of injury requires a category and value/description"
            )
        return values


class InsSegment(X12Segment):
    """
    Insured benefit.
    Example:
        INS*Y*18*021*28*A***FT~
    """

    class ResponseCode(str, Enum):
        """
        INS01 code values
        """

        NO = "N"
        YES = "Y"

    segment_name: X12SegmentName = X12SegmentName.INS
    member_indicator: ResponseCode
    individual_relationship_code: str = Field(min_length=2, max_length=2)
    maintenance_type_code: str = Field(min_length=3, max_length=3)
    maintenance_reason_code: Optional[str] = Field(max_length=3)
    benefit_status_code: str = Field(min_length=1, max_length=1)
    medicare_status_code: Optional[List[str]] = Field(is_component=True)
    cobra_qualifying_event_code: Optional[str] = Field(max_length=2)
    employment_status_code: Optional[str] = Field(max_length=2)
    student_status_code: Optional[str] = Field(max_length=1)
    handicap_indicator: Optional[ResponseCode]
    date_time_period_format_qualifier: Optional[str] = Field(max_length=3)
    member_death_date: Optional[Union[str, datetime.date]]
    confidentiality_code: Optional[str] = Field(max_length=1)
    city_name: Optional[str] = Field(max_length=30)
    state_province_code: Optional[str] = Field(max_length=2)
    country_code: Optional[str] = Field(max_length=3)
    birth_sequence_number: Optional[int]

    _validate_death_date = field_validator("member_death_date")(validate_date_field)

    @root_validator
    def validate_member_death_datefields(cls, values):
        """
        Validates that both a date_time_period_format_qualifier and member_death_date are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        date_fields: Tuple = values.get(
            "date_time_period_format_qualifier"
        ), values.get("member_death_date")

        if any(date_fields) and not all(date_fields):
            raise ValueError(
                "If member death date is reported both date time format qualifier and member_death_date are required."
            )

        return values


class IsaSegment(X12Segment):
    """
    Defines the interchange header and is an EDI control segment.
    The ISA Segment is a fixed length segment (106 characters)
    Example:
        ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~
    """

    segment_name: X12SegmentName = X12SegmentName.ISA
    authorization_information_qualifier: str = Field(min_length=2, max_length=2)
    authorization_information: str = Field(min_length=10, max_length=10)
    security_information_qualifier: str = Field(min_length=2, max_length=2)
    security_information: str = Field(min_length=10, max_length=10)
    interchange_sender_qualifier: str = Field(min_length=2, max_length=2)
    interchange_sender_id: str = Field(min_length=15, max_length=15)
    interchange_receiver_qualifier: str = Field(min_length=2, max_length=2)
    interchange_receiver_id: str = Field(min_length=15, max_length=15)
    interchange_date: Union[str, datetime.date]
    interchange_time: str
    repetition_separator: str = Field(min_length=1, max_length=1)
    interchange_control_version_number: str = Field(min_length=5, max_length=5)
    interchange_control_number: str = Field(min_length=9, max_length=9)
    acknowledgment_requested: str = Field(min_length=1, max_length=1)
    interchange_usage_indicator: str = Field(min_length=1, max_length=1)
    component_element_separator: str = Field(min_length=1, max_length=1)

    _validate_interchange_date = field_validator("interchange_date")(
        parse_interchange_date
    )

    def x12(self) -> str:
        """
        Overriden to support formatting the interchange date as yymmdd ( %y%m%d )
        """
        x12_string: str = super().x12()
        segment_fields = x12_string.split(self.delimiters.element_separator)

        interchange_date = datetime.datetime.strptime(
            segment_fields[9], "%Y%m%d"
        ).date()
        segment_fields[9] = interchange_date.strftime("%y%m%d")

        return self.delimiters.element_separator.join(segment_fields)


class K3Segment(X12Segment):
    """
    File information
    Example:
        K3*STATE DATA REQUIREMENT~
    """

    segment_name: X12SegmentName = X12SegmentName.K3
    fixed_format_information: str = Field(min_length=1, max_length=80)
    record_format_code: Optional[str] = Field(max_length=2)
    composite_unit_of_measurement: Optional[str] = Field(is_component=True)


class LeSegment(X12Segment):
    """
    Loop trailer segment.
    Used to "close" a loop grouping opened by a LS segment.
    Example:
        LE*2120~
    """

    segment_name: X12SegmentName = X12SegmentName.LE
    loop_id_code: str = Field(min_length=1, max_length=4)


class LinSegment(X12Segment):
    """
    Drug Identification
    Example:
        LIN**N4*01234567891~
    """

    class ProductServiceIdQualifier(str, Enum):
        """
        Code values for LIN02
        """

        EAN_UCC_13 = "EN"
        EAN_UCC_8 = "EO"
        HIBC_SUPPLIER_PRIMARY_DATA_MESSAGE = "HI"
        NATIONAL_DRUG_CODE_542_FORMAT = "N4"
        CUSTOMER_ORDER_NUMBER = "ON"
        GTIN_14_DIGIT_STRUCTURE = "UK"
        UCC_12 = "UP"

    segment_name: X12SegmentName = X12SegmentName.LIN
    assigned_identification: Optional[str] = Field(max_length=20)
    product_service_id_qualifier: ProductServiceIdQualifier
    national_drug_code_universal_product_number: str = Field(
        min_length=1, max_length=48
    )


class LqSegment(X12Segment):
    """
    Form Identification Code
    Example:
        LQ*UT*1.02~
    """

    class CodeListQualifierCode(str, Enum):
        """
        Code values for LQ01
        """

        FORM_TYPE_CODE = "AS"
        CMS_CMN_FORMS = "UT"

    segment_name: X12SegmentName = X12SegmentName.LQ
    code_list_qualifier_code: CodeListQualifierCode
    form_identifier: str = Field(min_length=1, max_length=30)


class LsSegment(X12Segment):
    """
    Loop Header Segment
    The LS segment is used to disambiguate loops which start with the same segment.
    Example:
        LS*2120~
    """

    segment_name: X12SegmentName = X12SegmentName.LS
    loop_id_code: str = Field(min_length=1, max_length=4)


class LuiSegment(X12Segment):
    """
    Member language
    Example:
        LUI*LD*123**8~
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for LUI01
        """

        NISO_Z39_53_LANGUAGE_CODES = "LD"
        ISO_639_LANGUAGE_CODES = "LE"

    class UseOfLanguageIndicator(str, Enum):
        """
        Code values for LUI04
        """

        LANGUAGE_READING = "5"
        LANGUAGE_WRITING = "6"
        LANGUAGE_SPEAKING = "7"
        NATIVE_LANGUAGE = "8"

    segment_name: X12SegmentName = X12SegmentName.LUI
    identification_code_qualifier: Optional[IdentificationCodeQualifier]
    identification_code: Optional[str] = Field(max_length=80)
    description: Optional[str] = Field(max_length=80)
    language_use_indicator: Optional[UseOfLanguageIndicator]


class LxSegment(X12Segment):
    """
    Transaction set line number
    """

    segment_name: X12SegmentName = X12SegmentName.LX
    assigned_number: conint(gt=0)


class MeaSegment(X12Segment):
    """
    Measurements
    Example:
        MEA*TR*R1*113.40~
    """

    class MeasurementReferenceIdCode(str, Enum):
        """
        Code values for MEA01
        """

        ORIGINAL = "OG"
        TEST_RESULTS = "TR"

    class MeasurementQualifier(str, Enum):
        """
        Code values for MEA02
        """

        HEIGHT = "HT"
        HEMOGLOBIN = "R1"
        HEMATOCRIT = "R2"
        EPOETIN_STARTING_DOSAGE = "R3"
        CREATINE = "R4"

    segment_name: X12SegmentName = X12SegmentName.MEA
    measurement_reference_id_code: MeasurementReferenceIdCode
    measurement_qualifier: MeasurementQualifier
    measurement_value: Decimal


class MiaSegment(X12Segment):
    """
    Medicare Inpatient Adjudication
    Example:
        MIA*0***138018.40~
    """

    segment_name: X12SegmentName = X12SegmentName.MIA
    covered_days_visit_count: Literal["0"]
    pps_operating_outlier_amount: Optional[Decimal]
    lifetime_psychiatric_days_count: Optional[Decimal]
    claim_drg_amount: Optional[Decimal]
    claim_payment_remark_code: Optional[str] = Field(max_length=20)
    claim_disproportionate_share_amount: Optional[Decimal]
    claim_msp_passthrough_amount: Optional[Decimal]
    claim_pps_capital_amount: Optional[Decimal]
    pps_capital_fsp_drg_amount: Optional[Decimal]
    pps_capital_hsp_drg_amount: Optional[Decimal]
    pps_capital_dsh_drg_amount: Optional[Decimal]
    old_capital_amount: Optional[Decimal]
    pps_capital_ime_amount: Optional[Decimal]
    pps_operating_hospital_specific_drg_amount: Optional[Decimal]
    cost_report_day_count: Optional[Decimal]
    pps_operating_federal_specific_drg_amount: Optional[Decimal]
    claim_pps_capital_outlier_amount: Optional[Decimal]
    claim_indirect_teaching_amount: Optional[Decimal]
    nonpayable_professional_component_amount: Optional[Decimal]
    claim_payment_remark_code_1: Optional[str] = Field(max_length=50)
    claim_payment_remark_code_2: Optional[str] = Field(max_length=50)
    claim_payment_remark_code_3: Optional[str] = Field(max_length=50)
    claim_payment_remark_code_4: Optional[str] = Field(max_length=50)
    pps_capital_exception_amount: Optional[Decimal]


class MoaSegment(X12Segment):
    """
    Outpatient Adjudication Information
    Example:
        MOA***A4~
    """

    segment_name: X12SegmentName = X12SegmentName.MOA
    reimbursement_rate: Optional[Decimal]
    hcpcs_payable_amount: Optional[Decimal]
    claim_payment_remark_code_1: Optional[str] = Field(max_length=50)
    claim_payment_remark_code_2: Optional[str] = Field(max_length=50)
    claim_payment_remark_code_3: Optional[str] = Field(max_length=50)
    claim_payment_remark_code_4: Optional[str] = Field(max_length=50)
    claim_payment_remark_code_5: Optional[str] = Field(max_length=50)
    end_stage_renal_disease_payment_amount: Optional[Decimal]
    nonpayable_professional_component_billable_amount: Optional[Decimal]


class MpiSegment(X12Segment):
    """
    Military Personnel Information
    """

    class InformationStatusCode(str, Enum):
        """
        Code values for MPI01
        """

        PARTIAL = "P"
        CURRENT = "C"
        LATEST = "L"
        OLDEST = "O"
        PRIOR = "P"
        SECOND_MOST_CURRENT = "S"
        THIRD_MOST_CURRENT = "T"

    class EmploymentStatusCode(str, Enum):
        """
        Code values for MPI02
        """

        ACTIVE_RESERVE = "AE"
        ACTIVE_MILITARY_OVERSEAS = "AO"
        ACADEMY_STUDENT = "AS"
        PRESIDENTIAL_APPOINTEE = "AT"
        ACTIVE_MILITARY_USA = "AU"
        CONTRACTOR = "CC"
        DISHONORABLY_DISCHARGED = "DD"
        HONORABLY_DISCHARGED = "HD"
        INACTIVE_RESERVES = "IR"
        LEAVE_OF_ABSENCE_MILITARY = "LX"
        PLAN_TO_ENSLIST = "PE"
        RECOMISSIONED = "RE"
        RETIRED_MILITARY_OVERSEAS = "RM"
        RETIRED_WITHOUT_RECALL = "RR"
        RETIRED_MILITARY_USA = "RU"

    class GovernmentServicesAffiliationCode(str, Enum):
        """
        Code values for MPI03
        """

        AIR_FORCE = "A"
        AIR_FORCE_RESERVE = "B"
        ARMY = "C"
        ARMY_RESERVES = "D"
        COAST_GUARD = "E"
        MARINE_CORPS = "F"
        MARINE_CORPS_RESERVE = "G"
        NATIONAL_GUARD = "H"
        NAVY = "I"
        NAVY_RESERVES = "J"
        OTHER = "K"
        PEACE_CORP = "L"
        REGULAR_ARMED_FORCES = "M"
        RESERVES = "N"
        US_PUBLIC_HEALTH_SERVICE = "O"
        FOREIGN_MILITARY = "Q"
        AMERICAN_RED_CROSS = "R"
        DEPARTMENT_OF_DEFENSE = "S"
        UNITED_SERVICES_ORGANIZATION = "U"
        MILITARY_SEALIFT_COMMAND = "W"

    class MilitaryServiceRankCode(str, Enum):
        """
        Code values for MPI05
        """

        ADMIRAL = "A1"
        AIRMAN = "A2"
        AIRMAN_FIRST_CLASS = "A3"
        BASIC_AIRMAN = "B1"
        BRIGADIER_GENERAL = "B2"
        CAPTAIN = "C1"
        CHIEF_MASTER_SERGEANT = "C2"
        CHIEF_PETTY_OFFICER = "C3"
        CHIEF_WARRANT = "C4"
        COLONEL = "C5"
        COMMANDER = "C6"
        COMMODORE = "C7"
        CORPORAL = "C8"
        CORPORAL_SPECIALIST_4 = "C9"
        ENSIGN = "E1"
        FIRST_LIEUTENANT = "F1"
        FIRST_SERGEANT = "F2"
        FIRST_SERGEANT_MASTER_SERGEANT = "F3"
        FLEET_ADMIRAL = "F4"
        GENERAL = "G1"
        GUNNERY_SERGEANT = "G4"
        LANCE_CORPORAL = "L1"
        LIEUTENANT = "L2"
        LIEUTENANT_COLONEL = "L3"
        LIEUTENANT_COMMANDER = "L4"
        LIEUTENANT_GENERAL = "L5"
        LIEUTENANT_JUNIOR_GRADE = "L6"
        MAJOR = "M1"
        MAJOR_GENERAL = "M2"
        MASTER_CHIEF_PETTY_OFFICER = "M3"
        MASTER_GUNNERY_SERGEANT_MAJOR = "M4"
        MASTER_SERGEANT = "M5"
        MASTER_SERGEANT_SPECIALIST_8 = "M6"
        PETTY_OFFICER_FIRST_CLASS = "P1"
        PETTY_OFFICER_SECOND_CLASS = "P2"
        PETTY_OFFICER_THIRD_CLASS = "P3"
        PRIVATE = "P4"
        PRIVATE_FIRST_CLASS = "P5"
        REAR_ADMIRAL = "R1"
        RECRUIT = "R2"
        SEAMAN = "S1"
        SEAMAN_APPRENTICE = "S2"
        SEAMAN_RECRUIT = "S3"
        SECOND_LIEUTENANT = "S4"
        SENIOR_CHIEF_PETTY_OFFICER = "S5"
        SENIOR_MASTER_SERGEANT = "S6"
        SERGEANT = "S7"
        SERGEANT_FIRST_CLASS_SPECIALIST_7 = "S8"
        SERGEANT_MAJOR_SPECIALIST_9 = "S9"
        SERGEANT_SPECIALIST_5 = "SA"
        STAFF_SERGEANT = "SB"
        STAFF_SERGEANT_SPECIALIST_6 = "SC"
        TECHNICAL_SERGEANT = "T1"
        VICE_ADMIRAL = "V1"
        WARRANT_OFFICER = "W1"

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code values for MPI06
        """

        DATE = "D8"
        DATE_RANGE = "RD8"

    segment_name: X12SegmentName = X12SegmentName.MPI
    information_status_code: InformationStatusCode
    employment_status_code: EmploymentStatusCode
    government_services_affiliation_code: GovernmentServicesAffiliationCode
    description: Optional[str] = Field(max_length=80)
    military_service_rank_code: Optional[MilitaryServiceRankCode]
    date_time_period_format_qualifier: Optional[DateTimePeriodFormatQualifier]
    date_time_period: Optional[str] = Field(max_length=35)

    @root_validator
    def validate_date_fields(cls, values):
        """
        Validates that both a date_time_format_qualifier and date_time_period are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        date_fields: Tuple = values.get("date_time_format_qualifier"), values.get(
            "date_time_period"
        )

        if any(date_fields) and not all(date_fields):
            raise ValueError(
                "If either date_time_period_format_qualifier or date_time_period are provided, both are required"
            )

        return values


class MsgSegment(X12Segment):
    """
    Message segment - for free form text.
    """

    segment_name: X12SegmentName = X12SegmentName.MSG
    free_form_text: str = Field(min_length=1, max_length=264)


class N1Segment(X12Segment):
    """
    Payer Identification
    """

    segment_name: X12SegmentName = X12SegmentName.N1
    entity_identifier_code: str = Field(min_length=2, max_length=3)
    name: str = Field(min_length=1, max_length=60)
    identification_code_qualifier: Optional[str] = Field(min_length=1, max_length=2)
    identification_code: Optional[str] = Field(min_length=2, max_length=80)


class N3Segment(X12Segment):
    """
    Party Location (Address)
    Example:
        N3*201 PARK AVENUE*SUITE 300~
    """

    segment_name: X12SegmentName = X12SegmentName.N3
    address_information_1: str = Field(min_length=1, max_length=55)
    address_information_2: Optional[str] = Field(max_length=55)


class N4Segment(X12Segment):
    """
    Geographic Location (Address)
    Example:
        N4*KANSAS CITY*MO*64108~
    """

    segment_name: X12SegmentName = X12SegmentName.N4
    city_name: str = Field(min_length=2, max_length=30)
    state_province_code: Optional[str] = Field(max_length=2)
    postal_code: Optional[str] = Field(max_length=15)
    country_code: Optional[str] = Field(max_length=3)
    location_qualifier: Optional[str] = Field(max_length=2)
    location_identifier: Optional[str] = Field(max_length=30)
    country_subdivision_code: Optional[str] = Field(max_length=3)

    @root_validator
    def validate_state_codes(cls, values):
        """
        Validates that a N4 segment does not contain both a state_province_code and country_subdivision_code

        :param values: The raw, unvalidated transaction data.
        """
        state_fields: Tuple = values.get("state_province_code"), values.get(
            "country_subdivision_code"
        )

        if all(state_fields):
            raise ValueError(
                "only one of state_province_code or country_subdivision_code is allowed"
            )

        return values


class Nm1Segment(X12Segment):
    """
    Entity Name and Identification Number
    Example:
        NM1*PR*2*PAYER C*****PI*12345~
    """

    class EntityQualifierCode(str, Enum):
        """
        NM1.02 Entity Qualifier Code to specify the entity type
        """

        PERSON = "1"
        NON_PERSON = "2"

    segment_name: X12SegmentName = X12SegmentName.NM1
    entity_identifier_code: str = Field(min_length=2, max_length=3)
    entity_type_qualifier: EntityQualifierCode
    name_last_or_organization_name: str = Field(min_length=1, max_length=60)
    name_first: Optional[str] = Field(max_length=35)
    name_middle: Optional[str] = Field(max_length=25)
    name_prefix: Optional[str] = Field(max_length=10)
    name_suffix: Optional[str] = Field(max_length=10)
    identification_code_qualifier: Optional[str] = Field(max_length=2)
    identification_code: Optional[str] = Field(max_length=80)
    entity_relationship_code: Optional[str] = Field(max_length=2)
    # NM111 - NM112 are not used

    @root_validator
    def validate_identification_codes(cls, values):
        """
        Validates that both an identification code and qualifier are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        id_fields: Tuple = values.get("identification_code_qualifier"), values.get(
            "identification_code"
        )

        if any(id_fields) and not all(id_fields):
            raise ValueError(
                "Identification code usage requires the code qualifier and code value"
            )

        return values

    @validator("name_first", "name_middle", "name_prefix", "name_suffix")
    def validate_organization_name_fields(cls, field_value, values):
        """
        Validates that person name fields are not used within an organizational record context.

        :param field_value: The person name field (first, middle, prefix, suffix) values
        :param values: The previously validated field names and values
        """
        entity_type = values["entity_type_qualifier"]

        if cls.EntityQualifierCode.NON_PERSON.value == entity_type:
            if field_value:
                raise ValueError(
                    "Invalid field usage for Organization/Non-Person Entity"
                )
        return field_value


class NteSegment(X12Segment):
    """
    Note/Special Instruction
    Example:
        NTE*ADD*SURGERY WAS UNUSUALLY LONG BECAUSE [FILL IN REASON]~
    """

    segment_name: X12SegmentName = X12SegmentName.NTE
    note_reference_code: str = Field(min_length=3, max_length=3)
    description: str = Field(min_length=1, max_length=80)


class OiSegment(X12Segment):
    """
    Other insurance information:
    Example:
        OI***Y*B**Y~
    """

    class BenefitsAssignmentCertificationIndicator(str, Enum):
        """
        Code values for OI03
        """

        NO = "NO"
        NOT_APPLICABLE = "N"
        YES = "Y"

    class ReleaseOfInformationCode(str, Enum):
        """
        Code values for OI06
        """

        INFORMED_CONSENT = "I"
        PROVIDER_SIGNED_STATEMENT = "Y"

    segment_name: X12SegmentName = X12SegmentName.OI
    claim_filing_indicator_code: Optional[str] = Field(max_length=2)
    claim_submission_reason_code: Optional[str] = Field(max_length=2)
    benefits_assignment_certification: BenefitsAssignmentCertificationIndicator
    patient_signature_source_code: Optional[Literal["P"]]
    provider_agreement_code: Optional[str] = Field(max_length=1)
    release_of_information_code: ReleaseOfInformationCode


class PatSegment(X12Segment):
    """
    Patient Information:
    Example:
        PAT******01*146~
    """

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code value for PAT04
        """

        SPECIFIC_DATE = "D8"

    segment_name: X12SegmentName = X12SegmentName.PAT
    individual_relationship_code: Optional[str] = Field(max_length=2)
    patient_location_code: Optional[str] = Field(max_length=1)
    employment_status_code: Optional[str] = Field(max_length=2)
    student_status_code: Optional[str] = Field(max_length=1)
    date_time_period_format_qualifier: Optional[DateTimePeriodFormatQualifier]
    patient_death_date: Optional[Union[str, datetime.date]]
    unit_basis_measurement_code: Optional[Literal["01"]]
    patient_weight: Optional[Decimal]
    pregnancy_indicator: Optional[Literal["Y"]]

    _validate_transaction_date = field_validator("patient_death_date")(parse_x12_date)

    @root_validator
    def validate_death_date(cls, values):
        """
        Validates that both a date format qualifier and the patient death date are both present, if one or the other is
        present.

        :param values: The raw, unvalidated transaction data.
        """
        date_fields: Tuple = values.get(
            "date_time_period_format_qualifier"
        ), values.get("patient_death_date")

        if any(date_fields) and not all(date_fields):
            raise ValueError(
                "Patient Death Date requires format qualifier and date value"
            )

        return values

    @root_validator
    def validate_weight(cls, values):
        """
        Validates that both a weight unit and value are present, if one or the other is
        present.

        :param values: The raw, unvalidated transaction data.
        """
        weight_fields: Tuple = values.get("unit_basis_measurement_code"), values.get(
            "patient_weight"
        )

        if any(weight_fields) and not all(weight_fields):
            raise ValueError("Patient weight requires units and value")

        return values


class PerSegment(X12Segment):
    """
    EDI Contact Information
    Example:
        PER*IC*JOHN SMITH*TE*5551114444*EX*123~
    """

    class ContactFunctionCode(str, Enum):
        """
        Code value for PER01
        """

        INFORMATION_CONTACT = "IC"

    segment_name: X12SegmentName = X12SegmentName.PER
    contact_function_code: ContactFunctionCode
    name: Optional[str] = Field(max_length=60)
    communication_number_qualifier_1: str = Field(max_length=2)
    communication_number_1: str = Field(max_length=256)
    communication_number_qualifier_2: Optional[str] = Field(max_length=2)
    communication_number_2: Optional[str] = Field(max_length=256)
    communication_number_qualifier_3: Optional[str] = Field(max_length=2)
    communication_number_3: Optional[str] = Field(max_length=256)

    @root_validator
    def validate_communication(cls, values):
        """
        Validates that both a communication qualifier and number are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        communication_fields: Tuple = values.get(
            "communication_number_qualifier_2"
        ), values.get("communication_number_2")

        if any(communication_fields) and not all(communication_fields):
            raise ValueError("communication fields require a qualifier and number")

        communication_fields = values.get(
            "communication_number_qualifier_3"
        ), values.get("communication_number_3")

        if any(communication_fields) and not all(communication_fields):
            raise ValueError("communication fields require a qualifier and number")

        return values


class PlaSegment(X12Segment):
    """
    Place or location
    Example:
        PLA*2*1P*19970628**AI~
    """

    segment_name: X12SegmentName = X12SegmentName.PLA
    action_code: str = Field(min_length=1, max_length=2)
    entity_identifier_code: str = Field(min_length=2, max_length=3)
    date: Union[str, datetime.date]
    time: Optional[str]
    maintenance_reason_code: str = Field(min_length=2, max_length=3)

    _validate_x12_date = field_validator("date")(validate_date_field)


class PlbSegment(X12Segment):
    """
    Provider Level Adjustment
    Example:
        PLB*1234567890*20000930*CV:9876514*-1.27~
    """

    segment_name: X12SegmentName = X12SegmentName.PLB
    provider_identifier: str = Field(min_length=1, max_length=50)
    fiscal_period_date: Union[str, datetime.date]
    adjustment_reason_code_1: str = Field(is_component=True)
    provider_adjustment_amount_1: Decimal
    adjustment_reason_code_2: Optional[str] = Field(is_component=True)
    provider_adjustment_amount_2: Optional[Decimal]
    adjustment_reason_code_3: Optional[str] = Field(is_component=True)
    provider_adjustment_amount_3: Optional[Decimal]
    adjustment_reason_code_4: Optional[str] = Field(is_component=True)
    provider_adjustment_amount_4: Optional[Decimal]
    adjustment_reason_code_5: Optional[str] = Field(is_component=True)
    provider_adjustment_amount_5: Optional[Decimal]
    adjustment_reason_code_6: Optional[str] = Field(is_component=True)
    provider_adjustment_amount_6: Optional[Decimal]

    _validate_x12_date = field_validator("fiscal_period_date")(validate_date_field)


class PrvSegment(X12Segment):
    """
    Provider Information
    Example:
        PRV*RF*PXC*207Q00000X~
    """

    segment_name: X12SegmentName = X12SegmentName.PRV
    provider_code: str = Field(min_length=1, max_length=3)
    reference_identification_qualifier: Optional[str] = Field(max_length=3)
    reference_identification: Optional[str] = Field(max_length=50)

    @root_validator
    def validate_reference_id(cls, values):
        """
        Validates that both an identification value and qualifier are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        reference_fields: Tuple = values.get(
            "reference_identification_qualifier"
        ), values.get("reference_identification")

        if any(reference_fields) and not all(reference_fields):
            raise ValueError(
                "only one of reference_identification_qualifier or reference_identification is allowed"
            )

        return values


class Ps1Segment(X12Segment):
    """
    Purchased Service Information
    Example:
        PS1*PN222222*110.00~
    """

    segment_name: X12SegmentName = X12SegmentName.PS1
    purchased_service_provider_identifier: str = Field(min_length=1, max_length=50)
    purchased_service_charge_amount: Decimal
    state_province_code: Optional[str] = Field(max_length=2)


class PwkSegment(X12Segment):
    """
    Paperwork
    Example:
        PWK*OZ*BM***AC*DMN0012~
    """

    segment_name: X12SegmentName = X12SegmentName.PWK
    report_type_code: str = Field(min_length=2, max_length=2)
    report_transmission_code: str = Field(min_length=1, max_length=2)
    report_copies_needed: Optional[str] = Field(max_length=2)
    entity_identifier_code: Optional[str] = Field(max_length=3)
    identification_code_qualifier: Optional[str] = Field(max_length=2)
    identification_code: Optional[str] = Field(max_length=80)
    description: Optional[str] = Field(max_length=80)
    actions_indicated: Optional[str] = Field(is_component=True)
    request_category_code: Optional[str] = Field(max_length=2)

    @root_validator
    def validate_identification_code(cls, values):
        """
        Validates that both an identification code and code qualifier are present if either exists.
        :param values: The model values
        :return: The model values
        """
        fields = (
            values.get("identification_code_qualifier"),
            values.get("identification_code"),
        )

        if any(fields) and not all(fields):
            raise ValueError("Identification code requires a qualifier and code value")

        return values


class QtySegment(X12Segment):
    """
    Quantity Information
    Example:
        QTY*PT*2.00~
    """

    segment_name: X12SegmentName = X12SegmentName.QTY
    quantity_qualifier: str = Field(min_length=2, max_length=2)
    quantity: Decimal
    composite_unit_of_measure: Optional[str] = Field(is_component=True)
    free_form_message: Optional[str] = Field(max_length=30)


class RdmSegment(X12Segment):
    """
    Remittance Delivery Method
    Example:
        RDM*
    """

    class ReportTransmissionCode(str, Enum):
        """
        Code values for RDM01
        """

        BY_MAIL = "BM"
        EMAIL = "EM"
        FILE_TRANSFER = "FT"
        ONLINE = "OL"

    segment_name: X12SegmentName = X12SegmentName.RDM
    report_transmission_code: ReportTransmissionCode
    name: Optional[str] = Field(max_length=60)
    communication_number: Optional[str] = Field(max_length=256)

    @root_validator(pre=True)
    def validate_remittance_destination(cls, values):
        """Validates that appropriate fields are populated"""
        code = values.get("report_transmission_code")

        if code == "BM" and not values.get("name"):
            raise ValueError("name is required for mail remittance")
        elif code != "BM" and not values.get("communication_number"):
            raise ValueError("communication_number is required for online remittance")

        return values


class RefSegment(X12Segment):
    """
    Reference Identification
    Example:
        REF*EO*477563928~
    """

    segment_name: X12SegmentName = X12SegmentName.REF
    reference_identification_qualifier: str = Field(min_length=2, max_length=3)
    reference_identification: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(max_length=80)


class SbrSegment(X12Segment):
    """
    Subscriber Information
    Example:
        SBR*P**2222-SJ******CI~
    """

    segment_name: X12SegmentName = X12SegmentName.SBR
    payer_responsibility_code: str = Field(min_length=1, max_length=1)
    individual_relationship_code: Optional[str] = Field(max_length=2)
    group_policy_number: Optional[str] = Field(max_length=50)
    group_name: Optional[str] = Field(max_length=60)
    insurance_type_code: Optional[str] = Field(max_length=3)
    coordination_of_benefits_code: Optional[str] = Field(max_length=1)
    condition_response_code: Optional[str] = Field(max_length=1)
    employment_status_code: Optional[str] = Field(max_length=2)
    claim_filing_indicator_code: str = Field(min_length=1, max_length=2)


class SeSegment(X12Segment):
    """
    Transaction Set Footer
    Example:
        SE*17*0001~
    """

    segment_name: X12SegmentName = X12SegmentName.SE
    transaction_segment_count: PositiveInt
    transaction_set_control_number: str = Field(min_length=4, max_length=9)


class StcSegment(X12Segment):
    """
    Status Information
    Example:
        STC*E0:24:41*20050830~
    """

    segment_name: X12SegmentName = X12SegmentName.STC
    health_care_claim_status_1: str = Field(is_component=True)
    status_effective_date: Union[str, datetime.date]
    action_code: Optional[str] = Field(max_length=2)
    total_claim_charge_amount: Optional[Decimal]
    claim_payment_amount: Optional[Decimal]
    adjudication_finalized_date: Optional[Union[str, datetime.date]]
    payment_method_code: Optional[str] = Field(max_length=3)
    remittance_date: Optional[Union[str, datetime.date]]
    remittance_trace_number: Optional[str] = Field(max_length=16)
    health_care_claim_status_2: Optional[str] = Field(is_component=True)
    health_care_claim_status_3: Optional[str] = Field(is_component=True)
    free_form_message_text: Optional[str] = Field(max_length=264)

    _validate_status_effective_date = field_validator("status_effective_date")(
        parse_x12_date
    )
    _validate_adjudication_finalized_date = field_validator(
        "adjudication_finalized_date"
    )(parse_x12_date)
    _validate_remittance_date = field_validator("remittance_date")(parse_x12_date)


class StSegment(X12Segment):
    """
    Transaction Set Header.
    Example:
        ST*270*0001*005010X279A1~
    """

    segment_name: X12SegmentName = X12SegmentName.ST
    transaction_set_identifier_code: str = Field(min_length=3, max_length=3)
    transaction_set_control_number: str = Field(min_length=4, max_length=9)
    implementation_convention_reference: str = Field(min_length=1, max_length=35)


class Sv1Segment(X12Segment):
    """
    Professional Service Segment
    Example:
        SV1*HC:99213*40*UN*1.0***1~
    """

    class UnitBasisMeasurementCode(str, Enum):
        """
        Code values for SV103
        """

        MINUTES = "MJ"
        UNIT = "UN"

    segment_name: X12SegmentName = X12SegmentName.SV1
    product_service_id_qualifier: str = Field(is_component=True)
    line_item_charge_amount: Decimal
    unit_basis_measurement_code: UnitBasisMeasurementCode
    service_unit_count: condecimal(gt=Decimal("0.0"))
    place_of_service_code: Optional[str] = Field(max_length=2)
    service_type_code: Optional[str] = Field(max_length=2)
    composite_diagnosis_code_pointer: str = Field(is_component=True)
    monetary_amount: Optional[Decimal]
    emergency_indicator: Optional[Literal["Y"]]
    multiple_procedure_code: Optional[str] = Field(max_length=2)
    epsdt_indicator: Optional[Literal["Y"]]
    family_planning_indicator: Optional[Literal["Y"]]
    review_code: Optional[str] = Field(max_length=2)
    national_local_assigned_review_value: Optional[str] = Field(max_length=2)
    copay_status_code: Optional[Literal["0"]]
    health_care_professional_shortage_area_code: Optional[str] = Field(max_length=1)
    reference_identification: Optional[str] = Field(max_length=50)
    postal_code: Optional[str] = Field(max_length=15)
    monetary_amount: Optional[Decimal]
    level_of_care_code: Optional[str] = Field(max_length=1)
    provider_agreement_code: Optional[str] = Field(max_length=1)


class Sv2Segment(X12Segment):
    """
    Institutional Claim Service Line
    Example:
        SV2*0120**1500*DA*5~
    """

    class MeasurementCodes(str, Enum):
        """
        Code values for SV204
        """

        DAYS = "DA"
        UNIT = "UN"

    segment_name: X12SegmentName = X12SegmentName.SV2
    service_line_revenue_code: str = Field(min_length=1, max_length=48)
    composite_medical_procedure_identifier: Optional[str] = Field(is_component=True)
    line_item_charge_amount: Decimal
    measurement_code: MeasurementCodes
    service_unit_count: Decimal
    unit_rate: Optional[Decimal]
    non_covered_charge_amount: Optional[Decimal]
    condition_response_code: Optional[str] = Field(max_length=1)
    nursing_home_residential_status_code: Optional[str] = Field(max_length=1)
    level_of_care_code: Optional[str] = Field(max_length=1)


class Sv5Segment(X12Segment):
    """
    Durable Medical Equipment Service
    Example:
        SV5*HC:A4631*DA*30.00*50.00*5000.00*4~
    """

    class RentalUnitPriceIndicator(str, Enum):
        """
        Code values for SV506
        """

        WEEKLY = "1"
        MONTHLY = "4"
        DAILY = "6"

    segment_name: X12SegmentName = X12SegmentName.SV5
    product_service_id_qualifier: str = Field(is_component=True)
    unit_basis_measurement_code: Literal["DA"]
    length_of_medical_necessity: condecimal(gt=Decimal("0.0"))
    dme_rental_price: Decimal
    dme_purchase_price: Decimal
    rental_unit_price_indicator: RentalUnitPriceIndicator
    prognosis_code: Optional[str] = Field(max_length=1)


class SvcSegment(X12Segment):
    """
    Service Information
    Example:
        SVC*HC:99214*100.00*80.00~
    """

    segment_name: X12SegmentName = X12SegmentName.SVC
    composite_medical_procedure_identifier_1: str = Field(is_component=True)
    line_item_charge_amount: Decimal
    line_item_provider_payment_amount: Decimal
    revenue_code: Optional[str] = Field(max_length=48)
    units_of_service_paid_count: Optional[Decimal]
    composite_medical_procedure_identifier_2: Optional[str] = Field(is_component=True)
    original_units_of_service_count: Optional[Decimal]


class SvdSegment(X12Segment):
    """
    Line Ajudication Information
    Example:
        SVD*43*55.00*HC:84550**3.00~
    """

    segment_name: X12SegmentName = X12SegmentName.SVD
    other_payer_primary_identifier: str = Field(min_length=2, max_length=80)
    service_line_paid_amount: Decimal
    composite_medical_procedure_identifier: str = Field(is_component=True)
    product_service_id: Optional[str] = Field(max_length=48)
    paid_service_count: Decimal
    bundled_unbundled_line_number: Optional[conint(gt=0)]


class TrnSegment(X12Segment):
    """
    Trace Number Segment
    Example:
        TRN*1*98175-012547*8877281234*RADIOLOGY~
    """

    segment_name: X12SegmentName = X12SegmentName.TRN
    trace_type_code: str = Field(min_length=1, max_length=2)
    reference_identification_1: str = Field(min_length=1, max_length=50)
    originating_company_identifier: str = Field(min_length=10, max_length=10)
    reference_identification_2: Optional[str] = Field(max_length=50)


class Ts2Segment(X12Segment):
    """
    Provider supplemental information
    Example:
        TS2*59786.00*55375.77~
    """

    segment_name: X12SegmentName = X12SegmentName.TS2
    total_drg_amount: Optional[Decimal]
    total_federal_specific_amount: Optional[Decimal]
    total_hospital_specific_amount: Optional[Decimal]
    total_disproportionate_share_amount: Optional[Decimal]
    total_capital_amount: Optional[Decimal]
    total_indirect_medical_education_amount: Optional[Decimal]
    total_outlier_day_count: Optional[condecimal(ge=Decimal("0.0"))]
    total_day_outlier_amount: Optional[Decimal]
    total_cost_outlier_amount: Optional[Decimal]
    average_drg_length_of_stay: Optional[condecimal(ge=Decimal("0.0"))]
    total_discharge_count: Optional[condecimal(ge=Decimal("0.0"))]
    total_cost_report_day_count: Optional[condecimal(ge=Decimal("0.0"))]
    total_covered_day_count: Optional[condecimal(ge=Decimal("0.0"))]
    total_covered_day_count: Optional[condecimal(ge=Decimal("0.0"))]
    total_noncovered_day_count: Optional[condecimal(ge=Decimal("0.0"))]
    total_msp_passthrough_amount: Optional[Decimal]
    average_drg_weight: Optional[condecimal(ge=Decimal("0.0"))]
    total_pps_capital_fsp_drg_amount: Optional[Decimal]
    total_pps_capital_hsp_drg_amount: Optional[Decimal]
    total_pps_dsh_drg_amount: Optional[Decimal]


class Ts3Segment(X12Segment):
    """
    Provider summary information
    Example:
        TS3*123456*11*20021031*10*130957.66~
    """

    segment_name: X12SegmentName = X12SegmentName.TS3
    provider_identifier: str = Field(min_length=1, max_length=50)
    facility_type_code: str = Field(min_length=1, max_length=2)
    fiscal_period_date: Union[str, datetime.date]
    total_claim_count: conint(ge=0)
    total_claim_charge_amount: Decimal
    monetary_amount_1: Optional[Decimal]
    monetary_amount_2: Optional[Decimal]
    monetary_amount_3: Optional[Decimal]
    monetary_amount_4: Optional[Decimal]
    monetary_amount_5: Optional[Decimal]
    monetary_amount_6: Optional[Decimal]
    monetary_amount_7: Optional[Decimal]
    total_msp_payer_amount: Optional[Decimal]
    monetary_amount_8: Optional[Decimal]
    total_non_lab_charge_amount: Optional[Decimal]
    monetary_amount_9: Optional[Decimal]
    total_hcpcs_reported_charge_amount: Optional[Decimal]
    total_hcpcs_payable_amount: Optional[Decimal]
    monetary_amount_10: Optional[Decimal]
    total_professional_component_amount: Optional[Decimal]
    total_msp_patient_liability_met_amount: Optional[Decimal]
    total_patient_reimbursement_amount: Optional[Decimal]
    total_pip_claim_count: Optional[condecimal(ge=Decimal("0.0"))]
    total_pip_adjustment_amount: Optional[Decimal]

    _validate_fiscal_period_date = field_validator("fiscal_period_date")(parse_x12_date)


# load segment classes into a lookup table indexed by segment name
SEGMENT_LOOKUP: Dict = {}

cached_attrs = [v for v in globals().values()]

for a in cached_attrs:
    if hasattr(a, "x12") and a.__name__ != "X12Segment":
        # clean up the string representation to limit it to the 2 - 3 character segment name
        # use pydantic metadata to grab the default value assigned to segment_name
        # this value is X12SegmentName[SegmentCode]
        segment_key: str = str(a.__fields__["segment_name"].default).replace(
            "X12SegmentName.", ""
        )
        SEGMENT_LOOKUP[segment_key] = a
