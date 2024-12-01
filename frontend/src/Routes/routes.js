const routes = {
  "/": () => import("../Pages/HomePage.js"),
  "/about": () => import("../Pages/AboutPage.js"),
  "/login": () => import("../Pages/LoginPage.js"),
  "/404": () => import("../Pages/NotFoundPage.js"),
  "/profile": () => import("../Pages/ProfilePage.js"),
  "/otp": () => import("../Pages/TwoFactorAuthPage.js"),
  "/oauth2/redirect": () => import("../Pages/Oauth2Page.js"),
  "/friends": () => import("../Pages/FriendsPage.js"),
  "/matching": () => import("../Pages/MatchingPage.js"),
};

export default routes;
