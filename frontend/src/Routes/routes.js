export const routes = {
    // Login
    "/": () => import("../Pages/StartPage.js"),
    "/login": () => import("../Pages/LoginPage.js"),
    "/oauth2/redirect": () => import("../Pages/Oauth2Page.js"),

    // MFA
    "/otp": () => import("../Pages/TwoFactorAuthPage.js"),
    "/otp/auth": () => import("../Pages/AuthPage.js"),

    // Game
    "/home": () => import("../Pages/HomePage.js"),
    "/profile": () => import("../Pages/ProfilePage.js"),
    "/profile/:userId": () => import("../Pages/ProfilePage.js"),
    "/profile/:userId/stat": () => import("../Pages/ProfilePage.js"),
    "/profile/:userId/history": () => import("../Pages/ProfilePage.js"),
    "/profile/:userId/history/match/:matchId": () =>
        import("../Pages/ProfilePage.js"),
    "/profile/:userId/history/tournament/:tournamenetId": () =>
        import("../Pages/ProfilePage.js"),
    "/settings": () => import("../Pages/SettingsPage.js"),
    "/matching": () => import("../Pages/MatchingPage.js"),
    "/result/:id" : () => import("../Pages/ResultPage.js"),
    "/playing/:id": () => import("../Pages/GamePage.js"),
    "/404": () => import("../Pages/NotFoundPage.js"),
};

export const routeChecker = {
    login: new Set(["/", "/login", "/oauth2/redirect"]),
    mfa: new Set(["/otp", "/otp/auth"]),
    game: new Set(["/home", "/profile", "/settings", "/matching", "/playing","/result"]),
};

export const staticRoutes = new Set([
    "/",
    "/login",
    "/oauth2/redirect",
    "/otp",
    "/otp/auth",
    "/home",
    "/settings",
    "/matching",
    "/404",
]);

export const dynamicRoutes = new Map([
    [
        "/profile",
        [
            "/profile",
            "/profile/:userId",
            "/profile/:userId/stat",
            "/profile/:userId/history",
            "/profile/:userId/history/match/:matchId",
            "/profile/:userId/history/tournament/:tournamenetId",
        ],
    ],
    ["/playing", ["/playing/:id"]],
    ["/result", ["/result/:id"]], 
]);

