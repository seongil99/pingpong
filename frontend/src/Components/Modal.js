const ProfileSummary = () => {
    const profileSummary = document.createElement("div");
    profileSummary.classList.add("profile-summary");

    const profileInfo = document.createElement("div");
    profileSummary.classList.add("profile-info");
    const profilePageBtn = document.createElement("button");
	profilePageBtn.classList.add("");
	profileSummary.appendChild(profileInfo);
    profileSummary.appendChild(profilePageBtn);
	return profileSummary;
};

const Modal = () => {
    const modal = document.createElement("div");
    modal.classList.add("modal");

    const modalContent = document.createElement("div");
    modalContent.classList.add("model-content");

    const profileSummary = ProfileSummary();
	

    modal.appendChild(modalContent);
    return modal;
};

export default Modal;
