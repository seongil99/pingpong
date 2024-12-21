import createElement from "../../Utils/createElement.js";
const AuthenticatorGuideStep = (stepImg, stepNum, stepTitle, stepDescription) => {
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
