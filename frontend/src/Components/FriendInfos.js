import createElement from "../Utils/createElement.js";

// User Data Parameter 생략. API 연동 작업 때 추가 예정. 만약 추가하면 삭제 처리도 충분히 쉽게 할 수 있음
const FriendInfos = (num) => {
    const friendImg = createElement(
        "img",
        { src: "", alt: "", class: "friend-img" },
        ""
    );

    const userId = createElement("h3", { class: "user-id" }, "");
    const userEmail = createElement("span", { class: "user-email" }, "");
    const userStatus = createElement("span", { class: "user-status" }, "");
    friendImg.src = "/src/Media/profile.png";
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
    const deleteBtn = createElement(
        "button",
        {
            class: "friend-delete-btn",
            events: {
                click: (event) => {
                    console.log(event.target.parentElement.classList);
                    const friendList = document.querySelector("#friends-list");
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
                click: () => {
                    console.log(`${num}`);
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
