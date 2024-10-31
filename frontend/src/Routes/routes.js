import AboutPage from "../Pages/AboutPage.js";
import HomePage from "../Pages/HomePage.js";
import LoginPage from "../Pages/LoginPage.js";
import NotFoundPage from "../Pages/NotFoundPage.js";

const routes = {
  "/": HomePage,
  "/about": AboutPage,
  "/login": LoginPage,
  "/404": NotFoundPage,
};

export default routes;
