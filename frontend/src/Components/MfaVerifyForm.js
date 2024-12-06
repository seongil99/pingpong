function createFormComponent() {
    // Create the form element
    const form = document.createElement('form');
    form.innerHTML = `
      <input name="otp" placeholder="OTP" required />
      <button type="submit">Enable 2fa</button>
    `;
  
    // Form submission logic
    form.addEventListener('submit', async function (event) {
      event.preventDefault();
  
      // Gather data
      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());
  
      // Send data with Fetch
      try {
        const response = await fetch('/api/v1/accounts/mfa/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });
  
        if (response.ok) {
          const result = await response.json();
          console.log('Success:', result);
          window.location.href = '/';
        } else {
          console.error('Error:', response.statusText);
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    });
  
    return form;
  }
  
  export default createFormComponent;