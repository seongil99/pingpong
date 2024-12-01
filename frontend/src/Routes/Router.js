class Router {
  constructor(routes) {
    this.routes = routes;
    this.init();
  }

  init() {
    window.addEventListener("popstate", () =>
      this.render(window.location.pathname),
    ); // 뒤로가기/앞으로가기
    document.addEventListener("DOMContentLoaded", () =>
      this.render(window.location.pathname),
    ); // 첫 로딩
  }

  navigate(pathname) {
    window.history.pushState({}, pathname, window.location.origin + pathname);
    this.render(pathname);
  }

  async render(pathname) {
    const routeLoader = this.routes[pathname] || this.routes["/404"];
    const routeModule = await routeLoader();
    const routeInstance = new routeModule.default(); // 동적으로 로드한 모듈 인스턴스화

    const $app = document.querySelector("#app");
    $app.innerHTML = "";
    $app.appendChild(await routeInstance.template());
  }
}

export default Router;
