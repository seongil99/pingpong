import createElement from "../Utils/createElement.js";
import FriendInfos from "./FriendInfos.js";

const FriendModal = () => {
    const profile = createElement(
        "div",
        { class: "friend-profile hide" },
        FriendInfos()
    );
    const modalMessage = createElement(
        "h3",
        { class: "friend-modal-message" },
        "유저를 검색해보세요."
    );
    const searchInput = createElement(
        "input",
        { class: "friend-search-input" },
        ""
    );
    const searchOrAddBtn = createElement(
        "button",
        {
            class: "search-add-btn search",
            events: {
                click: (event) => {
                    if (event.target.classList.contains("search")) {
                        const data = null;
                        document
                            .querySelector(".friend-search-input")
                            .classList.add("hide");
                        if (!data) {
                            event.target.classList.add("hide");
                            document.querySelector(
                                ".friend-modal-message"
                            ).textContent = `${
                                document.querySelector(".friend-search-input")
                                    .value
                            }님이 존재하지 않습니다.`;
                        } else {
                            document.querySelector(".friend-img").src =
                                data.img;
                            document.querySelector(".user-id").textContent =
                                data.id;
                            document.querySelector(".user-email").textContent =
                                data.email;
                            document.querySelector(".user-status").textContent =
                                data.status;
                            document
                                .querySelector(".friend-profile")
                                .classList.remove("hide");
                            if (data.added) {
                                event.target.classList.add("hide");
                                document.querySelector(
                                    ".friend-modal-message"
                                ).textContent = "이미 등록된 친구입니다.";
                            } else {
                                document
                                    .querySelector(".friend-modal-message")
                                    .classList.add("hide");
                                event.target.classList.remove("search");
                                event.target.classList.add("add");
                                event.target.textContent = "추가";
                            }
                        }
                    } else if (event.target.classList.contains("add")) {
                    }
                    document
                        .querySelector(".cancel-modal-btn")
                        .classList.add("cancel-result");
                    document.querySelector(".friend-search-input").value = "";
                },
            },
        },
        "검색"
    );
    const cancelBtn = createElement(
        "button",
        {
            class: "cancel-modal-btn",
            events: {
                click: (event) => {
                    if (event.target.classList.contains("cancel-result")) {
                        document
                            .querySelector(".friend-profile")
                            .classList.add("hide");
                        document
                            .querySelector(".friend-modal-message")
                            .classList.remove("hide");
                        document
                            .querySelector(".friend-search-input")
                            .classList.remove("hide");
                        event.target.classList.remove("cancel-result");
                        event.target.classList.add("cancel-model-btn");
                        document
                            .querySelector(".search-add-btn")
                            .classList.add("search");
                        document.querySelector(".search-add-btn").textContent =
                            "검색";
                        document
                            .querySelector(".search-add-btn")
                            .classList.remove("add", "hide");
                        document
                            .querySelector(".friend-modal-message")
                            .classList.remove("hide");
                    } else if (
                        event.target.classList.contains("cancel-modal-btn")
                    ) {
                        document.querySelector(".modal").classList.add("hide");
                    }
                    document.querySelector(".friend-search-input").value = "";
                    document.querySelector(
                        ".friend-modal-message"
                    ).textContent = "유저를 검색해보세요.";
                },
            },
        },
        "취소"
    );
    const buttonSet = createElement(
        "div",
        { class: "button-set" },
        searchOrAddBtn,
        cancelBtn
    );
    const friendModal = createElement(
        "div",
        { class: "modal-box friend-modal" },
        profile,
        modalMessage,
        searchInput,
        buttonSet
    );
    const modal = createElement("div", { class: "modal hide" }, friendModal);
    return modal;
};

export default FriendModal;
