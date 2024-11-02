from enum import Enum

class Error(Enum):
    USER_NOT_FOUND = "User not found."
    INVALID_OTP = "Invalid OTP."
    MFA_NOT_ENABLED = "2FA not enabled."
    NO_TOKEN_IN_COOKIE = "Token not found in cookies."
    ACCESS_DENIED = "Access denied."
    