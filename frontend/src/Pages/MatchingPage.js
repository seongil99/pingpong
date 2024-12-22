import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import ButtonToMatch from "../Components/ButtonToMatch.js";
import NavBar from "../Components/Common/Navbar.js";
import ButtonToMatch from "../Components/Matching/ButtonToMatch.js";
import WaitMatchBox from "../Components/Matching/WaitMatchBox.js";
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

    async template() {
        const navBar = NavBar();
        const title = createElement(
            "h2",
            { id: "matching-page-title" },
            i18next.t("matching_page_title")
        );

        const pvpButton = this.createMatchButton(
            "PVP",
            i18next.t("matching_waiting_pvp")
        );
        const tournamentButton = this.createMatchButton(
            "tournament",
            i18next.t("matching_waiting_tournament")
        );
        const pveButton = this.createMatchButton(
            "Pve",
            i18next.t("matching_waiting_pve")
        );

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

    createMatchButton(type, waitMessage) {
        return ButtonToMatch(type, async () => {
            this.matchType = type;
            if (this.matchType === "Pve") {
                localStorage.setItem("matchType", this.matchType);
                this.toggleButtonContainer();
                this.waitModal = this.createWaitModal(waitMessage);
                this.handleMatchFound("Pve");
                return;
            } else {
                if (
                    !this.socket ||
                    this.socket.readyState === WebSocket.CLOSED
                ) {
                    this.connectWebSocket(() => this.requestMatch());
                } else {
                    this.requestMatch();
                }
            }
            this.toggleButtonContainer();
            this.waitModal = this.createWaitModal(waitMessage);
        });
    }

    createWaitModal(message) {
        const waitBox = WaitMatchBox(
            message,
            () => {
                this.cancelMatch();
                this.toggleButtonContainer();
                waitBox.modal.dispose();
            },
            this.socket
        );
        this.container.append(waitBox.element);
        waitBox.modal.show();
        return waitBox;
    }

  toggleButtonContainer() {
    document.getElementById("match-btn-container")?.classList.toggle("hide");
  }

    connectWebSocket(callback) {
        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        const endpoint =
            this.matchType === "PVP" ? "matchmaking" : "tournament/matchmaking";
        const wsUrl = `${protocol}://${window.location.host}/api/ws/${endpoint}/`;

        this.socket = new WebSocket(wsUrl);

    this.socket.onopen = () => {
      console.log("WebSocket connected.");
        this.requestMatch();
    };

        this.socket.onmessage = (event) => this.handleSocketMessage(event);
        // this.socket.onclose = (event) => this.handleSocketClose(event);
        this.socket.onclose = (event) => console.log("soket was close!");
        this.socket.onerror = (error) =>
            console.error("WebSocket error:", error);
    }

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

    handleMatchFound(data) {
        const modal = document.getElementById("modal-body-target");
        const modalbtn = document.getElementById("modal-btn-target");
        modal.classList.add("hide");
        modalbtn.classList.add("hide");
        if (data.option_selector || this.matchType === "Pve") {
            const optionForm = document.getElementById("form-target");
            optionForm.classList.remove("hide");
            console.log("op select in this.tournamentId: ", this.tournamentId);
        }
        if (this.matchType === "Pve") return;
        localStorage.setItem("matchType", this.matchType);
        localStorage.setItem(
            "gameId",
            data.game_id ? data.game_id : data.tournament_id
        );
        this.tournamentId = data.tournament_id;
        localStorage.setItem("tid", this.tournamentId);
        console.log(`Match found! gameId: ${localStorage.getItem("gameId")}`);
    }

    async navigateToGame(gameId) {
        if (this.waitModal) {
            this.waitModal.modal.dispose();
            this.container.removeChild(this.waitModal.element);
            this.waitModal = null;
        }
        const serverdgameId = await getCurrentUserGameStatus();
        if (!serverdgameId) window.router.navigate(`/playing/${gameId}`, false);
        else window.router.navigate(`/playing/${serverdgameId.game_id}`, false);
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
  async closeWebSocketAndWait(timeout = 1000) {
      if (this.socket.readyState === WebSocket.CLOSED) {
        return;
      }
      this.socket.close();
      let count = 0;
      // 타임아웃 설정: 지정된 시간이 지나도 닫히지 않으면 실패 처리
      const waitngId = setTimeout(() => {
        console.log("close interval start");
        if(!this.socket || this.socket.readyState === WebSocket.CLOSED || count >5){
            console.log("socket closed or count out", this.socket.readyState , " " ,count);
            this.socket = null;
            clearInterval(waitngId);
            return;
        }
        console.log("close interval count ",count);
        count++;
      }, timeout);

  }
  
  /**
   * 매칭 취소
   */
  async cancelMatch() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      const message = { type: "cancel_match" };
      console.log("cancel match 1", message);
      this.socket.send(JSON.stringify(message));
      console.log("cancel match 2", this.socket.readyState);
      await this.closeWebSocketAndWait();
    //   this.socket.close();
      console.log("cancel match 3", this.socket);
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
