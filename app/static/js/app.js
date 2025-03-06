document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('searchForm');
    const results = document.getElementById('results');
    const loading = document.getElementById('loading');
    const companyStatus = document.getElementById('companyStatus');
    const productDetails = document.getElementById('productDetails');
    const alternatives = document.getElementById('alternatives');
    const alternativesList = document.getElementById('alternativesList');

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const productName = document.getElementById('productName').value;
        
        if (!productName) return;

        // Show loading state
        results.classList.add('hidden');
        loading.classList.remove('hidden');

        try {
            const formData = new FormData();
            formData.append('product_name', productName);

            const response = await fetch('/search', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                displayResults(data);
            } else {
                throw new Error(data.error || 'Failed to fetch results');
            }
        } catch (error) {
            alert(error.message);
        } finally {
            loading.classList.add('hidden');
            results.classList.remove('hidden');
        }
    });

    function displayResults(data) {
        // Display company status
        companyStatus.innerHTML = '';
        companyStatus.className = 'p-4 rounded-lg mb-4';
        
        if (data.product.is_trump_supporter) {
            companyStatus.classList.add('bg-red-100', 'text-red-700');
            companyStatus.innerHTML = `
                <div class="flex items-center">
                    <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                    </svg>
                    <span class="font-semibold">Warning: ${data.product.company} supports the Trump administration</span>
                </div>
            `;
        } else {
            companyStatus.classList.add('bg-green-100', 'text-green-700');
            companyStatus.innerHTML = `
                <div class="flex items-center">
                    <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                    </svg>
                    <span class="font-semibold">${data.product.company} does not support the Trump administration</span>
                </div>
            `;
        }

        // Display alternatives if company supports Trump
        if (data.product.is_trump_supporter && data.alternatives.length > 0) {
            alternatives.classList.remove('hidden');
            alternativesList.innerHTML = data.alternatives.map(alt => `
                <div class="bg-white p-4 rounded-lg shadow product-card">
                    <div class="flex items-start">
                        ${alt.product.image_url ? `
                            <img src="${alt.product.image_url}" alt="${alt.product.name}" class="w-24 h-24 object-cover rounded mr-4">
                        ` : ''}
                        <div class="flex-1">
                            <h3 class="font-semibold text-lg">${alt.product.name}</h3>
                            <p class="text-gray-600">${alt.product.description}</p>
                            <div class="mt-2">
                                <h4 class="font-medium">Where to Buy:</h4>
                                <ul class="space-y-1">
                                    ${alt.retailers.map(retailer => `
                                        <li>
                                            <a href="${retailer.url}" target="_blank" class="text-blue-500 hover:underline">
                                                ${retailer.name}: $${retailer.price.toFixed(2)}
                                            </a>
                                            ${retailer.address ? `<span class="text-gray-500"> - ${retailer.address}</span>` : ''}
                                        </li>
                                    `).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            alternatives.classList.add('hidden');
        }
    }
});
