import phonenumbers


def is_valid_phone(phone: str) -> bool:
    """True if `phone` is a real, plausible number with a country code (e.g. +201234567890)."""
    phone = (phone or "").strip()
    if not phone.startswith("+"):
        return False
    try:
        parsed = phonenumbers.parse(phone, None)
    except phonenumbers.NumberParseException:
        return False
    return phonenumbers.is_valid_number(parsed)
