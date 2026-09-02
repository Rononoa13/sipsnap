const menuResults = document.getElementById("menu-results");
const resultsError = document.getElementById("results-error");
const scanAgainButton = document.getElementById("scan-again");

function loadMenu() {
    const storedMenu = sessionStorage.getItem("sipsnap-menu");

    if (!storedMenu) {
        resultsError.hidden = false;
        return;
    }

    try {
        const menu = JSON.parse(storedMenu);

        console.log("Loaded menu:", menu);
    } catch (error) {
        console.error("Failed to read menu:", error);
        resultsError.hidden = false;
    }
}

scanAgainButton.addEventListener("click", () => {
    window.location.href = "/scan.html";
});

loadMenu();