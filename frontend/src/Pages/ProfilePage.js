import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import FriendInfos from "../Components/FriendInfos.js";

const StatDescription = () => {};

const HistoryDescription = () => {};

class ProfilePage {
    template() {
        const navBar = NavBar();
        const profileTitle = createElement(
            "h1",
            { class: "profile-title" },
            "jonghopa님의 프로필"
        );
        const profileInfos = FriendInfos();

        const gameModeSelect = createElement(
            "select",
            {
                class: "gamemode-select",
            },
            createElement(
                "option",
                { class: "gamemode-select-option", value: "p2p" },
                "1대 1(일반)"
            ),
            createElement(
                "option",
                { class: "gamemode-select-option", value: "tournament" },
                "토너먼트(일반)"
            ),
            createElement(
                "option",
                { class: "gamemode-select-option", value: "p2pCustom" },
                "1대 1(사용자 설정)"
            ),
            createElement(
                "option",
                { class: "gamemode-select-option", value: "tournamentCustom" },
                "토너먼트(사용자 설정)"
            )
        );
        const statBtn = createElement(
            "button",
            { class: "stat-btn" },
            "게임 스탯"
        );
        const historyBtn = createElement(
            "button",
            { class: "history-btn" },
            "전적 기록"
        );
        const gameStatAndHistory = createElement(
            "div",
            { class: "game-stat-history" },
            statBtn,
            historyBtn
        );
        const statOrHistoryDescription = createElement(
            "div",
            { class: "stat-history-description" },
            StatDescription(),
            HistoryDescription()
        );
        const main = createElement(
            "main",
            { class: "profile-content" },
            profileTitle,
            profileInfos,
            gameModeSelect,
            gameStatAndHistory,
            statOrHistoryDescription
        );
        const container = createElement("div", {}, navBar, main);
        return container;
    }
}

export default ProfilePage;
