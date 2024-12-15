import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import FriendInfos from "../Components/FriendInfos.js";

const StatDescription = () => {
    const description = document.createElement(
        "div",
        {},
        createElement("span", {}, `게임 수: 18`),
        createElement("span", {}, `승 • 패: 30 / 80`),
        createElement("span", {}, `승률: 25.21%`),
        createElement("span", {}, `플레이 시간: 100시간 0분`)
    );
    return description;
};

const Game = () => {
    const gameResult = createElement("h3", {}, `승리`);
    const gameInfo = createElement(
        "span",
        {},
        createElement("span", {}, `1대 1`),
        createElement("span", {}, `3 : 2`),
        createElement("span", {}, `게임시간: 10분 10초`),
        createElement("span", {}, `게임시작: 12월 25일 오후 12시 25분`)
    );
    const opponent = createElement(
        "div",
        {},
        createElement("img", {}, "/src/Components/profile.png"),
        createElement("span", {}, "sabyun")
    );
    const game = createElement("li", {}, gameResult, gameInfo, opponent);
    return game;
};

const GamesList = () => {
    const list = createElement("ul", {}, Game(), Game(), Game());
    return list;
};

const GameRounds = () => {
    const prevBtn = createElement();
    const game = createElement("div", {}, prevBtn, options, tournament, versus, rounds);
    return game;
}

const HistoryDescription = () => {
    const description = document.createElement(
        "div",
        { class: "history-description" },
        GamesList(),
        GameRounds()
    );
    return description;
};

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
