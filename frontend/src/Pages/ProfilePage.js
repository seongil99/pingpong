import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Common/Navbar.js";
import FetchUserData from "../Controller/Profile/FetchUserData.js";
import FetchOneUserGameHistory from "../Controller/Profile/FetchOneUserGameHistory.js";
import fetchUserProfile from "../Controller/Settings/fetchUserProfile.js";
import ScoreChart from "../Components/Profile/ScoreChart.js";
import calculateDiffDate from "../Utils/calculateDiffDate.js";
import StatDescription from "../Components/Profile/StatDescription.js";
import UserProfile from "../Components/Profile/UserProfile.js";

class ProfilePage {
    #offset;
    #limit;
    #gameTotalCount;
    #currentHistoryPage;
    #currentHistoryPagesBlock;
    #pageListContent = [];
    #pageNumBtns = [];
    #pagesBlocks = [];
    #descriptionSet;
    #currentDescription;

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
            session.tournament_id ? "토너먼트" : "PVP"
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

    #HistorySessionMatchDashboard = async (session) => {
        const scoreTitle = createElement(
            "h3",
            { class: "history-session-match-dashboard-title" },
            "Score"
        );
        const scoreChart = await ScoreChart(session);
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

    #HistorySessionTournamentDashboard = async (session) => {
        const tournamentData = await fetchUserTournamentData(
            session.tournament_id
        );
        const tournament = createElement(
            "div",
            { class: "history-session-tournamenet-dashboard" },
            []
        );
        const matchesDiv = createElement(
            "div",
            { class: "history-session-matches-div" },
            []
        );
        tournamentData.sessions.map(async v => {
            const match = await this.#HistorySessionMatchDashboard(v.session);
            matchesDiv.appendChild(match);
        })
        tournament.appendChild(matchesDiv);
        return tournament;
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

    #Pagination = async (userHistoryData, userid) => {
        const pagination = createElement(
            "div",
            { id: "history-description-pagination" },
            []
        );
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
                if (sessionData.ended_at !== null) {
                    const session = await this.#HistorySession(
                        sessionData,
                        userid
                    );
                    let sessionDashboard = "";
                    if (sessionData.gamemode === "PVP") {
                        sessionDashboard =
                            await this.#HistorySessionMatchDashboard(
                                sessionData,
                                j
                            );
                    } else {
                        sessionDashboard =
                            await this.#HistorySessionTournamentDashboard(
                                sessionData,
                                j
                            );
                    }
                    content.appendChild(session);
                    content.appendChild(sessionDashboard);
                }
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
                                }&limit=${this.#limit}`,
                                window.location.origin +
                                    `/profile/${userid}/history?offset=${
                                        this.#offset
                                    }&limit=${this.#limit}`
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
                                }&limit=${this.#limit}`,
                                window.location.origin +
                                    `/profile/${userid}/history?offset=${
                                        this.#offset
                                    }&limit=${this.#limit}`
                            );
                        }
                    },
                },
            },
            ">"
        );
        pagination.append(leftBtn);
        pagination.append(pageNumsDiv);
        pagination.append(rightBtn);
        return pagination;
    };

    #HistoryDescription = async (userHistoryData, userid) => {
        const historyScrollDiv = createElement(
            "div",
            { id: "history-scroll-div" },
            []
        );
        const history = createElement("div", { id: "history-description" }, []);
        const pagination = await this.#Pagination(userHistoryData, userid);
        const historyList = createElement(
            "ul",
            { id: "history-description-list" },
            this.#pageListContent[this.#currentHistoryPage - 1]
        );
        historyScrollDiv.appendChild(historyList);
        history.appendChild(historyScrollDiv);
        history.appendChild(pagination);
        return history;
    };

    #StatOrHistoryBtnSet = (userid) => {
        const statBtn = createElement(
            "button",
            {
                class: "profile-btn",
                events: {
                    click: () => {
                        const description = document.querySelector(
                            "#profile-stat-or-history-description"
                        );
                        description.removeChild(description.firstElementChild);
                        description.appendChild(this.#descriptionSet[0]);
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
                        const description = document.querySelector(
                            "#profile-stat-or-history-description"
                        );
                        description.removeChild(description.firstElementChild);
                        description.appendChild(this.#descriptionSet[1]);
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
        this.#gameTotalCount = 0;
        userHistoryData.results.map(
            (v) => (this.#gameTotalCount += v.ended_at !== null)
        );
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
        const user =
            pathParam.length === 2
                ? await fetchUserProfile()
                : await FetchUserData(parseInt(userId));
        const userHistoryData = await FetchOneUserGameHistory(user.id);
        this.#validateQueryParam(userHistoryData, queryParam);
        const historyDescription = await this.#HistoryDescription(
            userHistoryData,
            user.id
        );
        this.#descriptionSet = [
            StatDescription(userHistoryData, user.id),
            historyDescription,
        ];
        const container = createElement("div", {}, []);
        const main = createElement("main", { id: "profile-main" }, []);
        const navBar = NavBar();
        const profileTitle = createElement(
            "h1",
            { class: "profile-title" },
            `${user.username}님의 프로필`
        );
        const userProfile = UserProfile(user);
        const statOrHistoryBtnSet = this.#StatOrHistoryBtnSet(user.id);
        this.#currentDescription =
            info !== "history"
                ? this.#descriptionSet[0]
                : this.#descriptionSet[1];
        const description = createElement(
            "div",
            {
                id: "profile-stat-or-history-description",
            },
            this.#currentDescription
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
