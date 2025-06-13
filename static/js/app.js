/**
 * Smart Study Buddy - Frontend JavaScript
 * Handles user interactions and API communication
 */

class StudyBuddyApp {
    constructor() {
        this.isLoading = false;
        this.statsUpdateInterval = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateStats();
        this.startStatsUpdater();
        console.log('🎓 Smart Study Buddy initialized');
    }

    bindEvents() {
        // Form submission
        const queryForm = document.getElementById('query-form');
        if (queryForm) {
            queryForm.addEventListener('submit', (e) => this.handleQuerySubmit(e));
        }

        // Example cards
        const exampleCards = document.querySelectorAll('.example-card');
        exampleCards.forEach(card => {
            card.addEventListener('click', () => this.handleExampleClick(card));
        });

        // Modal events
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal(e.target.id);
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllModals();
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                const queryForm = document.getElementById('query-form');
                if (queryForm && !this.isLoading) {
                    queryForm.dispatchEvent(new Event('submit'));
                }
            }
        });

        // Auto-resize textarea
        const queryTextarea = document.getElementById('query');
        if (queryTextarea) {
            queryTextarea.addEventListener('input', () => {
                this.autoResizeTextarea(queryTextarea);
            });
        }
    }

    async handleQuerySubmit(e) {
        e.preventDefault();
        
        if (this.isLoading) return;

        const formData = new FormData(e.target);
        const query = formData.get('query').trim();

        if (!query) {
            this.showError('Please enter a question');
            return;
        }

        this.setLoading(true);
        this.hideResponse();

        try {
            const response = await this.makeAPICall('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    routing_strategy: 'triton'
                })
            });

            // Check if response has an error field
            if (response.error) {
                this.showError(response.error);
            } else {
                // Response is successful, display it directly
                this.displayResponse(response);
                this.updateStats();
            }
        } catch (error) {
            console.error('Query error:', error);
            this.showError('Failed to process your query. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }

    handleExampleClick(card) {
        const query = card.dataset.query;

        // Fill form with example data
        document.getElementById('query').value = query;

        // Auto-resize textarea
        this.autoResizeTextarea(document.getElementById('query'));

        // Scroll to form
        document.getElementById('query-form').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });

        // Focus on query textarea
        setTimeout(() => {
            document.getElementById('query').focus();
        }, 500);

        // Add visual feedback
        card.style.transform = 'scale(0.98)';
        setTimeout(() => {
            card.style.transform = '';
        }, 150);
    }

    displayResponse(data) {
        const responseSection = document.getElementById('response-section');
        const responseContent = document.getElementById('response-content');
        const responseMeta = document.getElementById('response-meta');
        const responseDetection = document.getElementById('response-detection');

        // Update response content
        responseContent.textContent = data.response;

        // Calculate cost from usage if available
        const cost = data.usage && data.usage.total_tokens ? 
            (data.usage.total_tokens * 0.0001) : 0; // Rough estimate

        // Update metadata with available fields
        responseMeta.innerHTML = `
            <span><i class="fas fa-robot"></i> ${this.formatModelName(data.model_used || 'Unknown')}</span>
            <span><i class="fas fa-dollar-sign"></i> $${cost.toFixed(4)}</span>
            <span><i class="fas fa-clock"></i> ${((data.response_time || 0) * 1000).toFixed(0)}ms</span>
            <span><i class="fas fa-route"></i> ${data.classifier_used || 'Unknown'}</span>
        `;

        // Update detection information
        responseDetection.innerHTML = `
            <div class="detection-item">
                <i class="fas fa-book"></i>
                <span>Subject:</span>
                <span class="detection-value">${data.detected_subject || 'General'}</span>
            </div>
            <div class="detection-item">
                <i class="fas fa-layer-group"></i>
                <span>Level:</span>
                <span class="detection-value">${data.detected_difficulty || 'Unknown'}</span>
            </div>
        `;

        // Show response section with animation
        responseSection.style.display = 'block';
        responseSection.classList.add('fade-in');

        // Scroll to response
        setTimeout(() => {
            responseSection.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }, 100);
    }

    formatModelName(modelName) {
        const modelMap = {
            'meta/llama-3.1-8b-instruct': 'Llama 3.1 8B',
            'nvidia/llama-3.3-nemotron-super-49b-v1': 'Nemotron 70B',
            'deepseek-ai/deepseek-coder-33b-instruct': 'DeepSeek Coder',
            'mistralai/mixtral-8x22b-instruct-v0.1': 'Mixtral 8x22B',
            'meta/llama-3.1-70b-instruct': 'Llama 3.1 70B'
        };
        return modelMap[modelName] || modelName.split('/').pop();
    }

    hideResponse() {
        const responseSection = document.getElementById('response-section');
        responseSection.style.display = 'none';
        responseSection.classList.remove('fade-in');
    }

    setLoading(loading) {
        this.isLoading = loading;
        const loadingElement = document.getElementById('loading');
        const submitBtn = document.getElementById('submit-btn');

        if (loading) {
            loadingElement.style.display = 'block';
            loadingElement.classList.add('fade-in');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        } else {
            loadingElement.style.display = 'none';
            loadingElement.classList.remove('fade-in');
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Ask Study Buddy';
        }
    }

    async updateStats() {
        try {
            const stats = await this.makeAPICall('/api/stats');
            
            document.getElementById('query-count').textContent = stats.total_queries || 0;
            
            // Use actual cost from backend instead of rough estimate
            const actualCost = stats.total_cost || 0;
            document.getElementById('session-cost').textContent = `$${actualCost.toFixed(4)}`;
            
            // Better time formatting - show seconds for short sessions, minutes for longer ones
            const totalSeconds = stats.total_response_time || 0;
            let timeDisplay;
            if (totalSeconds < 60) {
                timeDisplay = `${Math.round(totalSeconds)}s`;
            } else if (totalSeconds < 3600) {
                const minutes = Math.floor(totalSeconds / 60);
                const seconds = Math.round(totalSeconds % 60);
                timeDisplay = seconds > 0 ? `${minutes}m ${seconds}s` : `${minutes}m`;
            } else {
                const hours = Math.floor(totalSeconds / 3600);
                const minutes = Math.floor((totalSeconds % 3600) / 60);
                timeDisplay = minutes > 0 ? `${hours}h ${minutes}m` : `${hours}h`;
            }
            document.getElementById('session-time').textContent = timeDisplay;
        } catch (error) {
            console.error('Failed to update stats:', error);
        }
    }

    startStatsUpdater() {
        // Update stats every 30 seconds
        this.statsUpdateInterval = setInterval(() => {
            this.updateStats();
        }, 30000);
    }

    async makeAPICall(url, options = {}) {
        const response = await fetch(url, {
            ...options,
            credentials: 'same-origin'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    showError(message) {
        // Create or update error notification
        let errorDiv = document.getElementById('error-notification');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'error-notification';
            errorDiv.className = 'error-notification';
            document.body.appendChild(errorDiv);
        }

        errorDiv.innerHTML = `
            <div class="error-content">
                <i class="fas fa-exclamation-triangle"></i>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="error-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        errorDiv.classList.add('show');

        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (errorDiv) {
                errorDiv.classList.remove('show');
                setTimeout(() => {
                    if (errorDiv && errorDiv.parentNode) {
                        errorDiv.parentNode.removeChild(errorDiv);
                    }
                }, 300);
            }
        }, 5000);
    }

    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
    }

    showAbout() {
        this.showModal('about-modal');
    }

    showHelp() {
        // Create help modal content dynamically
        const helpContent = `
            <div class="modal-header">
                <h3>How to Use Smart Study Buddy</h3>
                <button class="modal-close" onclick="studyBuddy.closeModal('help-modal')">&times;</button>
            </div>
            <div class="modal-body">
                <h4>Getting Started</h4>
                <ol>
                    <li>Select your subject and difficulty level</li>
                    <li>Type your question in the text area</li>
                    <li>Click "Ask Study Buddy" or press Ctrl+Enter</li>
                    <li>Get an intelligent response routed to the best AI model</li>
                </ol>
                
                <h4>Tips for Better Results</h4>
                <ul>
                    <li>Be specific in your questions</li>
                    <li>Include context when needed</li>
                    <li>Use the example cards for inspiration</li>
                    <li>Try different difficulty levels for varied explanations</li>
                </ul>
                
                <h4>Keyboard Shortcuts</h4>
                <ul>
                    <li><kbd>Ctrl+Enter</kbd> - Submit query</li>
                    <li><kbd>Esc</kbd> - Close modals</li>
                </ul>
            </div>
        `;

        this.createModal('help-modal', helpContent);
        this.showModal('help-modal');
    }

    createModal(id, content) {
        // Remove existing modal if it exists
        const existingModal = document.getElementById(id);
        if (existingModal) {
            existingModal.remove();
        }

        // Create new modal
        const modal = document.createElement('div');
        modal.id = id;
        modal.className = 'modal';
        modal.innerHTML = `<div class="modal-content">${content}</div>`;
        
        document.body.appendChild(modal);
    }

    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('show');
            document.body.style.overflow = '';
        }
    }

    closeAllModals() {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            modal.classList.remove('show');
        });
        document.body.style.overflow = '';
    }

    // Cleanup method
    destroy() {
        if (this.statsUpdateInterval) {
            clearInterval(this.statsUpdateInterval);
        }
    }
}

// Global functions for HTML onclick handlers
function showAbout() {
    studyBuddy.showAbout();
}

function showHelp() {
    studyBuddy.showHelp();
}

function closeModal(modalId) {
    studyBuddy.closeModal(modalId);
}

// Initialize app when DOM is loaded
let studyBuddy;

document.addEventListener('DOMContentLoaded', () => {
    studyBuddy = new StudyBuddyApp();
});

// Add error notification styles dynamically
const errorStyles = `
    .error-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1001;
        max-width: 400px;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    }
    
    .error-notification.show {
        opacity: 1;
        transform: translateX(0);
    }
    
    .error-content {
        background: #fee2e2;
        border: 1px solid #fecaca;
        border-left: 4px solid #ef4444;
        border-radius: 0.5rem;
        padding: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    }
    
    .error-content i:first-child {
        color: #ef4444;
        font-size: 1.25rem;
    }
    
    .error-content span {
        flex: 1;
        color: #991b1b;
        font-weight: 500;
    }
    
    .error-close {
        background: none;
        border: none;
        color: #991b1b;
        cursor: pointer;
        padding: 0.25rem;
        border-radius: 0.25rem;
        transition: background-color 0.2s ease;
    }
    
    .error-close:hover {
        background: #fecaca;
    }
    
    kbd {
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 0.25rem;
        padding: 0.125rem 0.375rem;
        font-size: 0.75rem;
        font-family: monospace;
    }
`;

// Inject error styles
const styleSheet = document.createElement('style');
styleSheet.textContent = errorStyles;
document.head.appendChild(styleSheet); 