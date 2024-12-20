import checkMfaAuthentication from "../Controller/Auth/checkMfaAuthentication.js";
import detectAnonymous from "../Controller/Auth/detectAnonymous.js";
import detectLoginStatus from "../Controller/Auth/detectLoginStatus.js";
import { routes, routeChecker, staticRoutes, dynamicRoutes } from "./routes.js";

const AuthorizationStatus = {
    ANONYMOUS: 0,
    NOLOGIN: 1,
    LOGIN: 2,
    NOTHING: -1,
};
Object.freeze(AuthorizationStatus);
const { ANONYMOUS, NOLOGIN, LOGIN, NOTHING } = AuthorizationStatus;

class Router {
    constructor() {
        this.init();
    }

    init() {
        window.addEventListener("popstate", () =>
            this.render(window.location.pathname)
        ); // 뒤로가기/앞으로가기
        document.addEventListener("DOMContentLoaded", () =>
            this.render(window.location.pathname)
        ); // 첫 로딩
    }

    navigate(pathname, isRedirect) {
        isRedirect
            ? window.history.replaceState(
                  {},
                  pathname,
                  window.location.origin + pathname
              )
            : window.history.pushState(
                  {},
                  pathname,
                  window.location.origin + pathname
              );
        this.render(pathname);
    }

    #parseQueryParams(pathname) {
        console.log(pathname);
        const queryStart = pathname.indexOf("?");
        console.log(queryStart);
        if (queryStart >= 0) {
            const pathname = pathname.substring(0, queryStart);
            const queryText = pathname.substring(queryStart + 1);
            const queries = queryText.split("&");
            const queryMap = new Map();
            for (let query of queries) {
                const [key, value] = query.split("=");
                queryMap.set(key, value);
            }
            return [pathname, queryMap];
        }
        return [pathname, null];
    }

    #hasRoute(pathname) {
        let res = ["static", "404", "404"];
        if (staticRoutes.has(pathname)) res = ["static", pathname, pathname];
        else {
            dynamicRoutes.forEach((routes, key) => {
                for (let route of routes) {
                    const regexPattern =
                        route.replace(/:\w+/g, "(\\d+)").replace(/\//g, "\\/") +
                        "$";
                    const regex = new RegExp(`^${regexPattern}$`);
                    if (regex.test(pathname)) {
                        res = ["dynamic", key, route];
                    }
                }
            });
        }
        return res;
    }

    async #checkAuthorization(pathname) {
        const isAnonymous = await detectAnonymous();
        if (isAnonymous) {
            if (routeChecker["game"].has(pathname)) {
                return ANONYMOUS;
            }
            if (routeChecker["mfa"].has(pathname)) {
                const isMfa = await checkMfaAuthentication();
                if (isMfa === false || isMfa.status !== "logged in")
                    return ANONYMOUS;
            }
            return NOTHING;
        }
        const loginStatus = await detectLoginStatus();
        if (!loginStatus && routeChecker["game"].has(pathname)) {
            return NOLOGIN;
        }
        if (
            loginStatus &&
            (routeChecker["login"].has(pathname) ||
                routeChecker["mfa"].has(pathname))
        ) {
            return LOGIN;
        }
        return NOTHING;
    }

    async render(pathname) {
        const queryStrings = window.location.search;
        const queries = new URLSearchParams(queryStrings);
        const [routeMethod, authCheckpath, correctRoute] =
            this.#hasRoute(pathname);
        if (routeMethod === "static" && pathname !== "/oauth2/redirect" && queries.size !== 0) {
            window.router.navigate(pathname, true);
            return;
        }
        const isAuthorization = await this.#checkAuthorization(authCheckpath);
        if (isAuthorization != NOTHING) {
            let redirectPath;
            if (isAuthorization === ANONYMOUS || isAuthorization === NOLOGIN)
                redirectPath = "/login";
            else if (isAuthorization === LOGIN) redirectPath = "/home";
            window.router.navigate(redirectPath, true);
            return;
        }
        const routeLoader = routes[correctRoute] || routes["/404"];
        const routeModule = await routeLoader();
        const routeInstance = new routeModule.default(); // 동적으로 로드한 모듈 인스턴스화
        const app = document.querySelector("#app");
        if(routeInstance.dispose)
            routeInstance.dispose();
        app.innerHTML = "";
        const dynamicData =
            routeMethod === "dynamic" ? pathname.split("/") : null;
        app.appendChild(await routeInstance.template(dynamicData, queries));
    }
}

export default Router;
