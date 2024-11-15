function loadStylesheet(url) {
    const existingLink = document.getElementById('dynamic-stylesheet');
    if (existingLink) {
        existingLink.href = url; // Update existing link
    } else {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = url;
        link.id = 'dynamic-stylesheet'; // Assign an ID for easy reference
        document.head.appendChild(link);
    }
}