import NavBar from "../Components/Navbar.js";
import createFormComponent from "../Components/MfaForm.js";

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

    this.fetchFriends();

    return container; // 최종 DOM 반환
  }

  async fetchFriends() {
    let page = document.getElementById("friends-list");
    let response = await fetch("/api/v1/users/friends", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => response.json());
    let friendList = document.createElement("div");
    const title = document.createElement("h3");
    title.innerHTML = "Friends";
    friendList.appendChild(title);
    let data = response.results;
    console.log(data);
    for (let friend of data) {
      console.log(friend);
      let friendUser = friend["other_user"];
      friendList.innerHTML += `
                <div class="friend">
                    <div class="friend-info">
                        <img src="${friendUser.avatar}" alt="profile picture">
                        <h3>${friendUser.email}</h3>
                        <p>Status: ${friendUser.is_online ? "✅" : "❌"}</p >
                    </div >
            <div class="friend-actions">
                <button class="btn">Remove</button>
            </div>
                </div >
            `;
    }
    page.appendChild(friendList);
  }
}

export default FriendsPage;
