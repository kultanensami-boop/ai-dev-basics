let activeCategory = null;

// Haetaan tuotteet API:sta ja näytetään ne sivulla
async function fetchItems(filterCategory = null) {
    const response = await fetch("http://localhost:5000/items");
    const items = await response.json();

    let filteredItems = items;
    

    if (filterCategory) {
        filteredItems = items.filter(item => item.category === filterCategory);
    }

    const container = document.getElementById("items-container");
    container.innerHTML = "";


    filteredItems.forEach(item => {
        const div = document.createElement("div");
        div.className = "item-card";
        div.setAttribute("data-id", item.id);

        div.innerHTML = `
       <img 
    src="${item.image_url || '/static/default.jpg'}" 
    class="item-image"
/>
            <h3>${item.name}</h3>
            <p>${item.description}</p>
            <p>Hinta: ${item.price} €</p>
            <p>Kategoria: ${item.category}</p>
           <p class="stock-text">${item.in_stock ? "Varastossa" : "Ei varastossa"} (${item.stock} kpl)</p>
           <div class="stock-controls">
    <button onclick="updateStock(${item.id}, -1)">−</button>
    <button onclick="updateStock(${item.id}, +1)">+</button>
</div>
           
           <button onclick="deleteItem(${item.id})">Poista</button>
        `;

        container.appendChild(div);
    });
}

// Uuden tuotteen lisääminen
document.getElementById("add-item-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("name", document.getElementById("name").value);
    formData.append("description", document.getElementById("description").value);
    formData.append("price", document.getElementById("price").value);
    formData.append("stock", document.getElementById("stock").value);
    formData.append("category", document.getElementById("categorySelect").value);

    const imageFile = document.getElementById("image").files[0];
    if (imageFile) {
        formData.append("image", imageFile);
    }

    const response = await fetch("http://localhost:5000/items", {
    method: "POST",
    body: formData
});


    if (response.ok) {
        fetchItems();
        e.target.reset();
    }
});


// Tuotteen poistaminen
async function deleteItem(id) {
    await fetch(`http://localhost:5000/items/${id}`, {
        method: "DELETE"
    });

    fetchItems();
}
async function renderCategoryButtons() {
    const categories = await loadCategories();
    const container = document.getElementById("category-buttons");

    container.innerHTML = "";

    // "Kaikki" -painike
    const allBtn = document.createElement("button");
    allBtn.textContent = "Kaikki";
    allBtn.className = activeCategory === null ? "active-category" : "";
    allBtn.onclick = () => {
        activeCategory = null;
        fetchItems();
        renderCategoryButtons();
    };
    container.appendChild(allBtn);

    // Luodaan painike jokaiselle kategorialle
    categories.forEach(cat => {
        const btn = document.createElement("button");
        btn.textContent = cat;

        // Korostus
        btn.className = activeCategory === cat ? "active-category" : "";

        btn.onclick = () => {
            activeCategory = cat;
            fetchItems(cat);
            renderCategoryButtons();
        };

        container.appendChild(btn);
    });
}


async function loadCategories() {
    const response = await fetch("http://localhost:5000/categories");
    const categories = await response.json();
    return categories;
}
async function populateCategoryDropdown() {
    const categories = await loadCategories();
    const select = document.getElementById("categorySelect");

    // Tyhjennetään varmuuden vuoksi (jos siellä on jotain)
    select.innerHTML = '<option value="">Valitse kategoria</option>';

    categories.forEach(cat => {
        const option = document.createElement("option");
        option.value = cat;
        option.textContent = cat;
        select.appendChild(option);
    });
}


async function updateStock(id, change) {
    const response = await fetch(`http://localhost:5000/items/${id}/stock`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ change: change })
    });

    const updatedItem = await response.json();

    // Päivitä DOM heti
    const card = document.querySelector(`[data-id="${id}"]`);
    if (card) {
        const stockText = card.querySelector(".stock-text");
        stockText.textContent = `${updatedItem.in_stock ? "Varastossa" : "Ei varastossa"} (${updatedItem.stock} kpl)`;
    }
}



// Ladataan tuotteet sivun avautuessa
fetchItems();
populateCategoryDropdown();
renderCategoryButtons();



