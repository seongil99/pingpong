import createElement from "../../Utils/createElement.js";

const UserProfile = (userData) => {
    const profileUserImg = createElement(
        "img",
        {
            class: "profile-user-img",
            src: `${userData.avatar}`,
            alt: `${userData.username}'s profile image`,
        },
        []
    );
    const profileUserName = createElement(
        "h3",
        { class: "profile-user-name" },
        `${userData.username}`
    );
    const profileUserEmail = createElement(
        "span",
        { class: "profile-user-email" },
        `${userData.email}`
    );
    const profileUserInfos = createElement(
        "div",
        { class: "profile-user-infos" },
        profileUserName,
        profileUserEmail
    );
    const userProfile = createElement(
        "div",
        { class: `profile-user-profile ${userData.username}` },
        profileUserImg,
        profileUserInfos
    );
    return userProfile;
};
export default UserProfile;
