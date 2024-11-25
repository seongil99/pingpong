from .models import PingPongHistory


def end_game(user1, user2, user1_score, user2_score, gamemode, started_at, ended_at):
    if user1_score < 0 or user2_score < 0:
        raise ValueError("점수는 0 이상이어야 합니다.")
    if not isinstance(user1_score, int) or not isinstance(user2_score, int):
        raise ValueError("점수는 정수여야 합니다.")

    if user1_score > user2_score:
        winner = user1
    elif user2_score > user1_score:
        winner = user2
    else:
        winner = None  # 무승부 처리

    game_record = PingPongHistory.objects.create(
        user1=user1,
        user2=user2,
        winner=winner,
        user1_score=user1_score,
        user2_score=user2_score,
        gamemode=gamemode,
        started_at=started_at,
        ended_at=ended_at
    )
    return game_record
