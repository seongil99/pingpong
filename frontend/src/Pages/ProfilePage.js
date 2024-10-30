import LoginButton from "../Components/LoginButton.js";
import NavBar from "../Components/Navbar.js";
import { qrcodeImage } from "../Components/mfaQRcode.js"

class LoginPage {
  async template() {

    const navBar = document.createElement("div");
    navBar.innerHTML = NavBar;
    const title = document.createElement("h2");

    const container = document.createElement('div');
    container.id = 'profile-page';
    container.appendChild(navBar);
    container.appendChild(title);

    const mainDiv = document.createElement('div');
    mainDiv.innerHTML = `
        <div id="profile-info">
        <p id="email">Email: <span></span></p>
        <p id="first-name">First Name: <span></span></p>
        <p id="last-name">Lirst Name: <span></span></p>
            <button id="edit-profile">Edit Profile</button>
        </div>
        <div id="edit-profile-form" style="display: none;">
            <h2>Edit Profile</h2>
            <input type="email" id="edit-email" placeholder="Enter new email" />
            <input type="text" id="edit-first-name" placeholder="Enter new first name" />
            <input type="text" id="edit-last-name" placeholder="Enter new last name" />
            <button id="save-changes">Save Changes</button>
            <button id="cancel-edit">Cancel</button>
        </div>
    `;
    
    container.appendChild(mainDiv);

    document.getElementById('app').innerHTML = ''; // Clear previous content
    document.getElementById('app').appendChild(container); // Append the profile page

    // Add event listeners for the buttons
    // document.getElementById('edit-profile').addEventListener('click', showEditForm);
    // document.getElementById('save-changes').addEventListener('click', saveChanges);
    // document.getElementById('cancel-edit').addEventListener('click', cancelEdit);
    // 컨테이너 div 생성
    // const container = document.createElement("div");
    // container.classList.add("login-container");


    // // 제목 추가
    // title.textContent = "Profile Page";

    

    // // 로그인 버튼 생성

    // // DOM에 요소 추가
    
    
    const userData = await fetchUserProfile();
    displayProfile(userData);

    if (!userData.mfa_enabled) {
        const enableMfaButton = document.createElement('button');
    } else {
        document.createElement('div');
    }


    return container; // 최종 DOM 반환
  }
}

async function fetchUserProfile() {
    try {
        const response = await fetch('/api/v1/accounts/user');
        if (!response.ok) throw new Error('Network response was not ok');
        
        const userData = await response.json(); // Assuming it returns { username: '...', email: '...' }
        // Populate the profile info
        
        return userData;
    } catch (error) {
        console.error('Error fetching user profile:', error);
    }
}

function displayProfile(userData) {
    // console.log(`email: ${userData.email}`);
    // console.log(`first_name: ${userData.first_name}`);
    // console.log(`last_name: ${userData.last_name}`);
    document.getElementById('email').querySelector('span').textContent = userData.email;

    const firstName = document.getElementById('first-name').querySelector('span');
    const lastName = document.getElementById('last-name').querySelector('span');

    if (userData.first_name === null || userData.first_name === '') {
        firstName.textContent = 'Not provided';
    } else {
        firstName.textContent = userData.first_name;
    }
    if (userData.last_name === null || userData.last_name === '') {
        lastName.textContent = 'Not provided';
    } else {
        lastName.textContent = userData.last_name;
    }
}

function generate2fa() {
    
}

export default new LoginPage();
