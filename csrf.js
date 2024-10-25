// export async function getCSRFToken(){
//     // Check if the token exists in localStorage
//   const storedToken = localStorage.getItem('csrfToken');
  
//   if (storedToken) {
//     // If the token exists, return it immediately
//     return Promise.resolve(storedToken);
//   } else {
//     // If no token exists, fetch it from the server
//     return await fetch('/api/get-csrf-token/', {
//       credentials: 'include',  // This is important to include cookies
//     })
//     .then(response => response.json())
//     .then(data => {
//       // Store the new token in localStorage
//       localStorage.setItem('csrfToken', data.csrfToken);
//       return data.csrfToken;
//     })
//     .catch(error => {
//       console.error('Error fetching CSRF token:', error);
//       throw error;
//     });
//   }
// }