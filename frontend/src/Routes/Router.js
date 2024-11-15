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
    const route = this.routes[pathname] || this.routes["/404"]; // 경로에 맞는 컴포넌트, 없으면 404 페이지
    const app = document.querySelector("#app");
    app.innerHTML = "";
    app.appendChild(await route.template());
  }
}

export default Router;
