from enum import Enum

class FriendError(Enum):
    EMPTY_ID = "Target user ID is required"
    REQUEST_ALREADY_SENT = "Friend request already sent"
    ALREADY_FRIENDS = "You are already friends :)"
    INVALID_REQUEST = "Invalid request"