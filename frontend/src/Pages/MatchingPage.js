import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";
import ButtonToMatch from "../Components/ButtonToMatch.js";
import WaitMatchBox from "../Components/WaitMacthBox.js";

class MatchingPage {
    constructor() {
        this.socket = null;
        this.container = null;
        this.hiddenInput = null;
        this.waitModal = null;
        this.matchType = null;
        this.tournamentId = null;
    }

    async template() {
        const navBar = NavBar();
        const title = createElement("h2", { id: "matching-page-title" }, "Matching Page");
        this.hiddenInput = createElement("input", { class: "hide", id: "hidden-input", value: "none" });

        const pvpButton = this.createMatchButton("PVP", "waiting for PvP User");
        const tournamentButton = this.createMatchButton("tournament", "waiting for Tournament Users");

        const buttonContainer = createElement("div", { id: "match-btn-container" }, pvpButton, tournamentButton);

        const main = createElement("main", { id: "matching-main" }, title, buttonContainer);
        this.container = createElement("div", {}, navBar, main, this.hiddenInput);

        return this.container;
    }

    createMatchButton(type, waitMessage) {
        return ButtonToMatch(type, () => {
            this.matchType = type;
            if (!this.socket || this.socket.readyState === WebSocket.CLOSED) {
                this.connectWebSocket(() => this.requestMatch());
            } else {
                this.requestMatch();
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
        const endpoint = this.matchType === "PVP" ? "matchmaking" : this.tournamentId ? "tournament/matchmaking": `tournament/game/${this.tournamentId}/`;
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
            "set_option": () => this.navigateToGame(this.matchType ==="PVP" ? data.game_id : data.tournament_id),
            "already_joined": () => this.navigateToGame(data.game_id),
            "match_waiting": () => console.log("waiting for tounament"),
        };

        (messageHandlers[data.type] || (() => console.warn("Unhandled message type:", data.type)))();
    }

    handleMatchFound(data) {
        const modal = document.getElementById("modal-body-target");
        const modalbtn = document.getElementById("modal-btn-target");
        modal.classList.add("hide");
        modalbtn.classList.add("hide");
        if(data.option_selector){
            const optionForm = document.getElementById("form-target");
            optionForm.classList.remove("hide");
            this.hiddenInput.value = data.game_id;
        }
        console.log(`Match found! Opponent: ${data.opponent_username}`);
        if(this.type === "tournament"){
            this.tournamentId = data.tournament_id;
        }
        else
            this.hiddenInput.value = data.game_id;
    }

    navigateToGame(gameId) {
        this.waitModal.modal.dispose();
        this.container.removeChild(this.waitModal.element);
    if(this.matchType === "PVP")
        window.router.navigate(`/playing/${gameId}`, false);
    else{
        this.connectWebSocket(()=> this.requestTournamentMatch());
    }
    }
    requestTournamentMatch() {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            const message = {
                type: "ready",
            };
            this.socket.send(JSON.stringify(message));
            console.log("Match Tournamentrequest sent:", message);
        } else {
            console.error("WebSocket is not open.");
        }
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
