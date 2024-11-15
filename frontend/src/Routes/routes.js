import AboutPage from "../Pages/AboutPage.js";
import HomePage from "../Pages/HomePage.js";
import LoginPage from "../Pages/LoginPage.js";
import NotFoundPage from "../Pages/NotFoundPage.js";
import Oauth2Page from "../Pages/Oauth2Page.js";
import ProfilePage from "../Pages/ProfilePage.js";
import TwoFactorAuthPage from "../Pages/TwoFactorAuthPage.js";
import AuthenticatorPage from "../Pages/AuthenticatorPage.js";
import StartPage from "../Pages/StartPage.js";

const routes = {
  "/": StartPage,
  "/home": HomePage,
  "/about": AboutPage,
  "/login": LoginPage,
  "/404": NotFoundPage,
  "/profile": ProfilePage,
  "/verification": TwoFactorAuthPage,
  "/verification/authenticator": AuthenticatorPage,
  "/oauth2/redirect": Oauth2Page,
};

export default routes;
