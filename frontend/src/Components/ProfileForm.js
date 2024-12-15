import createElement from "../Utils/createElement.js";

const ProfileForm = () => {
    let data = { name: "jonghopa", email: "jonghopa@student.42seoul.kr" };
    const editIcon = createElement(
        "span",
        { style: { color: "white" } },
        "Edit"
    );
    const editBg = createElement("button", { class: "edit-bg hide" }, editIcon);
    const realImg = createElement(
        "img",
        { src: "/src/Media/profile.png", alt: "real" },
        []
    );
    const profileImg = createElement(
        "div",
        { class: "settings-profile-image" },
        editBg,
        realImg
    );
    const idText = createElement("h3", {}, "Good Boy");
    const nameInputLegend = createElement(
        "label",
        { for: "account-name" },
        "Name: "
    );
    const nameInput = createElement(
        "input",
        { type: "text", id: "account-name", value: data.name, readonly: true, maxlength: 100 },
        ""
    );
    const nameInputBox = createElement(
        "p",
        { class: "input-box" },
        nameInputLegend,
        nameInput
    );
    const emailInputLegend = createElement(
        "label",
        { for: "account-email" },
        "E-mail: "
    );
    const emailInput = createElement(
        "input",
        {
            type: "email",
            id: "account-email",
            value: data.email,
            readonly: true,
            maxlength: 254
        },
        ""
    );
    const emailInputBox = createElement(
        "p",
        { class: "input-box" },
        emailInputLegend,
        emailInput
    );
    const profileInputs = createElement(
        "div",
        { class: "settings-profile-inputs" },
        idText,
        nameInputBox,
        emailInputBox
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
                    document
                        .querySelectorAll(".input-box > input")
                        .forEach((input) => (input.readOnly = false));

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
                click: (event) => {
                    const inputs =
                        document.querySelectorAll(".input-box > input");
                    const email = inputs[1];
                    const emailRegex = /^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$/;
                    if (!emailRegex.test(email.value)) {
                        console.error("Invalid Email");
                        return;
                    }
                    // updateProfileInfos({
                    //     name: inputs[0].value,
                    //     email: inputs[1].value,
                    // });
                    data.name = inputs[0].value;
                    data.email = inputs[1].value;
                    inputs.forEach((input) => (input.readOnly = true));
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
        "Save"
    );
    const cancelBtn = createElement(
        "button",
        {
            class: "settings-btn profile-cancel-btn hide",
            events: {
                click: (event) => {
                    const inputs =
                        document.querySelectorAll(".input-box > input");
                    inputs[0].value = data.name;
                    inputs[1].value = data.email;
                    inputs.forEach((input) => (input.readOnly = true));
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
        profileInputs
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
