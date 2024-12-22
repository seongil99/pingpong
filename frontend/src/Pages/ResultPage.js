import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Common/Navbar.js";
import getTournamentData from "../Controller/Game/GetTournamentData.js";

class TournamentPage {
    async template(pathParam, queryParam) {
        // 1) pathParam이 정상인지 확인
        if (!pathParam || pathParam.length < 2) {
            console.error("Invalid pathParam:", pathParam);
            // 상황에 따라 홈으로 리다이렉트
            window.router.navigate(`/home`, false);
            return createElement("div", {}, "Invalid parameters.");
        }

        const [_, path, gameId] = pathParam;
        // gameId가 없으면 예외 처리
        if (!gameId) {
            console.error("Game ID is missing.");
            window.router.navigate(`/home`, false);
            return createElement("div", {}, "No Game ID provided.");
        }

        // 2) localStorage 값 확인
        const checkmatch = localStorage.getItem("matchType");
        if (!checkmatch || checkmatch === "null") {
            // 예외 처리: 매칭 타입이 null이면 홈으로 이동
            window.router.navigate(`/home`, false);
            return createElement("div", {}, "Invalid match type.");
        }

        // 3) match/tournament 타입 결정
        const type = checkmatch === "PVP" ? "match" : "tournament";

        // 4) getTournamentData 호출 및 예외 처리
        let data = null;
        try {
            data = await getTournamentData(type, gameId);
        } catch (error) {
            console.error("Error fetching tournament data:", error);
            window.router.navigate(`/home`, false);
            return createElement("div", {}, "Failed to load tournament data.");
        }

        if (!data) {
            console.error("No tournament data received.");
            window.router.navigate(`/home`, false);
            return createElement("div", {}, "Tournament data is null or undefined.");
        }

        // data.matches가 배열인지 확인
        if (!Array.isArray(data.matches)) {
            console.error("Invalid matches in data:", data.matches);
            window.router.navigate(`/home`, false);
            return createElement("div", {}, "Matches data is invalid.");
        }

        // 5) UI 생성
        const navicontainer = createElement("div", {}, NavBar());
        const header = this.createHeader(data);
        const resultsSection = this.createResultsSection(data);

        const main = createElement(
            "div",
            { id: "tournament-results", class: "container py-5" },
            header,
            resultsSection
        );
        const total = createElement("div", {}, navicontainer, main);

        // ReplaceState 관련 로직: URL 변경 감지
        const originalReplaceState = history.replaceState;
        const urlChangeEvent = new Event("urlchange");

        history.replaceState = function (...args) {
            originalReplaceState.apply(this, args);
            window.dispatchEvent(urlChangeEvent);
        };

        window.addEventListener("urlchange", (event) => {
            // 이벤트 리스너 제거 (중복 방지)
            window.removeEventListener("urlchange", arguments.callee, false);

            localStorage.setItem("matchType", "null");
            localStorage.setItem("tid", "null");
            window.router.navigate(`/home`, false);
        });

        return total;
    }

    createHeader(data) {
        // data.startDate, data.endDate가 없을 수 있으므로 방어 코드 추가
        const startDate = data.startDate ? new Date(data.startDate) : null;
        const endDate = data.endDate ? new Date(data.endDate) : null;

        return createElement(
            "header",
            { class: "text-center mb-5" },
            createElement(
                "h1",
                {
                    id: "header-title",
                    class: "text-3xl font-bold mb-3",
                    "data-i18n": "results_title",
                },
                // localStorage가 null이 아닐 때만 표시
                `${localStorage.getItem("matchType") || ""} ${i18next.t("results")}`
            ),
            createElement(
                "div",
                { class: "text-gray-600" },
                createElement(
                    "span",
                    { id: "start-date", "data-i18n": "start_date" },
                    // 날짜가 null이면 대안 메시지
                    startDate
                        ? `${i18next.t("start_date")}: ${startDate.toLocaleString("ko-KR", { timeZone: "UTC" })}`
                        : "No start date"
                ),
                " - ",
                createElement(
                    "span",
                    { id: "end-date", "data-i18n": "end_date" },
                    endDate
                        ? `${i18next.t("end_date")}: ${endDate.toLocaleString("ko-KR", { timeZone: "UTC" })}`
                        : "No end date"
                )
            )
        );
    }

    createResultsSection(data) {
        // 이미 data.matches가 배열임을 확인했지만, 한 번 더 방어 코딩
        if (!Array.isArray(data.matches)) {
            return createElement("div", {}, "No matches found.");
        }

        const resultsSection = createElement("section", {
            id: "results-section",
            class: "row g-4",
        });

        data.matches.forEach((match, index) => {
            // match가 객체이고, players 배열인지 확인
            if (!match || !Array.isArray(match.players)) {
                console.warn(`Invalid match at index ${index}:`, match);
                return; // 건너뛰기
            }

            const [player1, player2] = match.players;

            // player1, player2가 제대로 있는지 확인
            if (!player1 || !player2) {
                console.warn(`One or both players are missing in match at index ${index}.`, match.players);
                return;
            }

            // player1.score, player2.score, match.round 등이 제대로 있는지
            const p1Score = typeof player1.score === "number" ? player1.score : "?";
            const p2Score = typeof player2.score === "number" ? player2.score : "?";
            const roundName = match.round || `Round ${index + 1}`;

            const matchCard = createElement(
                "div",
                { class: "col-lg-6" },
                createElement(
                    "div",
                    { class: "card shadow-sm p-4" },
                    createElement(
                        "h2",
                        { class: "card-title text-xl font-semibold mb-3" },
                        roundName
                    ),
                    createElement(
                        "div",
                        {
                            class: "d-flex justify-content-between align-items-center",
                        },
                        this.createPlayerInfo(
                            player1,
                            player1.status === "winner"
                        ),
                        createElement(
                            "div",
                            {
                                class: "text-center mx-4 align-self-center font-mono",
                            },
                            createElement(
                                "span",
                                { class: "font-bold text-lg" },
                                `${p1Score} - ${p2Score}`
                            )
                        ),
                        this.createPlayerInfo(
                            player2,
                            player2.status === "winner"
                        )
                    )
                )
            );

            resultsSection.appendChild(matchCard);
        });

        return resultsSection;
    }

    createPlayerInfo(player, isLeft) {
        // player가 존재하는지, name, status가 있는지 확인
        if (!player) {
            return createElement("div", {}, "No player data.");
        }

        const playerName = player.name || "Unknown";
        const isWinner = player.status === "winner";
        const i18nKey = isWinner ? "winner" : "loser";

        return createElement(
            "div",
            { class: `d-flex ${isLeft ? "" : "text-end"} flex-column` },
            createElement(
                "p",
                { class: "font-semibold mb-0", "data-i18n": "player_name" },
                playerName
            ),
            createElement(
                "p",
                {
                    class: `mb-0 ${
                        isWinner ? "text-success" : "text-muted"
                    }`,
                    "data-i18n": i18nKey,
                },
                i18next.t(i18nKey)
            )
        );
    }
}

export default TournamentPage;
