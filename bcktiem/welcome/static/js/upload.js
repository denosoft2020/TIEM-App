// Get UI elements
const uploadBtn = document.getElementById("upload-btn");
const uploadPopup = document.getElementById("upload-popup");
const closePopup = document.getElementById("close-popup");
const cameraPreview = document.getElementById("camera-preview");
const galleryInput = document.getElementById("gallery-input");
const filters = document.getElementById("filters");
const durationSelect = document.getElementById("duration-select");
const postBtn = document.getElementById("post-btn");

let stream;

// Show upload pop-up when clicking the upload button
uploadBtn.addEventListener("click", () => {
    uploadPopup.style.display = "flex";
    startCamera();
});

// Close upload pop-up
closePopup.addEventListener("click", () => {
    uploadPopup.style.display = "none";
    stopCamera();
});

// Start camera preview with fallback for mobile browsers
async function startCamera() {
    const constraints = {
        video: {
            facingMode: "user", // Front camera
            width: { ideal: 1280 },
            height: { ideal: 720 }
        }
    };

    try {
        stream = await navigator.mediaDevices.getUserMedia(constraints);
        cameraPreview.srcObject = stream;
        cameraPreview.play();
    } catch (error) {
        alert("Camera access denied or not supported on your device.");
    }
}

// Stop camera when closing pop-up
function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
}

// Handle gallery image selection
galleryInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            cameraPreview.srcObject = null; // Stop camera
            cameraPreview.src = e.target.result; // Show image preview
        };
        reader.readAsDataURL(file);
    }
});

// Apply filters
filters.addEventListener("change", () => {
    cameraPreview.style.filter = filters.value;
});

// Handle posting
postBtn.addEventListener("click", () => {
    alert("Post uploaded successfully! (Backend integration needed)");
    uploadPopup.style.display = "none";
    stopCamera();
});

document.addEventListener("DOMContentLoaded", () => {
    const mediaInput = document.getElementById("media-input");
    const previewVideo = document.getElementById("preview-video");
    const previewImage = document.getElementById("preview-image");
    const filterSelect = document.getElementById("filter-select");

    mediaInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (file) {
            const url = URL.createObjectURL(file);
            if (file.type.startsWith("video/")) {
                previewVideo.src = url;
                previewVideo.classList.remove("hidden");
                previewImage.classList.add("hidden");
            } else if (file.type.startsWith("image/")) {
                previewImage.src = url;
                previewImage.classList.remove("hidden");
                previewVideo.classList.add("hidden");
            }
        }
    });

    filterSelect.addEventListener("change", () => {
        const filter = filterSelect.value;
        previewVideo.style.filter = filter;
        previewImage.style.filter = filter;
    });
});
