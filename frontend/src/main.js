import Router from "./Routes/Router.js";
import routes from "./Routes/routes.js";
import { handleClick } from "./Utils/clickHandler.js";

const $app = document.querySelector("#app");

const router = new Router(routes);
document.addEventListener("click", (event) => handleClick(event, router));
