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

function FriendItem(user) {
    const li = document.createElement("li");
    li.classList.add("friend-item");

    const editCheckbox = document.createElement("input");
    editCheckbox.setAttribute("type", "checkbox");
    editCheckbox.setAttribute("name", "jonghopa");

    const friendImg = document.createElement("img");
    friendImg.setAttribute("src", "/src/Components/profile.png");
    friendImg.setAttribute("alt", "tokikikki");

    const infoBox = document.createElement("div");
    infoBox.classList.add("friend-info");
    const userid = document.createElement("h3");
    userid.textContent = "jonghopa";
    const email = document.createElement("span");
    email.textContent = "jonghopa@student.42seoul.kr";
    const status = document.createElement("span");
    // status.textContent = user.is_online ? "✅" : "❌";
    status.textContent = "✅";
    infoBox.appendChild(userid);
    infoBox.appendChild(email);
    infoBox.appendChild(status);

    li.appendChild(friendImg);
    li.appendChild(infoBox);

    return li;
}

function FriendList() {
    // const friendsInfo = fetchFriendsInfo();
    const friends = document.createElement("div");
    friends.setAttribute("id", "friends");
    friends.classList.add("hide");

    const friendsList = document.createElement("ul");
    friendsList.setAttribute("id", "friends-list");
    // for (let info of friendsInfo) {
    //     console.log(info);
    //     const friendUser = info["other_user"];
    //     const item = FriendItem(friendUser);
    //     FriendList.appendChild(item);
    // }
    const friendItem = FriendItem();
    const friendItem2 = FriendItem();
    const friendItem3 = FriendItem();
    friendsList.appendChild(friendItem);
    friendsList.appendChild(friendItem2);
    friendsList.appendChild(friendItem3);

    const friendsManagement = document.createElement("div");
    friendsManagement.setAttribute("id", "friends-management");
    const friendAppendBtn = document.createElement("button");
    friendAppendBtn.textContent = "친구추가";
    const friendEditBtn = document.createElement("button");
    friendEditBtn.textContent = "친구편집";
    friendsManagement.appendChild(friendAppendBtn);
    friendsManagement.appendChild(friendEditBtn);

    friends.appendChild(friendsList);
    friends.appendChild(friendsManagement);
    return friends;
}

export default FriendList;
