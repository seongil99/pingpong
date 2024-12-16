callback_schema = {
    "/api/v1/accounts/oauth2/fortytwo/login/callback/": {
        "post": {
            "operationId": "fortytwo_oauth2_login",
            "description": "42 OAuth2 로그인 엔드포인트입니다.",
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "description": "42 OAuth2 authorization code.",
                                },
                            },
                            "required": ["code"],
                        },
                    },
                },
            },
            "tags": ["Authentication"],
            "responses": {
                "200": {
                    "description": "로그인 성공",
                },
            },
        },
    },
}

matchmaking_schema = {
    "/api/ws/matchmaking/": {
        "get": {
            "operationId": "matchmaking_ws",
            "summary": "매치메이킹을 위한 WebSocket 연결",
            "description": """
이 엔드포인트는 매치메이킹을 위한 WebSocket 연결을 설정합니다.

### WebSocket 연결

WebSocket 클라이언트는 다음 URL로 연결해야 합니다:

`wss://localhost/api/ws/matchmaking/`

### 메시지 형식

**클라이언트 → 서버:**

- **매칭 요청**:

```json
{ "type": "request_match", "gamemode": "1v1" }
```
    
- **매칭 취소**:

```json
{ "type": "cancel_match" }
```
    
**서버 → 클라이언트:**

- **매칭 대기 중**:
    
```json
{ "type": "waiting_for_match" }
```
     
- **매칭 성공**:

```json
{ "type": "match_found", "opponent_id": 1, "opponent_username": "opponent" }
```
      
- **매칭 취소**:

```json
{ "type": "match_canceled" }
```
      
- **에러**:

```json
{ "type": "error", "message": "에러 메시지" }
```
      
### 예제
    
```json
{ "type": "request_match", "gamemode": "1v1" }
```
    
""",
            "tags": ["Matchmaking"],
            "servers": [{"url": "wss://localhost/"}],
            "responses": {
                "101": {"description": "Switching Protocols"},
                "400": {"description": "Bad Request"},
                "401": {"description": "Unauthorized"},
            },
        },
    },
}

tournament_matchmaking_schema = {
    "/api/ws/tournament/matchmaking/": {
        "get": {
            "operationId": "tournament_matchmaking_ws",
            "summary": "토너먼트 매치메이킹을 위한 WebSocket 연결",
            "description": """
이 엔드포인트는 토너먼트 매치메이킹을 위한 WebSocket 연결을 설정합니다.

### WebSocket 연결

WebSocket 클라이언트는 다음 URL로 연결해야 합니다:

`wss://localhost/api/ws/tournament/matchmaking/`

### 메시지 형식

**클라이언트 → 서버:**

- **매칭 요청**:

```json

{ "type": "request_match" }

```

- **매칭 취소**:

```json

{ "type": "cancel_match" }

```

**서버 → 클라이언트:**

- **매칭 대기 중**:

```json

{ "type": "match_waiting", "count": 1 }

```

- **매칭 성공**:

```json

{ "type": "match_found", "opponents": ["opponent1", "opponent2", "opponent3"], "tournament_id": 1 }

```

- **매칭 취소**:

```json

{ "type": "match_canceled" }

```

- **에러**:

```json

{ "type": "error", "message": "에러 메시지" }

```

### 예제

```json

{ "type": "request_match" }

```

""",
            "tags": ["Tournament"],
            "servers": [{"url": "wss://localhost/"}],
            "responses": {
                "101": {"description": "Switching Protocols"},
                "400": {"description": "Bad Request"},
                "401": {"description": "Unauthorized"},
            },
        },
    },
}

tournament_game_schema = {
    "/api/ws/tournament/game/{tournament_id}/": {
        "get": {
            "operationId": "tournament_game_ws",
            "summary": "토너먼트 게임을 위한 WebSocket 연결",
            "description": """
이 엔드포인트는 토너먼트 게임을 위한 WebSocket 연결을 설정합니다.

### WebSocket 연결

WebSocket 클라이언트는 다음 URL로 연결해야 합니다:

`wss://localhost/api/ws/tournament/game/{tournament_id}/`

### 메시지 형식

**클라이언트 → 서버:**

- **게임 준비**:

```json

{ "type": "ready" }

```

**서버 → 클라이언트:**

- **게임 시작**:

```json

{ "type": "game_started", "game_id": 1, "tournament_id": 1, "opponent": "opponent" }

```

- **에러**:
                
```json

{ "type": "error", "message": "에러 메시지" }

```
            
### 예제

```json

{ "type": "ready" }

```

""",
            "tags": ["Tournament"],
            "servers": [{"url": "wss://localhost/"}],
            "responses": {
                "101": {"description": "Switching Protocols"},
                "400": {"description": "Bad Request"},
                "401": {"description": "Unauthorized"},
            },
        },
    },
}
