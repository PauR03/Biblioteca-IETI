function logout() {
    // Clear localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('username');

    // Redirect to index.html
    window.location.href = '/index.html';
}