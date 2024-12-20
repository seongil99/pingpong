import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import getTournamentData from "../Controller/Game/GetTournamentData.js";
// JSON 데이터 예시
const tournamentData = {
    "eventId": 1,
    "eventType": "tournament",
    "startDate": "2024-01-15T14:00:00Z",
    "endDate": "2024-01-20T18:00:00Z",
    "matches": [
        {
            "matchId": 101,
            "round": "PlayerOne vs PlayerTwo",
            "startTime": "2024-01-15T16:00:00Z",
            "endTime": "2024-01-15T17:30:00Z",
            "players": [
                { "playerId": 1, "name": "PlayerOne", "score": 3, "status": "winner" },
                { "playerId": 2, "name": "PlayerTwo", "score": 1, "status": "loser" }
            ]
        },
        {
            "matchId": 102,
            "round": "PlayerThree vs PlayerFour",
            "startTime": "2024-01-15T18:00:00Z",
            "endTime": "2024-01-15T18:10:00Z",
            "players": [
                { "playerId": 3, "name": "PlayerThree", "score": 2, "status": "loser" },
                { "playerId": 4, "name": "PlayerFour", "score": 3, "status": "winner" }
            ]
        },
        {
            "matchId": 103,
            "round": "PlayerOne vs PlayerFour",
            "startTime": "2024-01-15T18:20:00Z",
            "endTime": "2024-01-15T18:30:00Z",
            "players": [
                { "playerId": 1, "name": "PlayerOne", "score": 2, "status": "loser" },
                { "playerId": 4, "name": "PlayerFour", "score": 3, "status": "winner" }
            ]
        }
    ]
};

class TournamentPage {
	async template(pathParam,queryParam) {
        const [_, path, gameId] = pathParam;
        const type = localStorage.getItem("matchType") === "PVP" ? 'match':'tournament';
		const data = await getTournamentData(type,gameId);  // JSON 데이터를 인스턴스 변수로 관리
		const navicontainer = createElement("div",{},NavBar()); 
        const header = this.createHeader(data);
        const resultsSection = this.createResultsSection(data);
		const main = createElement("div", { id: "tournament-results",class: "container py-5" }, header,resultsSection);
		const total = createElement("div", {},navicontainer,main); 
        return total;  // 전체 컨테이너 반환
    }

    createHeader(data) {
        return createElement(
            "header",
            { class: "text-center mb-5" },
            createElement("h1", { class: "text-3xl font-bold mb-3" }, `${localStorage.getItem("matchType")} Results`),
            createElement(
                "div",
                { class: "text-gray-600" },
                createElement("span", {}, `Start Date: ${new Date(data.startDate).toLocaleDateString()}`),
                " - ",
                createElement("span", {}, `End Date: ${new Date(data.endDate).toLocaleDateString()}`)
            )
        );
    }

    createResultsSection(data) {
        const resultsSection = createElement("section", { class: "row g-4" });

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
                        { class: "d-flex justify-content-between align-items-center" },
                        this.createPlayerInfo(player1, player1.status === 'winner'? true:false),
                        createElement(
                            "div",
                            { class: "text-center mx-4 align-self-center font-mono" },
                            createElement("span", { class: "font-bold text-lg" }, `${player1.score} - ${player2.score}`)
                        ),
                        this.createPlayerInfo(player2, player2.status === 'winner'? true:false)
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
            createElement("p", { class: "font-semibold mb-0" }, player.name),
            createElement(
                "p",
                { class: `mb-0 ${player.status === "winner" ? "text-success" : "text-muted"}` },
                player.status === "winner" ? "Winner" : "loser"
            )
        );
    }
}

export default TournamentPage;
