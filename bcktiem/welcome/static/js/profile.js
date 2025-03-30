// Follow button functionality
document.querySelectorAll('.follow-btn').forEach(btn => {
    btn.addEventListener('click', async function() {
        const userId = this.getAttribute('data-user-id');
        const isFollowing = this.textContent.trim() === 'Following';
        
        try {
            const response = await fetch(`/follow/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: isFollowing ? 'unfollow' : 'follow'
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                this.textContent = isFollowing ? 'Follow' : 'Following';
                document.querySelector('.stat-number:nth-child(2)').textContent = data.followers_count;
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}