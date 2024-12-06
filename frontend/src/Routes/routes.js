const routes = {
  "/": () => import("../Pages/StartPage.js"),
  "/home": () => import("../Pages/HomePage.js"),
  "/login": () => import("../Pages/LoginPage.js"),
  "/404": () => import("../Pages/NotFoundPage.js"),
  "/profile": () => import("../Pages/ProfilePage.js"),
  "/otp": () => import("../Pages/TwoFactorAuthPage.js"),
  "/verification": MFAPage,
  "/verification/auth": AuthenticatorPage,
  "/oauth2/redirect": () => import("../Pages/Oauth2Page.js"),
  "/friends": () => import("../Pages/FriendsPage.js"),
  "/matching": () => import("../Pages/MatchingPage.js"),
};

export default routes;
