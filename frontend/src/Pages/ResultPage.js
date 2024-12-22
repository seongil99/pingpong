import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Common/Navbar.js";
import getTournamentData from "../Controller/Game/GetTournamentData.js";

class TournamentPage {
    async template(pathParam, queryParam) {
        const [_, path, gameId] = pathParam;
        const checkmatch = localStorage.getItem("matchType");
        if (checkmatch === "null") window.router.navigate(`/home`, false);
        const type = checkmatch === "PVP" ? "match" : "tournament";
        const data = await getTournamentData(type, gameId);
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

        const originalReplaceState = history.replaceState;
        const urlChangeEvent = new Event("urlchange");

        history.replaceState = function (...args) {
            originalReplaceState.apply(this, args);
            window.dispatchEvent(urlChangeEvent);
        };

        window.addEventListener("urlchange", (event) => {
            window.removeEventListener("urlchange");
            localStorage.setItem("matchType", "null");
            localStorage.setItem("tid", "null");
            window.router.navigate(`/home`, false);
        });
        return total;
    }

    createHeader(data) {
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
                `${localStorage.getItem("matchType")} ${i18next.t("results")}`
            ),
            createElement(
                "div",
                { class: "text-gray-600" },
                createElement(
                    "span",
                    { id: "start-date", "data-i18n": "start_date" },
                    `${i18next.t("start_date")}: ${new Date(
                        data.startDate
                    ).toLocaleString("ko-KR", { timeZone: "UTC" })}`
                ),
                " - ",
                createElement(
                    "span",
                    { id: "end-date", "data-i18n": "end_date" },
                    `${i18next.t("end_date")}: ${new Date(
                        data.endDate
                    ).toLocaleString("ko-KR", { timeZone: "UTC" })}`
                )
            )
        );
    }

    createResultsSection(data) {
        const resultsSection = createElement("section", {
            id: "results-section",
            class: "row g-4",
        });

    data.matches.forEach((match) => {
      const [player1, player2] = match.players;

            const matchCard = createElement(
                "div",
                { class: "col-lg-6" },
                createElement(
                    "div",
                    { class: "card shadow-sm p-4" },
                    createElement(
                        "h2",
                        { class: "card-title text-xl font-semibold mb-3" },
                        match.round
                    ),
                    createElement(
                        "div",
                        {
                            class: "d-flex justify-content-between align-items-center",
                        },
                        this.createPlayerInfo(
                            player1,
                            player1.status === "winner" ? true : false
                        ),
                        createElement(
                            "div",
                            {
                                class: "text-center mx-4 align-self-center font-mono",
                            },
                            createElement(
                                "span",
                                { class: "font-bold text-lg" },
                                `${player1.score} - ${player2.score}`
                            )
                        ),
                        this.createPlayerInfo(
                            player2,
                            player2.status === "winner" ? true : false
                        )
                    )
                )
            );

      resultsSection.appendChild(matchCard);
    });

    return resultsSection;
  }

    createPlayerInfo(player, isLeft) {
        return createElement(
            "div",
            { class: `d-flex ${isLeft ? "" : "text-end"} flex-column` },
            createElement(
                "p",
                { class: "font-semibold mb-0", "data-i18n": "player_name" },
                player.name
            ),
            createElement(
                "p",
                {
                    class: `mb-0 ${
                        player.status === "winner"
                            ? "text-success"
                            : "text-muted"
                    }`,
                    "data-i18n":
                        player.status === "winner" ? "winner" : "loser",
                },
                i18next.t(player.status === "winner" ? "winner" : "loser")
            )
        );
    }
}

export default TournamentPage;
