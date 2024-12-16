import callCallback from "../Controller/Auth/callCallback.js";

class Oauth2Page {
    async template() {
        try {
            const data = await callCallback();
            let redirectPath;
            if (data.detail !== "OTP required") {
                redirectPath = "/home";
            } else if (data.status === "redirect") {
                redirectPath = data.url;
            } else {
                alert("Failed to login");
                redirectPath = "/login";
            }
            window.router.navigate(redirectPath, true);
        } catch (error) {
            console.error(error);
        }
        const container = document.createElement("div");
        return container;
    }
}

export default Oauth2Page;
