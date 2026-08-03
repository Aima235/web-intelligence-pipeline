REQUIRED_FIELDS = [
    "company",
    "services",
    "technologies",
    "pain_points",
    "business_gaps",
    "candidate_match",
    "proposal"
]


def validate_schema(data):

    missing = []

    for field in REQUIRED_FIELDS:

        if field not in data:
            missing.append(field)

    return missing