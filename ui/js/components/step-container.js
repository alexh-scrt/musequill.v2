/**
 * Step Container Component
 * Manages step content display and transitions
 */

function stepContainer() {
    return {
        // Data
        isTransitioning: false,
        transitionDirection: 'forward', // 'forward' or 'backward'

        // Computed
        get currentStepComponent() {
            const stepNumber = this.$store.wizard.currentStep;
            return `step${stepNumber}Data`;
        },

        get isLoading() {
            return this.$store.wizard.isLoading;
        },

        get hasError() {
            return this.$store.wizard.error !== null;
        },

        get shouldShowContent() {
            return !this.isLoading && !this.hasError;
        },

        // Step transition methods
        async transitionToStep(newStep, oldStep) {
            this.isTransitioning = true;
            this.transitionDirection = newStep > oldStep ? 'forward' : 'backward';

            // Add transition class
            const container = this.$refs.stepContent;
            if (container) {
                container.classList.add('step-transitioning');

                // Wait for transition to complete
                await new Promise(resolve => setTimeout(resolve, 200));

                container.classList.remove('step-transitioning');
            }

            this.isTransitioning = false;
        },

        // Content management
        getStepTitle(stepNumber) {
            const step = this.$store.wizard.getStepByNumber(stepNumber);
            return step?.name || `Step ${stepNumber}`;
        },

        getStepDescription(stepNumber) {
            const descriptions = {
                1: "Tell us about your book concept in 2-3 sentences. This will help us guide you through the creation process.",
                2: "Based on your concept, we'll recommend the best commercial genres for your book.",
                3: "Choose your target audience to optimize your book's market appeal and publishing strategy.",
                4: "Select a writing style that matches your genre and audience for maximum commercial success.",
                5: "Determine the optimal book length based on your genre and target market.",
                6: "Choose a proven story structure that works well for your selected genre.",
                7: "Define your book's world and setting to match your genre and style.",
                8: "Specify any content preferences, themes, or restrictions for your book.",
                9: "Review your complete book definition and make any final adjustments."
            };

            return descriptions[stepNumber] || "Complete this step to continue.";
        },

        // Error handling
        retryCurrentStep() {
            this.$store.wizard.clearError();
            // Optionally reload step data
            this.loadCurrentStepData();
        },

        async loadCurrentStepData() {
            const currentStep = this.$store.wizard.currentStep;

            // For steps beyond 1, we might need to reload data
            if (currentStep > 1 && this.$store.wizard.sessionId) {
                try {
                    // This would reload step-specific data if needed
                    console.log(`Loading data for step ${currentStep}`);
                } catch (error) {
                    console.error('Error loading step data:', error);
                }
            }
        },

        // Loading state management
        showLoadingSpinner() {
            return this.isLoading || this.isTransitioning;
        },

        getLoadingMessage() {
            if (this.isTransitioning) {
                return "Transitioning to next step...";
            } else if (this.isLoading) {
                return "Processing your request...";
            }
            return "";
        },

        // Content visibility
        shouldShowStep(stepNumber) {
            return this.$store.wizard.currentStep === stepNumber && this.shouldShowContent;
        },

        // Animation classes
        getStepContentClasses() {
            const baseClasses = "step-content";
            const transitionClasses = this.isTransitioning ? 'transitioning' : '';
            const directionClasses = this.transitionDirection === 'forward' ? 'forward' : 'backward';

            return `${baseClasses} ${transitionClasses} ${directionClasses}`.trim();
        },

        // Step validation
        validateStepContent(stepNumber) {
            // This could be expanded to validate each step's content
            switch (stepNumber) {
                case 1:
                    return this.$store.wizard.formData.concept?.length >= 10;
                case 2:
                    return this.$store.wizard.formData.genre !== '';
                case 3:
                    return this.$store.wizard.formData.audience !== '';
                case 4:
                    return this.$store.wizard.formData.style !== '';
                case 5:
                    return this.$store.wizard.formData.length !== '';
                case 6:
                    return this.$store.wizard.formData.structure !== '';
                case 7:
                    return this.$store.wizard.formData.world !== '';
                case 8:
                    return true; // Content preferences can be empty
                case 9:
                    return true; // Summary step
                default:
                    return false;
            }
        },

        // Help and guidance
        getStepHelpText(stepNumber) {
            const helpTexts = {
                1: "💡 Tip: Focus on the main character and their central conflict. What challenge will they face?",
                2: "💡 Tip: Consider your book's commercial appeal. Some genres have larger markets than others.",
                3: "💡 Tip: Your target audience affects everything from vocabulary to themes to book length.",
                4: "💡 Tip: Writing style should match both your genre and your target audience's expectations.",
                5: "💡 Tip: Book length varies by genre. Romance novels are typically shorter than epic fantasy.",
                6: "💡 Tip: Proven story structures help readers connect with your narrative.",
                7: "💡 Tip: Your world should serve the story. Complex world-building works better in longer books.",
                8: "💡 Tip: Be specific about content you want to include or avoid. This helps shape the final book.",
                9: "💡 Tip: Review everything carefully. You can always make changes later in the writing process."
            };

            return helpTexts[stepNumber] || "";
        },

        showStepHelp(stepNumber) {
            const helpText = this.getStepHelpText(stepNumber);
            if (helpText) {
                // You could implement a tooltip or modal here
                console.log(helpText);
            }
        },

        // Keyboard shortcuts
        handleKeyPress(event) {
            if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
                return; // Don't interfere with form inputs
            }

            switch (event.key) {
                case 'ArrowRight':
                case 'ArrowDown':
                    event.preventDefault();
                    if (this.$store.wizard.canProceed()) {
                        // Trigger next step via navigation component
                        this.$refs.navigation?.goToNextStep();
                    }
                    break;
                case 'ArrowLeft':
                case 'ArrowUp':
                    event.preventDefault();
                    if (this.$store.wizard.currentStep > 1) {
                        // Trigger previous step via navigation component
                        this.$refs.navigation?.goToPreviousStep();
                    }
                    break;
                case '?':
                    event.preventDefault();
                    this.showStepHelp(this.$store.wizard.currentStep);
                    break;
            }
        },

        // Accessibility
        getStepAriaLabel() {
            const currentStep = this.$store.wizard.currentStep;
            const totalSteps = this.$store.wizard.totalSteps;
            const stepTitle = this.getStepTitle(currentStep);

            return `${stepTitle}, step ${currentStep} of ${totalSteps}`;
        },

        // Lifecycle
        init() {
            // Watch for step changes to handle transitions
            this.$watch('$store.wizard.currentStep', (newStep, oldStep) => {
                if (oldStep !== undefined) {
                    this.transitionToStep(newStep, oldStep);
                }
            });

            // Add keyboard event listeners
            document.addEventListener('keydown', this.handleKeyPress.bind(this));

            // Load initial step data if needed
            this.loadCurrentStepData();
        },

        destroy() {
            // Clean up event listeners
            document.removeEventListener('keydown', this.handleKeyPress.bind(this));
        },

        // Dynamic component data for each step
        getStepData(stepNumber) {
            const baseData = {
                stepTitle: this.getStepTitle(stepNumber),
                stepDescription: this.getStepDescription(stepNumber),
                stepNumber: stepNumber,
                isValid: this.validateStepContent(stepNumber),
                helpText: this.getStepHelpText(stepNumber)
            };

            // Add step-specific data
            switch (stepNumber) {
                case 1:
                    return { ...baseData, ...this.getStep1Data() };
                case 2:
                    return { ...baseData, ...this.getStep2Data() };
                case 3:
                    return { ...baseData, ...this.getStep3Data() };
                default:
                    return baseData;
            }
        },

        getStep1Data() {
            return {
                concept: this.$store.wizard.formData.concept || '',
                additionalNotes: this.$store.wizard.formData.additionalNotes || ''
            };
        },

        getStep2Data() {
            return {
                selectedGenre: this.$store.wizard.formData.genre || '',
                options: this.$store.wizard.currentStepData.options || []
            };
        },

        getStep3Data() {
            return {
                selectedAudience: this.$store.wizard.formData.audience || '',
                options: this.$store.wizard.currentStepData.options || []
            };
        }
    };
}

// Individual step data functions for Alpine.js x-data
function step1Data() {
    return {
        stepTitle: "Tell us about your book idea",
        stepDescription: "Describe your book concept in 2-3 sentences. This will help us guide you through the creation process.",
        stepNumber: 1
    };
}

function step2Data() {
    return {
        stepTitle: "Choose Your Genre",
        stepDescription: "Based on your concept, we'll recommend the best commercial genres for your book.",
        stepNumber: 2
    };
}

function step3Data() {
    return {
        stepTitle: "Select Your Target Audience",
        stepDescription: "Choose your target audience to optimize your book's market appeal and publishing strategy.",
        stepNumber: 3
    };
}

function step4Data() {
    return {
        stepTitle: "Select Your Writing Style",
        stepDescription: "Choose a writing style that matches your genre and audience for maximum commercial success.",
        stepNumber: 4
    };
}

function step5Data() {
    return {
        stepTitle: "Determine Book Length",
        stepDescription: "Select the optimal book length based on your genre and target market.",
        stepNumber: 5
    };
}

function step6Data() {
    return {
        stepTitle: "Choose Story Structure",
        stepDescription: "Pick a proven story structure that works well for your selected genre.",
        stepNumber: 6
    };
}

function step7Data() {
    return {
        stepTitle: "Design Your World",
        stepDescription: "Define your book's world and setting to match your genre and style.",
        stepNumber: 7
    };
}

function step8Data() {
    return {
        stepTitle: "Content Preferences",
        stepDescription: "Specify any content preferences, themes, or restrictions for your book.",
        stepNumber: 8
    };
}

function step9Data() {
    return {
        stepTitle: "Review & Finalize",
        stepDescription: "Review your complete book definition and make any final adjustments.",
        stepNumber: 9
    };
}