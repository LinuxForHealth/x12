"""
loops.py

Models the loops, or logical segment groupings, for the HealthCare Claims Professional 837 005010X222A2 transaction set.
The HealthCare Claims Professional set organizes loops into a hierarchical and nested model.

-- Header
    -- Loop 1000A (Submitter Name)
        -- Loop 1000B (Receiver Name)
    -- Loop 2000A (Billing Provider)
        -- Loop 2010AA (Billing Provider Name)
        -- Loop 2010AB (Pay to Address)
        -- Loop 2010AC (Pay to Plan Name)
        -- Loop 2000B (Subscriber)
            -- Loop 2010BA (Subscriber Name)
            -- Loop 2010BB (Payer Name)
            -- Loop 2300 (Claim Information)
                -- Loop 2310A (Referring Provider Name)
                -- Loop 2310B (Rendering Provider Name)
                -- Loop 2310C (Service Facility Location Name)
                -- Loop 2310D (Supervising Provider Name)
                -- Loop 2310E (Ambulance Pickup Location)
                -- Loop 2310F (Ambulance Dropoff Location)
                -- Loop 2320 (Other Subscriber Information)
                    -- Loop 2330A (Other Subscriber Name)
                    -- Loop 2330B (Other Payer Name)
                    -- Loop 2330C (Other Payer Referring Provider Name)
                    -- Loop 2330D (Other Payer Rendering Provider Name)
                    -- Loop 2330E (Other Payer Service Facility Location)
                    -- Loop 2330F (Other Payer Supervising Provider Name)
                    -- Loop 2330G (Other Payer Billing Provider Name)
                -- Loop 2400 (Service Line)
                    -- Loop 2410 (Drug Identification Name)
                    -- Loop 2420A (Rendering Provider Name)
                    -- Loop 2420B (Purchased Service Provider Name)
                    -- Loop 2420C (Service Facility Location Name)
                    -- Loop 2420D (Supervising Provider Name)
                    -- Loop 2420E (Ordering Provider Name)
                    -- Loop 2420F (Referring Provider Name)
                    -- Loop 2420G (Ambulance Pickup Location)
                    -- Loop 2420H (Ambulance Dropoff Location)
                    -- Loop 2430 (Line Adjudication Information)
                    -- Loop 2440 (Form Identification)
            -- Loop 2000C (Patient Loop)
                -- Loop 2010CA (Patient Name)
                -- Loop 2300 (Claim Information)
-- Footer

The Header and Footer components are not "loops" per the specification, but are included to standardize and simplify
transactional modeling and processing.
"""
