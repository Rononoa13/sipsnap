const cameraInput = document.getElementById("camera-input");
const fileInput = document.getElementById("file-input");
const preview = document.getElementById("preview");
const errorMessage = document.getElementById("error-message");

const scanButton = document.getElementById("scan-button");
let selectedFile = null;

const MAX_IMAGE_SIZE = 10 * 1024 * 1024;

const ALLOWED_IMAGE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp",
];

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.hidden = false;
    preview.hidden = true;
}

function clearError() {
    errorMessage.textContent = "";
    errorMessage.hidden = true;
}

function validateImage(file) {
    if (!file) {
        return "Please select an image.";
    }

    if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
        return "Please select a JPEG, PNG, or WebP image.";
    }

    if (file.size > MAX_IMAGE_SIZE) {
        return "Image must be smaller than 10 MB.";
    }

    return null;
}

function showPreview(file) {
    clearError();

    const error = validateImage(file);

    if (error) {
        selectedFile = null;
        scanButton.hidden = true;
        showError(error);
        return;
    }

    selectedFile = file;

    const imageUrl = URL.createObjectURL(file);

    preview.src = imageUrl;
    preview.hidden = false;
    scanButton.hidden = false;
}

cameraInput.addEventListener("change", () => {
    showPreview(cameraInput.files[0]);
});

fileInput.addEventListener("change", () => {
    showPreview(fileInput.files[0]);
});

// Form Data
async function scanMenu() {
    if (!selectedFile) {
        return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
        const response = await fetch("http://localhost:8000/api/scan", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Scan failed: ${response.status}`);
        }

        const result = await response.json();

        sessionStorage.setItem(
            "sipsnap-menu",
            JSON.stringify(result)
        );

        window.location.href = "/results.html";
    } catch (error) {
        console.error("Scan failed:", error);
    }
}

scanButton.addEventListener("click", scanMenu);