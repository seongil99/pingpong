import NavBar from "../Components/Navbar.js";

class MatchingPage {
  constructor() {
    this.socket = null;
    this.isMatching = false;
    this.container = null;
    this.requestMatchButton = null;
    this.cancelMatchButton = null;
    this.statusDiv = null;
  }

  async template() {
    this.container = document.createElement("div");

    // 네비게이션 바 추가
    const navBarContainer = document.createElement("div");
    navBarContainer.innerHTML = NavBar;
    this.container.appendChild(navBarContainer);

    // 제목 추가
    const title = document.createElement("h2");
    title.id = "h2";
    title.textContent = "Matching Page";
    this.container.appendChild(title);

    // 매칭 요청 버튼 생성
    this.requestMatchButton = document.createElement("button");
    this.requestMatchButton.id = "requestMatchButton";
    this.requestMatchButton.textContent = "매칭 요청";
    this.container.appendChild(this.requestMatchButton);

    // 매칭 취소 버튼 생성
    this.cancelMatchButton = document.createElement("button");
    this.cancelMatchButton.id = "cancelMatchButton";
    this.cancelMatchButton.textContent = "매칭 취소";
    this.cancelMatchButton.disabled = true; // 초기에는 비활성화
    this.container.appendChild(this.cancelMatchButton);

    // 상태 표시 영역 생성
    this.statusDiv = document.createElement("div");
    this.statusDiv.id = "status";
    this.container.appendChild(this.statusDiv);

    // 이벤트 리스너 및 웹소켓 설정
    this.setupEventListeners();

    return this.container;
  }

  setupEventListeners() {
    // 이벤트 핸들러에서의 'this' 바인딩을 위해 화살표 함수를 사용합니다.

    // 매칭 요청 버튼 클릭 이벤트
    this.requestMatchButton.addEventListener("click", () => {
      if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
        this.connectWebSocket(() => {
          // 연결 후 매칭 요청을 보냅니다.
          this.requestMatch();
        });
      } else {
        this.requestMatch();
      }
    });

    // 매칭 취소 버튼 클릭 이벤트
    this.cancelMatchButton.addEventListener("click", () => {
      this.cancelMatch();
    });

    // 페이지를 떠날 때 웹소켓 연결 종료
    window.addEventListener("beforeunload", () => {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.close();
      }
    });
  }

  connectWebSocket(callback) {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const wsUrl = `${protocol}://${window.location.host}/api/ws/matchmaking/`;
    this.socket = new WebSocket(wsUrl);

    this.socket.onopen = () => {
      console.log("WebSocket 연결이 열렸습니다.");
      this.statusDiv.textContent = "서버와 연결되었습니다.";
      if (callback) callback();
    };

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("수신한 데이터:", data);

      if (data.type === "waiting_for_match") {
        this.statusDiv.textContent = "상대를 기다리는 중...";
        this.isMatching = true;
        this.requestMatchButton.disabled = true;
        this.cancelMatchButton.disabled = false;
      } else if (data.type === "match_found") {
        this.statusDiv.textContent = `매칭 성공! 상대방: ${data.opponent_username}`;
        this.isMatching = false;
        this.requestMatchButton.disabled = false;
        this.cancelMatchButton.disabled = true;
        const gameUrl = "/api/static/public/index.html";
        const gameId = data.game_id;
        window.location.href = `${gameUrl}?gameId=${gameId}`;
      } else if (data.type === "match_canceled") {
        this.statusDiv.textContent = "매칭이 취소되었습니다.";
        this.isMatching = false;
        this.requestMatchButton.disabled = false;
        this.cancelMatchButton.disabled = true;
      } else if (data.type === "error") {
        this.statusDiv.textContent = `에러 발생: ${data.message}`;
        this.isMatching = false;
        this.requestMatchButton.disabled = false;
        this.cancelMatchButton.disabled = true;
      }
    };

    this.socket.onclose = (event) => {
      console.log("WebSocket 연결이 닫혔습니다.", event);
      this.statusDiv.textContent = "서버와의 연결이 끊어졌습니다.";
      this.isMatching = false;
      this.requestMatchButton.disabled = false;
      this.cancelMatchButton.disabled = true;
    };

    this.socket.onerror = (error) => {
      console.error("WebSocket 에러 발생:", error);
    };
  }

  requestMatch() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      const message = {
        type: "request_match",
        gamemode: "1v1", // 필요한 게임 모드로 설정
      };
      this.socket.send(JSON.stringify(message));
      console.log("매칭 요청을 보냈습니다:", message);
    } else {
      console.error("WebSocket이 연결되지 않았습니다.");
    }
  }

  cancelMatch() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      const message = {
        type: "cancel_match",
      };
      this.socket.send(JSON.stringify(message));
      console.log("매칭 취소를 보냈습니다:", message);
    } else {
      console.error("WebSocket이 연결되지 않았습니다.");
    }
  }
}

export default MatchingPage;
