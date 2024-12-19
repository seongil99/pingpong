import Router from "./Routes/Router.js";
import {routes, routeChecker, staticRoutes, dynamicRoutes} from "./Routes/routes.js";
import { handleClick } from "./Utils/clickHandler.js";
import data from "./Translate/data.js"

const router = new Router(routes);
window.router = router;
i18next.init(
	{
		lng: "한국어",
		debug: true,
		resources: data,
	},
	(err) => {

		if (err) {
			console.error("i18next 초기화 오류:", err);
		}
	});
document.addEventListener("click", (event) => handleClick(event, router));