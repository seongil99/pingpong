import createElement from "../Utils/createElement.js";
import NavBar from "../Components/Navbar.js";

class NotFoundPage {
    template() {
        const navBar = NavBar();
        const aboutText = createElement("h1", {}, "404 Not Found Page");
        const container = createElement("div", {}, navBar, aboutText);
        return container; // 최종 DOM을 반환
    }
}

export default NotFoundPage;
