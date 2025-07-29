/**
 * Navigation Component
 * Handles wizard navigation between steps
 */

function navigation() {
    return {
        // Data
        isNavigating: false,

        // Computed
        get canGoBack() {
            return this.$store.wizard.currentStep > 1 && !this.isNavigating;
        },

        get canGoForward() {
            return this.$store.wizard.currentStep < this.$store.wizard.totalSteps &&
                this.$store.wizard.canProceed() &&
                !this.isNavigating;
        },

        get isLastStep() {
            return this.$store.wizard.currentStep === this.$store.wizard.totalSteps;
        },

        get nextButtonText() {
            if (this.isLastStep) {
                return 'Complete Book Setup';
            }
            return 'Next';
        },

        get nextButtonClass() {
            const baseClasses = "px-6 py-2 rounded-lg transition-colors flex items-center";

            if (this.isLastStep) {
                return `${baseClasses} bg-green-500 text-white hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed`;
            }

            return `${baseClasses} bg-blue-500 text-white hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed`;
        },

        // Methods
        async goToPreviousStep() {
            if (!this.canGoBack) return;

            this.isNavigating = true;

            try {
                const success = this.$store.wizard.goToPrevious();

                if (success) {
                    // Additional logic for specific steps if needed
                    await this.onStepChange();
                }
            } catch (error) {
                console.error('Error navigating to previous step:', error);
                this.$store.wizard.setError('Failed to navigate. Please try again.');
            } finally {
                this.isNavigating = false;
            }
        },

        async goToNextStep() {
            if (!this.canGoForward) return;

            this.isNavigating = true;

            try {
                if (this.isLastStep) {
                    await this.completeWizard();
                } else {
                    const success = await this.$store.wizard.goToNext();

                    if (success) {
                        await this.onStepChange();
                    }
                }
            } catch (error) {
                console.error('Error navigating to next step:', error);
                this.$store.wizard.setError('Failed to navigate. Please try again.');
            } finally {
                this.isNavigating = false;
            }
        },

        async completeWizard() {
            try {
                // Get final session data
                const sessionData = await this.$store.wizard.getSession();

                if (sessionData) {
                    // Show completion message
                    this.showCompletionMessage(sessionData);
                } else {
                    throw new Error('Unable to retrieve session data');
                }
            } catch (error) {
                console.error('Error completing wizard:', error);
                this.$store.wizard.setError('Failed to complete wizard. Please try again.');
            }
        },

        showCompletionMessage(sessionData) {
            // You could integrate with a notification system here
            alert('Congratulations! Your book setup is complete. You can now start writing!');

            // Optionally redirect or show next steps
            console.log('Wizard completed with data:', sessionData);
        },

        // Navigation validation
        async validateCurrentStep() {
            const currentStep = this.$store.wizard.currentStep;

            switch (currentStep) {
                case 1:
                    return this.validateStep1();
                case 2:
                    return this.validateStep2();
                case 3:
                    return this.validateStep3();
                case 4:
                    return this.validateStep4();
                case 5:
                    return this.validateStep5();
                case 6:
                    return this.validateStep6();
                case 7:
                    return this.validateStep7();
                case 8:
                    return this.validateStep8();
                case 9:
                    return true; // Final step
                default:
                    return false;
            }
        },

        validateStep1() {
            const concept = this.$store.wizard.formData.concept;
            return concept && concept.trim().length >= 10;
        },

        validateStep2() {
            return this.$store.wizard.formData.genre !== '';
        },

        validateStep3() {
            return this.$store.wizard.formData.audience !== '';
        },

        validateStep4() {
            return this.$store.wizard.formData.style !== '';
        },

        validateStep5() {
            return this.$store.wizard.formData.length !== '';
        },

        validateStep6() {
            return this.$store.wizard.formData.structure !== '';
        },

        validateStep7() {
            return this.$store.wizard.formData.world !== '';
        },

        validateStep8() {
            // Content preferences can be empty
            return true;
        },

        // Step-specific navigation logic
        async onStepChange() {
            const currentStep = this.$store.wizard.currentStep;

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });

            // Step-specific logic
            switch (currentStep) {
                case 1:
                    await this.onEnterStep1();
                    break;
                case 2:
                    await this.onEnterStep2();
                    break;
                case 3:
                    await this.onEnterStep3();
                    break;
                case 4:
                    await this.onEnterStep4();
                    break;
                case 5:
                    await this.onEnterStep5();
                    break;
                case 6:
                    await this.onEnterStep6();
                    break;
                case 7:
                    await this.onEnterStep7();
                    break;
                case 8:
                    await this.onEnterStep8();
                    break;
                case 9:
                    await this.onEnterStep9();
                    break;
            }
        },

        async onEnterStep1() {
            // Focus on concept input
            this.$nextTick(() => {
                const conceptInput = document.getElementById('concept');
                if (conceptInput) {
                    conceptInput.focus();
                }
            });
        },

        async onEnterStep2() {
            // Load genre data if not available
            if (this.$store.wizard.currentStepData.options.length === 0) {
                // Will be handled by the step component
            }
        },

        async onEnterStep3() {
            // Load audience data
            console.log('Entering step 3: Target Audience');
        },

        async onEnterStep4() {
            // Load writing style data
            console.log('Entering step 4: Writing Style');
        },

        async onEnterStep5() {
            // Load book length data
            console.log('Entering step 5: Book Length');
        },

        async onEnterStep6() {
            // Load story structure data
            console.log('Entering step 6: Story Structure');
        },

        async onEnterStep7() {
            // Load world building data
            console.log('Entering step 7: World Building');
        },

        async onEnterStep8() {
            // Content preferences step
            console.log('Entering step 8: Content Preferences');
        },

        async onEnterStep9() {
            // Final summary step
            console.log('Entering step 9: Final Summary');
        },

        // Utility methods
        canProceed() {
            return this.$store.wizard.canProceed();
        },

        // Keyboard navigation
        handleKeyPress(event) {
            if (event.key === 'Enter' && event.ctrlKey) {
                // Ctrl+Enter to go to next step
                if (this.canGoForward) {
                    this.goToNextStep();
                }
            } else if (event.key === 'Escape') {
                // Escape to go back
                if (this.canGoBack) {
                    this.goToPreviousStep();
                }
            }
        },

        // Lifecycle
        init() {
            // Listen for keyboard shortcuts
            document.addEventListener('keydown', this.handleKeyPress.bind(this));
        },

        destroy() {
            // Clean up event listeners
            document.removeEventListener('keydown', this.handleKeyPress.bind(this));
        }
    };
}