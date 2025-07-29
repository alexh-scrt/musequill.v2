/**
 * Wizard Store - Alpine.js Global State Management
 * Manages the wizard's state, session, and data flow
 */

document.addEventListener('alpine:init', () => {
    Alpine.store('wizard', {
        // Core State
        currentStep: 1,
        totalSteps: 9,
        sessionId: null,
        isLoading: false,
        error: null,

        // Step Configuration
        steps: [
            { number: 1, name: 'Book Concept', shortName: 'Concept', key: 'concept' },
            { number: 2, name: 'Genre Selection', shortName: 'Genre', key: 'genre' },
            { number: 3, name: 'Target Audience', shortName: 'Audience', key: 'audience' },
            { number: 4, name: 'Writing Style', shortName: 'Style', key: 'style' },
            { number: 5, name: 'Book Length', shortName: 'Length', key: 'length' },
            { number: 6, name: 'Story Structure', shortName: 'Structure', key: 'structure' },
            { number: 7, name: 'World Building', shortName: 'World', key: 'world' },
            { number: 8, name: 'Content Preferences', shortName: 'Content', key: 'content' },
            { number: 9, name: 'Final Summary', shortName: 'Summary', key: 'summary' }
        ],

        // Form Data
        formData: {
            concept: '',
            additionalNotes: '',
            genre: '',
            subgenre: '',
            audience: '',
            style: '',
            length: '',
            structure: '',
            world: '',
            contentPreferences: ''
        },

        // Current Step Data
        currentStepData: {
            question: '',
            options: [],
            llmReasoning: '',
            canGoBack: false,
            isFinalStep: false
        },

        // Book Summary
        bookSummary: null,

        // Methods
        setLoading(loading) {
            this.isLoading = loading;
        },

        setError(error) {
            this.error = error;
            this.isLoading = false;
        },

        clearError() {
            this.error = null;
        },

        setCurrentStep(step) {
            if (step >= 1 && step <= this.totalSteps) {
                this.currentStep = step;
            }
        },

        setSessionId(sessionId) {
            this.sessionId = sessionId;
        },

        updateFormData(key, value) {
            this.formData[key] = value;
        },

        setStepData(stepData) {
            this.currentStepData = {
                question: stepData.question || '',
                options: stepData.options || [],
                llmReasoning: stepData.llm_reasoning || '',
                canGoBack: stepData.can_go_back || false,
                isFinalStep: stepData.is_final_step || false
            };
        },

        getStepByNumber(number) {
            return this.steps.find(step => step.number === number);
        },

        getCurrentStepKey() {
            const step = this.getStepByNumber(this.currentStep);
            return step ? step.key : null;
        },

        hasSelection(stepKey) {
            return this.formData[stepKey] && this.formData[stepKey].trim() !== '';
        },

        canProceed() {
            if (this.currentStep === 1) {
                return this.formData.concept && this.formData.concept.trim().length >= 10;
            }

            const currentStepKey = this.getCurrentStepKey();
            if (!currentStepKey) return false;

            // For content preferences step, allow empty input
            if (currentStepKey === 'content') {
                return true;
            }

            return this.hasSelection(currentStepKey);
        },

        getProgress() {
            return Math.round((this.currentStep / this.totalSteps) * 100);
        },

        reset() {
            this.currentStep = 1;
            this.sessionId = null;
            this.isLoading = false;
            this.error = null;
            this.formData = {
                concept: '',
                additionalNotes: '',
                genre: '',
                subgenre: '',
                audience: '',
                style: '',
                length: '',
                structure: '',
                world: '',
                contentPreferences: ''
            };
            this.currentStepData = {
                question: '',
                options: [],
                llmReasoning: '',
                canGoBack: false,
                isFinalStep: false
            };
            this.bookSummary = null;
        },

        // API Integration Methods
        async startWizard(concept, additionalNotes = '') {
            this.setLoading(true);
            this.clearError();

            try {
                const response = await window.apiClient.startWizard({
                    concept: concept,
                    additional_notes: additionalNotes
                });

                if (response.success) {
                    this.setSessionId(response.data.session_id);
                    this.updateFormData('concept', concept);
                    this.updateFormData('additionalNotes', additionalNotes);

                    // Set step data from response
                    if (response.data.first_step) {
                        this.setStepData(response.data.first_step);
                    }

                    this.setCurrentStep(2); // Move to genre selection
                    return true;
                } else {
                    throw new Error(response.message || 'Failed to start wizard');
                }
            } catch (error) {
                console.error('Error starting wizard:', error);
                this.setError(error.message || 'Failed to start wizard. Please try again.');
                return false;
            } finally {
                this.setLoading(false);
            }
        },

        async processStep(stepNumber, selection, additionalInput = '') {
            if (!this.sessionId) {
                this.setError('No active session. Please restart the wizard.');
                return false;
            }

            this.setLoading(true);
            this.clearError();

            try {
                const response = await window.apiClient.processStep(stepNumber, {
                    session_id: this.sessionId,
                    selection: selection,
                    additional_input: additionalInput
                });

                if (response.success) {
                    this.setStepData(response.data);

                    // Update form data
                    const stepKey = this.getCurrentStepKey();
                    if (stepKey) {
                        if (stepKey === 'content') {
                            this.updateFormData('contentPreferences', additionalInput);
                        } else {
                            this.updateFormData(stepKey, selection);
                        }
                    }

                    return true;
                } else {
                    throw new Error(response.message || 'Failed to process step');
                }
            } catch (error) {
                console.error('Error processing step:', error);
                this.setError(error.message || 'Failed to process step. Please try again.');
                return false;
            } finally {
                this.setLoading(false);
            }
        },

        async getSession() {
            if (!this.sessionId) {
                return null;
            }

            try {
                const response = await window.apiClient.getSession(this.sessionId);
                if (response.success) {
                    return response.data;
                }
            } catch (error) {
                console.error('Error getting session:', error);
            }

            return null;
        },

        // Navigation Methods
        async goToNext() {
            if (!this.canProceed()) {
                return false;
            }

            if (this.currentStep < this.totalSteps) {
                this.setCurrentStep(this.currentStep + 1);

                // If we're past step 1, we need to load step data
                if (this.currentStep > 1) {
                    await this.loadStepData();
                }

                return true;
            }

            return false;
        },

        goToPrevious() {
            if (this.currentStep > 1) {
                this.setCurrentStep(this.currentStep - 1);
                return true;
            }
            return false;
        },

        async loadStepData() {
            // For now, just return true - step data will be loaded when processing
            return true;
        }
    });
});

// Initialize wizard store helper
function wizardStore() {
    return {
        initWizard() {
            // Any initialization logic
            console.log('Wizard initialized');
        }
    };
}