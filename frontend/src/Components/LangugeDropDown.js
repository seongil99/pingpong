import createElement from "../Utils/createElement.js";
function createLanguageDropdown() {
    // 네비게이션 토글 버튼 생성
    const navbarToggler = createElement(
        "button",
        {
            class: "navbar-toggler",
            type: "button",
            "data-bs-toggle": "collapse",
            "data-bs-target": "#navbarNavLanguage",
            "aria-controls": "navbarNavLanguage",
            "aria-expanded": "false",
            "aria-label": "Toggle navigation",
        },
        createElement("span", { class: "navbar-toggler-icon" })
    );

    // 드롭다운 메뉴 항목 생성
    const dropdownItems = ["English", "한국어", "日本語"].map((lang) =>
        createElement(
            "li",
            {},
            createElement(
                "a",
                {
                    class: "dropdown-item",
                    href: "#",
                    events: {
                        click: () => {
                            changeLanguage(lang);
                        },
                    },
                },
                lang
            )
        )
    );

    // 드롭다운 메뉴 생성
    const dropdownMenu = createElement(
        "ul",
        {
            class: "dropdown-menu dropdown-menu-dark",
            "aria-labelledby": "navbarLanguageMenu",
        },
        ...dropdownItems
    );

    // 드롭다운 토글 생성
    const dropdownToggle = createElement(
        "a",
        {
            class: "nav-link dropdown-toggle",
            href: "#",
            id: "navbarLanguageMenu",
            role: "button",
            "data-bs-toggle": "dropdown",
            "aria-expanded": "false",
        },
        "🌍"
    );

    // 드롭다운 메뉴 항목 래퍼 생성
    const dropdownWrapper = createElement(
        "li",
        { class: "nav-item dropdown" },
        dropdownToggle,
        dropdownMenu
    );

    // 네비게이션 메뉴 생성
    const navMenu = createElement(
        "ul",
        { class: "navbar-nav" },
        dropdownWrapper
    );

    // 네비게이션 바 전체 생성
    const navbarCollapse = createElement(
        "div",
        { class: "collapse navbar-collapse", id: "navbarNavLanguage" },
        navMenu
    );

    const navbarContainer = createElement(
        "div",
        { class: "container-fluid" },
        navbarToggler,
        navbarCollapse
    );

    return navbarContainer;
}

// 언어 변경 함수
function changeLanguage(lang) {
	i18next.changeLanguage(lang);
}

// 실행
export default createLanguageDropdown;
