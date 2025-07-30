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

        // Computed
        get hasSelection() {
            return this.selectedWorld !== '';
        },

        get canProceed() {
            return this.hasSelection;
        },

        // Methods
        async selectWorld(worldId) {
            this.selectedWorld = worldId;

            // Update store
            this.$store.wizard.updateFormData('world', worldId);

            // Process world selection
            await this.processWorldSelection();
        },

        async processWorldSelection() {
            if (!this.selectedWorld) return;

            this.isSubmitting = true;

            try {
                const success = await this.$store.wizard.processStep(
                    7, // Step number
                    this.selectedWorld
                );

                if (success) {
                    await this.proceedToNextStep();
                }
            } catch (error) {
                console.error('Error processing world selection:', error);
            } finally {
                this.isSubmitting = false;
            }
        },

        async proceedToNextStep() {
            // Move to step 8 (content preferences)
            this.$store.wizard.setCurrentStep(8);

            // Load step 8 data
            await this.loadContentPreferencesData();
        },

        async loadContentPreferencesData() {
            try {
                const success = await this.$store.wizard.processStep(8, null);
                // Step 8 data will be loaded automatically through the store
            } catch (error) {
                console.error('Error loading content preferences data:', error);
            }
        },

        // Data loading
        loadStepData() {
            const stepData = this.$store.wizard.currentStepData;

            this.options = stepData.options || [];
            this.llmMessage = stepData.llmReasoning || this.getDefaultMessage();

            // Load any existing selection
            this.selectedWorld = this.$store.wizard.formData.world || '';
        },

        getDefaultMessage() {
            const selectedGenre = this.$store.wizard.formData.genre;
            return `For your ${selectedGenre || 'chosen genre'} story, these settings offer commercial appeal:`;
        },

        // Navigation
        goBack() {
            // Go back to step 6 (story structure)
            this.$store.wizard.setCurrentStep(6);
        },

        // Lifecycle
        init() {
            this.loadStepData();

            // If we don't have step data, load it
            if (this.options.length === 0 || !this.options[0].id) {
                this.loadWorldOptions();
            }
        },

        async loadWorldOptions() {
            // Load options based on current selections
            try {
                const success = await this.$store.wizard.processStep(7, null);
                if (success) {
                    this.loadStepData();
                }
            } catch (error) {
                console.error('Error loading world options:', error);
                // Fallback to sample data
                this.options = this.getSampleWorlds();
            }
        },

        // Utility methods
        getOptionById(optionId) {
            return this.options.find(option => option.id === optionId);
        },

        getSelectedWorldInfo() {
            return this.getOptionById(this.selectedWorld);
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
            const selectedGenre = this.$store.wizard.formData.genre;

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
                    why_recommended: 'Combines familiar setting with fantasy elements'
                });
            } else if (selectedGenre === 'romance') {
                baseWorlds.push({
                    id: 'workplace',
                    name: 'Workplace Setting',
                    description: 'Professional environments like offices, hospitals, schools',
                    recommendation_score: 85,
                    research_complexity: 'low',
                    commercial_appeal: 'Very High',
                    why_recommended: 'Built-in conflict and forced proximity'
                });
                baseWorlds.push({
                    id: 'vacation_destination',
                    name: 'Vacation/Resort Setting',
                    description: 'Romantic locations like beaches, mountains, or exotic destinations',
                    recommendation_score: 82,
                    research_complexity: 'medium',
                    commercial_appeal: 'High',
                    why_recommended: 'Inherently romantic atmosphere'
                });
            } else if (selectedGenre === 'mystery') {
                baseWorlds.push({
                    id: 'closed_community',
                    name: 'Closed Community',
                    description: 'Isolated settings like islands, boarding schools, or gated communities',
                    recommendation_score: 92,
                    research_complexity: 'low',
                    commercial_appeal: 'Excellent',
                    why_recommended: 'Limited suspects and heightened tension'
                });
                baseWorlds.push({
                    id: 'institutional',
                    name: 'Institutional Setting',
                    description: 'Police departments, law firms, or other professional institutions',
                    recommendation_score: 80,
                    research_complexity: 'medium',
                    commercial_appeal: 'High',
                    why_recommended: 'Built-in expertise and procedural elements'
                });
            } else if (selectedGenre === 'science_fiction') {
                baseWorlds.push({
                    id: 'near_future',
                    name: 'Near Future Earth',
                    description: 'Earth 20-50 years in the future with recognizable technology',
                    recommendation_score: 85,
                    research_complexity: 'medium',
                    commercial_appeal: 'High',
                    why_recommended: 'Accessible to general readers'
                });
                baseWorlds.push({
                    id: 'space_station',
                    name: 'Space Station/Ship',
                    description: 'Contained space environments with clear boundaries',
                    recommendation_score: 78,
                    research_complexity: 'medium',
                    commercial_appeal: 'Good',
                    why_recommended: 'Controlled environment for storytelling'
                });
            }

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

        getResearchBadgeClass(complexity) {
            const classes = {
                'low': 'bg-green-100 text-green-800',
                'medium': 'bg-yellow-100 text-yellow-800',
                'high': 'bg-red-100 text-red-800'
            };
            return classes[complexity] || 'bg-gray-100 text-gray-800';
        }
    };
}