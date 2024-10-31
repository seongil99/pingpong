from enum import Enum

class Detail(Enum):
    TOKEN_IS_VALID = "Token is valid."
    MFA_ENABLED = "2FA enabled."
    MFA_DISABLED = "2FA disabled."