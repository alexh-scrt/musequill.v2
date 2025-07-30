/**
 * Step 1: Book Concept Component
 * Handles initial book concept input and validation
 * Now with access to stored concept analysis
 */

function step1Concept() {
    return {
        // Data
        concept: '',
        additionalNotes: '',
        isSubmitting: false,
        validationErrors: [],
        showAnalysis: false, // Toggle to show/hide analysis results

        // Computed
        get isValid() {
            return this.concept.trim().length >= 10 && this.concept.trim().length <= 1000;
        },

        get characterCount() {
            return this.concept.length;
        },

        get remainingCharacters() {
            return 1000 - this.concept.length;
        },

        get conceptWordCount() {
            return this.concept.trim() ? this.concept.trim().split(/\s+/).length : 0;
        },

        // Access stored concept analysis
        get conceptAnalysis() {
            return this.$store.wizard.conceptAnalysis;
        },

        get hasAnalysis() {
            return this.conceptAnalysis && this.conceptAnalysis.analysis_successful;
        },

        get genreRecommendations() {
            return this.$store.wizard.getGenreRecommendations();
        },

        // Validation
        validateConcept() {
            this.validationErrors = [];

            if (!this.concept.trim()) {
                this.validationErrors.push('Please enter your book concept');
                return false;
            }

            if (this.concept.trim().length < 10) {
                this.validationErrors.push('Please provide at least 10 characters');
                return false;
            }

            if (this.concept.trim().length > 1000) {
                this.validationErrors.push('Please keep your concept under 1000 characters');
                return false;
            }

            if (this.additionalNotes.length > 500) {
                this.validationErrors.push('Additional notes must be under 500 characters');
                return false;
            }

            return true;
        },

        // Methods
        async submitConcept() {
            if (!this.validateConcept()) {
                return;
            }

            this.isSubmitting = true;

            try {
                // Start wizard session with concept
                const success = await this.$store.wizard.startWizard(
                    this.concept.trim(),
                    this.additionalNotes.trim()
                );

                if (success) {
                    // Show analysis results briefly before proceeding
                    this.showAnalysis = true;

                    // Log the analysis for debugging
                    console.log('Concept Analysis:', this.$store.wizard.conceptAnalysis);

                    // Optionally keep the form data visible for review
                    // or clear it as before
                    // this.concept = '';
                    // this.additionalNotes = '';
                    this.validationErrors = [];

                    // Wizard store handles navigation to step 2
                    console.log('Concept submitted successfully');

                    // Auto-hide analysis after 3 seconds and proceed
                    setTimeout(() => {
                        this.showAnalysis = false;
                    }, 3000);
                } else {
                    // Error is handled by the store
                    console.error('Failed to submit concept');
                }
            } catch (error) {
                console.error('Unexpected error:', error);
                this.validationErrors.push('An unexpected error occurred. Please try again.');
            } finally {
                this.isSubmitting = false;
            }
        },

        // Method to manually reanalyze without proceeding
        async reanalyzeConcept() {
            if (!this.validateConcept()) {
                return;
            }

            this.isSubmitting = true;

            try {
                // Just get analysis without proceeding
                const success = await this.$store.wizard.startWizard(
                    this.concept.trim(),
                    this.additionalNotes.trim()
                );

                if (success) {
                    this.showAnalysis = true;
                    // Don't proceed to next step, just show analysis
                    this.$store.wizard.setCurrentStep(1);
                }
            } catch (error) {
                console.error('Reanalysis error:', error);
                this.validationErrors.push('Failed to analyze concept. Please try again.');
            } finally {
                this.isSubmitting = false;
            }
        },

        // Input handlers
        onConceptInput() {
            // Real-time validation feedback
            if (this.validationErrors.length > 0) {
                this.validateConcept();
            }

            // Update store with current concept
            this.$store.wizard.updateFormData('concept', this.concept);

            // Hide analysis when editing
            this.showAnalysis = false;
        },

        onNotesInput() {
            this.$store.wizard.updateFormData('additionalNotes', this.additionalNotes);
        },

        // Analysis display helpers
        getAnalysisDisplay() {
            if (!this.hasAnalysis) return null;

            const analysis = this.conceptAnalysis;
            return {
                success: analysis.analysis_successful,
                totalRecommendations: analysis.total_recommendations || 0,
                recommendations: this.genreRecommendations,
                error: analysis.error || null
            };
        },

        // Lifecycle
        init() {
            // Load any existing data from store
            this.concept = this.$store.wizard.formData.concept || '';
            this.additionalNotes = this.$store.wizard.formData.additionalNotes || '';

            // Show analysis if we already have it
            this.showAnalysis = this.hasAnalysis;

            // Focus on concept input
            this.$nextTick(() => {
                const conceptInput = document.getElementById('concept');
                if (conceptInput) {
                    conceptInput.focus();
                }
            });
        },

        // Utility methods
        clearForm() {
            this.concept = '';
            this.additionalNotes = '';
            this.validationErrors = [];
            this.showAnalysis = false;
            this.$store.wizard.updateFormData('concept', '');
            this.$store.wizard.updateFormData('additionalNotes', '');
            this.$store.wizard.setConceptAnalysis(null);
        },

        // Sample concepts for inspiration
        sampleConcepts: [
            "A young detective in Victorian London discovers that supernatural forces are behind a series of mysterious murders plaguing the city.",
            "In a world where emotions manifest as visible colors, a color-blind girl must navigate a society that judges people by their emotional displays.",
            "A time-traveling historian gets stuck in ancient Rome and must use their knowledge of future events to survive while finding a way home.",
            "Two rival food truck owners are forced to work together when a corporate chain threatens to destroy their neighborhood's street food culture.",
            "A retired superhero working as a high school guidance counselor must come out of retirement when their former nemesis targets their students.",
            "A child story about a bunny adventure in Africa, learning about courage and friendship while helping other animals."
        ],

        useSampleConcept(conceptText) {
            this.concept = conceptText;
            this.onConceptInput();
        },

        // Helper text and tips
        get helpText() {
            if (this.hasAnalysis && this.showAnalysis) {
                return "Great! Your concept has been analyzed. You can edit it or proceed to genre selection.";
            } else if (this.concept.length === 0) {
                return "Start with a simple premise: Who is your main character and what challenge do they face?";
            } else if (this.concept.length < 50) {
                return "Good start! Add a bit more detail about the setting or conflict.";
            } else if (this.concept.length < 150) {
                return "Great! You're developing your concept well. Consider adding what's at stake.";
            } else {
                return "Excellent! Your concept is well-developed and ready for analysis.";
            }
        },

        // Debug helpers
        logAnalysis() {
            this.$store.wizard.logConceptAnalysis();
        },

        logStore() {
            this.$store.wizard.logState();
        }
    };
}