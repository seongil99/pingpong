import createElement from "../../Utils/createElement.js";
import AuthenticatorGuideStep from "../Auth/AuthenticatorGuideStep.js";
import enableMfa from "../../Controller/Auth/enableMFA.js";
import fetchQRcode from "../../Controller/Auth/fetchQRCode.js";

const SettingsModal = async () => {
    const enableTitle = createElement(
        "h1",
        { class: "two-auth-enable-title" },
        i18next.t("settings_enable_2fa")
    );
    const stepOne = createElement(
        "p",
        { class: "authenticator-guide-step-content" },
        "휴대전화나 태블릿에 ",
        createElement(
            "a",
            { href: "#" },
            `Google ${i18next.t("settings_authenticator")}`
        ),
        ", ",
        createElement("a", { href: "#" }, "Duo Mobile"),
        ", ",
        createElement("a", { href: "#" }, "Authy"),
        " 또는 ",
        createElement(
            "a",
            { href: "#" },
            `Microsoft ${i18next.t("settings_authenticator")}`
        ),
        " 앱을 다운로드하여 설치합니다."
    );
    const stepTwo = createElement(
        "div",
        { class: "authenticator-guide-step-content" },
        "인증 앱을 열고 다음을 수행합니다.",
        createElement(
            "ul",
            {},
            createElement("li", {}, '앱 오른쪽 상단의 "+" 아이콘을 누릅니다.'),
            createElement(
                "li",
                {},
                "휴대전화 카메라를 사용하여 이미지를 왼쪽으로 스캔합니다."
            )
        ),
        createElement(
            "a",
            { class: "authenticator-qrcode-scan-guide" },
            "이 바코드를 스캔할 수 없나요?"
        )
    );
    const stepThree = createElement(
        "div",
        { class: "authenticator-guide-step-content" },
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
            createElement(
                "input",
                {
                    id: "otp-number-input",
                    placeholder: "코드",
                    maxlength: 6,
                    events: {
                        input: (event) => {
                            const value = event.target.value;
                            const filteredValue = value.replace(/[^0-9]/g, "");
                            if (value !== filteredValue) {
                                event.target.value = filteredValue;
                            }
                        },
                    },
                },
                ""
            ),
            createElement(
                "button",
                {
                    type: "submit",
                    class: "otp-submit-btn",
                    events: {
                        click: (event) => {
                            enableMfa(
                                document.querySelector("#otp-number-input")
                                    .value
                            );
                        },
                    },
                },
                "코드 확인 및 활성화"
            )
        )
    );
    const qrcode = createElement(
        "img",
        {
            src: "",
            alt: "2FA QR Code",
            class: "authenticator-guide-step-img",
            id: "mfa-qrcode",
        },
        []
    );
    const guide = createElement(
        "div",
        { class: "authenticator-guide" },
        AuthenticatorGuideStep(
            createElement(
                "div",
                { class: "authenticator-guide-step-img-div" },
                createElement(
                    "img",
                    {
                        src: "/src/Media/step1.png",
                        class: "authenticator-guide-step-img",
                    },
                    []
                )
            ),
            1,
            "Download App",
            stepOne
        ),
        AuthenticatorGuideStep(
            createElement(
                "div",
                { class: "authenticator-guide-step-img-div" },
                qrcode
            ),
            2,
            "Scan The QR Code",
            stepTwo
        ),
        AuthenticatorGuideStep(
            createElement(
                "div",
                { class: "authenticator-guide-step-img-div" },
                createElement(
                    "img",
                    {
                        src: "/src/Media/step3.png",
                        class: "authenticator-guide-step-img",
                    },
                    []
                )
            ),
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
                click: async () => {
                    const qrcodeImg = await fetchQRcode();
                    document
                        .querySelector(".two-auth-package")
                        .classList.add("hide");
                    document
                        .querySelector(".two-auth-authenticator-guide")
                        .classList.remove("hide");
                    document
                        .querySelector(".settings-modal-prev-btn")
                        .classList.remove("hide");
                    document.querySelector("#mfa-qrcode").src = qrcodeImg.qrcode;
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
                    document.querySelector("#otp-number-input").value = "";
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
        i18next.t("settings_modal_prev_btn")
    );
    const confirmBtn = createElement(
        "button",
        { class: "settings-modal-confirm-btn hide" },
        i18next.t("settings-modal_confirm_btn")
    );
    const cancelBtn = createElement(
        "button",
        {
            class: "settings-modal-cancel-btn",
            events: {
                click: () => {
                    document.querySelector("#otp-number-input").value = "";
                    document.querySelector(".modal").classList.add("hide");
                    document
                        .querySelector(".two-auth-package")
                        .classList.add("hide");
                    document
                        .querySelector(".two-auth-authenticator-guide")
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
        i18next.t("settings_modal_cancel_btn")
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
        settingsBtnSet
    );
    const modal = createElement("div", { class: "modal hide" }, settingsModal);
    return modal;
};

export default SettingsModal;
