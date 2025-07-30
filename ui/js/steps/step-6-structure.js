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

        // Computed
        get hasSelection() {
            return this.selectedStructure !== '';
        },

        get canProceed() {
            return this.hasSelection;
        },

        // Methods
        async selectStructure(structureId) {
            this.selectedStructure = structureId;

            // Update store
            this.$store.wizard.updateFormData('structure', structureId);

            // Process structure selection
            await this.processStructureSelection();
        },

        async processStructureSelection() {
            if (!this.selectedStructure) return;

            this.isSubmitting = true;

            try {
                const success = await this.$store.wizard.processStep(
                    6, // Step number
                    this.selectedStructure
                );

                if (success) {
                    await this.proceedToNextStep();
                }
            } catch (error) {
                console.error('Error processing structure selection:', error);
            } finally {
                this.isSubmitting = false;
            }
        },

        async proceedToNextStep() {
            // Move to step 7 (world building)
            this.$store.wizard.setCurrentStep(7);

            // Load step 7 data
            await this.loadWorldBuildingData();
        },

        async loadWorldBuildingData() {
            try {
                const success = await this.$store.wizard.processStep(7, null);
                // Step 7 data will be loaded automatically through the store
            } catch (error) {
                console.error('Error loading world building data:', error);
            }
        },

        // Data loading
        loadStepData() {
            const stepData = this.$store.wizard.currentStepData;

            this.options = stepData.options || [];
            this.llmMessage = stepData.llmReasoning || this.getDefaultMessage();

            // Load any existing selection
            this.selectedStructure = this.$store.wizard.formData.structure || '';
        },

        getDefaultMessage() {
            const selectedGenre = this.$store.wizard.formData.genre;
            return `These proven structures work excellently for ${selectedGenre || 'your chosen genre'} books:`;
        },

        // Navigation
        goBack() {
            // Go back to step 5 (book length)
            this.$store.wizard.setCurrentStep(5);
        },

        // Lifecycle
        init() {
            this.loadStepData();

            // If we don't have step data, load it
            if (this.options.length === 0 || !this.options[0].id) {
                this.loadStructureOptions();
            }
        },

        async loadStructureOptions() {
            // Load options based on current selections
            try {
                const success = await this.$store.wizard.processStep(6, null);
                if (success) {
                    this.loadStepData();
                }
            } catch (error) {
                console.error('Error loading structure options:', error);
                // Fallback to sample data
                this.options = this.getSampleStructures();
            }
        },

        // Utility methods
        getOptionById(optionId) {
            return this.options.find(option => option.id === optionId);
        },

        getSelectedStructureInfo() {
            return this.getOptionById(this.selectedStructure);
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
            const selectedGenre = this.$store.wizard.formData.genre;

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
        }
    };
}