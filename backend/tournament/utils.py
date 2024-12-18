from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Min, Max
from django.db import transaction
from django.utils import timezone

from .models import (
    Tournament,
    TournamentMatchParticipants,
    TournamentParticipant,
    TournamentGame,
)
from pingpong_history.models import PingPongHistory, PingPongRound

User = get_user_model()


def build_event_data(tournament_id):
    # Tournament 가져오기
    tournament = Tournament.objects.get(tournament_id=tournament_id)

    # eventType: 여기선 Tournament 이므로 "tournament"로 가정
    event_type = "tournament"

    # 해당 Tournament와 연결된 TournamentGame 조회
    games = TournamentGame.objects.filter(tournament_id=tournament)

    # PingPongHistory와 join해서 시작/끝 시간 조회
    # matches 데이터 생성
    matches_data = []

    # 전체 startDate/endDate 계산을 위해 min(started_at), max(ended_at) 추출
    # 여기서는 단순히 모든 게임 히스토리의 최소 시작, 최대 종료를 사용
    # ended_at이 null일 수도 있으니 coalesce 필요할 수 있음
    start_end_info = TournamentGame.objects.filter(tournament_id=tournament).aggregate(
        min_start=Min('game_id__started_at'),
        max_end=Max('game_id__ended_at')
    )
    overall_start = start_end_info['min_start']
    overall_end = start_end_info['max_end']

    for game in games:
        history = game.game_id  # OneToOneField -> PingPongHistory 객체
        # round명: "{user1.username} vs {user2.username}"
        # user1, user2 존재 가정
        user1 = history.user1
        user2 = history.user2

        round_name = f"{user1.username if user1 else 'Unknown'} vs {user2.username if user2 else 'Unknown'}"

        # 승패 판단: history.winner
        # player 정보 구성
        # user1_score, user2_score 사용
        # winner와 비교해서 status 설정
        player_list = []
        if user1:
            player1_status = None
            if history.winner:
                if history.winner == user1:
                    player1_status = "winner"
                else:
                    player1_status = "loser"
            # draw인 경우 둘다 'draw'라 가정하려면 score 동일 시 draw 판단
            if history.user1_score is not None and history.user2_score is not None:
                if history.user1_score == history.user2_score:
                    player1_status = "draw"
            player_list.append({
                "playerId": user1.id,
                "name": user1.username,
                "score": history.user1_score if history.user1_score is not None else 0,
                "status": player1_status
            })
        if user2:
            player2_status = None
            if history.winner:
                if history.winner == user2:
                    player2_status = "winner"
                else:
                    player2_status = "loser"
            # draw 판단
            if history.user1_score is not None and history.user2_score is not None:
                if history.user1_score == history.user2_score:
                    player2_status = "draw"
            player_list.append({
                "playerId": user2.id,
                "name": user2.username,
                "score": history.user2_score if history.user2_score is not None else 0,
                "status": player2_status
            })

        # 만약 user2가 없거나(예: PVE)라면 player_list에 1명만 들어갈 수도 있음
        # startTime, endTime은 history의 started_at, ended_at
        matches_data.append({
            "matchId": history.id,
            "round": round_name,
            "startTime": history.started_at,
            "endTime": history.ended_at,
            "players": player_list
        })

    # eventId = tournament_id
    event_data = {
        "eventId": tournament_id,
        "eventType": event_type,
        "startDate": overall_start,
        "endDate": overall_end,
        "matches": matches_data
    }

    return event_data


@transaction.atomic
def create_tournament(user1: User, user2: User, user3: User, user4: User) -> Tournament:
    """
    4인의 참가자로 토너먼트를 생성하고 Tournament, TournamentMatchParticipants, TournamentParticipant를 기록.
    초기 상태: current_round=0, pending 상태.
    """
    tournament = Tournament.objects.create(
        status='pending',
        current_round=0
    )
    TournamentMatchParticipants.objects.create(
        tournament=tournament,
        user1=user1,
        user2=user2,
        user3=user3,
        user4=user4
    )
    # 참가자 정보 기록
    for u in [user1, user2, user3, user4]:
        TournamentParticipant.objects.create(user=u, tournament=tournament, is_ready=False)

    return tournament


@transaction.atomic
def start_round(tournament: Tournament, round_number: int):
    """
    라운드를 시작하는 함수.
    round_number:
      1: user1 vs user2 경기를 시작
      2: user3 vs user4 경기를 시작
      3: round_1_winner vs round_2_winner 경기를 시작
    """
    participants = TournamentMatchParticipants.objects.get(tournament=tournament)

    if round_number == 1:
        # user1 vs user2 경기 생성
        create_game_and_history(tournament, round_number, participants.user1, participants.user2)
        tournament.current_round = 1
        tournament.status = 'ongoing'
        tournament.save()

    elif round_number == 2:
        # user3 vs user4 경기 생성
        create_game_and_history(tournament, round_number, participants.user3, participants.user4)
        tournament.current_round = 2
        tournament.status = 'ongoing'
        tournament.save()

    elif round_number == 3:
        # round_1_winner vs round_2_winner 경기를 시작
        if not tournament.round_1_winner or not tournament.round_2_winner:
            raise ValueError("Winners for round 1 and 2 are not set.")

        create_game_and_history(tournament, round_number, tournament.round_1_winner, tournament.round_2_winner)
        tournament.current_round = 3
        tournament.status = 'ongoing'
        tournament.save()
    else:
        raise ValueError("Invalid round number.")


def create_game_and_history(tournament: Tournament, round_number: int, user1: User, user2: User):
    """
    PingPongHistory와 TournamentGame을 생성하는 헬퍼 함수
    """
    history = PingPongHistory.objects.create(
        user1=user1,
        user2=user2,
        gamemode='PVP',
        started_at=timezone.now()
    )

    TournamentGame.objects.create(
        game_id=history,
        tournament_id=tournament,
        tournament_round=round_number,
        user_1=user1,
        user_2=user2,
        status='ongoing',
    )


@transaction.atomic
def finish_game(game_id: int, user1_score: int, user2_score: int):
    """
    경기가 끝났을 때 점수와 승자를 반영하는 함수.
    round_number에 따라 round_1_winner, round_2_winner, round_3_winner 설정.
    """
    history = PingPongHistory.objects.select_for_update().get(id=game_id)
    t_game = TournamentGame.objects.select_for_update().get(game_id=history)

    # 점수 반영
    history.user1_score = user1_score
    history.user2_score = user2_score
    history.ended_at = timezone.now()

    # 승자 결정
    # 패자, 무승부는 TournamentParticipant에서 삭제
    if user1_score > user2_score:
        winner = history.user1
        TournamentParticipant.objects.filter(user=history.user2, tournament=t_game.tournament_id).delete()
    elif user2_score > user1_score:
        winner = history.user2
        TournamentParticipant.objects.filter(user=history.user1, tournament=t_game.tournament_id).delete()
    else:
        # 무승부 처리 (둘 다 draw 상태)
        winner = None
        TournamentParticipant.objects.filter(user=history.user1, tournament=t_game.tournament_id).delete()
        TournamentParticipant.objects.filter(user=history.user2, tournament=t_game.tournament_id).delete()

    history.winner = winner
    history.save()

    t_game.winner = winner
    t_game.status = 'finished'
    t_game.ended_at = timezone.now()
    t_game.save()

    # 토너먼트 우승자 필드 업데이트
    tournament = t_game.tournament_id
    round_number = t_game.tournament_round

    if round_number == 1:
        # round1 경기 결과 -> round_1_winner 세팅
        tournament.round_1_winner = winner
    elif round_number == 2:
        # round2 경기 결과 -> round_2_winner 세팅
        tournament.round_2_winner = winner
    elif round_number == 3:
        # round3 경기 결과 -> round_3_winner 세팅, 토너먼트 종료
        tournament.round_3_winner = winner
        tournament.status = 'finished'

    tournament.save()


@transaction.atomic
def check_and_advance_round(tournament: Tournament):
    """
    현재 라운드 상태를 체크하고 다음 라운드를 진행할지 결정하는 함수.
    라운드 구조:
      - round1 끝나면 round1_winner 결정
      - round2 끝나면 round2_winner 결정
      - round1, round2 모두 끝나면 round3 시작
      - round3 끝나면 토너먼트 종료
    """
    # 현재 라운드 확인
    # round 1 완료되면 round_1_winner가 설정됨
    # round 2 완료되면 round_2_winner가 설정됨
    # 둘 다 설정되면 round 3 시작

    if tournament.current_round == 1:
        # round_1_winner가 설정되어 있고 round_2_winner가 아직 없으면 round2 시작
        if tournament.round_1_winner and not tournament.round_2_winner:
            start_round(tournament, 2)

    elif tournament.current_round == 2:
        # round_2_winner 설정 완료 시 round3 시작
        if tournament.round_1_winner and tournament.round_2_winner:
            start_round(tournament, 3)

    elif tournament.current_round == 3:
        # round_3_winner까지 설정되면 토너먼트 종료
        if tournament.round_3_winner:
            tournament.status = 'finished'
            tournament.save()


@transaction.atomic
def create_pingpong_round(history: PingPongHistory, rally: int, start: datetime, end: datetime,
                          user1_score: int, user2_score: int):
    """
    PingPongRound 생성하는 함수
    """
    PingPongRound.objects.create(
        match=history,
        rally=rally,
        start=start,
        end=end,
        user1_score=user1_score,
        user2_score=user2_score,
    )
