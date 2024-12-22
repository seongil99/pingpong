import createElement from "../../Utils/createElement.js";
import FriendInfos from "./FriendInfos.js";
import SearchFriends from "../../Controller/Friends/SearchFriends.js";
import AppendFriends from "../../Controller/Friends/AppendFriends.js";
import FetchFriends from "../../Controller/Friends/FetchFriends.js";

async function appendFriend(target, list) {
    const ret = await FetchFriends();
    ret.map((v) => {
        if (v.friend_user.id === target.id) {
            list.appendChild(FriendInfos(v));
        }
    });
}

const FriendModal = () => {
    const profile = createElement("div", { class: "friend-profile hide" });

    const modalMessage = createElement(
        "h3",
        { class: "friend-modal-message" },
        i18next.t("friend_modal_message")
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
                click: async (event) => {
                    if (event.target.classList.contains("search")) {
                        const input = document.querySelector(
                            ".friend-search-input"
                        );
                        const data = await SearchFriends(input.value);

                        input.classList.add("hide");
                        if (!data.length) {
                            event.target.classList.add("hide");
                            document.querySelector(
                                ".friend-modal-message"
                            ).textContent = i18next.t("friend_not_found", {
                                username: input.value,
                            });
                        } else {
                            const friendProfile =
                                document.querySelector(".friend-profile");
                            friendProfile.classList.remove("hide");
                            friendProfile.appendChild(
                                FriendInfos({ friend_user: data[0] })
                            );
                            document
                                .querySelector(".friend-modal-message")
                                .classList.add("hide");

                            event.target.classList.remove("search");
                            event.target.classList.add("add");
                            event.target.textContent = i18next.t("friend_add");
                        }
                    } else if (event.target.classList.contains("add")) {
                        const friendList =
                            document.getElementById("friends-list");
                        const profile =
                            document.querySelector(".friend-profile");
                        const userId = profile.querySelector(".user-id");
                        const username = userId.getAttribute("data-id");

                        const result = await AppendFriends(username);
                        friendList.appendChild(FriendInfos(result));

                        profile.replaceChildren();
                        document.querySelector(".modal").classList.add("hide");
                        document
                            .querySelector(".friend-modal-message")
                            .classList.remove("hide");
                        document
                            .querySelector(".friend-search-input")
                            .classList.remove("hide");

                        event.target.textContent = i18next.t("friend_search");
                        event.target.classList.remove("add");
                        event.target.classList.add("search");
                    }
                    document
                        .querySelector(".cancel-modal-btn")
                        .classList.add("cancel-result");
                    document.querySelector(".friend-search-input").value = "";
                },
            },
        },
        i18next.t("friend_search")
    );

    const cancelBtn = createElement(
        "button",
        {
            class: "cancel-modal-btn",
            events: {
                click: (event) => {
                    const friendProfile =
                        document.querySelector(".friend-profile");

                    if (event.target.classList.contains("cancel-result")) {
                        friendProfile.replaceChildren();
                        friendProfile.classList.add("hide");
                        document
                            .querySelector(".friend-modal-message")
                            .classList.remove("hide");
                        document
                            .querySelector(".friend-search-input")
                            .classList.remove("hide");

                        event.target.classList.remove("cancel-result");
                        event.target.classList.add("cancel-modal-btn");

                        const searchBtn =
                            document.querySelector(".search-add-btn");
                        searchBtn.classList.add("search");
                        searchBtn.textContent = i18next.t("friend_search");
                        searchBtn.classList.remove("add", "hide");
                    } else if (
                        event.target.classList.contains("cancel-modal-btn")
                    ) {
                        document.querySelector(".modal").classList.add("hide");
                    }
                    document.querySelector(".friend-search-input").value = "";
                    document.querySelector(
                        ".friend-modal-message"
                    ).textContent = i18next.t("friend_modal_message");
                },
            },
        },
        i18next.t("friend_cancel")
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
