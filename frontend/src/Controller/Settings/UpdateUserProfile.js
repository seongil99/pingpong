const updateUserProfile = async (formData) => {
  try {
    const response = await fetch("/api/v1/users/me/", {
      method: "PATCH",
      credentials: "include",
      body: formData,
    });
    if (!response.ok) throw new Error("Network response was not ok");
    const userData = await response.json();
    userData.avatar = userData.avatar?.replace("http://", "https://");
    return userData;
  } catch (error) {
    console.error("Error updating profile image:", error);
  }
};

export default updateUserProfile;
