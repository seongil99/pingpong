import VerificationButton from "../Components/VerificationButton.js";

class AuthenticatorForm {
    create() {
        const form = document.createElement("form");
        form.setAttribute("id", "auth-form");

        const CodeNumbersBox = document.createElement("div");
        CodeNumbersBox.classList.add("code-numbers-box");
        for (let i = 0; i < 6; i++)
            CodeNumbersBox.appendChild(this.#CodeNumber());

        const submitBtn = VerificationButton("white", "tomato", "Confirm");
        submitBtn.setAttribute("type", "submit");
        form.addEventListener("submit", (event) => {
            const codeNumbers = document.querySelectorAll(".code-number");
            for (let i=0; i<codeNumbers.length; i++)
                if (codeNumbers[i].value.length != 1)
                    return ;
            event.preventDefault();
            this.#verifyOTP(); // Call the method to verify OTP
        });

        const cancelBtn = VerificationButton("black", "white", "Cancel");
        cancelBtn.classList.add("navigate");
        cancelBtn.setAttribute("path", "/verification");

        const errorMessage = document.createElement("div");
        errorMessage.setAttribute("id", "error-message");

        form.appendChild(CodeNumbersBox);
        form.appendChild(submitBtn);
        form.appendChild(cancelBtn);
        form.appendChild(errorMessage);
        return form;
    }

    #CodeNumber() {
        const codeNumber = document.createElement("input");
        codeNumber.setAttribute("type", "text");
        codeNumber.setAttribute("maxlength", "1");
        codeNumber.classList.add("code-number");
        return codeNumber;
    }

    async #verifyOTP() {
        const otp = document.getElementById("otp").value;

        try {
            const response = await fetch(
                "/api/v1/users/accounts/mfa/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ otp }),
                }
            );
            const data = await response.json();

            if (response.ok) {
                // Redirect to the main app or dashboard
                alert("2FA verification successful!");
                window.location.href = "/home";
                // location.reload();
            } else {
                this.#showErrorMessage(
                    data.error || "Verification failed. Please try again."
                );
            }
        } catch (error) {
            console.error("Error:", error);
            this.#showErrorMessage("An error occurred. Please try again.");
        }
    }

    #showErrorMessage(message) {
        const errorMessage = document.getElementById("error-message");
        errorMessage.innerText = message;
        errorMessage.style.display = "block";
    }
}

export default AuthenticatorForm;
