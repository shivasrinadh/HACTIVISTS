def _to_float(value, field_name):
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid number.") from exc


def _to_int(value, field_name):
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid integer.") from exc


def prepare_features_from_form(form_data: dict):
    claimant_name = form_data.get("claimant_name", "").strip()
    claim_type = form_data.get("claim_type", "").strip()
    incident_date = form_data.get("incident_date", "").strip()

    if not claimant_name:
        raise ValueError("Claimant name is required.")
    if not claim_type:
        raise ValueError("Claim type is required.")
    if not incident_date:
        raise ValueError("Incident date is required.")

    claim_amount = _to_float(form_data.get("claim_amount"), "Claim amount")
    age_of_policy_days = _to_int(
        form_data.get("age_of_policy_days"), "Policy age in days"
    )
    previous_claims = _to_int(
        form_data.get("number_of_previous_claims"), "Number of previous claims"
    )
    location_risk_score = _to_float(
        form_data.get("location_risk_score"), "Location risk score"
    )
    police_report_filed = _to_int(
        form_data.get("police_report_filed"), "Police report filed"
    )
    witnesses = _to_int(form_data.get("witnesses"), "Witness count")

    if claim_amount <= 0:
        raise ValueError("Claim amount must be greater than zero.")
    if age_of_policy_days < 0:
        raise ValueError("Policy age cannot be negative.")
    if previous_claims < 0:
        raise ValueError("Number of previous claims cannot be negative.")
    if witnesses < 0:
        raise ValueError("Witness count cannot be negative.")
    if not 0 <= location_risk_score <= 1:
        raise ValueError("Location risk score must be between 0 and 1.")
    if police_report_filed not in (0, 1):
        raise ValueError("Police report filed must be 0 (No) or 1 (Yes).")

    return {
        "claim_amount": claim_amount,
        "age_of_policy_days": age_of_policy_days,
        "number_of_previous_claims": previous_claims,
        "location_risk_score": location_risk_score,
        "police_report_filed": police_report_filed,
        "witnesses": witnesses,
    }
