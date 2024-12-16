import createElement from "../Utils/createElement.js";
import FriendInfos from "./FriendInfos.js";
// import SearchFriends from "../Controller/Friends/SearchFriends.js";
import Friendapi from "../Controller/Friends/FriendApi.js";
const FriendModal = () => {
    const profile = createElement(
        "div",
        { class: "friend-profile hide" }
    );
    const modalMessage = createElement(
        "h3",
        { class: "friend-modal-message" },
        "유저를 검색해보세요."
    );
    const searchInput = createElement("input", { class: "friend-search-input" }, "");
    const searchOrAddBtn = createElement(
        "button",
        {
            class: "search-add-btn search",
            events: {
                click: async (event) => {
                    if (event.target.classList.contains("search")) {
                        const input = document  
                        .querySelector(".friend-search-input");
                        console.log('intput',input);
                        // const data = await SearchFriends(input.value);
                        const data = await Friendapi("GET","/api/v1/users/friendable/?search=",input.value);
                        console.log(data);
                        input.classList.add("hide");
                            if (!data) {
                                event.target.classList.add("hide");
                                document.querySelector(
                                    ".friend-modal-message"
                                ).textContent = `${input.value}님이 존재하지 않거나 추가할수 없는 유저입니다.`;
                            } else {
                            const friendProfile = document
                                .querySelector(".friend-profile");
                                friendProfile.classList.remove("hide");
                            friendProfile.appendChild(FriendInfos({other_user:data}));
                                document
                                    .querySelector(".friend-modal-message")
                                    .classList.add("hide");
                                event.target.classList.remove("search");
                                event.target.classList.add("add");
                                event.target.textContent = "추가";
                            }
                    } else if (event.target.classList.contains("add")) {
                        /*
                        친구추가 부분
                        */
                        document
                        .querySelector(".friend-profile").replaceChildren(); // 검색된 유저 제거.
                    }
                    document
                        .querySelector(".cancel-modal-btn")
                        .classList.add("cancel-result");
                    document  
                    .querySelector(".friend-search-input").value = "";
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
                        .querySelector(".friend-profile").replaceChildren();
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
                    document.querySelector(".friend-modal-message").textContent =
                        "유저를 검색해보세요.";
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
