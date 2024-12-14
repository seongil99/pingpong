import detectLoginStatus from "../Controller/Auth/detectLoginStatus.js";
// import detectMfaEnabled from "../Controller/Auth/detectMfaEnabled.js";

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

    navigate(pathname) {
        window.history.pushState(
            {},
            pathname,
            window.location.origin + pathname
        );
        this.render(pathname);
    }

    async #checkAuthorization(pathname) {
        const loginStatus = await detectLoginStatus();
        console.log(loginStatus);
        if (!loginStatus && this.routes["game"][pathname]) {
            return 0;
        }
        if (
            loginStatus &&
            (this.routes["auth"][pathname] || this.routes["mfa"][pathname])
        ) {
            return 1;
        }
        return -1;
    }

    async render(pathname) {
        const isAuthorization = await this.#checkAuthorization(pathname);

        if (isAuthorization >= 0) {
            if (isAuthorization === 1) window.router.navigate("/home");
            else if (isAuthorization === 0) window.router.navigate("/login");
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
