document.addEventListener('DOMContentLoaded', function() {
    // Initialize sample data if database is empty
    initializeSampleData();
    
    // Load categories and APIs
    loadCategories();
    loadAPIs();
    
    // Search functionality
    document.getElementById('search-btn').addEventListener('click', performSearch);
    document.getElementById('search-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // All APIs button
    document.getElementById('all-apis-btn').addEventListener('click', function() {
        loadAPIs();
    });
    
    // Refresh button
    document.getElementById('refresh-btn').addEventListener('click', function() {
        loadAPIs();
    });
    
    // Favorites button
    document.getElementById('favorites-btn').addEventListener('click', showFavorites);
    
    // Close modal buttons
    document.getElementById('close-modal').addEventListener('click', closeModal);
    document.getElementById('close-favorites').addEventListener('click', closeFavorites);
    
    // Close modal when clicking outside
    document.getElementById('api-modal').addEventListener('click', function(e) {
        if (e.target === this) closeModal();
    });
    
    document.getElementById('favorites-modal').addEventListener('click', function(e) {
        if (e.target === this) closeFavorites();
    });
});

// Initialize sample data
async function initializeSampleData() {
    try {
        const response = await fetch('/api/init_sample_data');
        const data = await response.json();
        console.log(data.message);
    } catch (error) {
        console.error('Error initializing sample data:', error);
    }
}

// Load categories
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const categories = await response.json();
        
        const container = document.getElementById('categories-container');
        container.innerHTML = '';
        
        categories.forEach(category => {
            const categoryElement = document.createElement('div');
            categoryElement.className = 'bg-white rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer card-hover';
            categoryElement.innerHTML = `
                <div class="text-center">
                    <div class="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-2">
                        <i class="fa fa-${getCategoryIcon(category.name)} text-primary text-xl"></i>
                    </div>
                    <h3 class="font-medium text-gray-900">${category.name}</h3>
                </div>
            `;
            
            categoryElement.addEventListener('click', () => loadAPIs(category.name));
            container.appendChild(categoryElement);
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Get category icon
function getCategoryIcon(categoryName) {
    const icons = {
        'Weather': 'cloud',
        'Maps & Geocoding': 'map-marker',
        'News': 'newspaper-o',
        'AI & Machine Learning': 'robot',
        'Social Media': 'share-alt',
        'Finance': 'dollar',
        'Development Tools': 'code'
    };
    
    return icons[categoryName] || 'cog';
}

// Load APIs
async function loadAPIs(category = null) {
    try {
        const container = document.getElementById('apis-container');
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                <p class="text-gray-500">Loading APIs...</p>
            </div>
        `;
        
        let url = '/api/apis';
        if (category) {
            url += `?category=${encodeURIComponent(category)}`;
        }
        
        const response = await fetch(url);
        const apis = await response.json();
        
        container.innerHTML = '';
        
        if (apis.length === 0) {
            container.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <i class="fa fa-search text-gray-400 text-4xl mb-4"></i>
                    <p class="text-gray-500">No APIs found</p>
                </div>
            `;
            return;
        }
        
        apis.forEach(api => {
            const apiCard = document.createElement('div');
            apiCard.className = 'bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer card-hover';
            apiCard.innerHTML = `
                <div class="p-6">
                    <div class="flex justify-between items-start mb-4">
                        <h3 class="text-lg font-semibold text-gray-900">${api.name}</h3>
                        <span class="px-3 py-1 bg-${api.auth_required ? 'red' : 'green'}-100 text-${api.auth_required ? 'red' : 'green'}-800 rounded-full text-xs font-medium">
                            ${api.auth_required ? 'API Key Required' : 'No Auth'}
                        </span>
                    </div>
                    <p class="text-gray-600 mb-4 line-clamp-3">${api.description || 'No description available'}</p>
                    <div class="flex flex-wrap gap-2 mb-4">
                        <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">${api.category}</span>
                        <span class="px-2 py-1 bg-gray-100 text-gray-800 rounded text-xs">${api.rate_limit || 'Unlimited'}</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <button class="view-details-btn px-4 py-2 bg-primary text-white rounded hover:bg-primary/90 transition-colors text-sm" data-api-id="${api.id}">
                            View Details
                        </button>
                        <button class="favorite-btn px-3 py-1 border border-gray-300 rounded hover:bg-gray-50 transition-colors text-sm" data-api-id="${api.id}">
                            <i class="fa fa-star-o mr-1"></i>
                            <span>Add to Favorites</span>
                        </button>
                    </div>
                </div>
            `;
            
            apiCard.querySelector('.view-details-btn').addEventListener('click', () => showAPIDetails(api.id));
            apiCard.querySelector('.favorite-btn').addEventListener('click', (e) => toggleFavorite(e, api.id));
            
            container.appendChild(apiCard);
        });
    } catch (error) {
        console.error('Error loading APIs:', error);
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <i class="fa fa-exclamation-triangle text-yellow-500 text-4xl mb-4"></i>
                <p class="text-gray-500">Error loading APIs. Please try again later.</p>
            </div>
        `;
    }
}

// Perform search
async function performSearch() {
    const searchTerm = document.getElementById('search-input').value.trim();
    if (!searchTerm) {
        loadAPIs();
        return;
    }
    
    try {
        const container = document.getElementById('apis-container');
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                <p class="text-gray-500">Searching APIs...</p>
            </div>
        `;
        
        const response = await fetch(`/api/apis?search=${encodeURIComponent(searchTerm)}`);
        const apis = await response.json();
        
        container.innerHTML = '';
        
        if (apis.length === 0) {
            container.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <i class="fa fa-search text-gray-400 text-4xl mb-4"></i>
                    <p class="text-gray-500">No APIs found matching "${searchTerm}"</p>
                </div>
            `;
            return;
        }
        
        apis.forEach(api => {
            const apiCard = document.createElement('div');
            apiCard.className = 'bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer card-hover';
            apiCard.innerHTML = `
                <div class="p-6">
                    <div class="flex justify-between items-start mb-4">
                        <h3 class="text-lg font-semibold text-gray-900">${api.name}</h3>
                        <span class="px-3 py-1 bg-${api.auth_required ? 'red' : 'green'}-100 text-${api.auth_required ? 'red' : 'green'}-800 rounded-full text-xs font-medium">
                            ${api.auth_required ? 'API Key Required' : 'No Auth'}
                        </span>
                    </div>
                    <p class="text-gray-600 mb-4 line-clamp-3">${api.description || 'No description available'}</p>
                    <div class="flex flex-wrap gap-2 mb-4">
                        <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">${api.category}</span>
                        <span class="px-2 py-1 bg-gray-100 text-gray-800 rounded text-xs">${api.rate_limit || 'Unlimited'}</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <button class="view-details-btn px-4 py-2 bg-primary text-white rounded hover:bg-primary/90 transition-colors text-sm" data-api-id="${api.id}">
                            View Details
                        </button>
                        <button class="favorite-btn px-3 py-1 border border-gray-300 rounded hover:bg-gray-50 transition-colors text-sm" data-api-id="${api.id}">
                            <i class="fa fa-star-o mr-1"></i>
                            <span>Add to Favorites</span>
                        </button>
                    </div>
                </div>
            `;
            
            apiCard.querySelector('.view-details-btn').addEventListener('click', () => showAPIDetails(api.id));
            apiCard.querySelector('.favorite-btn').addEventListener('click', (e) => toggleFavorite(e, api.id));
            
            container.appendChild(apiCard);
        });
    } catch (error) {
        console.error('Error searching APIs:', error);
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <i class="fa fa-exclamation-triangle text-yellow-500 text-4xl mb-4"></i>
                <p class="text-gray-500">Error searching APIs. Please try again later.</p>
            </div>
        `;
    }
}

// Show API details
async function showAPIDetails(apiId) {
    try {
        const response = await fetch(`/api/apis/${apiId}`);
        const api = await response.json();
        
        if (!api) {
            alert('API not found');
            return;
        }
        
        document.getElementById('modal-title').textContent = api.name;
        const modalContent = document.getElementById('modal-content');
        
        modalContent.innerHTML = `
            <div class="space-y-6">
                <div>
                    <h4 class="text-lg font-semibold text-gray-900 mb-2">Description</h4>
                    <p class="text-gray-600">${api.description || 'No description available'}</p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <h4 class="text-lg font-semibold text-gray-900 mb-2">API Endpoint</h4>
                        <div class="bg-gray-100 p-3 rounded font-mono text-sm overflow-x-auto">
                            ${api.url || 'Not available'}
                        </div>
                    </div>
                    <div>
                        <h4 class="text-lg font-semibold text-gray-900 mb-2">Category</h4>
                        <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">${api.category}</span>
                    </div>
                </div>
                
                <div>
                    <h4 class="text-lg font-semibold text-gray-900 mb-2">Authentication</h4>
                    <p class="text-gray-600 mb-2">${api.auth_required ? 'API Key Required' : 'No Authentication Required'}</p>
                    ${api.auth_required ? `
                        <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4">
                            <div class="flex">
                                <div class="flex-shrink-0">
                                    <i class="fa fa-info-circle text-yellow-500"></i>
                                </div>
                                <div class="ml-3">
                                    <p class="text-sm text-yellow-700">${api.api_key_instructions || 'No instructions available'}</p>
                                </div>
                            </div>
                        </div>
                    ` : ''}
                </div>
                
                <div>
                    <h4 class="text-lg font-semibold text-gray-900 mb-2">Rate Limits</h4>
                    <p class="text-gray-600">${api.rate_limit || 'Unlimited'}</p>
                </div>
                
                <div>
                    <h4 class="text-lg font-semibold text-gray-900 mb-2">Documentation</h4>
                    <a href="${api.documentation_url || '#'}" target="_blank" class="text-primary hover:text-primary/80 inline-flex items-center">
                        <i class="fa fa-external-link mr-2"></i>
                        View Documentation
                    </a>
                </div>
                
                <div class="flex space-x-4 pt-4">
                    <button class="px-6 py-3 bg-primary text-white rounded hover:bg-primary/90 transition-colors" onclick="window.open('${api.url || '#'}', '_blank')">
                        <i class="fa fa-external-link mr-2"></i>
                        Visit API
                    </button>
                    <button class="px-6 py-3 border border-gray-300 rounded hover:bg-gray-50 transition-colors" onclick="toggleFavorite(null, ${api.id}, true)">
                        <i class="fa fa-star-o mr-2"></i>
                        Add to Favorites
                    </button>
                </div>
            </div>
        `;
        
        document.getElementById('api-modal').classList.remove('hidden');
    } catch (error) {
        console.error('Error loading API details:', error);
        alert('Error loading API details. Please try again.');
    }
}

// Toggle favorite
async function toggleFavorite(event, apiId, fromModal = false) {
    try {
        const userId = 'user123'; // In a real app, this would be the authenticated user ID
        
        const response = await fetch('/api/favorites', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: userId, api_id: apiId }),
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (event) {
                const button = event.currentTarget;
                button.innerHTML = '<i class="fa fa-star mr-1 text-yellow-500"></i><span>Added to Favorites</span>';
                button.classList.add('bg-yellow-50');
            }
            
            if (fromModal) {
                alert('Added to favorites!');
            }
        }
    } catch (error) {
        console.error('Error adding to favorites:', error);
        alert('Error adding to favorites. Please try again.');
    }
}

// Show favorites
async function showFavorites() {
    try {
        const userId = 'user123'; // In a real app, this would be the authenticated user ID
        
        const response = await fetch(`/api/favorites/${userId}`);
        const favorites = await response.json();
        
        const favoritesContent = document.getElementById('favorites-content');
        
        if (favorites.length === 0) {
            favoritesContent.innerHTML = `
                <div class="text-center py-8">
                    <i class="fa fa-heart-o text-gray-400 text-4xl mb-4"></i>
                    <p class="text-gray-500">You haven't added any APIs to your favorites yet.</p>
                </div>
            `;
        } else {
            favoritesContent.innerHTML = '';
            favorites.forEach(api => {
                const favoriteItem = document.createElement('div');
                favoriteItem.className = 'bg-white rounded-lg shadow-sm p-4 border border-gray-100';
                favoriteItem.innerHTML = `
                    <div class="flex justify-between items-start">
                        <div>
                            <h4 class="font-semibold text-gray-900">${api.name}</h4>
                            <p class="text-gray-600 text-sm mt-1">${api.description ? api.description.substring(0, 100) + '...' : 'No description'}</p>
                            <div class="flex items-center mt-2 text-sm text-gray-500">
                                <span class="mr-4">${api.category}</span>
                                <span>${api.rate_limit || 'Unlimited'}</span>
                            </div>
                        </div>
                        <div class="flex space-x-2">
                            <button class="px-3 py-1 bg-primary text-white rounded text-sm" onclick="showAPIDetails(${api.id})">
                                <i class="fa fa-eye mr-1"></i>View
                            </button>
                            <button class="px-3 py-1 border border-gray-300 rounded text-sm hover:bg-gray-50">
                                <i class="fa fa-trash-o mr-1"></i>Remove
                            </button>
                        </div>
                    </div>
                `;
                favoritesContent.appendChild(favoriteItem);
            });
        }
        
        document.getElementById('favorites-modal').classList.remove('hidden');
    } catch (error) {
        console.error('Error loading favorites:', error);
        favoritesContent.innerHTML = `
            <div class="text-center py-8">
                <i class="fa fa-exclamation-triangle text-yellow-500 text-2xl mb-2"></i>
                <p class="text-gray-500">Error loading favorites. Please try again.</p>
            </div>
        `;
        document.getElementById('favorites-modal').classList.remove('hidden');
    }
}

// Close modal
function closeModal() {
    document.getElementById('api-modal').classList.add('hidden');
}

// Close favorites modal
function closeFavorites() {
    document.getElementById('favorites-modal').classList.add('hidden');
}

// Close modals when ESC key is pressed
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
        closeFavorites();
    }
});