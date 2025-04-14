// script.js
console.log("Testing workability");

let cart = JSON.parse(localStorage.getItem('cart')) || {};

// Add to cart with robust price parsing
$(document).on('click', '.atc', function () {
    const itemId = this.id.toString();
    
    // Clean name
    const productName = document.getElementById(`name-${itemId}`)
                        .textContent
                        .trim()
                        .replace(/\s\s+/g, ' ');
    
    // Extract first valid number from price
    const priceText = document.getElementById(`price-${itemId}`).textContent;
    const productPrice = parseFloat(
        priceText.match(/[\d]+(\.[\d]+)?/)?.[0] || '0'
    );

    if (!cart[itemId]) {
        cart[itemId] = {
            quantity: 0,
            name: productName,
            price: productPrice
        };
    }
    cart[itemId].quantity++;

    console.log(cart);
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartDisplay();
});

// Rest of your code remains the same except for the fixes above
function initPopover() {
    new bootstrap.Popover(document.getElementById('cart'), {
        html: true,
        placement: 'bottom',
        title: 'Your Cart',
        content: generatePopoverContent(),
        trigger: 'click'
    });
}

function generatePopoverContent() {
    if (!Object.keys(cart).length) return 'Your cart is empty';

    // Calculate total price
    const totalPrice = Object.values(cart).reduce(
        (sum, item) => sum + (item.price * item.quantity),
        0
    );

    return `
        <div class="cart-items-list" style="min-width: 250px">
            ${Object.entries(cart).map(([id, item], index) => `
                <div class="cart-item d-flex justify-content-between py-2">
                    <span class="text-muted me-2">${index + 1}.</span>
                    <span class="text-truncate">${item.name}</span>
                    <div>
                        <span class="badge bg-primary ms-2">Qty: ${item.quantity}</span>
                    </div>
                </div>  
            `).join('')}
            
            <!-- Total Price Section -->
            <div class="mt-3 border-top pt-2">
                <div class="d-flex justify-content-between fw-bold">
                    <span>Total:</span>
                    <span>$${totalPrice.toFixed(2)}</span>
                </div>
            </div>
            
            <div class="mt-3">
                <a href="/checkout" class="btn btn-warning w-100">Checkout</a>
            </div>
        </div>
    `;
}

function updateCartDisplay() {
    const cartButton = document.getElementById('cart');
    if (!cartButton) return;

    // Calculate item count
    const itemCount = Object.values(cart).reduce(
        (total, item) => total + item.quantity, 
        0
    );

    // Update button
    cartButton.innerHTML = `Cart (${itemCount})`;

    // Update popover
    const popover = bootstrap.Popover.getInstance(cartButton);
    if (popover) {
        popover.setContent({
            '.popover-header': 'Your Cart',
            '.popover-body': generatePopoverContent()
        });
        popover.update();
    }
}

// Initialize when ready
document.addEventListener('DOMContentLoaded', () => {
    // Convert legacy cart format if needed
    if (localStorage.getItem('cart') && typeof Object.values(cart)[0] === 'number') {
        cart = {};
        localStorage.removeItem('cart');
    }
    
    initPopover();
    updateCartDisplay();
});