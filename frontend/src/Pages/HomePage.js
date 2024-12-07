import NavBar from "../Components/Navbar.js";
import FriendList from "../Components/FriendList.js";

class HomePage {
    template() {
        // 컨테이너 div 생성
        const container = document.createElement("div");

        const modal = Modal();
        const navBar = NavBar();
        const main = document.createElement("main");

        const friendToggle = document.createElement("div");
        friendToggle.setAttribute("id", "friend-toggle");
        const friendToggleBtn = document.createElement("button");
        friendToggleBtn.textContent = "친구목록";
        friendToggleBtn.addEventListener("click", () => {
            const friends = document.querySelector("#friends");
            const match = document.querySelector(".match-div");
            friends.classList.toggle("hide");
            match.classList.toggle("hide");
            friendToggleBtn.textContent = (!friends.classList.contains("hide")) ? "X" : "친구목록";

        });
        // 친구 목록 버튼 Div 안에 친구 목록 화면 활성화 버튼 추가
        friendToggle.appendChild(friendToggleBtn);

        const friendList = FriendList();

        const matching = document.createElement("div");
        matching.classList.add("match-div");
        const matchingButton = document.createElement("button");
        matchingButton.classList.add("match-btn", "navigate");
        matchingButton.setAttribute("path", "/matching");
        matchingButton.textContent = "Go to Matching Page";
        // 게임시작 Div에 게임시작 버튼 추가
        matching.appendChild(matchingButton);

        // main 요소에 친구 목록 버튼 상자, 친구 목록 화면, 게임 시작 버튼 추가
        main.appendChild(friendToggle);
        main.appendChild(friendList);
        main.appendChild(matching);

        // 컨테이너에 네비게이션 바, main 요소
        container.appendChild(modal);
        container.appendChild(navBar);
        container.appendChild(main);

        return container; // 컨테이너를 반환
    }
}

export default HomePage;
