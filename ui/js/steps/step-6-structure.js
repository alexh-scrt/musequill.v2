/**
 * Step 6: Story Structure Component
 * Handles story structure selection based on genre and previous choices
 */

function step6Structure() {
    return {
        // Data
        selectedStructure: '',
        isSubmitting: false,

        // Step data from API
        options: [],
        llmMessage: '',

        // UI state
        hoveredOption: null,

        // Computed properties with logging
        get hasSelection() {
            const result = this.selectedStructure !== '';
            console.log('✅ Step6Structure - hasSelection:', result, 'selectedStructure:', this.selectedStructure);
            return result;
        },

        get canProceed() {
            const result = this.hasSelection;
            console.log('🚀 Step6Structure - canProceed:', result);
            return result;
        },

        // Access wizard store data with logging
        get currentStepData() {
            const data = this.$store.wizard.currentStepData;
            console.log('📊 Step6Structure - currentStepData accessed:', data);
            return data;
        },

        get selectedGenre() {
            const genre = this.$store.wizard.formData.genre;
            console.log('🎭 Step6Structure - selectedGenre:', genre);
            return genre;
        },

        get selectedLength() {
            const length = this.$store.wizard.formData.length;
            console.log('📏 Step6Structure - selectedLength:', length);
            return length;
        },

        // Methods
        async selectStructure(structureId) {
            console.log('🎯 Step6Structure - selectStructure called with:', structureId);
            this.selectedStructure = structureId;

            // Update store
            this.$store.wizard.updateFormData('structure', structureId);
            console.log('📝 Step6Structure - Updated formData with structure:', structureId);

            // Process structure selection
            await this.processStructureSelection();
        },

        async processStructureSelection() {
            console.log('⚡ Step6Structure - processStructureSelection started');
            console.log('⚡ Step6Structure - selectedStructure:', this.selectedStructure);

            if (!this.selectedStructure) {
                console.log('❌ Step6Structure - No selectedStructure, aborting');
                return;
            }

            this.isSubmitting = true;
            console.log('⚡ Step6Structure - Set isSubmitting to true');

            try {
                console.log('🌐 Step6Structure - Calling processStep with:', {
                    stepNumber: 6,
                    selection: this.selectedStructure
                });

                const success = await this.$store.wizard.processStep(
                    6, // Step number
                    this.selectedStructure
                );

                console.log('🌐 Step6Structure - processStep result:', success);

                if (success) {
                    console.log('🔥 Step6Structure - Processing successful, proceeding to next step');
                    await this.proceedToNextStep();
                } else {
                    console.error('❌ Step6Structure - processStep failed');
                }
            } catch (error) {
                console.error('💥 Step6Structure - Error in processStructureSelection:', error);
            } finally {
                this.isSubmitting = false;
                console.log('🔥 Step6Structure - processStructureSelection finished');
            }
        },

        async proceedToNextStep() {
            console.log('➡️ Step6Structure - proceedToNextStep called');

            // Move to step 7 (world building)
            this.$store.wizard.setCurrentStep(7);
            console.log('➡️ Step6Structure - Set current step to 7');

            // Load step 7 data
            await this.loadWorldBuildingData();
        },

        async loadWorldBuildingData() {
            console.log('🌐 Step6Structure - loadWorldBuildingData called');

            try {
                const success = await this.$store.wizard.processStep(7, null);
                console.log('🌐 Step6Structure - loadWorldBuildingData result:', success);
                // Step 7 data will be loaded automatically through the store
            } catch (error) {
                console.error('💥 Step6Structure - Error loading world building data:', error);
            }
        },

        // Data loading with comprehensive logging
        loadStepData() {
            console.log('📥 Step6Structure - loadStepData called');

            const stepData = this.$store.wizard.currentStepData;
            console.log('📥 Step6Structure - Raw stepData:', stepData);

            // Load options with fallback
            if (stepData && stepData.options && stepData.options.length > 0) {
                console.log('📥 Step6Structure - Using stepData.options:', stepData.options.length, 'options');
                this.options = stepData.options;
            } else {
                console.log('📥 Step6Structure - No stepData.options, keeping current options or using getSampleStructures');
                if (this.options.length === 0) {
                    this.options = this.getSampleStructures();
                }
            }
            console.log('📥 Step6Structure - Final this.options length:', this.options.length);

            // Set LLM message
            const newMessage = stepData?.llmReasoning || this.getDefaultMessage();
            console.log('📥 Step6Structure - Setting llmMessage:', newMessage);
            this.llmMessage = newMessage;

            // Load any existing selection
            const existingSelection = this.$store.wizard.formData.structure || '';
            console.log('📥 Step6Structure - Loading existing selection:', existingSelection);
            this.selectedStructure = existingSelection;

            console.log('📥 Step6Structure - loadStepData completed');
        },

        getDefaultMessage() {
            const selectedGenre = this.selectedGenre;
            const message = `These proven structures work excellently for ${selectedGenre || 'your chosen genre'} books:`;
            console.log('💬 Step6Structure - getDefaultMessage:', message);
            return message;
        },

        // Lifecycle with comprehensive logging
        init() {
            // IMMEDIATE early return if not on step 6 - don't even log
            if (this.$store.wizard.currentStep !== 6) {
                return;
            }

            console.log('🏁 Step6Structure - INIT STARTING');
            console.log('🏁 Step6Structure - Component initialization...');

            // Log wizard store state
            console.log('🏪 Step6Structure - Wizard Store State:');
            console.log('🏪 Step6Structure - currentStep:', this.$store.wizard.currentStep);
            console.log('🏪 Step6Structure - sessionId:', this.$store.wizard.sessionId);
            console.log('🏪 Step6Structure - formData:', this.$store.wizard.formData);
            console.log('🏪 Step6Structure - currentStepData:', this.$store.wizard.currentStepData);

            // Initialize with fallback data first to show something
            this.options = this.getSampleStructures();
            this.llmMessage = this.getDefaultMessage();
            console.log('📦 Step6Structure - Initialized with fallback data');

            // CRITICAL: Check if we have a valid session before making API calls
            if (!this.$store.wizard.sessionId) {
                console.log('❌ Step6Structure - No session ID, staying with fallback data');
                console.log('🏁 Step6Structure - INIT COMPLETED (with fallback data)');
                return;
            }

            // Load current step data from wizard store
            console.log('📥 Step6Structure - Loading step data from store...');
            this.loadStepData();

            // Check if we have step data from previous navigation
            if (this.currentStepData?.options && this.currentStepData.options.length > 0) {
                console.log('✅ Step6Structure - Found existing step data, using it');
                this.options = this.currentStepData.options;
                this.llmMessage = this.currentStepData.llmReasoning || this.getDefaultMessage();
                console.log('🏁 Step6Structure - INIT COMPLETED (with existing data)');
                return;
            }

            // Only make API call if we have session and don't have options and we're on step 6
            console.log('🌐 Step6Structure - No step data found, loading from API...');
            this.loadStructureOptions();

            console.log('🏁 Step6Structure - INIT COMPLETED');
        },

        // Add a method to be called when step becomes visible
        async onStepVisible() {
            console.log('👁️ Step6Structure - onStepVisible called');

            if (this.$store.wizard.currentStep !== 6) {
                console.log('❌ Step6Structure - Not on step 6, ignoring visibility');
                return;
            }

            // Wait a moment for any pending store updates
            await this.$nextTick();

            // Check if we have fresh data from the previous step
            console.log('👁️ Step6Structure - Checking for fresh data...');
            const freshStepData = this.$store.wizard.currentStepData;
            console.log('👁️ Step6Structure - Fresh step data:', freshStepData);

            // If we have step data with options, use it
            if (freshStepData && freshStepData.options && freshStepData.options.length > 0) {
                console.log('✅ Step6Structure - Found fresh step data, updating options');
                this.options = freshStepData.options;
                this.llmMessage = freshStepData.llmReasoning || this.getDefaultMessage();
                return;
            }

            // Initialize if not already done
            if (this.options.length === 0) {
                console.log('🔄 Step6Structure - No options loaded, initializing...');
                this.options = this.getSampleStructures();
                this.llmMessage = this.getDefaultMessage();
            } else {
                console.log('✅ Step6Structure - Already have options:', this.options.length);
            }
        },

        async loadStructureOptions() {
            console.log('🌐 Step6Structure - loadStructureOptions called');

            // Final safety checks - MULTIPLE GUARDS
            if (this.$store.wizard.currentStep !== 6) {
                console.log('❌ Step6Structure - Not on Step 6, aborting API call. Current step:', this.$store.wizard.currentStep);
                return;
            }

            if (!this.$store.wizard.sessionId) {
                console.log('❌ Step6Structure - No session ID, aborting API call');
                return;
            }

            // Additional guard: check if we even have previous step data
            const hasGenre = this.$store.wizard.formData.genre;
            const hasLength = this.$store.wizard.formData.length;

            if (!hasGenre || !hasLength) {
                console.log('❌ Step6Structure - Missing required previous step data:', {
                    hasGenre, hasLength
                });
                console.log('❌ Step6Structure - Using fallback data instead of API call');
                this.options = this.getSampleStructures();
                return;
            }

            try {
                console.log('🌐 Step6Structure - Making API call to processStep(6, null)');
                const success = await this.$store.wizard.processStep(6, null);
                console.log('🌐 Step6Structure - loadStructureOptions result:', success);

                if (success) {
                    console.log('✅ Step6Structure - API call successful, reloading step data');
                    this.loadStepData();
                } else {
                    console.log('❌ Step6Structure - API call failed, using fallback');
                    this.options = this.getSampleStructures();
                }
            } catch (error) {
                console.error('💥 Step6Structure - Error loading structure options:', error);
                // Fallback to sample data
                console.log('🔄 Step6Structure - Using fallback sample data');
                this.options = this.getSampleStructures();
            }
        },

        // Utility methods
        getOptionById(optionId) {
            const option = this.options.find(option => option.id === optionId);
            console.log('🔍 Step6Structure - getOptionById called with:', optionId, 'found:', option);
            return option;
        },

        getSelectedStructureInfo() {
            const info = this.getOptionById(this.selectedStructure);
            console.log('ℹ️ Step6Structure - getSelectedStructureInfo:', info);
            return info;
        },

        formatRecommendationScore(score) {
            if (!score) return null;
            return `${Math.round(score)}% Match`;
        },

        formatDifficulty(difficulty) {
            const difficultyMap = {
                'easy': 'Easy to Execute',
                'medium': 'Moderate Complexity',
                'hard': 'Advanced Structure'
            };
            return difficultyMap[difficulty] || difficulty;
        },

        // Sample structures for testing/fallback
        getSampleStructures() {
            console.log('📦 Step6Structure - getSampleStructures called');

            const selectedGenre = this.selectedGenre;

            console.log('📦 Step6Structure - getSampleStructures context:', {
                selectedGenre
            });

            // Base structures that work for most genres
            const baseStructures = [
                {
                    id: 'three_act',
                    name: 'Three-Act Structure',
                    description: 'Classic beginning, middle, end with clear turning points',
                    recommendation_score: 85,
                    difficulty: 'easy',
                    commercial_appeal: 'Very High',
                    why_recommended: 'Time-tested structure with proven commercial success'
                },
                {
                    id: 'heros_journey',
                    name: "Hero's Journey",
                    description: 'Character transformation through challenges and growth',
                    recommendation_score: 80,
                    difficulty: 'medium',
                    commercial_appeal: 'High',
                    why_recommended: 'Deeply satisfying character arc that resonates with readers'
                },
                {
                    id: 'save_the_cat',
                    name: 'Save the Cat! Structure',
                    description: '15-beat structure optimized for commercial storytelling',
                    recommendation_score: 90,
                    difficulty: 'easy',
                    commercial_appeal: 'Very High',
                    why_recommended: 'Designed specifically for commercial success'
                }
            ];

            // Genre-specific additional structures
            if (selectedGenre === 'romance') {
                baseStructures.push({
                    id: 'romance_arc',
                    name: 'Romance Beat Sheet',
                    description: 'Specialized structure for romantic relationship development',
                    recommendation_score: 95,
                    difficulty: 'easy',
                    commercial_appeal: 'Excellent',
                    why_recommended: 'Proven formula for romance genre success'
                });
            } else if (selectedGenre === 'mystery') {
                baseStructures.push({
                    id: 'mystery_structure',
                    name: 'Mystery Investigation Arc',
                    description: 'Clue revelation and investigation progression structure',
                    recommendation_score: 92,
                    difficulty: 'medium',
                    commercial_appeal: 'Very High',
                    why_recommended: 'Maintains suspense while satisfying mystery readers'
                });
            }

            console.log('📦 Step6Structure - Generated sample structures:', baseStructures.length, 'options');
            return baseStructures;
        },

        // Styling helpers
        getStructureCardClass(structure) {
            let baseClass = 'p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 ';

            if (this.selectedStructure === structure.id) {
                baseClass += 'border-blue-500 bg-blue-50 shadow-md ';
            } else if (this.hoveredOption === structure.id) {
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

        getDifficultyBadgeClass(difficulty) {
            const classes = {
                'easy': 'bg-green-100 text-green-800',
                'medium': 'bg-yellow-100 text-yellow-800',
                'hard': 'bg-red-100 text-red-800'
            };
            return classes[difficulty] || 'bg-gray-100 text-gray-800';
        },

        // Navigation
        goBack() {
            console.log('⬅️ Step6Structure - goBack called');
            // Go back to step 5 (book length)
            this.$store.wizard.setCurrentStep(5);
        }
    };
}