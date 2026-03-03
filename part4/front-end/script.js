document.addEventListener('DOMContentLoaded', () => {
    console.log('HBnB application loaded successfully');
    
    initializePage();
    
    setupCommonEventListeners();
});

function initializePage() {
    const currentPage = window.location.pathname.split('/').pop();
    switch(currentPage) {
        case 'index.html':
        case '':
            initializeHomePage();
            break;
        case 'login.html':
            initializeLoginPage();
            break;
        case 'place.html':
            initializePlaceDetailsPage();
            break;
        case 'add_review.html':
            initializeAddReviewPage();
            break;
        case 'register.html':
            initializeRegisterPage();
            break;
        default:
            console.log('Page specific initialization not required');
    }
}

function initializeRegisterPage() {
    console.log('Initializing registration page...');
}

function initializeHomePage() {
    console.log('Initializing homepage...');
    checkAuthentication();
    setupPriceFilter();
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLinks = document.querySelectorAll('.login-button, nav a[href="login.html"]');
    
    console.log('Token found:', !!token);
    console.log('Login links found:', loginLinks.length);
    
    if (!token) {
        loginLinks.forEach(link => {
            link.classList.remove('hidden');
            console.log('Showing login link:', link);
        });
        
        const existingUserInfo = document.querySelector('.user-info');
        if (existingUserInfo) {
            existingUserInfo.remove();
        }
    } else {
        loginLinks.forEach(link => {
            link.classList.add('hidden');
        });
        
        const header = document.querySelector('.header-container');
        if (header && !header.querySelector('.user-info')) {
            const userInfo = document.createElement('div');
            userInfo.className = 'user-info';
            userInfo.innerHTML = `
                <span>Welcome back!</span>
                <button onclick="logout()" class="logout-button">Logout</button>
            `;
            header.appendChild(userInfo);
        }
    }
    fetchPlaces(token);
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

async function fetchPlaces(token) {
    console.log('Fetching places from API...');
    console.log('Backend URL:', 'http://localhost:5000/api/v1/places/');
    console.log('Current page URL:', window.location.href); 

    try {
        const response = await fetch('http://localhost:5000/api/v1/places/');
        if (!response.ok) throw new Error('Failed to fetch places');
        const places = await response.json();
        window.allPlaces = places;
        displayPlaces(places);
    } catch (err) {
        console.error('Error fetching places:', err);

        const placesList = document.getElementById('places-list');
        if (placesList) {
            placesList.innerHTML = `
                <div style="text-align: center; margin-top: 20px;">
                    <h3>Unable to load places</h3>
                    <p>Error: ${err.message}</p>
                </div>
            `;
        }
    }
}



function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';
    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places found.</p>';
        return;
    }
    places.forEach((place, index) => {  
        const card = document.createElement('div');
        card.className = 'place-card';
        

        let imageSrc = '';
        console.log(`Card for place: ${index + 1}: ${place.title}`);

        const titleLower = place.title.toLowerCase();
        
        if (titleLower.includes('cozy downtown') || titleLower.includes('downtown')) {
            imageSrc = 'place1.jpg';
        } else if (titleLower.includes('modern studio') || titleLower.includes('studio')) {
            imageSrc = 'place2.jpg';
        } else if (titleLower.includes('luxury villa') || titleLower.includes('villa')) {
            imageSrc = 'place3.jpg';
        } else if (titleLower.includes('beach house') || titleLower.includes('beach')) {
            imageSrc = 'place4.jpg';
        } else if (titleLower.includes('mountain cabin') || titleLower.includes('mountain') || titleLower.includes('cabin')) {
            imageSrc = 'place5.jpg';
        } else if (titleLower.includes('urban loft') || titleLower.includes('loft') || titleLower.includes('urban')) {
            imageSrc = 'place6.jpg';
        }

        console.log(`Selected image "${place.title}": ${imageSrc}`);

        const imageHtml = imageSrc ? `<img src="${imageSrc}" alt="${place.title}">` : '';
        
        card.innerHTML = `
            ${imageHtml}
            <h3>${place.title}</h3>
            <p>${place.description || ''}</p>
            <div class="place-price">$${place.price}/night</div>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(card);
        console.log(`Card added for place: ${place.title}`);
    });
}


function setupPriceFilter() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;
    filter.addEventListener('change', (event) => {
        const value = event.target.value;
        let filtered = window.allPlaces || [];
        if (value === 'all') {
            displayPlaces(filtered);
            return;
        }
        const max = parseInt(value, 10);
        filtered = filtered.filter(place => place.price <= max);
        displayPlaces(filtered);
    });
}


function initializeLoginPage() {
    console.log('Initializing login page...');
    
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLoginSubmit);
    }
}


function initializePlaceDetailsPage() {
    console.log('Initializing place details page...');
    
    testAPIConnectivity();
    
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (placeId) {
        console.log('Loading details for place ID:', placeId);
        loadPlaceDetails(placeId);
    }
    
    setupReviewInteractions();
}

function testAPIConnectivity() {
    console.log('Testing API connectivity...');
    fetch('http://localhost:5000/api/v1/places/', {
        method: 'GET',
        mode: 'cors'
    })
    .then(response => {
        console.log('API connectivity test - Status:', response.status);
        console.log('API connectivity test - OK:', response.ok);
        if (response.ok) {
            console.log('APIis reachable');
        } else {
            console.log('API returned error status');
        }
    })
    .catch(error => {
        console.log('API connectivity test failed:', error);
        console.log('This usually means:');
        console.log('1. Backend server is not running on port 5000');
        console.log('2. CORS is not properly configured');
        console.log('3. Network connectivity issues');
    });
}

function initializeAddReviewPage() {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(reviewForm);
            const reviewText = formData.get('review');
            const rating = formData.get('rating');
            let reviewer = formData.get('reviewer');
            if (!reviewText || !rating) {
                alert('Please provide both a rating and review text');
                return;
            }
            try {
                const response = await fetch(`http://localhost:8000/api/v1/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        reviewer: reviewer,
                        rating: rating,
                        text: reviewText
                    })
                });
                if (response.ok) {
                    alert('Review submitted successfully!');
                    reviewForm.reset();
                } else {
                    let errorMsg = 'Failed to submit review';
                    try {
                        const err = await response.json();
                        if (err && err.message) errorMsg = err.message;
                    } catch {}
                    alert(errorMsg);
                }
            } catch (err) {
                alert('Failed to submit review: ' + err.message);
            }
        });
    }
    if (typeof setupRatingInteraction === 'function') {
        setupRatingInteraction();
    }
}

function checkAddReviewAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}


function setupCommonEventListeners() {
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            console.log('Navigation:', e.target.textContent);
        });
    });
    
    const loginButton = document.querySelector('.login-button');
    if (loginButton) {
        loginButton.addEventListener('click', (e) => {
            console.log('Login button clicked');
        });
    }
}

function handleLoginSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const email = formData.get('email');
    const password = formData.get('password');
    
    console.log('Login attempt:', email);
    
    if (!email || !password) {
        alert('Please fill in all fields');
        return;
    }
    
    if (!isValidEmail(email)) {
        alert('Please enter a valid email address');
        return;
    }
    
    loginUser(email, password);
}

async function loginUser(email, password) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            let errorMsg = 'Login failed';
            try {
                const err = await response.json();
                if (err && err.message) errorMsg = err.message;
            } catch {}
            alert(errorMsg);
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
}


function handleReviewSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const rating = formData.get('rating');
    const review = formData.get('review');
    const placeName = formData.get('place-name');
    
    console.log('Review submission:', { rating, review, placeName });
    
    if (!rating || !review.trim()) {
        alert('Please provide both a rating and review text');
        return;
    }
    
    if (review.trim().length < 10) {
        alert('Please provide a more detailed review (at least 10 characters)');
        return;
    }
    
    simulateReviewSubmission(rating, review, placeName);
}

function addPlaceCardHoverEffects() {
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            console.log('Hovering over:', card.querySelector('h3').textContent);
        });
    });
}

function setupReviewInteractions() {
    const reviewCards = document.querySelectorAll('.review-card');
    
    reviewCards.forEach(card => {
        card.addEventListener('click', () => {
            const reviewer = card.querySelector('.review-user').textContent;
            console.log('Review clicked by:', reviewer);
        });
    });
}

function setupRatingInteraction() {
    const ratingSelect = document.getElementById('rating');
    
    if (ratingSelect) {
        ratingSelect.addEventListener('change', (e) => {
            console.log('Rating selected:', e.target.value);
        });
    }
}
function loadPlaceDetails(placeId) {
    console.log(`Loading place details for ID ${placeId}...`);
    console.log('Attempting to fetch from:', `http://localhost:5000/api/v1/places/${placeId}`);
    
    fetch(`http://localhost:5000/api/v1/places/${placeId}`)
        .then(response => {
            console.log('API Response status:', response.status);
            console.log('API Response ok:', response.ok);
            console.log('API Response headers:', response.headers);
            
            if (!response.ok) {
                return response.text().then(text => {
                    console.log('Error response text:', text);
                    throw new Error(`HTTP ${response.status}: ${text}`);
                });
            }
            return response.json();
        })
        .then(place => {
            console.log('Place data loaded:', place);
            document.getElementById('place-title').textContent = place.title || 'Unknown Title';
            let hostName = 'Unknown';
            if (place.owner && (place.owner.first_name || place.owner.last_name)) {
                hostName = `${place.owner.first_name || ''} ${place.owner.last_name || ''}`.trim();
            }
            document.getElementById('host-name').textContent = hostName || 'Unknown';
            document.getElementById('place-price').textContent = (place.price !== undefined && place.price !== null) ? `$${place.price}/night` : 'N/A';
            let locationText = 'N/A';
            if (place.latitude && place.longitude) {
                locationText = `Lat: ${place.latitude}, Lng: ${place.longitude}`;
            }
            document.getElementById('location-text').textContent = locationText;
            document.getElementById('max-guests').textContent = place.max_guests || 'N/A';
            document.getElementById('place-description').textContent = place.description || 'No description available';
            const imageElement = document.getElementById('place-image');
            if (place.title) {
                const titleLower = place.title.toLowerCase();
                if (titleLower.includes('cozy downtown') || titleLower.includes('downtown')) {
                    imageElement.src = 'place1.jpg';
                    imageElement.style.display = 'block';
                } else if (titleLower.includes('modern studio') || titleLower.includes('studio')) {
                    imageElement.src = 'place2.jpg';
                    imageElement.style.display = 'block';
                } else if (titleLower.includes('luxury villa') || titleLower.includes('villa')) {
                    imageElement.src = 'place3.jpg';
                    imageElement.style.display = 'block';
                } else if (titleLower.includes('beach house') || titleLower.includes('beach')) {
                    imageElement.src = 'place4.jpg';
                    imageElement.style.display = 'block';
                } else if (titleLower.includes('mountain cabin') || titleLower.includes('mountain') || titleLower.includes('cabin')) {
                    imageElement.src = 'place5.jpg';
                    imageElement.style.display = 'block';
                } else if (titleLower.includes('urban loft') || titleLower.includes('loft') || titleLower.includes('urban')) {
                    imageElement.src = 'place6.jpg';
                    imageElement.style.display = 'block';
                } else {
                    imageElement.style.display = 'none';
                }
            } else {
                imageElement.style.display = 'none';
            }
            imageElement.alt = place.title || 'Place image';
            loadPlaceReviews(placeId);
        })
        .catch(error => {
            console.error('Detailed error loading place details:', error);
            console.error('Error message:', error.message);
            console.error('Place ID that failed:', placeId);
            document.getElementById('place-title').textContent = `Error loading place (ID: ${placeId})`;
            document.getElementById('host-name').textContent = 'API Error';
            document.getElementById('place-price').textContent = 'Check console for details';
            document.getElementById('location-text').textContent = error.message || 'Network error';
            document.getElementById('max-guests').textContent = 'N/A';
            document.getElementById('place-description').textContent = `Unable to load place details. Error: ${error.message}. Check the browser console for more details.`;
        });
}

function loadPlaceReviews(placeId) {
    fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`)
        .then(response => {
            console.log('Reviews API Response status:', response.status);
            if (!response.ok) {
                console.log('No reviews found or error loading reviews');
                return [];
            }
            return response.json();
        })
        .then(reviews => {
            const reviewsSection = document.getElementById('reviews');
            const existingReviewCards = reviewsSection.querySelectorAll('.review-card');
            
            existingReviewCards.forEach(card => card.remove());
            
            if (reviews && reviews.length > 0) {
                reviews.forEach(review => {
                    const reviewCard = document.createElement('div');
                    reviewCard.className = 'review-card';
                    reviewCard.innerHTML = `
                        <div class="review-header">
                            <span class="review-user">${review.user?.first_name || 'Anonymous'} ${review.user?.last_name || ''}</span>
                            <span class="review-rating">${'★'.repeat(review.rating)}${'☆'.repeat(5-review.rating)} ${review.rating}/5</span>
                        </div>
                        <p class="review-comment">${review.comment}</p>
                    `;
                    
                    const addReviewButton = reviewsSection.querySelector('.text-center');
                    reviewsSection.insertBefore(reviewCard, addReviewButton);
                });
            } else {
                const defaultReviews = [
                    { user: { first_name: 'Alice', last_name: 'Johnson' }, rating: 5, comment: 'Amazing place! Very clean and exactly as described. The location is perfect for exploring downtown. Great host and very responsive. Highly recommend!' },
                    { user: { first_name: 'Michael', last_name: 'Brown' }, rating: 4, comment: 'Great apartment with all the amenities you need. The wifi was fast and the kitchen was well-equipped. Only minor issue was some street noise at night, but overall a wonderful stay.' },
                    { user: { first_name: 'Sarah', last_name: 'Davis' }, rating: 5, comment: 'Perfect location and beautiful apartment! Everything was spotless and the host provided excellent recommendations for local restaurants. Will definitely stay here again!' }
                ];
                
                defaultReviews.forEach(review => {
                    const reviewCard = document.createElement('div');
                    reviewCard.className = 'review-card';
                    reviewCard.innerHTML = `
                        <div class="review-header">
                            <span class="review-user">${review.user.first_name} ${review.user.last_name}</span>
                            <span class="review-rating">${'★'.repeat(review.rating)}${'☆'.repeat(5-review.rating)} ${review.rating}/5</span>
                        </div>
                        <p class="review-comment">${review.comment}</p>
                    `;
                    
                    const addReviewButton = reviewsSection.querySelector('.text-center');
                    reviewsSection.insertBefore(reviewCard, addReviewButton);
                });
            }
        })
        .catch(error => {
            console.error('Error loading reviews:', error);
        });
}

function simulateLogin(email) {
    console.log('Simulating login for:', email);
    
    alert('Login successful! Welcome to HBnB.');
    
    
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1000);
}

function simulateReviewSubmission(rating, review, placeName) {
    console.log('Simulating review submission...');
    
    alert('Review submitted successfully! Thank you for your feedback.');
    
    setTimeout(() => {
        window.location.href = 'place.html';
    }, 1000);
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    
    window.location.reload();
}

const HBnBUtils = {
   
    formatPrice: function(price) {
        return `$${price}/night`;
    },
    
 
    generateStars: function(rating) {
        const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
        return `${stars} ${rating}/5`;
    },
    
    
    truncateText: function(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
};

window.HBnBUtils = HBnBUtils;
