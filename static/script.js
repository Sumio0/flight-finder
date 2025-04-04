document.addEventListener("DOMContentLoaded", function() {
    console.log("📌 Flight Finder JS loaded!");

    const searchInput = document.getElementById("search-input");
    const suggestionsBox = document.getElementById("search-suggestions");
    
    // ✅ 主页：动态加载热门航班
    const popularFlightsContainer = document.getElementById("popular-flights");
    if (popularFlightsContainer) {
        loadPopularFlights();
    }
    
    // Setup form validation for add/edit forms
    const addForm = document.getElementById("add-flight-form");
    if (addForm) {
        setupAddFlightForm(addForm);
    }
    
    const editForm = document.getElementById("edit-flight-form");
    if (editForm) {
        setupEditFlightForm(editForm);
    }
    
    // Setup confirm dialog for discard changes
    const discardBtn = document.querySelector(".btn-discard");
    if (discardBtn) {
        setupDiscardConfirmation(discardBtn);
    }
    
    // Highlight search results
    highlightSearchResults();
    
    // Setup search autocomplete functionality
    if (searchInput && suggestionsBox) {
        searchInput.addEventListener("input", function() {
            let query = searchInput.value.trim().toLowerCase();

            fetch(`/autocomplete?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    console.log("🔍 自动补全返回:", data);
                    if (data.length === 0) {
                        suggestionsBox.style.display = "none";
                        return;
                    }

                    suggestionsBox.innerHTML = "";
                    data.forEach(city => {
                        let suggestion = document.createElement("div");
                        suggestion.textContent = city;
                        suggestion.classList.add("suggestion-item");

                        suggestion.addEventListener("click", function() {
                            searchInput.value = city;
                            suggestionsBox.style.display = "none";
                            document.getElementById("search-form").submit();
                        });

                        suggestionsBox.appendChild(suggestion);
                    });

                    let rect = searchInput.getBoundingClientRect();
                    suggestionsBox.style.left = `${rect.left}px`;
                    suggestionsBox.style.top = `${rect.bottom + window.scrollY}px`;
                    suggestionsBox.style.width = `${rect.width}px`;
                    suggestionsBox.style.display = "block";
                })
                .catch(error => {
                    console.error("Error fetching autocomplete suggestions:", error);
                });
        });

        document.addEventListener("click", function(e) {
            if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
                suggestionsBox.style.display = "none";
            }
        });
    }
});

// 修改后的热门航班加载函数
function loadPopularFlights() {
    fetch("/api/popular_flights")
        .then(response => response.json())
        .then(flights => {
            console.log("📌 热门航班数据:", flights);
            const container = document.getElementById("popular-flights");
            if (!container) return;
            
            // 清空容器并移除加载文本
            container.innerHTML = "";

            if (flights.length === 0) {
                container.innerHTML = "<p>No popular flights available at the moment.</p>";
                return;
            }

            // 为每个航班创建卡片，使用Bootstrap列布局
            flights.forEach(flight => {
                const flightCol = document.createElement("div");
                flightCol.className = "col-md-4 mb-4";
                
                // 提取机场代码
                const departureCode = flight.departure.split(" - ")[0]; // 只获取如"JFK"的代码
                
                // 提取目的地城市名（如果可能）
                const destinationCity = extractDestinationCity(flight.arrival);
                
                flightCol.innerHTML = `
                    <div class="flight-card">
                        <a href="/view/${flight.id}" class="flight-card-link">
                            <img src="${flight.image}" alt="${flight.title}" class="flight-card-image">
                            <div class="flight-info">
                                <h3>${flight.airline}</h3>
                                <p class="flight-route">${departureCode} → ${destinationCity}</p>
                                <p class="price-tag">$${flight.price}</p>
                            </div>
                        </a>
                    </div>
                `;
                
                container.appendChild(flightCol);
            });
        })
        .catch(error => {
            console.error("Error loading popular flights:", error);
            const container = document.getElementById("popular-flights");
            if (container) {
                container.innerHTML = "<p>Error loading flights. Please try again later.</p>";
            }
        });
}

// 辅助函数，从到达机场字符串中提取目的地城市名
function extractDestinationCity(arrivalString) {
    if (!arrivalString) return "Unknown";
    
    // 例如从 "HKG - Hong Kong International Airport" 提取 "Hong Kong"
    const parts = arrivalString.split(" - ");
    if (parts.length <= 1) return arrivalString;
    
    // 分离城市名（通常是目的地机场名称的前1-2个单词）
    const airportName = parts[1];
    const words = airportName.split(" ");
    
    // 处理特殊情况
    if (airportName.includes("Hong Kong")) return "Hong Kong";
    if (airportName.includes("Chongqing")) return "Chongqing";
    if (airportName.includes("Qingdao")) return "Qingdao";
    if (airportName.includes("Tianjin")) return "Tianjin";
    if (airportName.includes("Taiwan") || airportName.includes("Taipei")) return "Taipei";
    
    // 默认返回前两个单词作为城市名
    return words.slice(0, 2).join(" ");
}

// Helper function to extract city name from airport string
function extractCity(airportString) {
    if (!airportString) return "Unknown";
    
    const parts = airportString.split(" - ");
    return parts.length > 1 ? parts[1].split(" ")[0] : airportString;
}

// Setup the Add Flight form with validation and AJAX submission
function setupAddFlightForm(form) {
    form.addEventListener("submit", function(e) {
        e.preventDefault();
        
        // Reset previous error messages
        const errorElements = form.querySelectorAll(".error-message");
        errorElements.forEach(el => el.remove());
        
        const successMessage = form.querySelector(".success-message");
        if (successMessage) {
            successMessage.remove();
        }
        
        const inputs = form.querySelectorAll(".form-control");
        inputs.forEach(input => input.classList.remove("input-error"));
        
        // Gather form data
        const formData = {
            title: form.querySelector("#title").value,
            airline: form.querySelector("#airline").value,
            departure: form.querySelector("#departure").value,
            arrival: form.querySelector("#arrival").value,
            year: form.querySelector("#year").value,
            flight_time: form.querySelector("#flight_time").value,
            price: form.querySelector("#price").value,
            image: form.querySelector("#image").value,
            baggage_policy: form.querySelector("#baggage_policy").value,
            summary: form.querySelector("#summary").value,
            schedule: form.querySelector("#schedule").value,
            reviews: form.querySelector("#reviews").value
        };
        
        // Submit the data via fetch
        fetch("/api/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success message
                const successMsg = document.createElement("div");
                successMsg.className = "success-message";
                successMsg.setAttribute("role", "alert");
                successMsg.innerHTML = `
                    <div>New item successfully created.</div>
                    <a href="/view/${data.id}" class="view-link">See it here</a>
                `;
                
                form.prepend(successMsg);
                
                // Reset form fields
                form.reset();
                
                // Set focus to first field
                form.querySelector("#title").focus();
            } else {
                // Display validation errors
                for (const field in data.errors) {
                    const input = form.querySelector(`#${field}`);
                    if (input) {
                        input.classList.add("input-error");
                        
                        const errorMsg = document.createElement("div");
                        errorMsg.className = "error-message";
                        errorMsg.textContent = data.errors[field];
                        
                        input.parentNode.appendChild(errorMsg);
                    }
                }
            }
        })
        .catch(error => console.error("Error submitting form:", error));
    });
}

// Setup the Edit Flight form
function setupEditFlightForm(form) {
    const flightId = form.getAttribute("data-id");
    
    form.addEventListener("submit", function(e) {
        e.preventDefault();
        
        // Reset previous error messages
        const errorElements = form.querySelectorAll(".error-message");
        errorElements.forEach(el => el.remove());
        
        const inputs = form.querySelectorAll(".form-control");
        inputs.forEach(input => input.classList.remove("input-error"));
        
        // Gather form data
        const formData = {
            title: form.querySelector("#title").value,
            airline: form.querySelector("#airline").value,
            departure: form.querySelector("#departure").value,
            arrival: form.querySelector("#arrival").value,
            year: form.querySelector("#year").value,
            flight_time: form.querySelector("#flight_time").value,
            price: form.querySelector("#price").value,
            image: form.querySelector("#image").value,
            baggage_policy: form.querySelector("#baggage_policy").value,
            summary: form.querySelector("#summary").value,
            schedule: form.querySelector("#schedule").value,
            reviews: form.querySelector("#reviews").value
        };
        
        // Submit the data via fetch
        fetch(`/api/edit/${flightId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirect to view page
                window.location.href = `/view/${flightId}`;
            } else {
                // Display validation errors
                for (const field in data.errors) {
                    const input = form.querySelector(`#${field}`);
                    if (input) {
                        input.classList.add("input-error");
                        
                        const errorMsg = document.createElement("div");
                        errorMsg.className = "error-message";
                        errorMsg.textContent = data.errors[field];
                        
                        input.parentNode.appendChild(errorMsg);
                    }
                }
            }
        })
        .catch(error => console.error("Error updating flight:", error));
    });
}

// Setup confirmation dialog for discarding changes
function setupDiscardConfirmation(discardBtn) {
    const modal = document.getElementById("confirm-modal");
    if (!modal) return;
    
    const cancelBtn = modal.querySelector(".btn-cancel");
    const confirmBtn = modal.querySelector(".btn-confirm");
    
    discardBtn.addEventListener("click", function(e) {
        e.preventDefault();
        modal.classList.add("active");
    });
    
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function() {
            modal.classList.remove("active");
        });
    }
    
    if (confirmBtn) {
        confirmBtn.addEventListener("click", function() {
            window.location.href = discardBtn.getAttribute("data-return-url");
        });
    }
}

// Highlight search terms in search results
function highlightSearchResults() {
    const searchResults = document.querySelector(".search-results");
    if (!searchResults) return;
    
    const query = new URLSearchParams(window.location.search).get("q");
    if (!query) return;
    
    const searchTexts = document.querySelectorAll(".search-info h3, .search-info p");
    
    // Function to highlight matches with better visual prominence
    function highlightText(element, query) {
        const text = element.textContent;
        const lowerText = text.toLowerCase();
        const lowerQuery = query.toLowerCase();
        
        if (lowerText.includes(lowerQuery)) {
            const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
            element.innerHTML = text.replace(regex, '<span class="highlight">$1</span>');
        }
    }
    
    // Escape special regex characters
    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
    
    // Apply highlighting
    searchTexts.forEach(element => highlightText(element, query));
}

// Browse All Flights Component
function BrowseAllFlights() {
  // Create the container for all flights
  const container = document.createElement('div');
  container.className = 'flights-container';
  container.style.display = 'grid';
  container.style.gridTemplateColumns = 'repeat(auto-fill, minmax(300px, 1fr))';
  container.style.gap = '20px';
  container.style.padding = '20px';

  // Loop through all flights and create cards
  Object.values(flights).forEach(flight => {
    const card = document.createElement('div');
    card.className = 'flight-card';
    card.style.border = '1px solid #ddd';
    card.style.borderRadius = '8px';
    card.style.overflow = 'hidden';
    card.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
    
    // Add image
    const img = document.createElement('img');
    img.src = flight.image;
    img.alt = flight.title;
    img.style.width = '100%';
    img.style.height = '180px';
    img.style.objectFit = 'cover';
    
    // Add content container
    const content = document.createElement('div');
    content.style.padding = '15px';
    
    // Add title
    const title = document.createElement('h3');
    title.textContent = flight.title;
    title.style.margin = '0 0 10px 0';
    title.style.color = '#333';
    
    // Add route
    const route = document.createElement('p');
    route.innerHTML = `<strong>${flight.departure.split(' - ')[0]}</strong> → <strong>${flight.arrival.split(' - ')[0]}</strong>`;
    route.style.margin = '0 0 10px 0';
    
    // Add details
    const details = document.createElement('div');
    details.style.display = 'flex';
    details.style.justifyContent = 'space-between';
    details.style.marginBottom = '10px';
    
    const time = document.createElement('span');
    time.innerHTML = `<i class="fa fa-clock-o"></i> ${flight.flight_time}`;
    
    const price = document.createElement('span');
    price.innerHTML = `<strong>$${flight.price}</strong>`;
    price.style.color = '#e44d26';
    
    details.appendChild(time);
    details.appendChild(price);
    
    // Add airline
    const airline = document.createElement('p');
    airline.textContent = `Airline: ${flight.airline}`;
    airline.style.margin = '0 0 5px 0';
    airline.style.fontSize = '14px';
    
    // Add button
    const button = document.createElement('button');
    button.textContent = 'View Details';
    button.style.backgroundColor = '#0066cc';
    button.style.color = 'white';
    button.style.border = 'none';
    button.style.padding = '8px 15px';
    button.style.borderRadius = '4px';
    button.style.cursor = 'pointer';
    button.style.marginTop = '10px';
    button.style.width = '100%';
    
    // Assemble the card
    content.appendChild(title);
    content.appendChild(route);
    content.appendChild(details);
    content.appendChild(airline);
    content.appendChild(button);
    
    card.appendChild(img);
    card.appendChild(content);
    
    container.appendChild(card);
  });

  // Add the container to the document
  document.getElementById('browse-all-flights').appendChild(container);
}

// Initialize the component when the DOM is loaded
document.addEventListener('DOMContentLoaded', BrowseAllFlights);