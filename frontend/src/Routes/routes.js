const routes = {
    auth: {
        "/": () => import("../Pages/StartPage.js"),
        "/login": () => import("../Pages/LoginPage.js"),
        "/oauth2/redirect": () => import("../Pages/Oauth2Page.js"),
    },
    mfa: {
        "/otp": () => import("../Pages/TwoFactorAuthPage.js"),
        "/otp/auth": () => import("../Pages/AuthPage.js"),
    },
    game: {
        "/home": () => import("../Pages/HomePage.js"),
        "/profile": () => import("../Pages/ProfilePage.js"),
        "/settings": () => import("../Pages/SettingsPage.js"),
        "/matching": () => import("../Pages/MatchingPage.js"),
        "/playing": () => import("../Pages/GamePage.js"),
    },
    "/404": () => import("../Pages/NotFoundPage.js"),
};

export default routes;
