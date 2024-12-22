import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import ButtonToMatch from "../Components/ButtonToMatch.js";
import getCurrentUserGameStatus from "../Controller/Game/GetCurrentUserGameStatus.js";
import CreateFormSwitch from "../Components/CheckBox.js";

/**
 * 하나로 통합된 모달 생성 함수
 * - message: 모달에 보여줄 안내 문구
 * - onClose: 모달 닫기 버튼 클릭 시 실행할 콜백
 * - socket: 필요 시 소켓을 넘겨받아 추가 처리 가능
 */
function createMessageModal(message, onClose, socket) {
  // 모달 제목
  const modalTitle = createElement(
    "div",
    { class: "modal-title",
        id: "modal-title-content"
     },
    createElement("h5", {}, "잠시만 기다려 주세요.")
  );

  // 모달 본문
  const modalBody = createElement(
    "div",
    {
      id: "modal-body-target", 
      class: "modal-body",
    },
    createElement("p", {}, message)
  );

  // 닫기 버튼
  const btnClose = createElement(
    "button",
    {
      id: "modal-btn-target",
      type: "button",
      class: "btn btn-secondary",
      "data-bs-dismiss": "modal",
      events: {
        click: () => {
          // 모달 닫기 로직
          modalInstance.dispose(); // Bootstrap 모달 인스턴스 dispose
          if (modal.parentElement) {
            modal.parentElement.removeChild(modal);
          }
          // 추가 콜백
          onClose?.();
        },
      },
    },
    "Close"
  );

  // 모달 푸터
  const modalFooter = createElement(
    "div",
    { class: "modal-footer" },
    btnClose
  );

  // 모달 콘텐츠 (커스텀 체크박스/스위치 포함)
  const modalContent = createElement(
    "div",
    { class: "modal-content" },
    modalTitle,
    modalBody,
    modalFooter,
    CreateFormSwitch(socket) // 필요 시 소켓 관련 폼
  );

  // 모달 다이얼로그
  const modalDialog = createElement(
    "div",
    { class: "modal-dialog modal-static" }, // backdrop 닫기/ESC 비활성화를 위한 static
    modalContent
  );

  // 최종 모달 컨테이너
  const modal = createElement(
    "div",
    {
      id: "modal-tartget",
      class: "modal",
      tabindex: "-1",
    },
    modalDialog
  );

  // Bootstrap 모달 인스턴스
  const modalInstance = new bootstrap.Modal(modal, {
    backdrop: "static", // 배경 클릭 비활성화
    keyboard: false,    // ESC 키 입력 비활성화
  });

  return { element: modal, modal: modalInstance };
}

class MatchingPage {
  constructor(pathParam, queryParam) {
    // 필요한 상태값 정의
    this.socket = null;
    this.container = null;
    this.waitModal = null;       // 모달 보관
    this.matchType = null;
    this.tournamentId = null;
    this.gameId = null;
  }

  /**
   * 페이지 렌더 함수
   */
  async template() {
    const navBar = NavBar();
    const title = createElement(
      "h2",
      { id: "matching-page-title" },
      "Matching Page"
    );

    // 여러 매칭 버튼 준비
    const pvpButton = this.createMatchButton("PVP", "waiting for PvP User");
    const tournamentButton = this.createMatchButton(
      "tournament",
      "waiting for Tournament Users"
    );
    const pveButton = this.createMatchButton("Pve", "waiting for start");

    const buttonContainer = createElement(
      "div",
      { id: "match-btn-container" },
      pvpButton,
      tournamentButton,
      pveButton
    );

    const main = createElement(
      "main",
      { id: "matching-main" },
      title,
      buttonContainer
    );
    this.container = createElement("div", {}, navBar, main);

    return this.container;
  }

  /**
   * 매칭 버튼 하나를 만드는 유틸 함수
   */
  createMatchButton(type, waitMessage) {
    return ButtonToMatch(type, async () => {
      this.matchType = type;

      // PVE는 소켓 없이 바로 처리
      if (this.matchType === "Pve") {
        localStorage.setItem("matchType", this.matchType);
        this.toggleButtonContainer();
        this.showWaitModal(waitMessage, () => {
          // Close 시 처리 로직
          this.toggleButtonContainer();
          localStorage.setItem("matchType", "");
          localStorage.setItem("tid", "");
          localStorage.setItem("gameId", "");
        });
        // 곧바로 handleMatchFound("Pve")
        this.handleMatchFound("Pve");
        return;
      }

      // PVP나 tournament의 경우 웹소켓 연결 후 요청
      if (!this.socket || this.socket.readyState === WebSocket.CLOSED) {
        this.connectWebSocket(() => this.requestMatch());
      } else {
        this.requestMatch();
      }
      this.toggleButtonContainer();

      // 모달 띄우기
      this.showWaitModal(waitMessage, () => {
        // Close 시 처리 로직
        this.cancelMatch();
        this.toggleButtonContainer();
      });
    });
  }

  /**
   * 모달(대기창) 띄우는 함수
   * - 메시지 표시
   * - 닫기 버튼 누르면 onClose 콜백
   */
  showWaitModal(message, onClose) {
    // 이미 모달이 떠 있으면 제거
    if (this.waitModal?.element && this.container?.contains(this.waitModal.element)) {
      this.waitModal.modal.dispose();
      this.container.removeChild(this.waitModal.element);
      this.waitModal = null;
    }

    // 새 모달 생성
    const waitBox = createMessageModal(message, onClose, this.socket);
    // DOM에 추가 후 show()
    this.container.append(waitBox.element);
    waitBox.modal.show();
    // 추후 dispose 위해 보관
    this.waitModal = waitBox;
  }

  toggleButtonContainer() {
    document.getElementById("match-btn-container")?.classList.toggle("hide");
  }

  /**
   * 웹소켓 연결 함수
   */
  connectWebSocket(callback) {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const endpoint =
     this.matchType === "PVP" ? "matchmaking" : "tournament/matchmaking";
    const wsUrl = `${protocol}://${window.location.host}/api/ws/${endpoint}/`;
    try{
        this.socket = new WebSocket(wsUrl);
    }
    catch{
        this.socket = null;
        console.log("soket open error");
        const title = document.getElementById("modal-body-target");
        const bodymsg = document.getElementById("modal-title-content");
        title.textContent = "소켓생성 에러";
        bodymsg.textContent =  "close 하시고 다시 시도해 주세요";
    }
    if (!this.socket) return;
    this.socket.onopen = () => {
      console.log("WebSocket connected.");
      callback?.();
    };

    this.socket.onmessage = (event) => this.handleSocketMessage(event);
    // this.socket.onclose = (event) => this.handleSocketClose(event);
    this.socket.onclose = () => console.log("WebSocket closed!");
    this.socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        this.socket = null;
        console.log("soket open error");
        const title = document.getElementById("modal-body-target");
        if(title)
            title.textContent = "소켓생성 에러";
        const bodymsg = document.getElementById("modal-title-content");
        if(bodymsg)
            bodymsg.textContent =  "close 하시고 다시 시도해 주세요";
    };
  }

  /**
   * 소켓 메시지 수신 핸들러
   */
  handleSocketMessage(event) {
    const data = JSON.parse(event.data);
    console.log("Received data:", data);

    const messageHandlers = {
      waiting_for_match: () => console.log("Waiting for opponent..."),
      match_found: () => this.handleMatchFound(data),
      match_canceled: () => console.log("Match canceled."),
      error: () => console.error(`Error: ${data.message}`),
      set_option: () => this.navigateToGame(data.game_id),
      already_joined: () => this.navigateToGame(data.game_id),
      match_waiting: () => console.log("waiting for tounament"),
    };

    (
      messageHandlers[data.type] ||
      (() => console.warn("Unhandled message type:", data.type))
    )();
  }

  /**
   * 매칭 성공 시 처리
   * - PVE 문자열이 직접 넘어오는 경우도 있어, 그 경우 별도 처리
   */
  handleMatchFound(data) {
    // PVE
    
    // 일반 PVP or Tournament
    console.log("match_found:", data);
    // 모달 텍스트/버튼 숨기는 예시
    const modalBody = document.getElementById("modal-body-target");
    const modalBtn = document.getElementById("modal-btn-target");
    modalBody?.classList?.toggle("hide");
    modalBtn?.classList?.toggle("hide");
    if (data === "Pve") {
        
      const optionForm = document.getElementById("form-target");
      optionForm?.classList?.toggle("hide");
      console.log("PVE mode matched immediately");
      return;
    }

    // 옵션 선택 섹션이 있는 경우
    if (data.option_selector) {
      const optionForm = document.getElementById("form-target");
      optionForm?.classList?.toggle("hide");
      console.log("option selector open => this.tournamentId:", this.tournamentId);
    }

    localStorage.setItem("matchType", this.matchType);
    localStorage.setItem("gameId", data.game_id ? data.game_id : data.tournament_id);
    if(data.tournament_id){
        this.tournamentId = data.tournament_id;
        localStorage.setItem("tid", this.tournamentId);
    }
    console.log(`Match found! gameId: ${localStorage.getItem("gameId")}`);
  }

  /**
   * 매칭 완료 후 게임 페이지 이동
   */
  async navigateToGame(gameId) {
    const serverdgameId = await getCurrentUserGameStatus();
    if (!serverdgameId) {
      await window.router.navigate(`/playing/${gameId}`, false);
    } else {
      await window.router.navigate(`/playing/${serverdgameId.game_id}`, false);
    }
  }

  /**
   * 서버에 매칭 요청
   */
  requestMatch() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      const message = {
        type: "request_match",
        gamemode: this.matchType === "PVP" ? "1v1" : "tournament",
      };
      this.socket.send(JSON.stringify(message));
      console.log("Match request sent:", message);
    } else {
      console.error("WebSocket is not open.");
    }
  }

  /**
   * 매칭 취소
   */
  cancelMatch() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      const message = { type: "cancel_match" };
      console.log("cancel match 1", message);
      this.socket.send(JSON.stringify(message));
      console.log("cancel match 2", this.socket.readyState);
      this.socket.close();
      console.log("cancel match 2", this.socket.readyState);
      this.socket == null;
      console.log("cancel match 2", this.socket);
      console.log("Match cancel request sent:", message);
    } else {
      console.error("Failed to cancel match.");
    }
  }

  /**
   * 페이지 떠날 때 필요한 정리 로직
   * - 소켓 종료
   * - 모달 제거
   * - 기타 메모리 해제
   */
  dispose() {
    // 소켓 정리
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.close();
      this.socket = null;
    }

    // 모달 정리
    if (this.waitModal) {
      // Bootstrap Modal dispose
      if (this.waitModal.modal && typeof this.waitModal.modal.dispose === 'function') {
        console.log("modal dispose", this.waitModal.modal.dispose);
        this.waitModal.modal.dispose();
      }
      // DOM에서 제거
      if (
        this.waitModal.element &&
        this.container?.contains(this.waitModal.element)
      ) {
        this.container.removeChild(this.waitModal.element);
      }
      this.waitModal = null;
    }
  }
}

export default MatchingPage;
