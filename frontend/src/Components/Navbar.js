import createElement from "../Utils/createElement.js";
import LanguageDropdown from "./LangugeDropDown.js";

const logout = async () => {
    const url = "https://localhost/api/v1/users/accounts/logout/";
    const csrftoken = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        .split("=")[1];
    try {
        const response = await fetch(url, {
            method: "POST",
            credentials: "include", // 쿠키 전송 허용
            headers: {
                "X-CSRFToken": csrftoken, // CSRF 토큰을 헤더에 포함
            },
        });
        return response;
    } catch (error) {
        console.error("Error:", error);
    }
};

function NavBarItem(p, i18nKey) {
    const a = createElement(
        "a",
        { class: "nav-link navigate", path: p, "data-i18n": i18nKey },
        i18next.t(i18nKey)
    );
    const li = createElement("li", { class: "nav-item" }, a);
    return li;
}

function NavBarList() {
    const profileBtn = NavBarItem("/profile", "nav_profile");
    const settingBtn = NavBarItem("/settings", "nav_settings");
    const logoutBtn = NavBarItem("", "nav_logout");
    logoutBtn.lastElementChild.classList.remove("navigate");
    logoutBtn.onclick = async () => {
        const response = await logout();
        if (response.ok) {
            alert("logout success!!");
            window.router.navigate("/", false);
        } else {
            alert("logout fail");
        }
    };
    const ul = createElement(
        "ul",
        { class: "navbar-nav" },
        profileBtn,
        settingBtn,
        logoutBtn,
        LanguageDropdown()
    );
    return ul;
}

function NavBar() {
    const homeTitle = createElement(
        "a",
        { class: "navbar-title navbar-brand navigate", path: "/home", "data-i18n": "nav_home" },
        i18next.t("nav_home")
    );
    const navBarIcon = createElement(
        "span",
        { class: "navbar-toggler-icon" },
        []
    );
    const navBarToggleBtn = createElement(
        "button",
        {
            class: "navbar-toggler",
            type: "button",
            "data-bs-toggle": "collapse",
            "data-bs-target": "#navbarTogglerDemo02",
            "aria-controls": "navbarTogglerDemo02",
            "aria-expanded": "false",
            "aria-label": "Toggle navigation",
        },
        navBarIcon
    );
    const navBarList = NavBarList();
    const navBarListBox = createElement(
        "div",
        {
            class: "justify-content-end collapse navbar-collapse",
            id: "navbarTogglerDemo02",
        },
        navBarList
    );
    const navBarFrame = createElement(
        "div",
        { class: "container-fluid" },
        homeTitle,
        navBarToggleBtn,
        navBarListBox
    );
    const navBar = createElement(
        "nav",
        { class: "navbar navbar-expand-lg bg-body-tertiary" },
        navBarFrame
    );
    return navBar;
}

export default NavBar;
