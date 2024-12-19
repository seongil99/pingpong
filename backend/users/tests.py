from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.management import call_command

from pingpong_history.models import PingPongHistory
from tournament.models import TournamentGame, Tournament, TournamentMatchParticipants
from .models import User


class MyProfileTestCase(APITestCase):
    def setUp(self):
        call_command('migrate', verbosity=0)
        self.user = User.objects.create_user(
            email="seonyoon@student.42seoul.kr",
            password="1234",
            username="seonyoon",
            is_verified=False,
            avatar=None,
        )
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('my-profile')

    def test_my_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['is_verified'], self.user.is_verified)

    def test_update_my_profile(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        avatar = SimpleUploadedFile(
            name="avatar.jpg",
            content=b'\x47\x49\x46\x38\x37\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x0A\x00\x01\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3B',
            content_type="image/jpeg"
        )
        data = {
            'username': 'seonyoon2',
            'is_verified': True,
            'avatar': avatar,
        }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['is_verified'], data['is_verified'])
        self.assertIsNotNone(response.data['avatar'])


class MyCurrentGameViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email="test@test.com")
        self.url = reverse('current-game')

        # opponent for normal games or tournaments
        self.opponent = User.objects.create_user(username='opponent', password='opppass', email="test1@test.com")
        self.user3 = User.objects.create_user(username='user3', password='user3pass', email="test3@test.com")
        self.user4 = User.objects.create_user(username='user4', password='user4pass', email="test4@test.com")

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_no_game_returns_204(self):
        # 인증 후 게임 없이 조회 시도
        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_tournament_game_pending(self):
        tournament = Tournament.objects.create(
            status='pending',
            current_round=0
        )
        tournament_participants = TournamentMatchParticipants.objects.create(
            tournament=tournament,
            user1=self.user,
            user2=self.opponent,
            user3=self.user3,
            user4=self.user4
        )

        # PingPongHistory 생성 시 명시적으로 save()
        game_history = PingPongHistory(
            user1=self.user,
            user2=self.opponent,
            winner=None,
            ended_at=None,
            gamemode='tournament',
            tournament_id=tournament,
        )
        game_history.save()

        # TournamentGame 생성
        t_game = TournamentGame.objects.create(
            game_id=game_history,
            tournament_id=tournament,
            tournament_round=0,
            user_1=self.user,
            user_2=self.opponent,
            status='pending'
        )

        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['game_id'], game_history.id)
        self.assertEqual(data['tournament_id'], tournament.tournament_id)
        self.assertEqual(data['status'], 'pending')
        self.assertEqual(data['round'], 0)

    def test_tournament_game_ongoing(self):
        tournament = Tournament.objects.create(
            status='ongoing',
            current_round=1
        )

        tournament_participants = TournamentMatchParticipants.objects.create(
            tournament=tournament,
            user1=self.user,
            user2=self.opponent,
            user3=self.user3,
            user4=self.user4
        )
        tournament_participants.save()

        # PingPongHistory도 마찬가지로 명시적 save()
        game_history = PingPongHistory(
            user1=self.user,
            user2=self.opponent,
            winner=None,
            ended_at=None,
            gamemode='tournament',
            tournament_id=tournament,
        )
        game_history.save()

        t_game = TournamentGame.objects.create(
            game_id=game_history,
            tournament_id=tournament,
            tournament_round=1,
            user_1=self.user,
            user_2=self.opponent,
            status='ongoing'
        )

        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['game_id'], game_history.id)
        self.assertEqual(data['tournament_id'], tournament.tournament_id)
        self.assertEqual(data['status'], 'ongoing')
        self.assertEqual(data['round'], 1)

    def test_normal_game_pending(self):
        normal_game = PingPongHistory(
            user1=self.user,
            user2=None,
            winner=None,
            ended_at=None,
            gamemode='1v1'
        )
        normal_game.save()

        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['game_id'], normal_game.id)
        self.assertEqual(data['tournament_id'], None)
        self.assertEqual(data['status'], 'pending')
        self.assertEqual(data['round'], None)

    def test_normal_game_ongoing(self):
        normal_game = PingPongHistory(
            user1=self.user,
            user2=self.opponent,
            winner=None,
            ended_at=None,
            gamemode='1v1'
        )
        normal_game.save()

        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['game_id'], normal_game.id)
        self.assertEqual(data['tournament_id'], None)
        self.assertEqual(data['status'], 'ongoing')
        self.assertEqual(data['round'], None)

    def test_tournament_exists_but_no_tournamentgame(self):
        tournament = Tournament.objects.create(
            status='ongoing',
            current_round=1
        )
        tournament.save()

        tournament_participants = TournamentMatchParticipants.objects.create(
            tournament=tournament,
            user1=self.user,
            user2=self.opponent,
            user3=self.user3,
            user4=self.user4
        )
        tournament_participants.save()
        # TournamentGame 없음

        self.authenticate()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
