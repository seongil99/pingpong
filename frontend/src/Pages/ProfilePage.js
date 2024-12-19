import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import FetchUserData from "../Controller/Profile/FetchUserData.js";
import FetchOneUserGameHistory from "../Controller/Profile/FetchOneUserGameHistory.js";
import fetchUserProfile from "../Controller/Settings/fetchUserProfile.js";

class ProfilePage {
    #offset;
    #limit;
    #UserProfile = (userData) => {
        const profileUserImg = createElement(
            "img",
            {
                class: "profile-user-img",
                src: `${userData.avatar}`,
                alt: `${userData.username}'s profile image`,
            },
            []
        );
        const profileUserName = createElement(
            "h3",
            { class: "profile-user-name" },
            `${userData.username}`
        );
        const profileUserEmail = createElement(
            "span",
            { class: "profile-user-email" },
            `${userData.email}`
        );
        const profileUserInfos = createElement(
            "div",
            { class: "profile-user-infos" },
            profileUserName,
            profileUserEmail
        );
        const userProfile = createElement(
            "div",
            { class: `profile-user-profile ${userData.username}` },
            profileUserImg,
            profileUserInfos
        );
        return userProfile;
    };

    #StatDescription = (userHistoryData, userid) => {
        const gameTotalCount = userHistoryData.count;
        let gameWinCount = 0;
        let playtime = 0;
        let longestRallyCount = 0;
        let averageRallyTotal = 0;
        for (let idx = 0; idx < gameTotalCount; idx++) {
            if (userHistoryData.results[idx].winner === userid) gameWinCount++;
            const start = new Date(userHistoryData.results[idx].started_at);
            const end = new Date(userHistoryData.results[idx].ended_at);
            const diff = end.getTime() - start.getTime();
            playtime += diff;
            if (longestRallyCount < userHistoryData.results[idx].longest_rally)
                longestRallyCount = userHistoryData.results[idx].longest_rally;
            averageRallyTotal += userHistoryData.results[idx].average_rally;
        }
        const gameWinRate = gameTotalCount
            ? `${(gameWinCount / gameTotalCount) * 100} %`
            : "게임을 한 판 이상하면 승률을 확인할 수 있습니다.";
        const longestRally = gameTotalCount
            ? `${longestRallyCount} 회`
            : "게임을 한 판 이상하면 최장 랠리를 확인할 수 있습니다.";
        const averageRally = gameTotalCount
            ? `약 ${Math.floor(averageRallyTotal / gameTotalCount)} 회`
            : "게임을 한 판 이상하면 최장 랠리를 확인할 수 있습니다.";
        const mode = { p2p: 0, tournament: 0 };
        const mostMode = gameTotalCount
            ? mode["p2p"] > mode["tournament"]
                ? "1대 1"
                : mode["p2p"] < mode["tournament"]
                ? "토너먼트"
                : "비슷비슷해요 🙂"
            : "게임을 한 판 이상하면 가장 많이 한 모드 정보를 볼 수 있습니다.";
        // ** user game count
        const gameCount = createElement(
            "span",
            { class: "stat-description-data" },
            `게임 수: ${gameTotalCount} 회`
        );
        // ** user game win rate
        const winRate = createElement(
            "span",
            { class: "stat-description-data" },
            `승률: ${gameWinRate}`
        );
        // ** user game win count and lose count
        const winLoseCount = createElement(
            "span",
            { class: "stat-description-data" },
            `승 • 패: ${gameWinCount}/${gameTotalCount - gameWinCount}`
        );
        // ** user longest rally
        const longestRallyText = createElement(
            "span",
            { class: "stat-description-data" },
            `최장 랠리: ${longestRally}`
        );
        // ** user average rally
        const averageRallyText = createElement(
            "span",
            { class: "stat-description-data" },
            `평균 랠리: ${averageRally}`
        );
        const mostModeText = createElement(
            "span",
            { class: "stat-description-data" },
            `가장 많이 한 모드: ${mostMode}`
        );
        const stat = createElement(
            "div",
            { id: "profile-user-stat-description" },
            gameCount,
            winRate,
            winLoseCount,
            longestRallyText,
            averageRallyText,
            mostModeText
        );
        return stat;
    };

    #HistoryListItem = async (session, userid) => {
        const opponentId =
            session.user1 !== userid ? session.user1 : session.user2;
        const opponentData = await FetchUserData(opponentId);
        const gameResult = createElement(
            "span",
            { class: "history-list-item-game-result" },
            session.winner === userid ? "승리" : "패배"
        );
        const gameSummary = createElement(
            "div",
            { class: "history-list-item-summary" },
            gameMode,
            gameScore,
            gamePlaytime,
            gameStart
        );
        const versusText = createElement(
            "span",
            { class: "versus-text" },
            "VS"
        );
        const opponentAvatar = createElement(
            "img",
            { src: `${opponentData.avatar}`, class: "opponent-avatar" },
            []
        );
        const opponentUsername = createElement(
            "span",
            {
                class: "opponent-username",
            },
            `${opponentData.username}`
        );
        const opponentProfile = createElement(
            "div",
            { class: "history-list-item-opponent-profile" },
            opponentAvatar,
            opponentUsername
        );
        const gameVersus = createElement(
            "div",
            { class: "history-list-item-game-versus" },
            versusText,
            opponentProfile
        );
        const item = createElement(
            "li",
            { id: `${userid}`, class: "history-list-item" },
            gameResult,
            gameSummary,
            gameVersus
        );
        return item;
    };

    #HistoryDescription = (userHistoryData, userid) => {
        let curPageBlock = 0;
        let curPage = 1;
        const pageBlocks = [];
        const pageListContent = [];
        const pageItems = [];
        for (
            let i = 1;
            this.#limit &&
            i <=
                Math.floor(userHistoryData.count / this.#limit) +
                    (userHistoryData.count % this.#limit);
            i++
        ) {
            const curLimit =
                userHistoryData.count - this.#limit * i >= this.#limit
                    ? this.#limit
                    : userHistoryData.count - this.#limit * i;
            pageItems.append(
                createElement("button", {
                    id: `page${i}`,
                    offset: `${this.#limit * (i - 1) + 1}`,
                    limit: `${curLimit}`,
                    events: {
                        click: (event) => {
                            const list = document.getElementById(
                                "history-description-list"
                            );
                            list.removeChild(list.lastChild);
                            list.appendChild(pageListContent[i - 1]);
                            this.#offset = `${this.#limit * (i - 1) + 1}`;
                            window.history.pushState(
                                {},
                                `/profile/${userid}/history?offset=${
                                    this.#offset
                                }&limit=${curLimit}`,
                                window.location.origin +
                                    `/profile/${userid}/history?offset=${
                                        this.#offset
                                    }&limit=${curLimit}`
                            );
                        },
                    },
                })
            );
            const content = createElement(
                "div",
                { class: "history-description-pagination-content-list" },
                []
            );
            for (let j = 0; j < curLimit; j++) {
                content.appendChild(
                    this.#HistoryListItem(
                        userHistoryData.results[curLimit * (i - 1) + j],
                        userid
                    )
                );
            }
            pageListContent.append(content);
            if (
                !(i % 5) ||
                userHistoryData.count - this.#limit * i < this.#limit
            ) {
                const pageBlock = createElement(
                    "div",
                    { class: "history-description-pagination-pages" },
                    []
                );
                for (let item of pageItems) {
                    pageBlock.appendChild(item);
                }
                pageBlocks.append(pageBlock);
            }
        }
        curPageBlock = this.#limit
            ? Math.floor(Math.floor(this.#offset / this.#limit) / 5)
            : 0;
        curPage = this.#limit
            ? Math.floor(this.#offset / this.#limit) +
              (this.#offset % this.#limit)
            : 1;
        const pageNumsDiv = createElement(
            "div",
            { id: "history-description-pagination-nums-div" },
            pageBlocks[curPageBlock]
        );
        const leftBtn = createElement(
            "button",
            {
                class: "history-description-pagination-left-btn",
                events: {
                    click: () => {
                        if (curPageBlock - 1 >= 0) {
                            curPageBlock -= 1;
                            const paginationPages = document.getElementById(
                                "history-description-pagination-nums-div"
                            );
                            paginationPages.removeChild(
                                paginationPages.lastChild
                            );
                            paginationPages.appendChild(
                                pageBlocks[curPageBlock]
                            );
                            // 페이지 번호 버튼 색깔 변화
                            curPage = 5 * curPageBlock + 5;
                            this.#offset = this.#limit * (curPage - 1) + 1;
                            window.history.pushState(
                                {},
                                `/profile/${userid}/history?offset=${
                                    this.#offset
                                }&limit=${curLimit}`,
                                window.location.origin +
                                    `/profile/${userid}/history?offset=${
                                        this.#offset
                                    }&limit=${curLimit}`
                            );
                        }
                    },
                },
            },
            "<"
        );
        const rightBtn = createElement(
            "button",
            {
                class: "history-description-pagination-right-btn",
                events: {
                    click: () => {
                        if (
                            curPageBlock + 1 <=
                            Math.floor(userHistoryData.count / this.#limit) +
                                (userHistoryData.count % this.#limit)
                        ) {
                            curPageBlock += 1;
                            const paginationPages = document.getElementById(
                                "history-description-pagination-nums-div"
                            );
                            paginationPages.removeChild(
                                paginationPages.lastChild
                            );
                            paginationPages.appendChild(
                                pageBlocks[curPageBlock]
                            );
                            // 페이지 번호 버튼 색깔 변화
                            curPage = 5 * curPageBlock + 1;
                            this.#offset = this.#limit * (curPage - 1) + 1;
                            window.history.pushState(
                                {},
                                `/profile/${userid}/history?offset=${
                                    this.#offset
                                }&limit=${curLimit}`,
                                window.location.origin +
                                    `/profile/${userid}/history?offset=${
                                        this.#offset
                                    }&limit=${curLimit}`
                            );
                        }
                    },
                },
            },
            ">"
        );
        const pagination = createElement(
            "div",
            { id: "history-description-pagination" },
            leftBtn,
            pageNumsDiv,
            rightBtn
        );
        const historyList = createElement(
            "ul",
            { id: "history-description-list" },
            pageListContent[curPage]
        );
        const history = createElement(
            "div",
            { id: "history-description" },
            historyList,
            pagination
        );
        return history;
    };

    #StatOrHistoryBtnSet = (userHistoryData, userid) => {
        const statBtn = createElement(
            "button",
            {
                class: "profile-btn",
                events: {
                    click: () => {
                        const description = document.querySelector(
                            "#profile-stat-or-history-description"
                        );
                        description.removeChild(description.lastChild);
                        description.appendChild(
                            this.#StatDescription(userHistoryData, userid)
                        );
                        window.history.pushState(
                            {},
                            `/profile/${userid}/stat`,
                            window.location.origin + `/profile/${userid}/stat`
                        );
                    },
                },
            },
            "게임 스탯"
        );
        const historyBtn = createElement(
            "button",
            {
                class: "profile-btn",
                events: {
                    click: () => {
                        const description = document.querySelector(
                            "#profile-stat-or-history-description"
                        );
                        description.removeChild(description.lastElementChild);
                        description.appendChild(
                            this.#HistoryDescription(userHistoryData, userid)
                        );
                        window.history.pushState(
                            {},
                            `/profile/${userid}/history`,
                            window.location.origin +
                                `/profile/${userid}/history`
                        );
                    },
                },
            },
            "전적 기록"
        );
        const btnSet = createElement(
            "div",
            { class: "profile-btn-set" },
            statBtn,
            historyBtn
        );
        return btnSet;
    };

    #validateQueryParam(userHistoryData, queryParam) {
        const regex = /^[1-9]\d*$/;
        const offsetValue = queryParam.get("offset");
        const limitValue = queryParam.get("limit");
        this.#offset = regex.test(offsetValue) ? parseInt(offsetValue) : 1;
        this.#limit = regex.test(limitValue)
            ? parseInt(limitValue)
            : userHistoryData.count;
        if (this.#offset <= 0) this.#offset = 1;
        else if (this.#offset > userHistoryData.count)
            this.#offset = userHistoryData.count;
        if (this.#limit <= 0 || this.#limit > userHistoryData.count)
            this.#limit = userHistoryData.count;
    }

    async template(pathParam, queryParam) {
        const [_, path, userId, info] = pathParam;
        let user;
        console.log(pathParam);
        if (pathParam.length === 2) {
            user = await fetchUserProfile();
        } else {
            user = await FetchUserData(parseInt(userId));
        }
        const navBar = NavBar();
        const profileTitle = createElement(
            "h1",
            { class: "profile-title" },
            `${user.username}님의 프로필`
        );
        const userProfile = this.#UserProfile(user);
        const userHistoryData = await FetchOneUserGameHistory(user.id);
        this.#validateQueryParam(userHistoryData, queryParam);
        const statOrHistoryBtnSet = this.#StatOrHistoryBtnSet(
            userHistoryData,
            user.id
        );
        const description = createElement(
            "div",
            { id: "profile-stat-or-history-description" },
            info !== "history"
                ? this.#StatDescription(userHistoryData, user.id)
                : this.#HistoryDescription(userHistoryData, user.id)
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
