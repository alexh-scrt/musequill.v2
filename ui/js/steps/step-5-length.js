/**
 * Step 5: Book Length Component
 * Handles book length selection based on genre and market requirements
 */

function step5Length() {
    return {
        // Data
        selectedLength: '',
        isSubmitting: false,

        // Step data from API
        options: [],
        llmMessage: '',

        // UI state
        hoveredOption: null,
        showLengthDetails: false,

        // Computed properties with logging
        get hasSelection() {
            const result = this.selectedLength !== '';
            console.log('✅ Step5Length - hasSelection:', result, 'selectedLength:', this.selectedLength);
            return result;
        },

        get canProceed() {
            const result = this.hasSelection;
            console.log('🚀 Step5Length - canProceed:', result);
            return result;
        },

        // Access wizard store data with logging
        get currentStepData() {
            const data = this.$store.wizard.currentStepData;
            console.log('📊 Step5Length - currentStepData accessed:', data);
            return data;
        },

        get userConcept() {
            const concept = this.$store.wizard.formData.concept;
            console.log('💭 Step5Length - userConcept:', concept?.substring(0, 50) + '...');
            return concept;
        },

        get selectedGenre() {
            const genre = this.$store.wizard.formData.genre;
            console.log('🎭 Step5Length - selectedGenre:', genre);
            return genre;
        },

        get selectedAudience() {
            const audience = this.$store.wizard.formData.audience;
            console.log('👥 Step5Length - selectedAudience:', audience);
            return audience;
        },

        get selectedStyle() {
            const style = this.$store.wizard.formData.style;
            console.log('✏️ Step5Length - selectedStyle:', style);
            return style;
        },

        get hasConceptAnalysis() {
            const hasAnalysis = !!this.$store.wizard.conceptAnalysis;
            console.log('🔍 Step5Length - hasConceptAnalysis:', hasAnalysis);
            return hasAnalysis;
        },

        // Methods
        async selectLength(lengthId) {
            console.log('🎯 Step5Length - selectLength called with:', lengthId);
            this.selectedLength = lengthId;

            // Update store
            this.$store.wizard.updateFormData('length', lengthId);
            console.log('📝 Step5Length - Updated formData with length:', lengthId);

            // Process length selection
            await this.processLengthSelection();
        },

        async processLengthSelection() {
            console.log('⚡ Step5Length - processLengthSelection started');
            console.log('⚡ Step5Length - selectedLength:', this.selectedLength);

            if (!this.selectedLength) {
                console.log('❌ Step5Length - No selectedLength, aborting');
                return;
            }

            this.isSubmitting = true;
            console.log('⚡ Step5Length - Set isSubmitting to true');

            try {
                console.log('🌐 Step5Length - Calling processStep with:', {
                    stepNumber: 5,
                    selection: this.selectedLength
                });

                const success = await this.$store.wizard.processStep(
                    5, // Step number
                    this.selectedLength
                );

                console.log('🌐 Step5Length - processStep result:', success);

                if (success) {
                    console.log('🔥 Step5Length - Processing successful, proceeding to next step');
                    await this.proceedToNextStep();
                } else {
                    console.error('❌ Step5Length - processStep failed');
                }
            } catch (error) {
                console.error('💥 Step5Length - Error in processLengthSelection:', error);
            } finally {
                this.isSubmitting = false;
                console.log('🔥 Step5Length - processLengthSelection finished');
            }
        },

        async proceedToNextStep() {
            console.log('➡️ Step5Length - proceedToNextStep called');

            // Move to step 6 (story structure)
            this.$store.wizard.setCurrentStep(6);
            console.log('➡️ Step5Length - Set current step to 6');

            // Load step 6 data
            await this.loadStoryStructureData();
        },

        async loadStoryStructureData() {
            console.log('🌐 Step5Length - loadStoryStructureData called');

            try {
                const success = await this.$store.wizard.processStep(6, null);
                console.log('🌐 Step5Length - loadStoryStructureData result:', success);
                // Step 6 data will be loaded in the wizard store
            } catch (error) {
                console.error('💥 Step5Length - Error loading story structure data:', error);
            }
        },

        // UI Methods
        getOptionClasses(optionId) {
            const baseClasses = "border rounded-lg p-6 cursor-pointer transition-all duration-200 hover:shadow-md";
            const selectedClasses = "border-blue-500 bg-blue-50 ring-2 ring-blue-200";
            const defaultClasses = "border-gray-200 hover:border-gray-300";

            if (this.selectedLength === optionId) {
                return `${baseClasses} ${selectedClasses}`;
            }

            return `${baseClasses} ${defaultClasses}`;
        },

        getViabilityBadgeClasses(viability) {
            const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";

            switch (viability?.toLowerCase()) {
                case 'high':
                    return `${baseClasses} bg-green-100 text-green-800`;
                case 'medium':
                    return `${baseClasses} bg-yellow-100 text-yellow-800`;
                case 'low':
                    return `${baseClasses} bg-red-100 text-red-800`;
                default:
                    return `${baseClasses} bg-gray-100 text-gray-600`;
            }
        },

        getTimeBadgeClasses(timeToWrite) {
            const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";

            if (timeToWrite && timeToWrite.includes('month')) {
                return `${baseClasses} bg-blue-100 text-blue-800`;
            } else if (timeToWrite && timeToWrite.includes('year')) {
                return `${baseClasses} bg-purple-100 text-purple-800`;
            }

            return `${baseClasses} bg-gray-100 text-gray-600`;
        },

        onOptionHover(optionId) {
            this.hoveredOption = optionId;
        },

        onOptionLeave() {
            this.hoveredOption = null;
        },

        // Data loading with comprehensive logging
        loadStepData() {
            console.log('📥 Step5Length - loadStepData called');

            const stepData = this.$store.wizard.currentStepData;
            console.log('📥 Step5Length - Raw stepData:', stepData);

            // Load options with fallback
            if (stepData && stepData.options && stepData.options.length > 0) {
                console.log('📥 Step5Length - Using stepData.options:', stepData.options.length, 'options');
                this.options = stepData.options;
            } else {
                console.log('📥 Step5Length - No stepData.options, keeping current options or using getSampleLengths');
                if (this.options.length === 0) {
                    this.options = this.getSampleLengths();
                }
            }
            console.log('📥 Step5Length - Final this.options length:', this.options.length);

            // Set LLM message
            const newMessage = stepData?.llmReasoning || this.getDefaultMessage();
            console.log('📥 Step5Length - Setting llmMessage:', newMessage);
            this.llmMessage = newMessage;

            // Load any existing selection
            const existingSelection = this.$store.wizard.formData.length || '';
            console.log('📥 Step5Length - Loading existing selection:', existingSelection);
            this.selectedLength = existingSelection;

            console.log('📥 Step5Length - loadStepData completed');
        },

        getDefaultMessage() {
            const selectedGenre = this.selectedGenre;
            const message = `For commercial success in ${selectedGenre || 'your chosen genre'}, these lengths perform best:`;
            console.log('💬 Step5Length - getDefaultMessage:', message);
            return message;
        },

        // Lifecycle with comprehensive logging
        init() {
            // IMMEDIATE early return if not on step 5 - don't even log
            if (this.$store.wizard.currentStep !== 5) {
                return;
            }

            console.log('🏁 Step5Length - INIT STARTING');
            console.log('🏁 Step5Length - Component initialization...');

            // Log wizard store state
            console.log('🏪 Step5Length - Wizard Store State:');
            console.log('🏪 Step5Length - currentStep:', this.$store.wizard.currentStep);
            console.log('🏪 Step5Length - sessionId:', this.$store.wizard.sessionId);
            console.log('🏪 Step5Length - formData:', this.$store.wizard.formData);
            console.log('🏪 Step5Length - conceptAnalysis:', this.$store.wizard.conceptAnalysis);
            console.log('🏪 Step5Length - currentStepData:', this.$store.wizard.currentStepData);

            // Initialize with fallback data first to show something
            this.options = this.getSampleLengths();
            this.llmMessage = this.getDefaultMessage();
            console.log('📦 Step5Length - Initialized with fallback data');

            // CRITICAL: Check if we have a valid session before making API calls
            if (!this.$store.wizard.sessionId) {
                console.log('❌ Step5Length - No session ID, staying with fallback data');
                console.log('🏁 Step5Length - INIT COMPLETED (with fallback data)');
                return;
            }

            // Check concept analysis availability
            console.log('🔍 Step5Length - Checking concept analysis...');
            console.log('🔍 Step5Length - Has concept analysis:', this.hasConceptAnalysis);

            // Load current step data from wizard store
            console.log('📥 Step5Length - Loading step data from store...');
            this.loadStepData();

            // Check if we have step data from previous navigation
            if (this.currentStepData?.options && this.currentStepData.options.length > 0) {
                console.log('✅ Step5Length - Found existing step data, using it');
                this.options = this.currentStepData.options;
                this.llmMessage = this.currentStepData.llmReasoning || this.getDefaultMessage();
                console.log('🏁 Step5Length - INIT COMPLETED (with existing data)');
                return;
            }

            // Only make API call if we have session and don't have options and we're on step 5
            console.log('🌐 Step5Length - No step data found, loading from API...');
            this.loadLengthOptions();

            console.log('🏁 Step5Length - INIT COMPLETED');
        },

        // Add a method to be called when step becomes visible
        async onStepVisible() {
            console.log('👁️ Step5Length - onStepVisible called');

            if (this.$store.wizard.currentStep !== 5) {
                console.log('❌ Step5Length - Not on step 5, ignoring visibility');
                return;
            }

            // Wait a moment for any pending store updates
            await this.$nextTick();

            // Check if we have fresh data from the previous step
            console.log('👁️ Step5Length - Checking for fresh data...');
            const freshStepData = this.$store.wizard.currentStepData;
            console.log('👁️ Step5Length - Fresh step data:', freshStepData);

            // If we have step data with options, use it
            if (freshStepData && freshStepData.options && freshStepData.options.length > 0) {
                console.log('✅ Step5Length - Found fresh step data, updating options');
                this.options = freshStepData.options;
                this.llmMessage = freshStepData.llmReasoning || this.getDefaultMessage();
                return;
            }

            // Initialize if not already done
            if (this.options.length === 0) {
                console.log('🔄 Step5Length - No options loaded, initializing...');
                this.options = this.getSampleLengths();
                this.llmMessage = this.getDefaultMessage();
            } else {
                console.log('✅ Step5Length - Already have options:', this.options.length);
            }
        },

        async loadLengthOptions() {
            console.log('🌐 Step5Length - loadLengthOptions called');

            // Final safety checks - MULTIPLE GUARDS
            if (this.$store.wizard.currentStep !== 5) {
                console.log('❌ Step5Length - Not on Step 5, aborting API call. Current step:', this.$store.wizard.currentStep);
                return;
            }

            if (!this.$store.wizard.sessionId) {
                console.log('❌ Step5Length - No session ID, aborting API call');
                return;
            }

            // Additional guard: check if we even have previous step data
            const hasGenre = this.$store.wizard.formData.genre;
            const hasAudience = this.$store.wizard.formData.audience;
            const hasStyle = this.$store.wizard.formData.style;

            if (!hasGenre || !hasAudience || !hasStyle) {
                console.log('❌ Step5Length - Missing required previous step data:', {
                    hasGenre, hasAudience, hasStyle
                });
                console.log('❌ Step5Length - Using fallback data instead of API call');
                this.options = this.getSampleLengths();
                return;
            }

            try {
                console.log('🌐 Step5Length - Making API call to processStep(5, null)');
                const success = await this.$store.wizard.processStep(5, null);
                console.log('🌐 Step5Length - loadLengthOptions result:', success);

                if (success) {
                    console.log('✅ Step5Length - API call successful, reloading step data');
                    this.loadStepData();
                } else {
                    console.log('❌ Step5Length - API call failed, using fallback');
                    this.options = this.getSampleLengths();
                }
            } catch (error) {
                console.error('💥 Step5Length - Error loading length options:', error);
                // Fallback to sample data
                console.log('🔄 Step5Length - Using fallback sample data');
                this.options = this.getSampleLengths();
            }
        },

        // Utility methods
        getOptionById(optionId) {
            const option = this.options.find(option => option.id === optionId);
            console.log('🔍 Step5Length - getOptionById called with:', optionId, 'found:', option);
            return option;
        },

        getSelectedLengthInfo() {
            const info = this.getOptionById(this.selectedLength);
            console.log('ℹ️ Step5Length - getSelectedLengthInfo:', info);
            return info;
        },

        formatRecommendationScore(score) {
            if (!score) return null;
            return `${Math.round(score)}% Match`;
        },

        // Sample lengths for testing/fallback
        getSampleLengths() {
            console.log('📦 Step5Length - getSampleLengths called');

            const selectedGenre = this.selectedGenre;
            const selectedAudience = this.selectedAudience;

            console.log('📦 Step5Length - getSampleLengths context:', {
                selectedGenre,
                selectedAudience
            });

            const baseLengths = [
                {
                    id: 'novella',
                    name: 'Novella',
                    description: 'A shorter work perfect for focused storytelling and faster completion',
                    word_count: '20,000 - 40,000 words',
                    page_count: '80 - 160 pages',
                    time_to_write: '2-4 months',
                    publishing_viability: 'Medium',
                    market_appeal: 'Niche',
                    recommendation_score: this.calculateScore('novella', selectedGenre, selectedAudience),
                    advantages: ['Faster to write', 'Easy to read', 'Good for first books'],
                    considerations: ['Limited market', 'Shorter story arc', 'Pricing challenges']
                },
                {
                    id: 'standard_novel',
                    name: 'Standard Novel',
                    description: 'The industry standard length with broad market appeal and publishing support',
                    word_count: '70,000 - 90,000 words',
                    page_count: '280 - 360 pages',
                    time_to_write: '6-12 months',
                    publishing_viability: 'High',
                    market_appeal: 'High',
                    recommendation_score: this.calculateScore('standard_novel', selectedGenre, selectedAudience),
                    advantages: ['Market standard', 'Publishing friendly', 'Reader expectations'],
                    considerations: ['Longer commitment', 'More complex plotting', 'Higher word count pressure']
                },
                {
                    id: 'epic_novel',
                    name: 'Epic Novel',
                    description: 'A longer work for complex stories with multiple plotlines and deep world-building',
                    word_count: '100,000 - 150,000 words',
                    page_count: '400 - 600 pages',
                    time_to_write: '12-24 months',
                    publishing_viability: 'Medium',
                    market_appeal: 'Genre Dependent',
                    recommendation_score: this.calculateScore('epic_novel', selectedGenre, selectedAudience),
                    advantages: ['Epic storytelling', 'Complex plots', 'Series potential'],
                    considerations: ['Long writing time', 'Complex structure', 'Higher editing costs']
                }
            ];

            console.log('📦 Step5Length - Generated sample lengths:', baseLengths.length, 'options');
            return baseLengths;
        },

        calculateScore(lengthType, genre, audience) {
            console.log('🧮 Step5Length - calculateScore called:', { lengthType, genre, audience });

            // Base scores for different length types
            const baseScores = {
                'novella': 60,
                'standard_novel': 85,
                'epic_novel': 70
            };

            let score = baseScores[lengthType] || 50;

            // Adjust based on genre
            if (genre === 'fantasy' && lengthType === 'epic_novel') score += 15;
            if (genre === 'romance' && lengthType === 'standard_novel') score += 10;
            if (genre === 'mystery' && lengthType === 'standard_novel') score += 10;

            // Adjust based on audience
            if (audience === 'young_adult' && lengthType === 'standard_novel') score += 5;
            if (audience === 'adult' && lengthType === 'epic_novel') score += 5;

            const finalScore = Math.min(score, 95); // Cap at 95%
            console.log('🧮 Step5Length - calculated score:', finalScore);
            return finalScore;
        },

        // Navigation
        goBack() {
            console.log('⬅️ Step5Length - goBack called');
            // Go back to step 4 (writing style)
            this.$store.wizard.setCurrentStep(4);
        }
    };
}