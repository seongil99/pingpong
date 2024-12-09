import createElement from "../Utils/createElement.js";
import FriendInfos from "./FriendInfos.js";
// const fetchFriendsInfo = async () => {
//     const url = "https://localhost/api/v1/users/friends";
//     try {
//         const response = await fetch(url, {
//             method: "GET",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//         });
//         if (!response.ok) {
//             throw new Error("Not OK! Status Code: ", response.status);
//         }
//         return await response.json().results;
//     } catch (error) {
//         console.error("Error: ", error);
//     }
// };

function FriendList() {
    // const friendsInfo = fetchFriendsInfo();

    // for (let info of friendsInfo) {
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
