import createElement from "../Utils/createElement.js";
import fetchUserProfile from "../Controller/Settings/fetchUserProfile.js";
import updateUserProfile from "../Controller/Settings/updateUserProfile.js";

const ProfileForm = async () => {
    let data = await fetchUserProfile();
    console.log(data);
    const openFileBtn = createElement(
        "button",
        {
            id: "open-file-btn",
            events: {
                click: () => {
                    const fileInput = document.getElementById("img-input");
                    fileInput.click(); // 숨겨진 파일 입력을 트리거
                },
            },
        },
        "Edit"
    );
    const imgInput = createElement(
        "input",
        {
            type: "file",
            id: "img-input",
            accept: "image/*",
            events: {
                change: (event) => {
                    const file = event.target.files[0]; // 선택된 파일 가져오기
                    if (!file || file.size > 1000000) return;
                    // 이미지 파일만 허용: MIME 타입 체크
                    if (!file.type.startsWith("image/")) {
                        alert("이미지 파일만 선택해주세요.");
                        this.value = ""; // 선택 초기화
                        return;
                    }
                    const reader = new FileReader();
                    reader.onload = () => {
                        console.log(reader.result);

                        const profileImg = document.querySelector(
                            ".settings-profile-image > img"
                        );
                        profileImg.src = reader.result;
                        data.avatar = reader.result;
                    };
                    reader.readAsDataURL(file);
                },
            },
        },
        []
    );
    const editBg = createElement(
        "button",
        { class: "edit-bg hide" },
        openFileBtn
    );
    const realImg = createElement(
        "img",
        { src: data?.avatar, alt: "Real Image" },
        []
    );
    const profileImg = createElement(
        "div",
        { class: "settings-profile-image" },
        editBg,
        realImg,
        imgInput
    );
    const usernameInfo = createElement(
        "h3",
        { class: "username-info" },
        data?.username
    );
    const usernameInput = createElement(
        "input",
        { class: "username-input hide", type: "text", maxlength: 20 },
        ""
    );
    const emailInfo = createElement(
        "span",
        { class: "email-info" },
        data?.email
    );
    const profileInfos = createElement(
        "div",
        { class: "settings-profile-infos" },
        usernameInfo,
        emailInfo
    );
    const editBtn = createElement(
        "button",
        {
            class: "settings-btn profile-edit-btn",
            events: {
                click: (event) => {
                    document
                        .querySelector(".profile-save-btn")
                        .classList.remove("hide");
                    document
                        .querySelector(".profile-cancel-btn")
                        .classList.remove("hide");
                    document.querySelector(".edit-bg").classList.remove("hide");

                    event.target.classList.add("hide");
                },
            },
        },
        "Edit"
    );
    const saveBtn = createElement(
        "button",
        {
            class: "settings-btn profile-save-btn hide",
            events: {
                click: async (event) => {
                    document
                        .querySelector(".profile-cancel-btn")
                        .classList.add("hide");
                    document
                        .querySelector(".profile-edit-btn")
                        .classList.remove("hide");
                    document.querySelector(".edit-bg").classList.add("hide");
                    updateUserProfile(data);
                    event.target.classList.add("hide");
                    data = await fetchUserProfile();
                    document.querySelector(".username-info").textContent =
                        data?.username;
                    document.querySelector(".email-info").textContent =
                        data?.email;
                    document.querySelector(
                        ".settings-profile-image > img"
                    ).textContent = data?.avatar;
                },
            },
        },
        "Save"
    );
    const cancelBtn = createElement(
        "button",
        {
            class: "settings-btn profile-cancel-btn hide",
            events: {
                click: (event) => {
                    document
                        .querySelector(".profile-save-btn")
                        .classList.add("hide");
                    document
                        .querySelector(".profile-edit-btn")
                        .classList.remove("hide");
                    document.querySelector(".edit-bg").classList.add("hide");
                    event.target.classList.add("hide");
                },
            },
        },
        "Cancel"
    );
    const profileBtnSet = createElement(
        "div",
        { class: "settings-profile-btn-set" },
        editBtn,
        saveBtn,
        cancelBtn
    );
    const profileContent = createElement(
        "div",
        { class: "settings-profile-content" },
        profileImg,
        profileInfos
    );
    const profileForm = createElement(
        "form",
        {
            class: "settings-profile-form",
            events: {
                submit: (event) => {
                    event.preventDefault();
                },
            },
        },
        profileContent,
        profileBtnSet
    );
    return profileForm;
};

export default ProfileForm;
