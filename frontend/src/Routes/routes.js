const routes = {
    "/": () => import("../Pages/StartPage.js"),
    "/home": () => import("../Pages/HomePage.js"),
    "/login": () => import("../Pages/LoginPage.js"),
    // "/404": () => import("../Pages/NotFoundPage.js"),
    // "/otp": () => import("../Pages/TwoFactorAuthPage.js"),
    // "/oauth2/redirect": () => import("../Pages/Oauth2Page.js"),
    // "/verification": () => import("../Pages/TwoFactorAuthPage.js"),
    // "/verification/auth": import("../Pages/AuthenticatorPage.js"),
    "/profile": () => import("../Pages/ProfilePage.js"),
    "/settings": () => import("../Pages/SettingsPage.js"),
    // "/friends": () => import("../Pages/FriendsPage.js"),
    // "/matching": () => import("../Pages/MatchingPage.js"),
};

export default routes;
