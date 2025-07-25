const API_URL = "http://127.0.0.1:5000/products";

document.getElementById("saveProduct").addEventListener("click", async () => {
    const id = document.getElementById("productId").value;
    const name = document.getElementById("name").value.trim();
    const description = document.getElementById("description").value.trim();
    const price = parseFloat(document.getElementById("price").value);
    const quantity = parseInt(document.getElementById("quantity").value);

    if (!name || isNaN(price) || isNaN(quantity)) {
        alert("Please fill name, price and quantity correctly!");
        return;
    }

    const product = { name, description, price, quantity };

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(product)
        });

        if (!response.ok) {
            throw new Error("Failed to save product");
        }

        const data = await response.json();
        alert(data.message);
        loadProducts();
    } catch (error) {
        alert("Error: " + error.message);
    }
});

async function loadProducts() {
    try {
        const response = await fetch(API_URL);
        const products = await response.json();

        const table = document.querySelector("#productTable tbody");
        table.innerHTML = "";

        products.forEach((p) => {
            const row = `
                <tr>
                    <td>${p.name}</td>
                    <td>${p.description}</td>
                    <td>${p.price}</td>
                    <td>${p.quantity}</td>
                    <td><button onclick="deleteProduct(${p.id})">Delete</button></td>
                </tr>`;
            table.innerHTML += row;
        });
    } catch (error) {
        console.error("Error fetching products:", error);
    }
}

async function deleteProduct(id) {
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    loadProducts();
}

loadProducts();