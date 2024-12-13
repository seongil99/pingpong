import createElement from "../Utils/createElement.js";
import AuthenticatorGuideStep from "./AuthenticatorGuideStep.js";

const SettingsModal = () => {
    const enableTitle = createElement(
        "h1",
        { class: "two-auth-enable-title" },
        "2FA Enable"
    );
    const stepOne = createElement(
        "p",
        { class: "step-one" },
        "휴대전화나 태블릿에 ",
        createElement("a", { href: "#" }, "Google 인증"),
        ", ",
        createElement("a", { href: "#" }, "Duo Mobile"),
        ", ",
        createElement("a", { href: "#" }, "Authy"),
        " 또는 ",
        createElement("a", { href: "#" }, "Microsoft 인증"),
        " 앱을 다운로드하여 설치합니다."
    );
    const stepTwo = createElement(
        "ul",
        {},
        "인증 앱을 열고 다음을 수행합니다.",
        createElement("li", {}, '앱 오른쪽 상단의 "+" 아이콘을 누릅니다.'),
        createElement(
            "li",
            {},
            "휴대전화 카메라를 사용하여 이미지를 왼쪽으로 스캔합니다."
        ),
        "(",
        createElement("a", {}, "이 바코드를 스캔할 수 없나요?"),
        ")"
    );
    const stepThree = createElement(
        "div",
        {},
        "위의 바코드가 스캔되면 앱에서 생성한 6자리 인증 코드를 입력합니다.",
        createElement(
            "form",
            {
                events: {
                    submit: (event) => {
                        event.preventDefault();
                    },
                },
            },
            createElement("input", { placeholder: "코드" }, ""),
            createElement("button", { type: "submit" }, "코드 확인 및 활성화")
        )
    );
    const guide = createElement(
        "div",
        { class: "authenticator-guide" },
        AuthenticatorGuideStep(
            "/src/Components/profile.png",
            1,
            "Download App",
            stepOne
        ),
        AuthenticatorGuideStep(
            "/src/Components/profile.png",
            2,
            "Scan The QR Code",
            stepTwo
        ),
        AuthenticatorGuideStep(
            "/src/Components/profile.png",
            3,
            "Input Authentication Code",
            stepThree
        )
    );
    const twoAuthAuthenticatorGuide = createElement(
        "div",
        { class: "two-auth-authenticator-guide hide" },
        enableTitle,
        guide
    );
    const twoAuthAuthenticatorBtn = createElement(
        "button",
        {
            class: "two-auth-authenticator-btn",
            events: {
                click: () => {
                    document
                        .querySelector(".two-auth-package")
                        .classList.add("hide");
                    document
                        .querySelector(".two-auth-authenticator-guide")
                        .classList.remove("hide");
                    document
                        .querySelector(".settings-modal-prev-btn")
                        .classList.remove("hide");
                },
            },
        },
        "Authenticator App"
    );
    const twoAuthPackage = createElement(
        "div",
        { class: "two-auth-package hide" },
        enableTitle,
        twoAuthAuthenticatorBtn
    );
    const prevBtn = createElement(
        "button",
        {
            class: "settings-modal-prev-btn hide",
            events: {
                click: (event) => {
                    document
                        .querySelector(".two-auth-authenticator-guide")
                        .classList.add("hide");
                    document
                        .querySelector(".two-auth-package")
                        .classList.remove("hide");
                    event.target.classList.add("hide");
                },
            },
        },
        "Prev"
    );
    const confirmBtn = createElement(
        "button",
        { class: "settings-modal-confirm-btn hide" },
        "Confirm"
    );
    const cancelBtn = createElement(
        "button",
        {
            class: "settings-modal-cancel-btn",
            events: {
                click: () => {
                    document.querySelector(".modal").classList.add("hide");
                    document
                        .querySelector(".two-auth-package")
                        .classList.add("hide");
                    document
                        .querySelector(".two-auth-authenticator-guide")
                        .classList.add("hide");
                    document
                        .querySelector(".inactive-account-caution")
                        .classList.add("hide");
                    document
                        .querySelector(".settings-modal-prev-btn")
                        .classList.add("hide");
                    document
                        .querySelector(".settings-modal-confirm-btn")
                        .classList.add("hide");
                },
            },
        },
        "Cancel"
    );
    const inactiveAccountCaution = createElement(
        "div",
        { class: "inactive-account-caution hide" },
        "비활성화?"
    );
    const settingsBtnSet = createElement(
        "div",
        { class: "settings-btn-set" },
        prevBtn,
        confirmBtn,
        cancelBtn
    );
    const settingsModal = createElement(
        "div",
        { class: "modal-box settings-modal" },
        twoAuthPackage,
        twoAuthAuthenticatorGuide,
        inactiveAccountCaution,
        settingsBtnSet
    );
    const modal = createElement("div", { class: "modal hide" }, settingsModal);
    return modal;
};

export default SettingsModal;
