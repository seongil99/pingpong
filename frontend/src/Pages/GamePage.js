import createElement from "../Utils/createElement.js";
import { io } from "socket.io-client";
import PingPongClient from "../Components/Game/GameWindow.js";
import isEnded from "../Controller/Game/IsEnded.js";
class GamePage {
  constructor() {
    this.socket = null;
    this.game = null;
  }

  async template(pathParam, queryParam) {
    const [_, path, gameId] = pathParam;
    const backToHome = await isEnded(gameId);
    if(backToHome)
        await window.router.navigate(`/home`, false);
    // 소켓 연결
    this.socket = io("/api/game", {
      reconnection: false,
      transports: ["websocket"],
      debug: true,
      path: "/api/game/socket.io",
      query: { gameId },
    });

    // PingPongClient 초기화
    this.game = new PingPongClient(this.socket, gameId);

    // main 요소
    const main = createElement(
      "div",
      { id: "game-page" },
      // GameCommandInfo(), // 필요 시 사용
      this.game.makeWindow()
    );

    // 페이지 컨테이너 반환
    const container = createElement("div", {}, main);
    return container;
  }

  async dispose() {
    // PingPongClient 정리
    if (this.game) {
      await this.game.dispose();
    }
    // 소켓 연결 해제
    if (this.socket && this.socket.connected) {
      this.socket.disconnect();
      this.socket = null;
      console.log("Game Page dispose() called: socket disconnected");
    }
    console.log("Game Page dispose() called");
  }
}

export default GamePage;
