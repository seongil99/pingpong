import callCallback from "../Controller/Auth/callCallback.js";
import checkMfaAuthentication from "../Controller/Auth/checkMfaAuthentication.js";
import detectAnonymous from "../Controller/Auth/detectAnonymous.js";
import detectLoginStatus from "../Controller/Auth/detectLoginStatus.js";

const AuthorizationStatus = {
    ANONYMOUS: 0,
    NOLOGIN: 1,
    MFA: 2,
    LOGIN: 3,
    NOTHING: -1,
};
Object.freeze(AuthorizationStatus);
const { ANONYMOUS, NOLOGIN, MFA, LOGIN, NOTHING } = AuthorizationStatus;

class Router {
    constructor(routes) {
        this.routes = routes;
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
        console.log("Navigate Method> ", pathname);
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

    async #checkAuthorization(pathname) {
        const isAnonymous = await detectAnonymous();
        console.log("Anonymous User: ", isAnonymous);
        if (isAnonymous) {
            if (this.routes["game"][pathname]) {
                return ANONYMOUS;
            }
            if (this.routes["mfa"][pathname]) {
                const isMfa = await checkMfaAuthentication();
                console.log(isMfa);
                if (isMfa === false || isMfa.status !== "logged in")
                    return ANONYMOUS;
            }
            return NOTHING;
        }
        const loginStatus = await detectLoginStatus();
        console.log("Log In Status: ", loginStatus);
        if (!loginStatus && this.routes["game"][pathname]) {
            return NOLOGIN;
        }
        if (
            loginStatus &&
            (this.routes["auth"][pathname] || this.routes["mfa"][pathname])
        ) {
            return LOGIN;
        }
        return NOTHING;
    }

    async render(pathname) {
        const isAuthorization = await this.#checkAuthorization(pathname);
        console.log(isAuthorization);
        if (isAuthorization != NOTHING) {
            let redirectPath;
            if (isAuthorization === ANONYMOUS || isAuthorization === NOLOGIN)
                redirectPath = "/login";
            else if (isAuthorization === LOGIN) redirectPath = "/home";
            else redirectPath = "/otp"
            window.router.navigate(redirectPath, true);
            return;
        }
        const routeLoader =
            this.routes["auth"][pathname] ||
            this.routes["game"][pathname] ||
            this.routes["mfa"][pathname] ||
            this.routes["/404"];
        const routeModule = await routeLoader();
        const routeInstance = new routeModule.default(); // 동적으로 로드한 모듈 인스턴스화

        const app = document.querySelector("#app");
        app.innerHTML = "";
        app.appendChild(await routeInstance.template());
    }
}

export default Router;
