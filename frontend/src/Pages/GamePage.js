import createElement from "../Utils/createElement.js";
// import NavBar from "../Components/Navbar.js";
// import FriendList from "../Components/FriendList.js";
// import FriendModal from "../Components/FriendModal.js";
import GameWindow from "../Components/GameWindow.js"
import GameCommandInfo from "../Components/GameCommand.js";

class GamePage {
    async template(pathParam, queryParam){ 
        const [_, gameId] = pathParam;
        const game = new GameWindow(parseInt(gameId));
        // main 요소에 친구 목록 버튼 상자, 친구 목록 화면, 게임 시작 버튼 추가
        const main = createElement(
            "div",
            { id: "game-page" },
            GameCommandInfo(),
            game.makeWindow()
        );
        // 컨테이너에 모달, 네비게이션 바, main 요소 추가
        const container = createElement("div", {},  main);
        return container; // 컨테이너를 반환
    }
}

export default GamePage;
