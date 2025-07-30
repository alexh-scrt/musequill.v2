/**
 * API Client - Handles all communication with the FastAPI backend
 * Provides a clean interface for wizard API calls
 */

class ApiClient {
    constructor(baseUrl = 'http://musequill.ink:8000') {
        this.baseUrl = baseUrl;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };
    }

    /**
     * Make HTTP request with error handling
     */
    async makeRequest(url, options = {}) {
        const config = {
            headers: this.defaultHeaders,
            ...options
        };

        try {
            const response = await fetch(`${this.baseUrl}${url}`, config);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error (${url}):`, error);
            throw error;
        }
    }

    /**
     * GET request helper
     */
    async get(url) {
        return this.makeRequest(url, {
            method: 'GET'
        });
    }

    /**
     * POST request helper
     */
    async post(url, data) {
        return this.makeRequest(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // =================================================================
    // Wizard API Methods
    // =================================================================

    /**
     * Start a new wizard session with book concept
     * @param {Object} conceptData - { concept, additional_notes? }
     */
    async startWizard(conceptData) {
        return this.post('/wizard/start', conceptData);
    }

    /**
     * Process a wizard step
     * @param {number} stepNumber - Step number (1-9)
     * @param {Object} stepData - { session_id, selection?, additional_input? }
     */
    async processStep(stepNumber, stepData) {
        return this.post(`/wizard/step/${stepNumber}`, stepData);
    }

    /**
     * Get current wizard session state
     * @param {string} sessionId - Session ID
     */
    async getSession(sessionId) {
        return this.get(`/wizard/session/${sessionId}`);
    }

    // =================================================================
    // Health and Info Methods
    // =================================================================

    /**
     * Check API health
     */
    async getHealth() {
        return this.get('/health');
    }

    /**
     * Get model information
     */
    async getModelsInfo() {
        return this.get('/models/info');
    }

    // =================================================================
    // Utility Methods
    // =================================================================

    /**
     * Get available genres
     */
    async getGenres() {
        return this.get('/genres');
    }

    /**
     * Get available writing styles
     */
    async getWritingStyles() {
        return this.get('/writing-styles');
    }

    /**
     * Get available story structures
     */
    async getStoryStructures() {
        return this.get('/story-structures');
    }

    // =================================================================
    // Connection Testing
    // =================================================================

    /**
     * Test API connection
     */
    async testConnection() {
        try {
            const health = await this.getHealth();
            return {
                connected: true,
                status: health.data?.status || 'unknown',
                message: health.message || 'Connected successfully'
            };
        } catch (error) {
            return {
                connected: false,
                error: error.message,
                message: 'Failed to connect to API'
            };
        }
    }

    /**
     * Get API status with detailed information
     */
    async getApiStatus() {
        try {
            const [health, modelsInfo] = await Promise.all([
                this.getHealth(),
                this.getModelsInfo()
            ]);

            return {
                healthy: true,
                health: health.data,
                models: modelsInfo.data,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                healthy: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }
}

// Create global API client instance
window.apiClient = new ApiClient();

// Alpine.js data helper for API status
function apiStatus() {
    return {
        status: null,
        isChecking: false,
        lastChecked: null,

        async checkStatus() {
            this.isChecking = true;
            try {
                this.status = await window.apiClient.getApiStatus();
                this.lastChecked = new Date();
            } catch (error) {
                this.status = {
                    healthy: false,
                    error: error.message,
                    timestamp: new Date().toISOString()
                };
            } finally {
                this.isChecking = false;
            }
        },

        async testConnection() {
            this.isChecking = true;
            try {
                const result = await window.apiClient.testConnection();
                this.status = result;
                this.lastChecked = new Date();
                return result.connected;
            } catch (error) {
                this.status = {
                    connected: false,
                    error: error.message,
                    message: 'Connection test failed'
                };
                return false;
            } finally {
                this.isChecking = false;
            }
        },

        get statusText() {
            if (!this.status) return 'Unknown';
            if (this.status.healthy === false || this.status.connected === false) {
                return 'Disconnected';
            }
            return 'Connected';
        },

        get statusColor() {
            if (!this.status) return 'gray';
            if (this.status.healthy === false || this.status.connected === false) {
                return 'red';
            }
            return 'green';
        }
    };
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ApiClient, apiStatus };
}