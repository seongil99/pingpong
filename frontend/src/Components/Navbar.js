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
            "X-CSRFToken": csrftoken, // CSRF 토큰을 헤더에 포함
        });
        return response;
    } catch (error) {
        console.error("Error:", error);
    }
};

function NavBarItem(text) {
    const li = document.createElement("li");
    li.classList.add("nav-item");
    const a = document.createElement("a");
    a.classList.add("nav-link");
    a.textContent = text;
    li.appendChild(a);
    return li;
}

function NavBarList() {
    const ul = document.createElement("ul");
    ul.classList.add("navbar-nav");

    const profileBtn = NavBarItem("Profile");
    profileBtn.lastElementChild.setAttribute("path", "/profile");
    profileBtn.lastElementChild.classList.add("navigate");
    const settingBtn = NavBarItem("Setting");
    settingBtn.lastElementChild.setAttribute("path", "/settings");
    settingBtn.lastElementChild.classList.add("navigate");
    const logoutBtn = NavBarItem("Log out");
    logoutBtn.onClick = async () => {
        const response = await logout();
        if (response.ok) {
            document.getElementById("h2").textContent = " logout success";
        } else {
            document.getElementById("h2").textContent = " logout fail";
        }
    };
    ul.appendChild(profileBtn);
    ul.appendChild(settingBtn);
    ul.appendChild(logoutBtn);
    return ul;
}

function NavBar() {
    const navBar = document.createElement("nav");
    navBar.classList.add("navbar", "navbar-expand-lg", "bg-body-tertiary");

    // Navigation Bar Frame Divider
    const navBarFrame = document.createElement("div");
    navBarFrame.classList.add("container-fluid");

    // Main Page Button
    const homeTitle = document.createElement("a");
    homeTitle.classList.add("navbar-title", "navbar-brand", "navigate");
    const homePath = "/home";
    homeTitle.setAttribute("path", homePath);
    homeTitle.textContent = "ft_transcendence";

    // Navigation Bar Toggle Button
    const navBarToggleBtn = document.createElement("button");
    navBarToggleBtn.classList.add("navbar-toggler");
    navBarToggleBtn.setAttribute("type", "button");
    navBarToggleBtn.setAttribute("data-bs-toggle", "collapse");
    navBarToggleBtn.setAttribute("data-bs-target", "#navbarTogglerDemo02");
    navBarToggleBtn.setAttribute("aria-controls", "navbarTogglerDemo02");
    navBarToggleBtn.setAttribute("aria-expanded", "false");
    navBarToggleBtn.setAttribute("aria-label", "Toggle navigation");

    // Navigation Bar Toggle Button icon
    const navBarIcon = document.createElement("span");
    navBarIcon.classList.add("navbar-toggler-icon");

    navBarToggleBtn.appendChild(navBarIcon);

    // Navigation Bar Contents Group Divider
    const navBarListBox = document.createElement("div");
    navBarListBox.classList.add(
        "justify-content-end",
        "collapse",
        "navbar-collapse"
    );
    navBarListBox.setAttribute("id", "navbarTogglerDemo02");

    const navBarList = NavBarList();
    navBarListBox.appendChild(navBarList);

    // Append The Child Elements of Navigation Bar Frame
    navBarFrame.appendChild(homeTitle);
    navBarFrame.appendChild(navBarToggleBtn);
    navBarFrame.appendChild(navBarListBox);

    // Append The Child Element of Navigation Bar
    navBar.appendChild(navBarFrame);
    return navBar;
}

export default NavBar;
