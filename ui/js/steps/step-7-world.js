/**
 * Step 7: World Building Component  
 * Handles world/setting type selection based on genre and story structure
 */

function step7World() {
    return {
        // Data
        selectedWorld: '',
        isSubmitting: false,

        // Step data from API
        options: [],
        llmMessage: '',

        // UI state
        hoveredOption: null,

        // Computed properties with logging
        get hasSelection() {
            const result = this.selectedWorld !== '';
            console.log('✅ Step7World - hasSelection:', result, 'selectedWorld:', this.selectedWorld);
            return result;
        },

        get canProceed() {
            const result = this.hasSelection;
            console.log('🚀 Step7World - canProceed:', result);
            return result;
        },

        // Access wizard store data with logging
        get currentStepData() {
            const data = this.$store.wizard.currentStepData;
            console.log('📊 Step7World - currentStepData accessed:', data);
            return data;
        },

        get selectedGenre() {
            const genre = this.$store.wizard.formData.genre;
            console.log('🎭 Step7World - selectedGenre:', genre);
            return genre;
        },

        get selectedStructure() {
            const structure = this.$store.wizard.formData.structure;
            console.log('🏗️ Step7World - selectedStructure:', structure);
            return structure;
        },

        // Methods
        async selectWorld(worldId) {
            console.log('🎯 Step7World - selectWorld called with:', worldId);
            this.selectedWorld = worldId;

            // Update store
            this.$store.wizard.updateFormData('world', worldId);
            console.log('📝 Step7World - Updated formData with world:', worldId);

            // Process world selection
            await this.processWorldSelection();
        },

        async processWorldSelection() {
            console.log('⚡ Step7World - processWorldSelection started');
            console.log('⚡ Step7World - selectedWorld:', this.selectedWorld);

            if (!this.selectedWorld) {
                console.log('❌ Step7World - No selectedWorld, aborting');
                return;
            }

            this.isSubmitting = true;
            console.log('⚡ Step7World - Set isSubmitting to true');

            try {
                console.log('🌐 Step7World - Calling processStep with:', {
                    stepNumber: 7,
                    selection: this.selectedWorld
                });

                const success = await this.$store.wizard.processStep(
                    7, // Step number
                    this.selectedWorld
                );

                console.log('🌐 Step7World - processStep result:', success);

                if (success) {
                    console.log('🔥 Step7World - Processing successful, proceeding to next step');
                    await this.proceedToNextStep();
                } else {
                    console.error('❌ Step7World - processStep failed');
                }
            } catch (error) {
                console.error('💥 Step7World - Error in processWorldSelection:', error);
            } finally {
                this.isSubmitting = false;
                console.log('🔥 Step7World - processWorldSelection finished');
            }
        },

        async proceedToNextStep() {
            console.log('➡️ Step7World - proceedToNextStep called');

            // Move to step 8 (content preferences)
            this.$store.wizard.setCurrentStep(8);
            console.log('➡️ Step7World - Set current step to 8');

            // Load step 8 data
            await this.loadContentPreferencesData();
        },

        async loadContentPreferencesData() {
            console.log('🌐 Step7World - loadContentPreferencesData called');

            try {
                const success = await this.$store.wizard.processStep(8, null);
                console.log('🌐 Step7World - loadContentPreferencesData result:', success);
                // Step 8 data will be loaded automatically through the store
            } catch (error) {
                console.error('💥 Step7World - Error loading content preferences data:', error);
            }
        },

        // Data loading with comprehensive logging
        loadStepData() {
            console.log('📥 Step7World - loadStepData called');

            const stepData = this.$store.wizard.currentStepData;
            console.log('📥 Step7World - Raw stepData:', stepData);

            // Load options with fallback
            if (stepData && stepData.options && stepData.options.length > 0) {
                console.log('📥 Step7World - Using stepData.options:', stepData.options.length, 'options');
                this.options = stepData.options;
            } else {
                console.log('📥 Step7World - No stepData.options, keeping current options or using getSampleWorlds');
                if (this.options.length === 0) {
                    this.options = this.getSampleWorlds();
                }
            }
            console.log('📥 Step7World - Final this.options length:', this.options.length);

            // Set LLM message
            const newMessage = stepData?.llmReasoning || this.getDefaultMessage();
            console.log('📥 Step7World - Setting llmMessage:', newMessage);
            this.llmMessage = newMessage;

            // Load any existing selection
            const existingSelection = this.$store.wizard.formData.world || '';
            console.log('📥 Step7World - Loading existing selection:', existingSelection);
            this.selectedWorld = existingSelection;

            console.log('📥 Step7World - loadStepData completed');
        },

        getDefaultMessage() {
            const selectedGenre = this.selectedGenre;
            const message = `For your ${selectedGenre || 'chosen genre'} story, these settings offer commercial appeal:`;
            console.log('💬 Step7World - getDefaultMessage:', message);
            return message;
        },

        // Lifecycle with comprehensive logging
        init() {
            // IMMEDIATE early return if not on step 7 - don't even log
            if (this.$store.wizard.currentStep !== 7) {
                return;
            }

            console.log('🏁 Step7World - INIT STARTING');
            console.log('🏁 Step7World - Component initialization...');

            // Log wizard store state
            console.log('🏪 Step7World - Wizard Store State:');
            console.log('🏪 Step7World - currentStep:', this.$store.wizard.currentStep);
            console.log('🏪 Step7World - sessionId:', this.$store.wizard.sessionId);
            console.log('🏪 Step7World - formData:', this.$store.wizard.formData);
            console.log('🏪 Step7World - currentStepData:', this.$store.wizard.currentStepData);

            // Initialize with fallback data first to show something
            this.options = this.getSampleWorlds();
            this.llmMessage = this.getDefaultMessage();
            console.log('📦 Step7World - Initialized with fallback data');

            // CRITICAL: Check if we have a valid session before making API calls
            if (!this.$store.wizard.sessionId) {
                console.log('❌ Step7World - No session ID, staying with fallback data');
                console.log('🏁 Step7World - INIT COMPLETED (with fallback data)');
                return;
            }

            // Load current step data from wizard store
            console.log('📥 Step7World - Loading step data from store...');
            this.loadStepData();

            // Check if we have step data from previous navigation
            if (this.currentStepData?.options && this.currentStepData.options.length > 0) {
                console.log('✅ Step7World - Found existing step data, using it');
                this.options = this.currentStepData.options;
                this.llmMessage = this.currentStepData.llmReasoning || this.getDefaultMessage();
                console.log('🏁 Step7World - INIT COMPLETED (with existing data)');
                return;
            }

            // Only make API call if we have session and don't have options and we're on step 7
            console.log('🌐 Step7World - No step data found, loading from API...');
            this.loadWorldOptions();

            console.log('🏁 Step7World - INIT COMPLETED');
        },

        // Add a method to be called when step becomes visible
        async onStepVisible() {
            console.log('👁️ Step7World - onStepVisible called');

            if (this.$store.wizard.currentStep !== 7) {
                console.log('❌ Step7World - Not on step 7, ignoring visibility');
                return;
            }

            // Wait a moment for any pending store updates
            await this.$nextTick();

            // Check if we have fresh data from the previous step
            console.log('👁️ Step7World - Checking for fresh data...');
            const freshStepData = this.$store.wizard.currentStepData;
            console.log('👁️ Step7World - Fresh step data:', freshStepData);

            // If we have step data with options, use it
            if (freshStepData && freshStepData.options && freshStepData.options.length > 0) {
                console.log('✅ Step7World - Found fresh step data, updating options');
                this.options = freshStepData.options;
                this.llmMessage = freshStepData.llmReasoning || this.getDefaultMessage();
                return;
            }

            // Initialize if not already done
            if (this.options.length === 0) {
                console.log('🔄 Step7World - No options loaded, initializing...');
                this.options = this.getSampleWorlds();
                this.llmMessage = this.getDefaultMessage();
            } else {
                console.log('✅ Step7World - Already have options:', this.options.length);
            }
        },

        async loadWorldOptions() {
            console.log('🌐 Step7World - loadWorldOptions called');

            // Final safety checks - MULTIPLE GUARDS
            if (this.$store.wizard.currentStep !== 7) {
                console.log('❌ Step7World - Not on Step 7, aborting API call. Current step:', this.$store.wizard.currentStep);
                return;
            }

            if (!this.$store.wizard.sessionId) {
                console.log('❌ Step7World - No session ID, aborting API call');
                return;
            }

            // Additional guard: check if we even have previous step data
            const hasGenre = this.$store.wizard.formData.genre;
            const hasStructure = this.$store.wizard.formData.structure;

            if (!hasGenre || !hasStructure) {
                console.log('❌ Step7World - Missing required previous step data:', {
                    hasGenre, hasStructure
                });
                console.log('❌ Step7World - Using fallback data instead of API call');
                this.options = this.getSampleWorlds();
                return;
            }

            try {
                console.log('🌐 Step7World - Making API call to processStep(7, null)');
                const success = await this.$store.wizard.processStep(7, null);
                console.log('🌐 Step7World - loadWorldOptions result:', success);

                if (success) {
                    console.log('✅ Step7World - API call successful, reloading step data');
                    this.loadStepData();
                } else {
                    console.log('❌ Step7World - API call failed, using fallback');
                    this.options = this.getSampleWorlds();
                }
            } catch (error) {
                console.error('💥 Step7World - Error loading world options:', error);
                // Fallback to sample data
                console.log('🔄 Step7World - Using fallback sample data');
                this.options = this.getSampleWorlds();
            }
        },

        // Utility methods
        getOptionById(optionId) {
            const option = this.options.find(option => option.id === optionId);
            console.log('🔍 Step7World - getOptionById called with:', optionId, 'found:', option);
            return option;
        },

        getSelectedWorldInfo() {
            const info = this.getOptionById(this.selectedWorld);
            console.log('ℹ️ Step7World - getSelectedWorldInfo:', info);
            return info;
        },

        formatRecommendationScore(score) {
            if (!score) return null;
            return `${Math.round(score)}% Match`;
        },

        formatResearchComplexity(complexity) {
            const complexityMap = {
                'low': 'Minimal Research',
                'medium': 'Moderate Research',
                'high': 'Extensive Research'
            };
            return complexityMap[complexity] || complexity;
        },

        // Sample worlds for testing/fallback
        getSampleWorlds() {
            console.log('📦 Step7World - getSampleWorlds called');

            const selectedGenre = this.selectedGenre;

            console.log('📦 Step7World - getSampleWorlds context:', {
                selectedGenre
            });

            // Base world types that work for most genres
            const baseWorlds = [
                {
                    id: 'contemporary',
                    name: 'Contemporary/Modern Day',
                    description: 'Present-day real-world settings that readers recognize',
                    recommendation_score: 85,
                    research_complexity: 'low',
                    commercial_appeal: 'Very High',
                    why_recommended: 'Familiar to readers, easy to write authentically'
                },
                {
                    id: 'small_town',
                    name: 'Small Town/Community',
                    description: 'Tight-knit communities with strong local connections',
                    recommendation_score: 80,
                    research_complexity: 'low',
                    commercial_appeal: 'High',
                    why_recommended: 'Relatable setting with built-in character dynamics'
                },
                {
                    id: 'historical',
                    name: 'Historical Setting',
                    description: 'Well-documented historical periods with established atmosphere',
                    recommendation_score: 75,
                    research_complexity: 'medium',
                    commercial_appeal: 'High',
                    why_recommended: 'Rich atmosphere and proven reader interest'
                }
            ];

            // Genre-specific additional worlds
            if (selectedGenre === 'fantasy') {
                baseWorlds.push({
                    id: 'secondary_fantasy',
                    name: 'Secondary Fantasy World',
                    description: 'Original fantasy realm with magic systems and unique cultures',
                    recommendation_score: 90,
                    research_complexity: 'medium',
                    commercial_appeal: 'Excellent',
                    why_recommended: 'High demand in fantasy market with creative freedom'
                });
                baseWorlds.push({
                    id: 'urban_fantasy',
                    name: 'Urban Fantasy',
                    description: 'Modern world with hidden magical elements',
                    recommendation_score: 88,
                    research_complexity: 'low',
                    commercial_appeal: 'Very High',
                    why_recommended: 'Combines familiar settings with exciting magical elements'
                });
            } else if (selectedGenre === 'science_fiction') {
                baseWorlds.push({
                    id: 'near_future',
                    name: 'Near Future Earth',
                    description: 'Earth 20-100 years in the future with believable technology',
                    recommendation_score: 85,
                    research_complexity: 'medium',
                    commercial_appeal: 'High',
                    why_recommended: 'Relatable yet exciting for sci-fi readers'
                });
            } else if (selectedGenre === 'mystery') {
                baseWorlds.push({
                    id: 'urban_setting',
                    name: 'Urban/City Setting',
                    description: 'Complex urban environments with diverse investigation opportunities',
                    recommendation_score: 90,
                    research_complexity: 'low',
                    commercial_appeal: 'Very High',
                    why_recommended: 'Perfect for complex mysteries and diverse character interactions'
                });
            }

            console.log('📦 Step7World - Generated sample worlds:', baseWorlds.length, 'options');
            return baseWorlds;
        },

        // Styling helpers
        getWorldCardClass(world) {
            let baseClass = 'p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 ';

            if (this.selectedWorld === world.id) {
                baseClass += 'border-blue-500 bg-blue-50 shadow-md ';
            } else if (this.hoveredOption === world.id) {
                baseClass += 'border-gray-300 bg-gray-50 shadow-sm ';
            } else {
                baseClass += 'border-gray-200 hover:border-gray-300 hover:bg-gray-50 ';
            }

            return baseClass;
        },

        getRecommendationBadgeClass(score) {
            if (score >= 90) return 'bg-green-100 text-green-800';
            if (score >= 80) return 'bg-blue-100 text-blue-800';
            if (score >= 70) return 'bg-yellow-100 text-yellow-800';
            return 'bg-gray-100 text-gray-800';
        },

        getComplexityBadgeClass(complexity) {
            const classes = {
                'low': 'bg-green-100 text-green-800',
                'medium': 'bg-yellow-100 text-yellow-800',
                'high': 'bg-red-100 text-red-800'
            };
            return classes[complexity] || 'bg-gray-100 text-gray-800';
        },

        // Navigation
        goBack() {
            console.log('⬅️ Step7World - goBack called');
            // Go back to step 6 (story structure)
            this.$store.wizard.setCurrentStep(6);
        }
    };
}