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

- **옵션 선택**:

```json
{ "type": "set_option", "game_id": 1, "multi_ball": true }
```
    
**서버 → 클라이언트:**

- **매칭 대기 중**:
    
```json
{ "type": "waiting_for_match" }
```
     
- **매칭 성공**:

```json
{ "type": "match_found", "opponent_id": 1, "opponent_username": "opponent", "game_id": 1, "option_selector": true }
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

ingame_ws_schema = {
    "/api/game": {
        "get": {
            "operationId": "connect_game",
            "summary": "Ping Pong 게임 WebSocket 연결",
            "description": """
이 엔드포인트는 게임 클라이언트와 연결을 설정하고, 게임에 대한 인증 및 참여를 처리합니다.

### WebSocket 연결

WebSocket 클라이언트는 다음 URL로 연결해야 합니다:

`wss://example.com/api/game`

### 메시지 형식

**클라이언트 → 서버:**

- **연결 요청:**
```json
{
  "type": "connect",
  "gameId": "1234abcd",
}
```
auth 는 cookie 로

**서버 → 클라이언트: (data)**
- **render_data:**
```json
{
  "oneName": "minsepar",
  "twoName": "ai",
  "playerOne": {
    "x": -40,
    "y": 6,
    "z": 100
  },
  "playerTwo": {
    "x": 40,
    "y": 6,
    "z": -100
  },
  "balls": [
    {
      "id": 0,
      "position": {
        "x": 6.983907988413103,
        "y": 5,
        "z": 125.31975672627348
      },
      "velocity": {
        "x": -14.2151685776611,
        "y": 0,
        "z": 47.93671851836206
      },
      "summon_direction": true,
      "power_counter": 0,
      "radius": 5
    }
  ],
  "score": {
    "playerOne": 1,
    "playerTwo": 3
  },
}
```
- **게임 시작 알림 (gameStart):**
```json
{
  "type": "gameStart",
  { render_data }
}
```
- **점수 알림 (score):**
```json
{
  "type": "score"
  { render_data }
}
```
- **게임 대기 알림 (gameWait):**
```json
{
  "type": "gameWait",
}
```
- **게임 종료 알림 (gameEnd):**
```json
{
  "type": "gameEnd",
  "txt": "winner is ai"
}
```
- **두 번째 플레이어 입장 알림 (secondPlayer):**
```json
{
  "type": "secondPlayer",
}
```
**클라이언트 → 서버:**

- **키 입력 이벤트:**
```json
{
  "type": "keyPress",
  "key": " ",
  "pressed": true
}
```
**서버 → 클라이언트:**

- **게임 상태 (gameState):**
```json
{
  "type": "gameState"
  { render_data }
}

```

""",
            "tags": ["Game"],
            "servers": [{"url": "wss://example.com"}],
            "responses": {
                "101": {"description": "Switching Protocols"},
                "400": {"description": "Bad Request"},
                "401": {"description": "Unauthorized"},
                "404": {"description": "Game Not Found"},
            },
        },
    }
}

online_check_schema = {
    "/api/online-status/": {
        "get": {
            "tags": ["Online Status"],
            "operationId": "checkOnlineStatus",
            "description": """
1. **Connect**
   - **Purpose**: Establishes a WebSocket connection and marks the user as online if they are authenticated.
   - **Operation ID**: `connectOnlineStatus`
   - **Tags**: ["Online Status"]
   - **Responses**:
     - **101**: Indicates a successful protocol switch to WebSocket.
     - **401**: Indicates the user is unauthorized and not authenticated.

2. **Disconnect**
   - **Purpose**: Handles WebSocket disconnection and marks the user as offline if authenticated.
   - **Operation ID**: `disconnectOnlineStatus`
   - **Tags**: ["Online Status"]
   - **Responses**:
     - **200**: Confirms successful disconnection.

3. **Messages**
   - **Heartbeat**
     - **Purpose**: Receives a heartbeat message from the client to ensure the connection is active.
     - **Operation ID**: `receiveHeartbeatMessage`
     - **Tags**: ["Online Status"]
     - **Payload**:
       - **Type**: Object
       - **Properties**:
         - **type**: A string that specifies the type of message, restricted to the value `"heartbeat"`.
       - **Required Fields**:
         - `type`
     - **Responses**:
       - **200**: Acknowledges that the heartbeat message was received and processed successfully.

            """,
        }
    }
}
