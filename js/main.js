document.addEventListener('DOMContentLoaded', function() {
    let productCount = 1;
    
    // Add Product Button
    document.getElementById('addProductBtn').addEventListener('click', function() {
        productCount++;
        const container = document.getElementById('productsContainer');
        
        const productHtml = `
            <div class="product-item border rounded p-3 mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h5 class="mb-0">Product ${productCount}</h5>
                    <button type="button" class="btn btn-danger btn-sm remove-product">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label class="form-label">Product Name *</label>
                            <input type="text" class="form-control" name="product_name" required>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="mb-3">
                            <label class="form-label">Price ($)</label>
                            <input type="number" class="form-control" name="product_price" step="0.01" min="0">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label">Image</label>
                            <input type="file" class="form-control" name="product_image" accept="image/*">
                        </div>
                    </div>
                </div>
                <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea class="form-control" name="product_description" rows="2"></textarea>
                </div>
            </div>
        `;
        
        container.insertAdjacentHTML('beforeend', productHtml);
        updateRemoveButtons();
    });
    
    // Remove Product functionality
    document.addEventListener('click', function(e) {
        if (e.target.closest('.remove-product')) {
            const productItem = e.target.closest('.product-item');
            productItem.remove();
            updateProductNumbers();
            updateRemoveButtons();
        }
    });
    
    // Theme selection
    document.querySelectorAll('.theme-option').forEach(function(option) {
        option.addEventListener('click', function() {
            // Remove selected class from all options
            document.querySelectorAll('.theme-option').forEach(opt => opt.classList.remove('border-primary'));
            
            // Add selected class to clicked option
            this.classList.add('border-primary');
            
            // Check the radio button
            const radio = this.querySelector('input[type="radio"]');
            radio.checked = true;
        });
    });
    
    // File upload preview
    document.addEventListener('change', function(e) {
        if (e.target.type === 'file' && e.target.accept === 'image/*') {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Create preview if it doesn't exist
                    let preview = e.target.parentElement.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('div');
                        preview.className = 'image-preview mt-2';
                        e.target.parentElement.appendChild(preview);
                    }
                    preview.innerHTML = `<img src="${e.target.result}" alt="Preview" class="img-thumbnail" style="max-width: 150px; max-height: 150px;">`;
                };
                reader.readAsDataURL(file);
            }
        }
    });
    
    // Form validation
    document.getElementById('micrositeForm').addEventListener('submit', function(e) {
        const businessName = document.getElementById('business_name').value.trim();
        if (!businessName) {
            e.preventDefault();
            alert('Please enter a business name');
            return;
        }
        
        // Check if at least one product has a name
        const productNames = document.querySelectorAll('input[name="product_name"]');
        let hasProduct = false;
        productNames.forEach(function(input) {
            if (input.value.trim()) {
                hasProduct = true;
            }
        });
        
        if (!hasProduct) {
            e.preventDefault();
            alert('Please add at least one product');
            return;
        }
        
        // Show loading state
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
        submitBtn.disabled = true;
        
        // Re-enable button after 10 seconds in case of error
        setTimeout(function() {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 10000);
    });
    
    function updateRemoveButtons() {
        const products = document.querySelectorAll('.product-item');
        products.forEach(function(product, index) {
            const removeBtn = product.querySelector('.remove-product');
            if (products.length > 1) {
                removeBtn.style.display = 'inline-block';
            } else {
                removeBtn.style.display = 'none';
            }
        });
    }
    
    function updateProductNumbers() {
        const products = document.querySelectorAll('.product-item');
        products.forEach(function(product, index) {
            const heading = product.querySelector('h5');
            heading.textContent = `Product ${index + 1}`;
        });
        productCount = products.length;
    }
    
    // Initialize
    updateRemoveButtons();
});