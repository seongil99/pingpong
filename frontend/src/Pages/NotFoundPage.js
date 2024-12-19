import createElement from "../Utils/createElement.js";

class NotFoundPage {
    template(pathParam, queryParam) {
        const aboutText = createElement("h1", {}, "404 Not Found Page");
        const container = createElement("div", {}, aboutText);
        return container; // 최종 DOM을 반환
    }
}

export default NotFoundPage;
