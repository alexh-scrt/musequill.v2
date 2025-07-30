/**
 * Step 8: Content Preferences Component
 * Handles free-text content preferences and restrictions
 */

function step8Content() {
    return {
        // Data
        contentPreferences: '',
        isSubmitting: false,

        // Step data from API
        llmMessage: '',
        suggestions: [],

        // UI state
        showSuggestions: false,
        characterCount: 0,

        // Computed properties
        get canProceed() {
            // Content preferences are optional, so always allow proceeding
            return true;
        },

        get isValid() {
            return this.contentPreferences.length <= 1000;
        },

        get characterCountClass() {
            if (this.characterCount > 1000) return 'text-red-500';
            if (this.characterCount > 800) return 'text-yellow-500';
            return 'text-gray-500';
        },

        // Get data from wizard store
        get currentStepData() {
            return this.$store.wizard.currentStepData;
        },

        get formData() {
            return this.$store.wizard.formData;
        },

        // Methods
        updateContentPreferences() {
            console.log('📝 Step8Content - updateContentPreferences:', this.contentPreferences);
            this.characterCount = this.contentPreferences.length;

            // Update store
            this.$store.wizard.updateFormData('contentPreferences', this.contentPreferences);
            console.log('📝 Step8Content - Updated wizard store formData');
        },

        async proceedToSummary() {
            console.log('🚀 Step8Content - proceedToSummary called');
            console.log('🚀 Step8Content - contentPreferences:', this.contentPreferences);

            this.isSubmitting = true;

            try {
                console.log('🌐 Step8Content - Calling processStep with:', {
                    stepNumber: 8,
                    selection: null,
                    additionalInput: this.contentPreferences
                });

                const success = await this.$store.wizard.processStep(
                    8, // Step number
                    null, // No selection for this step
                    this.contentPreferences // Additional input
                );

                console.log('🌐 Step8Content - processStep result:', success);

                if (success) {
                    console.log('🔥 Step8Content - Processing successful, proceeding to summary view');
                    await this.proceedToFinalSummary();
                } else {
                    console.error('❌ Step8Content - processStep failed');
                }
            } catch (error) {
                console.error('💥 Step8Content - Error processing content preferences:', error);
            } finally {
                this.isSubmitting = false;
                console.log('🔥 Step8Content - proceedToSummary finished');
            }
        },

        async proceedToFinalSummary() {
            console.log('➡️ Step8Content - proceedToFinalSummary called');

            // Step 8 IS the final step according to backend
            // Just move to step 9 for UI display of summary
            this.$store.wizard.setCurrentStep(9);
            console.log('➡️ Step8Content - Set current step to 9 for summary display');

            // Don't make another API call - step 8 response should contain final summary
            console.log('✅ Step8Content - Summary data already loaded from step 8 response');
        },

        // Data loading
        loadStepData() {
            console.log('📥 Step8Content - loadStepData called');

            const stepData = this.$store.wizard.currentStepData;
            console.log('📥 Step8Content - Raw stepData:', stepData);

            // Load LLM message
            const newMessage = stepData?.llmReasoning || this.getDefaultMessage();
            console.log('📥 Step8Content - Setting llmMessage:', newMessage);
            this.llmMessage = newMessage;

            // Load suggestions if available
            if (stepData?.suggestions && Array.isArray(stepData.suggestions)) {
                console.log('📥 Step8Content - Loading suggestions:', stepData.suggestions.length);
                this.suggestions = stepData.suggestions;
                this.showSuggestions = this.suggestions.length > 0;
            }

            // Load any existing content preferences
            const existingPreferences = this.$store.wizard.formData.contentPreferences || '';
            console.log('📥 Step8Content - Loading existing preferences:', existingPreferences);
            this.contentPreferences = existingPreferences;
            this.characterCount = this.contentPreferences.length;

            console.log('📥 Step8Content - loadStepData completed');
        },

        getDefaultMessage() {
            return 'Specify any content preferences or restrictions for your book. This is optional but helps ensure the content aligns with your vision.';
        },

        // Lifecycle - following the pattern from other steps
        init() {
            console.log('🚀 Step8Content - INIT STARTED');
            console.log('🚀 Step8Content - Current step:', this.$store.wizard.currentStep);
            console.log('🚀 Step8Content - Session ID:', this.$store.wizard.sessionId);

            // IMPORTANT: Never make API calls during init()
            // Components are initialized for ALL steps when page loads
            console.log('⚠️ Step8Content - Init should never make API calls');

            // Only load existing data from store
            this.contentPreferences = this.$store.wizard.formData.contentPreferences || '';
            this.characterCount = this.contentPreferences.length;
            console.log('📥 Step8Content - Loaded existing preferences:', this.contentPreferences);

            // Set up fallback data immediately (no API calls)
            this.llmMessage = this.getDefaultMessage();
            console.log('📋 Step8Content - Set fallback message');

            // Set up a watcher to load data when we actually reach Step 8
            this.$watch('$store.wizard.currentStep', (newStep, oldStep) => {
                console.log('👀 Step8Content - Step changed from', oldStep, 'to', newStep);
                if (newStep === 8 && oldStep !== 8) {
                    console.log('🎯 Step8Content - Now entering Step 8, loading data...');
                    this.onEnterStep8();
                }
            });

            console.log('🏁 Step8Content - INIT COMPLETED (no API calls)');
        },

        // New method called only when actually entering Step 8
        async onEnterStep8() {
            console.log('🚀 Step8Content - onEnterStep8 called');

            // Check if we have a valid session
            if (!this.$store.wizard.sessionId) {
                console.log('❌ Step8Content - No session ID, keeping fallback data');
                return;
            }

            // Check if we already have fresh step data
            const stepData = this.$store.wizard.currentStepData;
            console.log('🔍 Step8Content - Checking existing stepData:', stepData);

            if (stepData && stepData.step_number === 8) {
                console.log('✅ Step8Content - Already have Step 8 data, using it');
                this.loadStepData();
                return;
            }

            // Load fresh data for step 8
            console.log('🌐 Step8Content - Loading fresh Step 8 data...');
            try {
                const success = await this.$store.wizard.processStep(8, null);
                console.log('🌐 Step8Content - processStep result:', success);

                if (success) {
                    console.log('✅ Step8Content - Successfully loaded Step 8 data');
                    this.loadStepData();
                } else {
                    console.error('❌ Step8Content - Failed to load Step 8 data, using fallback');
                }
            } catch (error) {
                console.error('💥 Step8Content - Error loading Step 8 data:', error);
                console.log('🔄 Step8Content - Using fallback data');
            }
        },

        // Navigation
        goBack() {
            console.log('⬅️ Step8Content - goBack called');
            this.$store.wizard.setCurrentStep(7);
        },

        // Debug helpers
        logDebugInfo() {
            console.log('🔧 Step8Content - DEBUG INFO:');
            console.log('🔧 Current Step:', this.$store.wizard.currentStep);
            console.log('🔧 Session ID:', this.$store.wizard.sessionId);
            console.log('🔧 Content Preferences:', this.contentPreferences);
            console.log('🔧 Character Count:', this.characterCount);
            console.log('🔧 Can Proceed:', this.canProceed);
            console.log('🔧 Is Valid:', this.isValid);
            console.log('🔧 Current Step Data:', this.currentStepData);
            console.log('🔧 Form Data:', this.formData);
            console.log('🔧 LLM Message:', this.llmMessage);
            console.log('🔧 Suggestions:', this.suggestions);
            console.log('🔧 Show Suggestions:', this.showSuggestions);
        }
    };
}