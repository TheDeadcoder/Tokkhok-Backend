from typing import Optional
import re

#################################### Validation Helper Functions #############################################################
def validate_email(email: Optional[str]) -> Optional[str]:
    if not email:
        return None

    email_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
        r'|^"([^\\"]|\\.)+"'
        r')@([A-Z0-9-]+\.)+[A-Z]{2,}$', re.IGNORECASE)

    if re.match(email_regex, email):
        return email
    else:
        return "invalid"
