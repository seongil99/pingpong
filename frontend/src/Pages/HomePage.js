import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Common/Navbar.js";
import FriendList from "../Components/Main/FriendList.js";
import FriendModal from "../Components/Main/FriendModal.js";

class HomePage {
    async template() {
        const friendToggleBtn = createElement(
            "button",
            {
                id: "friendToggleBtn",
                events: {
                    click: () => {
                        const friends = document.querySelector("#friends");
                        const match = document.querySelector(".match-div");
                        friends.classList.toggle("hide");
                        match.classList.toggle("hide");
                        friendToggleBtn.textContent =
                            !friends.classList.contains("hide")
                                ? i18next.t("btn_close")
                                : i18next.t("btn_friend_list");
                    },
                },
            },
            i18next.t("btn_friend_list")
        );

        const friendToggle = createElement(
            "div",
            { id: "friend-toggle" },
            friendToggleBtn
        );

        const friendList = await FriendList();

        const matchingButton = createElement(
            "button",
            {
                id: "matchingButton",
                class: "match-btn navigate",
                path: "/matching",
            },
            i18next.t("btn_go_matching")
        );

        const matching = createElement(
            "div",
            { class: "match-div" },
            matchingButton
        );

        const main = createElement(
            "main",
            { id: "home-main" },
            friendToggle,
            friendList,
            matching
        );

        const modal = FriendModal();
        const navBar = NavBar();
        const container = createElement("div", {}, modal, navBar, main);

        return container;
    }
}

export default HomePage;
