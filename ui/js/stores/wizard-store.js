// Enhanced wizard store that stores LLM analysis response
document.addEventListener('alpine:init', () => {
    Alpine.store('wizard', {
        // State
        currentStep: 1,
        totalSteps: 9,
        sessionId: null,
        isLoading: false,
        error: null,

        // Form data
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

        // Current step information
        currentStepData: {
            question: '',
            options: [],
            llmReasoning: '',
            canGoBack: false,
            isFinalStep: false
        },

        // Store the LLM concept analysis for later use
        conceptAnalysis: null,

        // Final book summary
        bookSummary: null,

        // Getters/Computed
        get stepKeys() {
            return ['concept', 'genre', 'audience', 'style', 'length', 'structure', 'world', 'content'];
        },

        get isComplete() {
            return this.currentStep > this.totalSteps;
        },

        // State management methods
        setCurrentStep(step) {
            this.currentStep = step;
        },

        setSessionId(sessionId) {
            this.sessionId = sessionId;
        },

        setLoading(loading) {
            this.isLoading = loading;
        },

        setError(error) {
            this.error = error;
        },

        clearError() {
            this.error = null;
        },

        setStepData(stepData) {
            this.currentStepData = {
                question: stepData.question || '',
                options: stepData.options || [],
                llmReasoning: stepData.llm_reasoning || stepData.llmReasoning || '',
                canGoBack: stepData.can_go_back || stepData.canGoBack || false,
                isFinalStep: stepData.is_final_step || stepData.isFinalStep || false
            };
        },

        setConceptAnalysis(analysis) {
            this.conceptAnalysis = analysis;
            console.log('Stored concept analysis:', analysis);
        },

        setBookSummary(summary) {
            this.bookSummary = summary;
        },

        updateFormData(key, value) {
            this.formData[key] = value;
        },

        // Helper methods
        getCurrentStepKey() {
            const stepMap = {
                1: 'concept',
                2: 'genre',
                3: 'audience',
                4: 'style',
                5: 'length',
                6: 'structure',
                7: 'world',
                8: 'content',
                9: 'summary'
            };
            return stepMap[this.currentStep] || null;
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

        // Get genre recommendations from stored concept analysis
        getGenreRecommendations() {
            if (!this.conceptAnalysis || !this.conceptAnalysis.genre_recommendations) {
                return [];
            }
            return this.conceptAnalysis.genre_recommendations;
        },

        // Get specific analysis results
        getAnalysisField(field) {
            return this.conceptAnalysis?.[field] || null;
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
            this.conceptAnalysis = null;
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

                    // Store the concept analysis for later use
                    if (response.data.concept_analysis) {
                        this.setConceptAnalysis(response.data.concept_analysis);
                    }

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
            this.setLoading(true);
            this.clearError();

            try {
                const response = await window.apiClient.processStep(stepNumber, {
                    session_id: this.sessionId,
                    selection: selection,
                    additional_input: additionalInput
                });

                if (response.success) {
                    // Update form data with selection
                    const stepKey = this.getCurrentStepKey();
                    if (stepKey && stepKey !== 'concept') {
                        this.updateFormData(stepKey, selection);
                    }

                    // Set step data from response
                    this.setStepData(response.data);

                    // If it's the final step, store book summary
                    if (response.data.is_final_step && response.data.book_summary) {
                        this.setBookSummary(response.data.book_summary);
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
        },

        // Debug helper methods
        logState() {
            console.log('Wizard State:', {
                currentStep: this.currentStep,
                sessionId: this.sessionId,
                formData: this.formData,
                conceptAnalysis: this.conceptAnalysis,
                currentStepData: this.currentStepData
            });
        },

        logConceptAnalysis() {
            if (this.conceptAnalysis) {
                console.log('Concept Analysis:', this.conceptAnalysis);
            } else {
                console.log('No concept analysis stored');
            }
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