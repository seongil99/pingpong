import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import ButtonToMatch from "../Components/ButtonToMatch.js";
import WaitMatchBox from "../Components/WaitMacthBox.js";
import GetCurrentUserGameStatus from "../Controller/Game/GetCurrentUserGameStatus.js";
import getCurrentUserGameStatus from "../Controller/Game/GetCurrentUserGameStatus.js";
class MatchingPage {
    constructor(pathParam, queryParam) {
        this.socket = null;
        this.container = null;
        this.waitModal = null;
        this.matchType = null;
        this.tournamentId = null;
        this.gameId = null;
    }

    async template() {
        const navBar = NavBar();
        const title = createElement("h2", { id: "matching-page-title" }, "Matching Page");

        const pvpButton = this.createMatchButton("PVP", "waiting for PvP User");
        const tournamentButton = this.createMatchButton("tournament", "waiting for Tournament Users");
        const pveButton = this.createMatchButton("Pve", "waiting for start");

        const buttonContainer = createElement("div", { id: "match-btn-container" }, pvpButton, tournamentButton, pveButton);

        const main = createElement("main", { id: "matching-main" }, title, buttonContainer);
        this.container = createElement("div", {}, navBar, main);

        return this.container;
    }

    createMatchButton(type, waitMessage) {
        return ButtonToMatch(type, async() => {
            this.matchType = type;
            if(this.matchType ==="Pve"){
                localStorage.setItem("matchType", this.matchType);
                this.toggleButtonContainer();
                this.waitModal = this.createWaitModal(waitMessage);
                this.handleMatchFound("Pve");
                return;
            }
            else{
                if (!this.socket || this.socket.readyState === WebSocket.CLOSED) {
                    this.connectWebSocket(() => this.requestMatch());
                } else {
                    this.requestMatch();
                }
            }
            this.toggleButtonContainer();
            this.waitModal = this.createWaitModal(waitMessage);
        });
    }

    createWaitModal(message) {
        const waitBox = WaitMatchBox(message, () => {
            this.cancelMatch();
            this.toggleButtonContainer();
            waitBox.modal.dispose();
        }, this.socket);
        this.container.append(waitBox.element);
        waitBox.modal.show();
        return waitBox;
    }

    toggleButtonContainer() {
        document.getElementById("match-btn-container").classList.toggle("hide");
    }

    connectWebSocket(callback) {
        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        const endpoint =
        this.matchType === "PVP" ?
        "matchmaking" :
        "tournament/matchmaking"
        const wsUrl = `${protocol}://${window.location.host}/api/ws/${endpoint}/`;

        this.socket = new WebSocket(wsUrl);

        this.socket.onopen = () => {
            console.log("WebSocket connected.");
            callback();
        };

        this.socket.onmessage = (event) => this.handleSocketMessage(event);
        // this.socket.onclose = (event) => this.handleSocketClose(event);
        this.socket.onclose = (event) => console.log("soket was close!");
        this.socket.onerror = (error) => console.error("WebSocket error:", error);
    }

    handleSocketMessage(event) {
        const data = JSON.parse(event.data);
        console.log("Received data:", data);

        const messageHandlers = {
            "waiting_for_match": () => console.log("Waiting for opponent..."),
            "match_found": () => this.handleMatchFound(data),
            "match_canceled": () => console.log("Match canceled."),
            "error": () => console.error(`Error: ${data.message}`),
            "set_option": () => this.navigateToGame(),
            "already_joined": () => this.navigateToGame(),
            "match_waiting": () => console.log("waiting for tounament"),
        };

        (messageHandlers[data.type] || (() => console.warn("Unhandled message type:", data.type)))();
    }

    handleMatchFound(data) {
        const modal = document.getElementById("modal-body-target");
        const modalbtn = document.getElementById("modal-btn-target");
        modal.classList.add("hide");
        modalbtn.classList.add("hide");
        if (data.option_selector || this.matchType === "Pve") {
            const optionForm = document.getElementById("form-target");
            optionForm.classList.remove("hide");
            console.log('op select in this.tournamentId: ', this.tournamentId);
        }
        if (this.matchType === "Pve") return;
        localStorage.setItem("matchType", this.matchType);
        localStorage.setItem("gameId", data.game_id ? data.game_id : data.tournament_id);
        this.tournamentId = data.tournament_id;
        localStorage.setItem("tid",this.tournamentId);
        console.log(`Match found! gameId: ${localStorage.getItem("gameId")}`);

    }

    async navigateToGame() {
        if(this.waitModal){
            console.log("modal distroryd");
            this.waitModal.modal.dispose();
            this.container.removeChild(this.waitModal.element);
            this.waitModal = null;
        }
        const gameId = await getCurrentUserGameStatus();
        window.router.navigate(`/playing/${gameId.game_id}`, false);
    }
    requestMatch() {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            const message = {
                type: "request_match",
                gamemode: this.matchType === "PVP" ? "1v1" : "tournament",
            };
            this.socket.send(JSON.stringify(message));
            console.log("Match request sent:", message);
        } else {
            console.error("WebSocket is not open.");
        }
    }

    cancelMatch() {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            const message = { type: "cancel_match" };
            this.socket.send(JSON.stringify(message));
            this.socket.close();
            console.log("Match cancel request sent.", message);
        } else {
            console.error("Failed to cancel match.");
        }
    }
}

export default MatchingPage;
