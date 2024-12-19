import createElement from "../Utils/createElement.js";
import DeleteFriend from "../Controller/Friends/DeleteFriends.js";
import DeleteFriend from "../Controller/Friends/DeleteFriends.js";

// User Data Parameter 생략. API 연동 작업 때 추가 예정. 만약 추가하면 삭제 처리도 충분히 쉽게 할 수 있음
const FriendInfos = (dataRef) => {
    console.log("dataRef: ", dataRef);
    const friendImg = createElement(
        "img",
        { src: "", alt: "", class: "friend-img" },
        ""
    );

    const userId = createElement("h3", { class: "user-id" }, "");
    const userEmail = createElement("span", { class: "user-email" }, "");
    const userStatus = createElement("span", { class: "user-status" }, "");
    friendImg.src = dataRef.friend_user.avatar ||"/src/Components/profile.png";
    userId.textContent = dataRef.friend_user.username || "jonghopa";
    userId.dataset.iduser = dataRef.id || null;
    userId.dataset.id = dataRef.friend_user.id || null;
    userEmail.textContent =  dataRef.friend_user.username || "jonghopa@student.42seoul.kr";
    userStatus.textContent = dataRef.friend_user.is_online ? "✅" : "❌";
    // status.textContent = user.is_online ? "✅" : "❌";
    const infoBox = createElement(
        "div",
        { class: "friend-info" },
        userId,
        userEmail,
        userStatus
    );
    const deleteBtn = createElement(
        "button",
        {
            class: "friend-delete-btn",
            events: {
                click: async (event) => {
                    const friendList = document.getElementById("friends-list");
                    const id = event.target.parentElement.querySelector('h3');
                    console.log('friendList: ', friendList);
                    console.log('삭제',event.target.parentElement);
                    await DeleteFriend(id.dataset.iduser);
                    friendList.removeChild(event.target.parentElement);
                },
            },
        },
        "삭제"
    );
    const friendInfos = createElement(
        "div",
        {
            class: `friend-infos`,
            events: {
                // 클릭 시 해당 유저 프로필 페이지 이동
                click: (event) => {
                    console.log(event.target.classList);
                    if(event.target.classList.contains("friend-delete-btn")) return;
                    console.log('삭제아님',event);
                },
            },
        },
        friendImg,
        infoBox,
        deleteBtn
    );
    return friendInfos;
};

export default FriendInfos;
