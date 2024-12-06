const fetchFriendsInfo = async () => {
    const url = "https://localhost/api/v1/users/friends";
    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });
        if (!response.ok) {
            throw new Error("Not OK! Status Code: ", response.status);
        }
        return await response.json().results;
    } catch (error) {
        console.error("Error: ", error);
    }
};

function FriendItem(user) {
    const li = document.createElement("li");
    li.classList.add("friend-item");

    const friendImg = document.createElement("img");
    friendImg.setAttribute("src", user.avatar);
    friendImg.setAttribute("alt", "profile picture");

    const infoBox = document.createElement("div");
    infoBox.classList.add("friend-info");
    const email = document.createElement("h3");
    email.textContent = user.email;
    const status = document.createElement("span");
    status.textContent = user.is_online ? "✅" : "❌";
    infoBox.appendChild(email);
    infoBox.appendChild(status);

    li.appendChild(friendImg);
    li.appendChild(infoBox);

    return li;
}

function FriendList() {
    const friendsInfo = fetchFriendsInfo();
    const friends = document.createElement("div");
    friends.setAttribute("id", "friends");

    const friendsList = document.createElement("ul");
    friendsList.setAttribute("id", "friends-list");
    for (let info of friendsInfo) {
        console.log(info);
        const friendUser = info["other_user"];
        const item = FriendItem(friendUser);
        FriendList.appendChild(item);
    }

    friends.appendChild(friendsList);
    return friends;
}

export default FriendList;
