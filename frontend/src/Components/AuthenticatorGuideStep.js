import createElement from "../Utils/createElement.js";
const AuthenticatorGuideStep = (img, stepNum, stepTitle, stepDescription) => {
    const stepImg = createElement(
        "img",
        { src: img, style: { width: "100px", height: "100px" } },
        []
    );
    const num = createElement(
        "span",
        { class: "authenticator-guide-step-number" },
        `STEP ${stepNum}`
    );
    const title = createElement(
        "h3",
        { class: "authenticator-guide-step-title" },
        stepTitle
    );
    const description = createElement(
        "p",
        { class: "authenticator-guide-step-description" },
        stepDescription
    );
    const stepContent = createElement(
        "div",
        { class: "authenticator-guide-step-content" },
        num,
        title,
        description
    );
    const step = createElement(
        "div",
        { class: "authenticator-guide-step" },
        stepImg,
        stepContent
    );
    return step;
};

export default AuthenticatorGuideStep;
