import React, { useState } from "react";

const SaleForm = () => {
  const [selectedProduct, setSelectedProduct] = useState<number | null>(null);
  const [quantity, setQuantity] = useState<number>(1);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (selectedProduct !== null && quantity > 0) {
      const saleData = {
        product_id: selectedProduct,
        quantity: quantity,
      };

      // Send sale data to the backend
      fetch("http://127.0.0.1:8000/api/sale/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(saleData),
      })
        .then((response) => response.json())
        .then((data) => console.log("Sale created:", data))
        .catch((error) => console.error("Error creating sale:", error));
    }
  };

  return (
    <div>
      <h2>Create Sale</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Select Product:</label>
          <select
            value={selectedProduct || ""}
            onChange={(e) => setSelectedProduct(Number(e.target.value))}
          >
            <option value="">Select a product</option>
            {/* You can replace this with a dynamic list of products */}
            <option value={1}>Product 1</option>
            <option value={2}>Product 2</option>
          </select>
        </div>
        <div>
          <label>Quantity:</label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(Number(e.target.value))}
            min="1"
          />
        </div>
        <button type="submit">Create Sale</button>
      </form>
    </div>
  );
};

export default SaleForm;
