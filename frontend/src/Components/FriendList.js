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
        {
            id: "friends-list",
        },
        FriendInfos(1),
        FriendInfos(2),
        FriendInfos(3),
        FriendInfos(4),
        FriendInfos(5),
        FriendInfos(6),
        FriendInfos(7),
        FriendInfos(8),
        FriendInfos(9),
        FriendInfos(10),
        FriendInfos(11),
        FriendInfos(12),
        FriendInfos(13),
        FriendInfos(14),
        FriendInfos(15)
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
