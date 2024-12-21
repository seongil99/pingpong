import createElement from "../../Utils/createElement.js";
import fetchUserProfile from "../../Controller/Settings/fetchUserProfile.js";
import UpdateUserProfile from "../../Controller/Settings/UpdateUserProfile.js";

const ProfileForm = async () => {
    let data = await fetchUserProfile();
    const openFileBtn = createElement(
        "button",
        {
            id: "open-file-btn",
            events: {
                click: () => {
                    const fileInput = document.getElementById(
                        "edit-profile-img-input"
                    );
                    fileInput.click(); // 숨겨진 파일 입력을 트리거
                },
            },
        },
        "Edit"
    );
    const editProfileImgInput = createElement(
        "input",
        {
            type: "file",
            id: "edit-profile-img-input",
            accept: "image/*",
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
        { id: "edit-profile-image", src: data?.avatar, alt: "Real Image" },
        []
    );
    const profileImg = createElement(
        "div",
        { class: "settings-profile-image" },
        editBg,
        realImg,
        editProfileImgInput
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
        usernameInput,
        emailInfo
    );
    const editBtn = createElement(
        "button",
        {
            type: "button",
            class: "settings-btn profile-edit-btn",
            id : "btn_edit",
            events: {
                click: (event) => {
                    document
                        .querySelector(".username-input")
                        .classList.remove("hide");
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
        i18next.t("btn_edit")
    );
    const allSettingsBtns = document.querySelectorAll(".settings-btn");
    allSettingsBtns.forEach((value) => {
        value.addEventListener("click", (event) => {
            if (event.target.classList.contains("profile-save-btn")) {
                return true;
            } else {
                return false;
            }
        });
    });
    const saveBtn = createElement(
        "button",
        {
            type: "submit",
            class: "settings-btn profile-save-btn hide",
            id: "save-id-btn",
            events: {
                click: async (event) => {
                    document
                        .querySelector(".username-input")
                        .classList.add("hide");
                    document
                        .querySelector(".profile-cancel-btn")
                        .classList.add("hide");
                    document
                        .querySelector(".profile-edit-btn")
                        .classList.remove("hide");
                    document.querySelector(".edit-bg").classList.add("hide");
                    event.target.classList.add("hide");
                },
            },
        },
        i18next.t("save-id-btn")
    );
    const cancelBtn = createElement(
        "button",
        {
            type: "button",
            class: "settings-btn profile-cancel-btn hide",
            id : "btn_cancel",
            events: {
                click: (event) => {
                    document
                        .querySelector(".profile-save-btn")
                        .classList.add("hide");
                    document
                        .querySelector(".profile-edit-btn")
                        .classList.remove("hide");
                    document.querySelector(".edit-bg").classList.add("hide");
                    document
                        .querySelector(".username-input")
                        .classList.add("hide");
                    event.target.classList.add("hide");
                },
            },
        },
        i18next.t("btn_cancel")
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
            enctype: "multipart/form-data",
            id: "edit-profile-image-form",
            events: {
                submit: async (event) => {
                    event.preventDefault();
                    const formData = new FormData();
                    const selectedImage = document.getElementById(
                        "edit-profile-img-input"
                    ).files[0];
                    const usernameInput =
                        document.querySelector(".username-input").value;
                    if (selectedImage !== undefined) {
                        formData.append("avatar", selectedImage);
                    }
                    if (usernameInput.length > 4) {
                        formData.append("username", usernameInput);
                    }
                    const userData = await UpdateUserProfile(formData);
                    console.log(userData);
                    document.querySelector(
                        "#edit-profile-image"
                    ).src = `${userData.avatar}`;
                    document.querySelector(".username-info").textContent =
                        userData.username;
                    document.querySelector(".username-input").value = "";
                },
            },
        },
        profileContent,
        profileBtnSet
    );
    return profileForm;
};

export default ProfileForm;
