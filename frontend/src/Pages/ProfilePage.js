import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";

class ProfilePage {
    #UserProfile = (userData) => {
        const profileUserImg = createElement("img", {class: "profile-user-img", src:`${}`, alt: `${}'s profile image`}, [])
        const profileUserName = createElement("h3", {class: "profile-user-name"}, `${}`);
        const profileUserEmail = createElement("span", {class: "profile-user-email"}, `${}`);
        const profileUserInfos = createElement("div", {class: "profile-user-infos"}, profileUserName, profileUserEmail);
        const userProfile = createElement("div", {class: `profile-user-profile ${}`}, profileUserImg, profileUserInfos);
        return userProfile;
    }

    // #StatDescription = (userData) => {
    //     // const gameTotalCount = ;
    //     // let gameWinCount = 0;
    //     // const longestRalleyCount = ;
    //     // const averageRalleyCount = ;
    //     // const mode = new Map(Object.entries({'p2p': 0, 'tournament': 0, 'p2p-option': 0, 'tournament-option': 0}));
    //     // userData.d.forEach(() => {});
    //     // let mostMode = ;

    //     // ** user game count
    //     const gameCount = createElement("span", {class: "stat-description-data"}, `${}`);
    //     // ** user game win rate
    //     const winRate = createElement("span", {class: "stat-description-data"}, `${}`);
    //     // ** user game win count and lose count
    //     const winLose = createElement("span", {class: "stat-description-data"}, `${}`);
    //     // ** user longest ralley
    //     const longestRalley = createElement("span", {class: "stat-description-data"}, `${}`);
    //     // ** user average ralley
    //     const averageRalley = createElement("span", {class: "stat-description-data"}, `${}`);
    //     const mostMode = createElement("span", {class: "stat-description-data"}, `${}`);
    //     const stat = createElement("div", {id: "profile-user-stat-description"}, `${}`);
    //     return stat;
    // };

    // #HistoryDescription = (userData) => {
    //     const historyList = createElement("ul", {id: "history-description-list"}, "");
    //     const firstPageBtn = createElement("button", {}, "<<");
    //     const lastPageBtn = createElement("button", {}, ">>");
    //     const prevPageBtn = createElement("button", {}, "<");
    //     const nextPageBtn = createElement("button", {}, ">");
    //     const one = createElement("button", {}, `${}`);
    //     const two = createElement("button", {}, `${}`);
    //     const three = createElement("button", {}, `${}`);
    //     const four = createElement("button", {}, `${}`);
    //     const five = createElement("button", {}, `${}`);
    //     const curPageBtns = createElement("div", {}, one, two, three, four, five);
    //     const pagination = createElement("div", {id: "history-description-pagination"}, firstPageBtn, prevPageBtn, curPageBtns, nextPageBtn, lastPageBtn);
    //     const history = createElement("div", {id:"history-description"}, historyList, pagination);
    //     return history;
    // }

    // #StatOrHistoryBtnSet = (userData) => {
    //     const stat = document.querySelector("#profile-user-stat-description");
    //     const history = document.querySelector("#profile-user-history-description");
    //     const description = document.querySelector("#profile-stat-or-history-description");
    //     const statBtn = createElement("button", {class: "profile-btn", events: {
    //         click: () => {
    //             stat.classList.remove("hide");
    //             history.classList.add("hide");
    //             description.removeChild(description.lastElementChild);
    //             description.appendChild(this.#StatDescription(userData));
    //         }
    //     }}, "게임 스탯");
    //     const historyBtn = createElement("button", {class: "profile-btn", events: {
    //         click: () => {
    //             stat.classList.add("hide");
    //             history.classList.remove("hide");
    //             description.removeChild(description.lastElementChild);
    //             description.appendChild(this.#HistoryDescription(userData));
    //         }
    //     }}, "전적 기록");
    //     const btnSet = createElement("div", {class: "profile-btn-set"}, statBtn, historyBtn);
    //     return btnSet;
    // }

    async template() {
        const username = window.location.pathname;
        const userData = await fetchUserData();
        const navBar = NavBar();
        const profileTitle = createElement(
            "h1",
            { class: "profile-title" },
            "jonghopa님의 프로필"
        );
        const userProfile = this.#UserProfile(userData);
        const statOrHistoryBtnSet = this.#StatOrHistoryBtnSet();
        const description = document.createElement(
            "div",
            { id: "profile-stat-or-history-description" },
            []
        );
        const main = createElement(
            "main",
            { id: "profile-main" },
            profileTitle,
            userProfile,
            statOrHistoryBtnSet,
            description
        );
        const container = createElement("div", {}, navBar, main);
        return container;
    }
}

export default ProfilePage;
