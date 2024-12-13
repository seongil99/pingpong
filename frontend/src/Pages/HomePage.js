import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import FriendList from "../Components/FriendList.js";
import FriendModal from "../Components/FriendModal.js";

class HomePage {
    template() {
        const friendToggleBtn = createElement(
            "button",
            {
                events: {
                    click: () => {
                        const friends = document.querySelector("#friends");
                        const match = document.querySelector(".match-div");
                        friends.classList.toggle("hide");
                        match.classList.toggle("hide");
                        friendToggleBtn.textContent =
                            !friends.classList.contains("hide")
                                ? "X"
                                : "친구목록";
                    },
                },
            },
            "친구목록"
        );
        // 친구 목록 버튼 Div 안에 친구 목록 화면 활성화 버튼 추가
        const friendToggle = createElement(
            "div",
            { id: "friend-toggle" },
            friendToggleBtn
        );
        const friendList = FriendList();
        // 게임시작 Div에 게임시작 버튼 추가
        const matchingButton = createElement(
            "button",
            { class: "match-btn navigate", path: "/matching" },
            "Go to Matching Page"
        );
        const matching = createElement(
            "div",
            { class: "match-div" },
            matchingButton
        );
        // main 요소에 친구 목록 버튼 상자, 친구 목록 화면, 게임 시작 버튼 추가
        const main = createElement(
            "main",
            { id: "home-main" },
            friendToggle,
            friendList,
            matching
        );
        // 컨테이너에 모달, 네비게이션 바, main 요소 추가
        const modal = FriendModal();
        const navBar = NavBar();
        const container = createElement("div", {}, modal, navBar, main);
        return container; // 컨테이너를 반환
    }
}

export default HomePage;
