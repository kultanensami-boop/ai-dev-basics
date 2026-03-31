// Haetaan tuotteet API:sta ja näytetään ne sivulla
async function fetchItems() {
    const response = await fetch("http://localhost:5000/items");
    const items = await response.json();

    const container = document.getElementById("items-container");
    container.innerHTML = "";

    items.forEach(item => {
        const div = document.createElement("div");
        div.className = "item-card";
        div.setAttribute("data-id", item.id);

        div.innerHTML = `
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
document.getElementById("add-item-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const newItem = {
    name: document.getElementById("name").value,
    description: document.getElementById("description").value,
    price: parseFloat(document.getElementById("price").value),
    category: document.getElementById("category").value,
    in_stock: document.getElementById("in_stock").checked,
    stock: parseInt(document.getElementById("stock").value)
};

    await fetch("http://localhost:5000/items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newItem)
    });

    e.target.reset();
    fetchItems();
});

// Tuotteen poistaminen
async function deleteItem(id) {
    await fetch(`http://localhost:5000/items/${id}`, {
        method: "DELETE"
    });

    fetchItems();
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
