// checkout.js
document.addEventListener('DOMContentLoaded', () => {
    const cart = JSON.parse(localStorage.getItem('cart')) || {};
    const listGroup = document.querySelector('.list-group');
    
    // Clear existing static content
    listGroup.innerHTML = '';

    if (Object.keys(cart).length === 0) {
        listGroup.innerHTML = `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                Your cart is empty
            </li>
        `;
        return;
    }

    // Create cart items
    Object.entries(cart).forEach(([itemId, item]) => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            ${item.name}
            <div>
                <span class="badge bg-primary rounded-pill me-2">Qty: ${item.quantity}</span>
                <span class="badge bg-success rounded-pill">${item.price}</span>
            </div>
        `;
        listGroup.appendChild(li);
    });
});