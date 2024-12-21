import createElement from "../../Utils/createElement.js";
import FetchFriends from "../../Controller/Friends/FetchFriends.js";
import FriendInfos from "./FriendInfos.js";
async function FriendList() {
    const userData = await FetchFriends();
    console.log("user data", userData);
    const friendsList = createElement(
        "div",
        { id: "friends-list" },
        ...userData.map((v) => FriendInfos(v))
    );
    const friendAppendBtn = createElement(
        "button",
        {
            events: {
                click: () => {
                    if (
                        document
                            .querySelector(".modal")
                            .classList.contains("hide")
                    ) {
                        console.log("clicked");
                        document
                            .querySelector(".modal")
                            .classList.remove("hide");
                    }
                },
            },
            id: "addFriend-btn",
        },
        i18next.t("addFriend-btn")
    );
    const friendsManagement = createElement(
        "div",
        { id: "friends-management" },
        friendAppendBtn
    );

    const friends = createElement(
        "div",
        { id: "friends", class: "hide" },
        friendsList,
        friendsManagement
    );
    return friends;
}

export default FriendList;
