document.addEventListener("DOMContentLoaded", function() {
    const homeBtn = document.getElementById("homeBtn");
    const friendsBtn = document.getElementById("friendsBtn");
    const notificationsBtn = document.getElementById("notificationsBtn");
    const profileBtn = document.getElementById("profileBtn");
    const uploadBtn = document.getElementById("uploadBtn");
    const logoBtn = document.querySelector(".logo");
    const reelTab = document.getElementById("reelTab");
    const friendsTab = document.getElementById("friendsTab");
    const searchBtn = document.getElementById("searchBtn");
    const videoFeed = document.querySelector(".video-feed");
    
    // Navigation functions
    homeBtn.addEventListener("click", () => console.log("Navigating to Home"));
    friendsBtn.addEventListener("click", () => console.log("Showing Friends Feed"));
    notificationsBtn.addEventListener("click", () => console.log("Opening Notifications"));
    profileBtn.addEventListener("click", () => console.log("Opening Profile"));
    
    // Upload function
    uploadBtn.addEventListener("click", () => console.log("Opening Upload Modal"));
    
    // Go live function
    logoBtn.addEventListener("click", () => console.log("Starting Live Stream"));
    
    // Toggle active tab between Reel and Friends
    reelTab.addEventListener("click", () => {
        console.log("Reel Feed Activated");
        reelTab.classList.add("active");
        friendsTab.classList.remove("active");
    });
    
    friendsTab.addEventListener("click", () => {
        console.log("Friends Feed Activated");
        friendsTab.classList.add("active");
        reelTab.classList.remove("active");
    });
    
    // Search function
    searchBtn.addEventListener("click", () => console.log("Search Triggered"));
    
    // Like, Comment, Share button functionalities
    document.addEventListener("click", function(event) {
        if (event.target.classList.contains("like-btn")) {
            console.log("Post Liked!");
            event.target.textContent = "❤️ Liked";
        }
        if (event.target.classList.contains("comment-btn")) {
            console.log("Opening Comment Section...");
            alert("Open comment section for this post");
        }
        if (event.target.classList.contains("share-btn")) {
            console.log("Sharing Post...");
            alert("Post shared!");
        }
        if (event.target.classList.contains("download-btn")) {
            let videoElement = event.target.closest(".post").querySelector("video");
            if (videoElement) {
                let videoUrl = videoElement.src;
                let link = document.createElement("a");
                link.href = videoUrl;
                link.download = "downloaded_video.mp4";
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                console.log("Video Downloaded!");
            }
        }
    });
    
    
    // Function to dynamically load videos with placeholders
    function loadVideos() {
        const posts = [
            {
                profilePic: "placeholder-profile.png",
                username: "@placeholder_user",
                description: "This is a placeholder post. #example @mention",
                videoSrc: "placeholder-video.mp4"
            }
        ];

        videoFeed.innerHTML = "";
        posts.forEach(post => {
            const postElement = document.createElement("div");
            postElement.classList.add("post");
            postElement.innerHTML = `
                <div class="post-header">
                    <img src="${post.profilePic}" alt="Profile Picture" class="profile-pic">
                    <div class="post-info">
                        <span class="username">${post.username}</span>
                        <p class="description">${post.description}</p>
                    </div>
                </div>
                <video src="${post.videoSrc}" controls></video>
                <div class="action-bar">
                    <button class="like-btn">❤️ Like</button>
                    <button class="comment-btn">💬 Comment</button>
                    <button class="share-btn">🔗 Share</button>
                </div>
            `;
            videoFeed.appendChild(postElement);
        });
    }
    
    loadVideos();
});
