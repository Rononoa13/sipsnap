const menuResults = document.getElementById("menu-results");
const resultsError = document.getElementById("results-error");
const scanAgainButton = document.getElementById("scan-again");

function renderMenu(menu) {
    menuResults.innerHTML = "";

    menu.items.forEach((item) => {
        const itemElement = document.createElement("article");
        itemElement.className = "menu-item";

        const nameElement = document.createElement("h2");
        nameElement.className = "menu-item-name";
        nameElement.textContent = item.name;

        itemElement.appendChild(nameElement);

        if (item.category) {
            const categoryElement = document.createElement("p");
            categoryElement.className = "menu-item-category";
            categoryElement.textContent = item.category;

            itemElement.appendChild(categoryElement);
        }

        if (item.description) {
            const descriptionElement = document.createElement("p");
            descriptionElement.className = "menu-item-description";
            descriptionElement.textContent = item.description;

            itemElement.appendChild(descriptionElement);
        }

        menuResults.appendChild(itemElement);
    });
}

function loadMenu() {
    const storedMenu = sessionStorage.getItem("sipsnap-menu");

    if (!storedMenu) {
        resultsError.hidden = false;
        return;
    }

    try {
        const menu = JSON.parse(storedMenu);

        renderMenu(menu);
    } catch (error) {
        console.error("Failed to read menu:", error);
        resultsError.hidden = false;
    }
}

scanAgainButton.addEventListener("click", () => {
    window.location.href = "/scan.html";
});

loadMenu();