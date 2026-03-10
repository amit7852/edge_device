// API Base URL - configurable
let API_BASE = "http://localhost:8000";

// Function to set API base URL from frontend
function setApiBaseUrl(url) {
    API_BASE = url;
    console.log("API Base URL set to:", API_BASE);
}

// Function to get current API base URL
function getApiBaseUrl() {
    return API_BASE;
}

// Create bubble effect on click
function createBubble(e) {
    const button = e.currentTarget;
    const bubble = document.createElement('span');
    bubble.classList.add('bubble');
    
    // Get button position and size
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    
    // Calculate click position relative to button
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;
    
    bubble.style.width = bubble.style.height = size + 'px';
    bubble.style.left = x + 'px';
    bubble.style.top = y + 'px';
    
    button.appendChild(bubble);
    
    // Remove bubble after animation
    setTimeout(() => {
        bubble.remove();
    }, 600);
}

// Add bubble effect to all buttons
document.addEventListener('DOMContentLoaded', () => {
    // Add click event to all buttons after page loads
    setTimeout(() => {
        document.querySelectorAll('button, .btn').forEach(btn => {
            btn.addEventListener('click', createBubble);
        });
    }, 100);
});

// Theme toggle function
function toggleTheme() {
    const body = document.body;
    const button = document.querySelector('.theme-toggle');
    
    body.classList.toggle('light-theme');
    
    if (body.classList.contains('light-theme')) {
        button.textContent = '☀️ Light';
        localStorage.setItem('theme', 'light');
    } else {
        button.textContent = '🌙 Dark';
        localStorage.setItem('theme', 'dark');
    }
}

// Load saved theme on page load
function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    const button = document.querySelector('.theme-toggle');
    
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        if (button) button.textContent = '☀️ Light';
    }
}

// Format timestamp to readable date/time
function formatTimestamp(timestamp) {
    const date = new Date(timestamp * 1000); // Convert Unix timestamp to milliseconds
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// Show main app
function showApp() {
    fetchEvents();
}

// Show loading state
function showLoading() {
    const table = document.getElementById('events');
    if (table) {
        table.innerHTML = '<tr><th>Camera</th><th>Type</th><th>Count</th><th>Time</th></tr>';
        const loadingRow = table.insertRow();
        loadingRow.innerHTML = '<td colspan="4" style="text-align:center;">Loading events...</td>';
    }
}

// Show error message with instructions
function showError(message) {
    const table = document.getElementById('events');
    if (table) {
        table.innerHTML = '<tr><th>Camera</th><th>Type</th><th>Count</th><th>Time</th></tr>';
        const errorRow = table.insertRow();
        errorRow.innerHTML = `
            <td colspan="4" style="text-align:center;">
                <p style="color:#ff4444;margin-bottom:15px;">Error: ${message}</p>
                <div style="text-align:left;max-width:400px;margin:0 auto;padding:15px;background:rgba(0,0,0,0.3);border-radius:5px;">
                    <p style="color:#00d4ff;margin:0 0 10px 0;font-size:13px;">To fix this, start the backend server:</p>
                    <code style="color:#fff;display:block;background:#1a1a2e;padding:8px;border-radius:3px;font-size:12px;margin-bottom:10px;">cd backend && uvicorn main:app --reload</code>
                    <button onclick="fetchEvents()" style="background:#00d4ff;color:#1a1a2e;border:none;padding:8px 16px;border-radius:4px;cursor:pointer;">Retry</button>
                </div>
            </td>
        `;
    }
}

// Fetch and display events
async function fetchEvents() {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/api/events`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const table = document.getElementById('events');
        
        if (!table) return;
        
        // Clear loading message
        table.innerHTML = '<tr><th>Camera</th><th>Type</th><th>Count</th><th>Time</th></tr>';
        
        if (data.length === 0) {
            const row = table.insertRow();
            row.innerHTML = '<td colspan="4" style="text-align:center;">No events found. Start the edge device to generate events.</td>';
            return;
        }
        
        data.forEach(e => {
            let row = table.insertRow();
            row.insertCell(0).innerText = e.camera_id;
            row.insertCell(1).innerText = e.type;
            row.insertCell(2).innerText = e.count;
            row.insertCell(3).innerText = formatTimestamp(e.timestamp);
        });
        
        // Update last updated time
        const lastUpdated = document.getElementById('last-updated');
        if (lastUpdated) {
            lastUpdated.textContent = 'Last updated: ' + new Date().toLocaleTimeString();
        }
        
    } catch (error) {
        console.error('Error fetching events:', error);
        showError(error.message);
    }
}

// Make fetchEvents globally available
window.fetchEvents = fetchEvents;

// ==================== ANALYTICS FUNCTIONS ====================

// Fetch event statistics from the API
async function fetchEventStats() {
    try {
        const response = await fetch(`${API_BASE}/api/events/stats/summary`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const stats = await response.json();
        return stats;
    } catch (error) {
        console.error('Error fetching event stats:', error);
        return null;
    }
}

// Load analytics data and display in the UI
async function loadAnalytics() {
    const totalEl = document.getElementById('total-events');
    const camerasEl = document.getElementById('cameras-active');
    const typesEl = document.getElementById('detection-types');
    
    if (!totalEl || !camerasEl || !typesEl) return;
    
    try {
        const stats = await fetchEventStats();
        
        if (stats) {
            totalEl.textContent = stats.total_events || 0;
            camerasEl.textContent = stats.unique_cameras || 0;
            typesEl.textContent = stats.unique_types || 0;
        } else {
            // Fallback to fetching all events
            const response = await fetch(`${API_BASE}/api/events`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            const totalEvents = data.length;
            const cameras = [...new Set(data.map(e => e.camera_id))];
            const types = [...new Set(data.map(e => e.type))];
            
            totalEl.textContent = totalEvents;
            camerasEl.textContent = cameras.length;
            typesEl.textContent = types.length;
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
        totalEl.textContent = '-';
        camerasEl.textContent = '-';
        typesEl.textContent = '-';
    }
}

// Make analytics functions globally available
window.loadAnalytics = loadAnalytics;
window.fetchEventStats = fetchEventStats;

// Auto-refresh events every 30 seconds
document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    showApp();
    setInterval(fetchEvents, 30000);
});

