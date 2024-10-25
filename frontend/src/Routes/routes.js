import AboutPage from "../Pages/AboutPage.js";
import HomePage from "../Pages/HomePage.js";
import LoginPage from "../Pages/LoginPage.js";
import NotFoundPage from "../Pages/NotFoundPage.js";
import ProfilePage from "../Pages/ProfilePage.js";

const routes = {
  "/": HomePage,
  "/about": AboutPage,
  "/login": LoginPage,
  "/404": NotFoundPage,
  "/profile": ProfilePage,
};

export default routes;
