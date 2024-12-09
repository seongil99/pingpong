import NavBar from "../Components/Navbar.js";
import fetchFriends from "../Controller/Friends/FetchFriends.js";

class FriendsPage {
    async template() {
        const navBar = document.createElement("div");
        navBar.innerHTML = NavBar;
        const title = document.createElement("h2");

        const container = document.createElement("div");
        container.id = "profile-page";
        container.appendChild(navBar);
        container.appendChild(title);

        const mainDiv = document.createElement("div");
        mainDiv.innerHTML = `
        <div id="friends-list">

        </div>
    `;

        container.appendChild(mainDiv);

        document.getElementById("app").innerHTML = ""; // Clear previous content
        document.getElementById("app").appendChild(container); // Append the profile page

        fetchFriends();

        return container; // 최종 DOM 반환
    }
}

export default FriendsPage;
