import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import FetchUserData from "../Controller/Profile/FetchUserData.js";
import FetchOneUserGameHistory from "../Controller/Profile/FetchOneUserGameHistory.js";
import fetchUserProfile from "../Controller/Settings/fetchUserProfile.js";
import ScoreChart from "../Components/ScoreChart.js";
import calculateDiffDate from "../Utils/calculateDiffDate.js";
import changeTimeToDate from "../Utils/changeTimeToDate.js";

class ProfilePage {
    #offset;
    #limit;
    #gameTotalCount;
    #currentHistoryPage;
    #currentHistoryPagesBlock;
    #pageListContent = [];
    #pageNumBtns = [];
    #pagesBlocks = [];
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
        let gameWinCount = 0;
        let playtime = 0;
        let longestRallyCount = 0;
        let averageRallyTotal = 0;
        const mode = { pvp: 0, tournament: 0 };
        for (let idx = 0; idx < this.#gameTotalCount; idx++) {
            if (userHistoryData.results[idx].winner === userid) gameWinCount++;
            const start = new Date(userHistoryData.results[idx].started_at);
            const end = new Date(userHistoryData.results[idx].ended_at);
            const diff =
                userHistoryData.results[idx].ended_at !== null
                    ? end.getTime() - start.getTime()
                    : 0;
            playtime += diff;
            if (longestRallyCount < userHistoryData.results[idx].longest_rally)
                longestRallyCount = userHistoryData.results[idx].longest_rally;
            averageRallyTotal += userHistoryData.results[idx].average_rally;
            userHistoryData.results[idx].tournament_id
                ? (mode["tournament"] += 1)
                : (mode["pvp"] += 1);
        }
        const gameWinRate = this.#gameTotalCount
            ? `${(gameWinCount / this.#gameTotalCount) * 100} %`
            : "게임을 한 판 이상하면 승률을 확인할 수 있습니다.";
        const longestRally = this.#gameTotalCount
            ? `${longestRallyCount} 회`
            : "게임을 한 판 이상하면 최장 랠리를 확인할 수 있습니다.";
        const averageRally = this.#gameTotalCount
            ? `약 ${Math.floor(averageRallyTotal / this.#gameTotalCount)} 회`
            : "게임을 한 판 이상하면 최장 랠리를 확인할 수 있습니다.";
        const modeCount = this.#gameTotalCount
            ? `PVP: ${mode["pvp"]}, 토너먼트: ${mode["tournament"]}`
            : "게임을 한 판 이상하면 가장 많이 한 모드 정보를 볼 수 있습니다.";
        const totalPlaytime = this.#gameTotalCount
            ? `${changeTimeToDate(playtime)}`
            : "게임을 한 판 이상하면 플레이타임 정보를 볼 수 있습니다.";
        // ** user game count
        const gameCount = createElement(
            "span",
            { class: "stat-description-data" },
            `게임 수: ${this.#gameTotalCount} 회`
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
            `승 • 패: ${gameWinCount}/${this.#gameTotalCount - gameWinCount}`
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
        const modeCountText = createElement(
            "span",
            { class: "stat-description-data" },
            `게임 모드: ${modeCount}`
        );
        const totalPlaytimeText = createElement(
            "span",
            { class: "stat-description-data" },
            `플레이 시간: ${totalPlaytime}`
        );
        const stat = createElement(
            "div",
            { id: "profile-user-stat-description" },
            gameCount,
            winRate,
            winLoseCount,
            longestRallyText,
            averageRallyText,
            modeCountText,
            totalPlaytimeText
        );
        return stat;
    };

    #HistorySession = async (session, userid) => {
        const opponentId =
            session.user1 !== userid ? session.user1 : session.user2;
        const opponentData = await FetchUserData(opponentId);
        const gameResult = createElement(
            "span",
            { class: "history-session-game-result" },
            session.winner === userid ? "승리" : "패배"
        );
        const gameMode = createElement(
            "span",
            {
                class: "history-session-game-mode",
            },
            session.gamemode
        );
        const gameScore = createElement(
            "span",
            {
                class: "history-session-game-user-score",
            },
            `${session.user1_score} : ${session.user2_score}`
        );
        const gamePlaytime = createElement(
            "span",
            {
                class: "history-session-game-playtime",
            },
            `게임 시간: ${calculateDiffDate(
                session.started_at,
                session.ended_at
            )}`
        );
        const gameStart = createElement(
            "span",
            {
                class: "history-session-game-startdate",
            },
            `게임 일자: ${new Date(session.started_at).toLocaleDateString(
                "ko-KR",
                {
                    year: "numeric",
                    month: "numeric",
                    day: "numeric",
                    hour: "numeric",
                    minute: "numeric",
                }
            )}`
        );
        const gameSummary = createElement(
            "div",
            { class: "history-session-summary" },
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
            { class: "history-session-opponent-profile" },
            opponentAvatar,
            opponentUsername
        );
        const gameVersus = createElement(
            "div",
            { class: "history-session-game-versus" },
            versusText,
            opponentProfile
        );
        const item = createElement(
            "li",
            { id: `${session.id}`, class: "history-session" },
            gameResult,
            gameSummary,
            gameVersus
        );
        return item;
    };

    #HistorySessionMatchDashboard = async (session, sessionIdx) => {
        const scoreTitle = createElement(
            "h3",
            { class: "history-session-match-dashboard-title" },
            "Score"
        );
        const scoreChart = await ScoreChart(session, sessionIdx);
        const scoreChartDiv = createElement(
            "div",
            { class: "history-session-chart" },
            scoreTitle,
            scoreChart
        );
        const match = createElement(
            "div",
            { class: "history-session-match-dashboard" },
            scoreChartDiv
        );
        return match;
    };

    #handlePageClick = (number, curLimit, userid) => {
        const list = document.getElementById("history-description-list");
        list.removeChild(list.lastChild);
        list.appendChild(this.#pageListContent[number - 1]);
        this.#offset = `${this.#limit * (number - 1) + 1}`;
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
    };

    #PageButton = (number, curLimit, userid) => {
        const pageButton = createElement(
            "button",
            {
                id: `page${number}`,
                offset: `${this.#limit * (number - 1) + 1}`,
                limit: `${curLimit}`,
                events: {
                    click: () => {
                        this.#handlePageClick(number, curLimit, userid);
                    },
                },
            },
            `${number}`
        );
        return pageButton;
    };

    #Pagination = async (userHistoryData, info, userid) => {
        const totalPage = this.#limit
            ? Math.floor(this.#gameTotalCount / this.#limit) +
              (this.#gameTotalCount % this.#limit)
            : 0;
        for (let i = 1; i <= totalPage; i++) {
            const curLimit =
                this.#gameTotalCount - this.#limit * (i - 1) >= this.#limit
                    ? this.#limit
                    : this.#gameTotalCount - this.#limit * i;
            this.#pageNumBtns.push(this.#PageButton(i, curLimit, userid));
            const content = createElement(
                "div",
                { class: "history-description-pagination-content-list" },
                []
            );
            for (let j = 0; j < curLimit; j++) {
                const sessionData =
                    userHistoryData.results[this.#limit * (i - 1) + j];
                const session = await this.#HistorySession(sessionData, userid);
                let sessionDashboard = "";
                if (sessionData.gamemode === "PVP")
                    sessionDashboard = await this.#HistorySessionMatchDashboard(
                        sessionData,
                        j
                    );
                content.appendChild(session);
                content.appendChild(sessionDashboard);
            }
            this.#pageListContent.push(content);
            if (
                !(i % 5) ||
                this.#gameTotalCount - this.#limit * i < this.#limit
            ) {
                const pagesBlock = createElement(
                    "div",
                    { class: "history-description-pagination-pages" },
                    []
                );
                while (this.#pageNumBtns.length) {
                    pagesBlock.appendChild(this.#pageNumBtns[0]);
                    this.#pageNumBtns.shift();
                }
                this.#pagesBlocks.push(pagesBlock);
            }
        }
        const pageNumsDiv = createElement(
            "div",
            { id: "history-description-pagination-nums-div" },
            this.#pagesBlocks[this.#currentHistoryPagesBlock]
        );
        const leftBtn = createElement(
            "button",
            {
                class: "history-description-pagination-left-btn",
                events: {
                    click: () => {
                        if (this.#currentHistoryPagesBlock - 1 >= 0) {
                            this.#currentHistoryPagesBlock -= 1;
                            const paginationPages = document.getElementById(
                                "history-description-pagination-nums-div"
                            );
                            paginationPages.removeChild(
                                paginationPages.lastChild
                            );
                            paginationPages.appendChild(
                                this.#pagesBlocks[
                                    this.#currentHistoryPagesBlock
                                ]
                            );
                            // 페이지 번호 버튼 색깔 변화
                            this.#currentHistoryPage =
                                5 * this.#currentHistoryPagesBlock + 5;
                            this.#offset =
                                this.#limit * (this.#currentHistoryPage - 1) +
                                1;
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
                            this.#currentHistoryPagesBlock + 1 <
                            this.#pagesBlocks.length
                        ) {
                            this.#currentHistoryPagesBlock += 1;
                            const paginationPages = document.getElementById(
                                "history-description-pagination-nums-div"
                            );
                            paginationPages.removeChild(
                                paginationPages.lastChild
                            );
                            paginationPages.appendChild(
                                this.#pagesBlocks[
                                    this.#currentHistoryPagesBlock
                                ]
                            );
                            // 페이지 번호 버튼 색깔 변화
                            this.#currentHistoryPage =
                                5 * this.#currentHistoryPagesBlock + 1;
                            this.#offset =
                                this.#limit * (this.#currentHistoryPage - 1) +
                                1;
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
        if (info === "stat") {
            console.log(info);
            pagination.classList.add("hide");
        }
        return pagination;
    };

    #HistoryDescription = async (userHistoryData, userid) => {
        const historyList = createElement(
            "ul",
            { id: "history-description-list" },
            this.#pageListContent[this.#currentHistoryPage - 1]
        );
        const history = createElement(
            "div",
            { id: "history-description" },
            historyList
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
                        const pagination = document.querySelector(
                            "#history-description-pagination"
                        );
                        pagination.classList.add("hide");
                        const description = document.querySelector(
                            "#profile-stat-or-history-description"
                        );
                        description.removeChild(description.firstElementChild);
                        description.insertBefore(
                            this.#StatDescription(userHistoryData, userid),
                            pagination
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
                    click: async () => {
                        const pagination = document.querySelector(
                            "#history-description-pagination"
                        );
                        console.log(pagination);
                        pagination.classList.remove("hide");
                        const description = document.querySelector(
                            "#profile-stat-or-history-description"
                        );
                        description.removeChild(description.firstElementChild);
                        description.insertBefore(
                            await this.#HistoryDescription(
                                userHistoryData,
                                userid
                            ),
                            pagination
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
        this.#gameTotalCount = userHistoryData.count;
        this.#offset = regex.test(offsetValue) ? parseInt(offsetValue) : 1;
        this.#limit = regex.test(limitValue)
            ? parseInt(limitValue)
            : this.#gameTotalCount;
        if (this.#offset <= 0) this.#offset = 1;
        else if (this.#offset > this.#gameTotalCount)
            this.#offset = this.#gameTotalCount;
        if (this.#limit <= 0 || this.#limit > this.#gameTotalCount)
            this.#limit = this.#gameTotalCount;
        this.#currentHistoryPagesBlock = this.#limit
            ? Math.floor(Math.floor(this.#offset / this.#limit) / 5)
            : 0;
        this.#currentHistoryPage = this.#limit
            ? Math.floor(this.#offset / this.#limit) +
              (this.#offset % this.#limit)
            : 1;
    }

    async template(pathParam, queryParam) {
        const [_, path, userId, info] = pathParam;
        let user;
        if (pathParam.length === 2) {
            user = await fetchUserProfile();
        } else {
            user = await FetchUserData(parseInt(userId));
        }
        const userHistoryData = await FetchOneUserGameHistory(user.id);
        this.#validateQueryParam(userHistoryData, queryParam);
        const pagination = await this.#Pagination(
            userHistoryData,
            info,
            user.id
        );
        let chosenDescription;
        if (info !== "history") {
            chosenDescription = this.#StatDescription(userHistoryData, user.id);
        } else {
            chosenDescription = await this.#HistoryDescription(
                userHistoryData,
                user.id
            );
        }

        const container = createElement("div", {}, []);
        const main = createElement("main", { id: "profile-main" }, []);
        const navBar = NavBar();
        const profileTitle = createElement(
            "h1",
            { class: "profile-title" },
            `${user.username}님의 프로필`
        );
        const userProfile = this.#UserProfile(user);
        const statOrHistoryBtnSet = this.#StatOrHistoryBtnSet(
            userHistoryData,
            user.id
        );
        const description = createElement(
            "div",
            {
                id: "profile-stat-or-history-description",
            },
            chosenDescription,
        );
        main.appendChild(profileTitle);
        main.appendChild(userProfile);
        main.appendChild(statOrHistoryBtnSet);
        main.appendChild(description);
        container.appendChild(navBar);
        container.appendChild(main);
        return container;
    }
}

export default ProfilePage;
