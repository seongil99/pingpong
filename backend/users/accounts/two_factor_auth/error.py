from enum import Enum

class Errors(Enum):
    INVALID_OTP = 'Invalid OTP code'
    NO_DEVICE = 'No unconfirmed device found for this user'