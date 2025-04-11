// script.js (for product page)
console.log("Testing workability");

let cart = JSON.parse(localStorage.getItem('cart')) || {};

// Modified Add to cart function to store product details
$(document).on('click', '.atc', function () {
    const itemId = this.id.toString();
    const productName = document.getElementById(`name-${itemId}`).textContent;
    const productPrice = document.getElementById(`price-${itemId}`).textContent;

    if (!cart[itemId]) {
        cart[itemId] = {
            quantity: 0,
            name: productName,
            price: productPrice
        };
    }
    cart[itemId].quantity++;
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartDisplay();
});

// initializing the popover
function initPopover() {
    new bootstrap.Popover(document.getElementById('cart'), {
        html: true, placement: 'bottom', title: 'Your Cart', content: generatePopoverContent(), trigger: 'click'
    });
}

// generating the Popover content
function generatePopoverContent() {
    if (Object.keys(cart).length === 0) return 'Your cart is empty';

    return `
        <div class="cart-items-list">
            ${Object.entries(cart).map(([id, qty], cartIndex) => {
        const productNameElement = document.getElementById(`name-${id}`);
        const productName = productNameElement
            ? productNameElement.textContent
            : `Item ${id}`;  // Fallback if name not found


        return `
                    <div class="cart-item d-flex justify-content-between py-2">
                    <span class="text-muted me-2">${cartIndex + 1}.</span>
                        <span>${productName}</span>
                        <span>Qty: ${qty}</span>

                        
                    </div>  
                `;
    }).join('')}
            <a href="/checkout" class="btn btn-warning" id="checkout">Checkout</a>
        </div>
    `;
}

//updating the popover
function updateCartDisplay() {
    const cartButton = document.getElementById('cart');
    const itemCount = Object.values(cart).reduce((a, b) => a + b, 0)

    // displaying the cart amount
    cartButton.innerHTML = `Cart(${itemCount})`;

    // setting the drop down
    const popover = bootstrap.Popover.getInstance(cartButton);
    if (popover) {
        popover.setContent({
            '.popover-body': generatePopoverContent()
        });
    }
}

function showTheCartPage() {
    const container = document.createElement('div');
    container.className = 'container mt-5';

    if (Object.keys(cart).length === 0) {
        container.innerHTML = '<p>Your cart is empty</p>';
        return;
    }

    let html = '<ul class="list-group">';

    Object.entries(cart).forEach(([itemId, quantity]) => {
        const productNameElement = document.getElementById(`name-${itemId}`);
        const productPriceElement = document.getElementById(`price-${itemId}`);

        const productName = productNameElement ? productNameElement.textContent : `Item ${itemId}`;
        const productPrice = productPriceElement ? productPriceElement.textContent : 'Price not available';

        html += `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                ${productName}
                <div>
                    <span class="badge bg-primary rounded-pill me-2">Qty: ${quantity}</span>
                    <span class="badge bg-success rounded-pill">${productPrice}</span>
                </div>
            </li>
        `;
    });

    html += '</ul>';
    container.innerHTML = html;

    // Clear existing content and show cart
    document.body.innerHTML = '';
    document.body.appendChild(container);
}

document.addEventListener('DOMContentLoaded', () => {
    initPopover();
    updateCartDisplay();

    // Add event delegation for dynamically created checkout button
    document.body.addEventListener('click', function (e) {
        if (e.target && e.target.id === 'checkout') {
            e.preventDefault();
            showTheCartPage();
        }
    });
});