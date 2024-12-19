import Router from "./Routes/Router.js";
import { handleClick } from "./Utils/clickHandler.js";

const router = new Router();
window.router = router;
document.addEventListener("click", (event) => handleClick(event, router));
