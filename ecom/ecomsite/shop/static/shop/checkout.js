// checkout.js
document.addEventListener('DOMContentLoaded', () => {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    const listGroup = document.querySelector('.list-group');
    let grandTotal = 0;

    function updateCartDisplay() {
        // Clear existing content
        listGroup.innerHTML = '';
        grandTotal = 0;

        if (Object.keys(cart).length === 0) {
            listGroup.innerHTML = `
                <li class="list-group-item">
                    Your cart is empty
                </li>
            `;
            localStorage.removeItem('cart');
            return;
        }

        // Create cart items
        Object.entries(cart).forEach(([itemId, item]) => {
            const itemTotal = item.quantity * item.price;
            grandTotal += itemTotal;

            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                <div class="d-flex flex-column flex-grow-1 me-3">
                    <span class="fw-bold">${item.name}</span>
                    <small class="text-muted">Price: $${item.price.toFixed(2)}</small>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <div class="input-group input-group-sm" style="width: 120px">
                        <button class="btn btn-outline-danger" onclick="adjustQuantity('${itemId}', -1)">-</button>
                        <input type="text" class="form-control text-center" value="${item.quantity}" readonly>
                        <button class="btn btn-outline-success" onclick="adjustQuantity('${itemId}', 1)">+</button>
                    </div>
                    <span class="badge bg-primary rounded-pill">$${itemTotal.toFixed(2)}</span>
                    <button class="btn btn-danger btn-sm" onclick="removeItem('${itemId}')">&times;</button>
                </div>
            `;
            listGroup.appendChild(li);
        });

        // Add grand total
        const totalLi = document.createElement('li');
        totalLi.className = 'list-group-item d-flex justify-content-between align-items-center fw-bold bg-light';
        totalLi.innerHTML = `
            <span>Grand Total:</span>
            <span class="badge bg-danger rounded-pill">$${grandTotal.toFixed(2)}</span>
        `;
        listGroup.appendChild(totalLi);
    }

    window.adjustQuantity = (itemId, delta) => {
        if (cart[itemId]) {
            cart[itemId].quantity += delta;
            
            if (cart[itemId].quantity < 1) {
                delete cart[itemId];
            }
            
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartDisplay();
        }
    };

    window.removeItem = (itemId) => {
        if (cart[itemId]) {
            delete cart[itemId];
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartDisplay();
        }
    };

    // Initial display
    updateCartDisplay();
});