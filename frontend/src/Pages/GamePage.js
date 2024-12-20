import createElement from "../Utils/createElement.js";
// import NavBar from "../Components/Navbar.js";
// import FriendList from "../Components/FriendList.js";
// import FriendModal from "../Components/FriendModal.js";
import GameWindow from "../Components/GameWindow.js"
import GameCommandInfo from "../Components/GameCommand.js";
import { io } from "socket.io-client";

class GamePage {
    async template(pathParam, queryParam) {
        const [_, path, gameId] = pathParam;
        const socket = io('/api/game', {
            reconnection: false,
            transports: ['websocket'],
            debug: true,
            path: '/api/game/socket.io',
            query: {
                gameId: gameId
            },
        });
        const game = new GameWindow(socket,gameId);
        // main 요소에 친구 목록 버튼 상자, 친구 목록 화면, 게임 시작 버튼 추가
        const main = createElement(
            "div",
            { id: "game-page" },
            GameCommandInfo(),
            game.makeWindow()
        );
        // 컨테이너에 모달, 네비게이션 바, main 요소 추가
        const container = createElement("div", {}, main);
        return container; // 컨테이너를 반환
    }
}

export default GamePage;
