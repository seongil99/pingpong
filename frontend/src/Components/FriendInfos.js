import createElement from "../Utils/createElement.js";

function FriendInfos() {
    const friendImg = createElement(
        "img",
        { src: "", alt: "", class: "friend-img" },
        ""
    );

    const userId = createElement("h3", { class: "user-id" }, "");
    const userEmail = createElement("span", { class: "user-email" }, "");
    const userStatus = createElement("span", { class: "user-status" }, "");
    friendImg.src = "/src/Components/profile.png";
    userId.textContent = "jonghopa";
    userEmail.textContent = "jonghopa@student.42seoul.kr";
    userStatus.textContent = "✅";
    // status.textContent = user.is_online ? "✅" : "❌";
    const infoBox = createElement(
        "div",
        { class: "friend-info" },
        userId,
        userEmail,
        userStatus
    );
    const friendInfos = createElement(
        "div",
        { class: "friend-infos" },
        friendImg,
        infoBox
    );
    return friendInfos;
}

export default FriendInfos;
