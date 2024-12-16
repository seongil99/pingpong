import createElement from "../Utils/createElement.js";
import FriendInfos from "./FriendInfos.js";
// import FetchFriends from "../Controller/Friends/FetchFriends.js";
import Friendapi from "../Controller/Friends/FriendApi.js";
async function FriendList() {
    // const userData = await FetchFriends();
    const userData = await Friendapi('GET',"/api/v1/users/friends");
    console.log('user data',userData);
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
