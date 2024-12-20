import createElement from "../Utils/createElement.js";
// import NavBar from "../Components/Navbar.js";
// import FriendList from "../Components/FriendList.js";
// import FriendModal from "../Components/FriendModal.js";
import GameWindow from "../Components/GameWindow.js"
import GameCommandInfo from "../Components/GameCommand.js";
import { io } from "socket.io-client";

class GamePage {
    constructor(){
        this.socket = null;
        this.game = null;
    }
    async template(pathParam, queryParam) {
        const [_, path, gameId] = pathParam;
        this.socket = io('/api/game', {
            reconnection: false,
            transports: ['websocket'],
            debug: true,
            path: '/api/game/socket.io',
            query: {
                gameId: gameId
            },
        });
        this.game = new GameWindow(this.socket,gameId);
        // main 요소에 친구 목록 버튼 상자, 친구 목록 화면, 게임 시작 버튼 추가
        const main = createElement(
            "div",
            { id: "game-page" },
            GameCommandInfo(),
            this.game.makeWindow()
        );
        // 컨테이너에 모달, 네비게이션 바, main 요소 추가
        const container = createElement("div", {}, main);
        return container; // 컨테이너를 반환
    }
    dispose() {
        if (this.socket && this.socket.connected) {
          this.socket.disconnect();
          this.socket = null;
          this.game.audio.dispose();
            console.log("Game Page dispose() called soket close");
        }
        console.log("Game Page dispose() called");
    }
}

export default GamePage;
