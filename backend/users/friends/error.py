from enum import Enum


class FriendError(Enum):
    EMPTY_ID = "Target user ID is required"
    INVALID_REQUEST = "Invalid request"
    DOES_NOT_EXIST = "Friendship does not exist"
    ALREADY_FRIENDS = "Users are already friends"
