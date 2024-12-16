import createElement from "../Utils/createElement.js";
import verifyOTP from "../Controller/Auth/verifyOTP.js";

const AuthForm = () => {
    const codeNumbersBox = createElement(
        "div",
        { class: "code-numbers-box" },
        ""
    );
    const codeNumbers = [];
    let mask = 0;
    for (let i = 0; i < 6; i++)
        codeNumbers.push(
            createElement("input", {
                class: "code-number",
                type: "text",
                maxlength: "1",
            })
        );
    codeNumbers.forEach((elem, idx) => {
        elem.addEventListener("input", (event) => {
            const value = event.target.value;
            const filteredValue = value.replace(/[^0-9]/g, ""); // 숫자만 남김
            // 입력값이 필터링된 값과 다르면 업데이트
            if (value !== filteredValue) {
                event.target.value = filteredValue;
            }
            if (event.target.value.length) {
                mask |= 1 << idx;
                if (codeNumbers.length !== idx + 1) {
                    const nextInput = codeNumbers[idx + 1];
                    nextInput.focus();
                }
            }
        });
        elem.addEventListener("keydown", (event) => {
            if (event.key === "Backspace") {
                if (elem.value === "") {
                    const prevInput = codeNumbers[idx - 1];
                    if (prevInput) {
                        prevInput.focus();
                        prevInput.value = "";
                        mask &= ~(1 << (idx - 1));
                    }
                } else {
                    mask &= ~(1 << idx);
                }
            }
            if (event.key === "ArrowLeft") {
                const prevInput = codeNumbers[idx - 1];
                if (prevInput) {
                    prevInput.focus();
                }
            }
            if (event.key === "ArrowRight") {
                const nextInput = codeNumbers[idx + 1];
                if (nextInput) {
                    nextInput.focus();
                }
            }
        });
        codeNumbersBox.appendChild(elem);
    });

    const submitBtn = createElement(
        "button",
        {
            type: "submit",
            style: {
                color: "white",
                backgroundColor: "tomato",
            },
        },
        "Confirm"
    );
    const cancelBtn = createElement(
        "button",
        {
            class: "navigate",
            path: "/otp",
            style: {
                color: "black",
                backgroundColor: "white",
            },
        },
        "Cancel"
    );
    const errorMessage = createElement("div", { id: "error-message" }, "");
    const form = createElement(
        "form",
        {
            id: "auth-form",
            events: {
                submit: (event) => {
                    event.preventDefault();
                    const codeNumbers =
                        document.querySelectorAll(".code-number");
                    if (mask != 0b111111) {
                        console.log("Nope: ", mask);
                        return;
                    }
                    let otp = 0;
                    codeNumbers.forEach((value) => {
                        otp = otp * 10 + parseInt(value.value);
                    });
                    console.log(otp);
                    verifyOTP(otp); // Call the method to verify OTP
                    codeNumbers.forEach((value) => (value.value = ""));
                    mask = 0;
                },
            },
        },
        codeNumbersBox,
        submitBtn,
        cancelBtn,
        errorMessage
    );
    return form;
};

export default AuthForm;
