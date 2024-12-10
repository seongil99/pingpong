import createElement from "../Utils/createElement.js";
import FriendInfos from "./FriendInfos.js";

function FriendList() {
    // const friendsInfos = fetchFriends();

    // for (let info of friendsInfos) {
    //     console.log(info);
    //     const friendUser = info["other_user"];
    //     const infos = FriendItem(friendUser);
    //     FriendList.appendChild(infos);
    // }
    const friendsList = createElement(
        "div",
        { id: "friends-list" },
        FriendInfos(),
        FriendInfos(),
        FriendInfos()
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
                        document
                            .querySelector(".modal")
                            .classList.remove("hide");
                    }
                },
            },
        },
        "친구추가"
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
