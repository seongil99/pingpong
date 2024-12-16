{
  "eventId": 1,
  "eventType": "tournament",         // "tournament" 또는 "match"
  "startDate": "2024-01-15T14:00:00Z",
  "endDate": "2024-01-20T18:00:00Z",
  "matches": [
    {
      "matchId": 101,
      "round": "PalyerOne vs PlayerTwo",     // 라운드 이름 (ex nickname vs nickname)
      "startTime": "2024-01-15T16:00:00Z",
      "endTime": "2024-01-15T17:30:00Z",
      "players": [
        {
          "playerId": 1,
          "name": "PlayerOne",
          "score": 3,
          "status": "winner"         // 승자/패자 여부 draw 면 양쪽다 draw
        },
        {
          "playerId": 2,
          "name": "PlayerTwo",
          "score": 1,
          "status": "loser"
        }
      ]
    },
    {
      "matchId": 102,
      "round": "PalyerThree vs PlayerFour",
      "startTime": "2024-01-15T18:00:00Z",
      "endTime": "2024-01-15T18:10:00Z",
      "players": [
        {
          "playerId": 3,
          "name": "PlayerThree",
          "score": 2
        },
        {
          "playerId": 4,
          "name": "PlayerFour",
          "score": 3
        }
      ]
    }
  ]
}
