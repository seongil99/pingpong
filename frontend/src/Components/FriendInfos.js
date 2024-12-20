import createElement from "../Utils/createElement.js";
import DeleteFriend from "../Controller/Friends/DeleteFriends.js";

// 친구 정보를 표시하는 컴포넌트
const FriendInfos = (dataRef) => {
    console.log("dataRef: ", dataRef);

    // 친구 프로필 이미지 생성
    const friendImg = createElement("img", {
        src: dataRef.friend_user.avatar || "/src/Components/profile.png",
        alt: "Friend Avatar",
        class: "friend-img",
    });

    // 친구 ID, 이메일, 상태 정보 생성
    const userId = createElement(
        "h3",
        {
            class: "user-id",
            "data-iduser": dataRef.id || "",
            "data-id": dataRef.friend_user.id || "",
        },
        dataRef.friend_user.username || "jonghopa"
    );

    const userEmail = createElement(
        "span",
        { class: "user-email" },
        dataRef.friend_user.username || "jonghopa@student.42seoul.kr"
    );

    const userStatus = createElement(
        "span",
        { class: "user-status" },
        dataRef.friend_user.is_online ? "✅" : "❌"
    );

    // 친구 정보 상자 생성
    const infoBox = createElement(
        "div",
        { class: "friend-info" },
        userId,
        userEmail,
        userStatus
    );

    // 삭제 버튼 생성
    const deleteBtn = createElement(
        "button",
        {
            class: "friend-delete-btn",
            events: {
                click: async (event) => {
                    const friendList = document.getElementById("friends-list");
                    const id = event.target.parentElement.querySelector(".user-id");

                    console.log("삭제 요청 ID:", id.dataset.iduser);

                    try {
                        await DeleteFriend(id.dataset.iduser);
                        friendList.removeChild(event.target.parentElement);
                        console.log("삭제 성공");
                    } catch (error) {
                        console.error("삭제 실패:", error);
                    }
                },
            },
        },
        "삭제"
    );

    // 친구 정보 컨테이너 생성
    const friendInfos = createElement(
        "div",
        {
            class: "friend-infos",
            events: {
                click: (event) => {
                    if (event.target.classList.contains("friend-delete-btn")) return;
                    console.log("프로필 클릭:", event.target);
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
