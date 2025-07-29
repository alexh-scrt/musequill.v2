/**
 * Progress Bar Component
 * Displays wizard progress and step indicators
 */

function progressBar() {
    return {
        // Data
        animationDuration: 300,

        // Computed
        get progressPercentage() {
            return Math.round((this.$store.wizard.currentStep / this.$store.wizard.totalSteps) * 100);
        },

        get currentStepInfo() {
            return this.$store.wizard.getStepByNumber(this.$store.wizard.currentStep);
        },

        get completedSteps() {
            return this.$store.wizard.currentStep - 1;
        },

        get remainingSteps() {
            return this.$store.wizard.totalSteps - this.$store.wizard.currentStep;
        },

        // Methods
        getStepStatus(stepNumber) {
            const currentStep = this.$store.wizard.currentStep;

            if (stepNumber < currentStep) {
                return 'completed';
            } else if (stepNumber === currentStep) {
                return 'current';
            } else {
                return 'pending';
            }
        },

        getStepClasses(stepNumber) {
            const status = this.getStepStatus(stepNumber);
            const baseClasses = "w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all duration-300";

            switch (status) {
                case 'completed':
                    return `${baseClasses} bg-green-500 text-white transform scale-100`;
                case 'current':
                    return `${baseClasses} bg-blue-500 text-white ring-4 ring-blue-200 transform scale-110`;
                case 'pending':
                default:
                    return `${baseClasses} bg-gray-200 text-gray-500 transform scale-100`;
            }
        },

        getConnectorClasses(stepNumber) {
            const isCompleted = stepNumber < this.$store.wizard.currentStep;
            const baseClasses = "flex-1 h-1 mx-2 rounded-full transition-all duration-500";

            if (isCompleted) {
                return `${baseClasses} bg-green-500`;
            } else {
                return `${baseClasses} bg-gray-200`;
            }
        },

        getStepIcon(stepNumber) {
            const status = this.getStepStatus(stepNumber);

            if (status === 'completed') {
                return '✓';
            } else {
                return stepNumber.toString();
            }
        },

        // Animation methods
        animateProgress() {
            const progressBar = this.$refs.progressBar;
            if (progressBar) {
                progressBar.style.transition = `width ${this.animationDuration}ms ease-in-out`;
            }
        },

        // Step navigation (optional - for clickable steps)
        canNavigateToStep(stepNumber) {
            // Allow navigation to completed steps and current step
            return stepNumber <= this.$store.wizard.currentStep;
        },

        async navigateToStep(stepNumber) {
            if (!this.canNavigateToStep(stepNumber)) {
                return;
            }

            // Only allow going back to previous steps
            if (stepNumber < this.$store.wizard.currentStep) {
                this.$store.wizard.setCurrentStep(stepNumber);
            }
        },

        // Progress text helpers
        getProgressText() {
            const current = this.$store.wizard.currentStep;
            const total = this.$store.wizard.totalSteps;
            return `Step ${current} of ${total}`;
        },

        getTimeEstimate() {
            const remainingSteps = this.remainingSteps;
            const estimatedMinutesPerStep = 2; // Average time per step
            const totalMinutes = remainingSteps * estimatedMinutesPerStep;

            if (totalMinutes === 0) {
                return "Almost done!";
            } else if (totalMinutes < 5) {
                return `~${totalMinutes} min remaining`;
            } else {
                return `~${Math.ceil(totalMinutes / 5) * 5} min remaining`;
            }
        },

        // Accessibility
        getStepAriaLabel(stepNumber) {
            const step = this.$store.wizard.getStepByNumber(stepNumber);
            const status = this.getStepStatus(stepNumber);

            return `Step ${stepNumber}: ${step?.name || 'Unknown'}, ${status}`;
        },

        getProgressAriaLabel() {
            return `Progress: ${this.progressPercentage}% complete, ${this.getProgressText()}`;
        },

        // Lifecycle
        init() {
            // Watch for step changes to trigger animations
            this.$watch('$store.wizard.currentStep', () => {
                this.animateProgress();
            });
        },

        // Visual feedback methods
        pulseCurrentStep() {
            const currentStepElement = this.$refs[`step_${this.$store.wizard.currentStep}`];
            if (currentStepElement) {
                currentStepElement.classList.add('animate-pulse');
                setTimeout(() => {
                    currentStepElement.classList.remove('animate-pulse');
                }, 1000);
            }
        },

        showStepTooltip(stepNumber) {
            const step = this.$store.wizard.getStepByNumber(stepNumber);
            const status = this.getStepStatus(stepNumber);

            return {
                title: step?.name || 'Unknown Step',
                description: this.getStepDescription(stepNumber),
                status: status,
                canNavigate: this.canNavigateToStep(stepNumber)
            };
        },

        getStepDescription(stepNumber) {
            const descriptions = {
                1: "Tell us about your book idea",
                2: "Choose your book's genre",
                3: "Define your target audience",
                4: "Select your writing style",
                5: "Determine your book length",
                6: "Pick your story structure",
                7: "Design your world",
                8: "Set content preferences",
                9: "Review and finalize"
            };

            return descriptions[stepNumber] || "Complete this step";
        }
    };
}