/**
 * Step 2: Genre Selection Component
 * Enhanced to access stored concept analysis and show LLM recommendations
 */

function step2Genre() {
    return {
        // Data
        selectedGenre: '',
        selectedSubgenre: '',
        showSubgenres: false,
        isSubmitting: false,

        // Step data from API
        options: [],
        subgenreOptions: [],
        llmMessage: '',

        // UI state
        hoveredOption: null,
        showAnalysisDetails: false,

        // Computed properties to access wizard store data (with logging)
        get conceptAnalysis() {
            const analysis = this.$store.wizard.conceptAnalysis;
            console.log('🔍 Step2Genre - Accessing conceptAnalysis:', analysis);
            return analysis;
        },

        get hasConceptAnalysis() {
            const hasAnalysis = this.conceptAnalysis && this.conceptAnalysis.analysis_successful;
            console.log('✅ Step2Genre - hasConceptAnalysis:', hasAnalysis);
            return hasAnalysis;
        },

        get genreRecommendations() {
            const recommendations = this.$store.wizard.getGenreRecommendations();
            console.log('📋 Step2Genre - genreRecommendations:', recommendations);
            console.log('📋 Step2Genre - recommendations count:', recommendations?.length || 0);
            return recommendations;
        },

        get currentStepData() {
            const stepData = this.$store.wizard.currentStepData;
            console.log('📊 Step2Genre - currentStepData:', stepData);
            return stepData;
        },

        get userConcept() {
            const concept = this.$store.wizard.formData.concept;
            console.log('💭 Step2Genre - userConcept:', concept);
            return concept;
        },

        // Existing computed properties
        get hasGenreSelection() {
            return this.selectedGenre !== '';
        },

        get hasSubgenreSelection() {
            return this.selectedSubgenre !== '';
        },

        get canProceed() {
            return this.hasGenreSelection && (!this.showSubgenres || this.hasSubgenreSelection);
        },

        get currentSelection() {
            if (this.showSubgenres && this.hasSubgenreSelection) {
                return this.selectedSubgenre;
            }
            return this.selectedGenre;
        },

        // Enhanced options that combine API data with concept analysis (with logging)
        get enhancedOptions() {
            console.log('🚀 Step2Genre - Building enhancedOptions...');
            console.log('🚀 Step2Genre - hasConceptAnalysis:', this.hasConceptAnalysis);
            console.log('🚀 Step2Genre - genreRecommendations length:', this.genreRecommendations?.length || 0);

            if (this.hasConceptAnalysis && this.genreRecommendations.length > 0) {
                console.log('✨ Step2Genre - Using LLM recommendations');

                // Prioritize LLM recommendations
                const enhancedRecs = this.genreRecommendations.map(rec => {
                    console.log('🎯 Step2Genre - Processing recommendation:', rec);

                    const enhanced = {
                        id: `${rec.genre.value}/${rec.subgenre.value}`,
                        genre_id: rec.genre.value,
                        subgenre_id: rec.subgenre.value,
                        name: rec.display_name || `${rec.genre.display_name} - ${rec.subgenre.display_name}`,
                        description: rec.reasoning || `${rec.genre.display_name} with ${rec.subgenre.display_name} elements`,
                        recommendation_score: Math.round(rec.confidence * 100),
                        market_appeal: this.getMarketAppeal(rec.confidence),
                        source: 'llm_analysis',
                        confidence: rec.confidence,
                        reasoning: rec.reasoning
                    };

                    console.log('🎯 Step2Genre - Enhanced recommendation:', enhanced);
                    return enhanced;
                });

                console.log('✨ Step2Genre - Final enhanced recommendations:', enhancedRecs);
                return enhancedRecs;
            }

            // Fallback to API data or sample data
            console.log('⚠️ Step2Genre - Using fallback options');
            console.log('⚠️ Step2Genre - this.options:', this.options);
            console.log('⚠️ Step2Genre - this.options.length:', this.options.length);

            const fallbackOptions = this.options.length > 0 ? this.options : this.getSampleGenres();
            console.log('⚠️ Step2Genre - Final fallback options:', fallbackOptions);

            return fallbackOptions;
        },

        // Methods (with enhanced logging)
        async selectGenre(optionId) {
            console.log('🎬 Step2Genre - selectGenre called with:', optionId);

            // Handle both genre-only and genre/subgenre combinations
            const option = this.getOptionById(optionId);
            console.log('🎬 Step2Genre - Found option:', option);

            if (option && option.source === 'llm_analysis') {
                console.log('🤖 Step2Genre - Processing LLM recommendation');

                // This is an LLM recommendation with both genre and subgenre
                this.selectedGenre = option.genre_id;
                this.selectedSubgenre = option.subgenre_id;

                console.log('🤖 Step2Genre - Set selectedGenre:', this.selectedGenre);
                console.log('🤖 Step2Genre - Set selectedSubgenre:', this.selectedSubgenre);

                // Update store with both values
                this.$store.wizard.updateFormData('genre', option.genre_id);
                this.$store.wizard.updateFormData('subgenre', option.subgenre_id);

                console.log('🤖 Step2Genre - Updated wizard store formData');
                console.log('🤖 Step2Genre - Current formData:', this.$store.wizard.formData);

                // Process the complete selection
                await this.processCompleteSelection(option);
            } else {
                console.log('🎭 Step2Genre - Processing traditional genre selection');

                // Traditional genre-only selection
                this.selectedGenre = optionId;
                this.selectedSubgenre = ''; // Reset subgenre when genre changes

                console.log('🎭 Step2Genre - Set selectedGenre:', this.selectedGenre);
                console.log('🎭 Step2Genre - Reset selectedSubgenre');

                // Update store
                this.$store.wizard.updateFormData('genre', optionId);
                console.log('🎭 Step2Genre - Updated wizard store with genre:', optionId);

                // Process genre selection and get subgenres
                await this.processGenreSelection();
            }
        },

        async processCompleteSelection(option) {
            console.log('🔥 Step2Genre - processCompleteSelection called with:', option);

            this.isSubmitting = true;

            try {
                const stepData = {
                    session_id: this.$store.wizard.sessionId,
                    selection: `${option.genre_id}/${option.subgenre_id}`,
                    additional_input: `Selected from LLM analysis: ${option.reasoning}`
                };

                console.log('🔥 Step2Genre - Calling processStep with:', stepData);

                const success = await this.$store.wizard.processStep(
                    2,
                    `${option.genre_id}/${option.subgenre_id}`,
                    `Selected from LLM analysis: ${option.reasoning}`
                );

                console.log('🔥 Step2Genre - processStep result:', success);

                if (success) {
                    console.log('🔥 Step2Genre - Processing successful, proceeding to next step');
                    await this.proceedToNextStep();
                } else {
                    console.error('❌ Step2Genre - processStep failed');
                }
            } catch (error) {
                console.error('💥 Step2Genre - Error in processCompleteSelection:', error);
            } finally {
                this.isSubmitting = false;
                console.log('🔥 Step2Genre - processCompleteSelection finished');
            }
        },

        async processGenreSelection() {
            if (!this.selectedGenre) return;

            this.isSubmitting = true;

            try {
                const success = await this.$store.wizard.processStep(
                    2, // Step number
                    this.selectedGenre
                );

                if (success) {
                    // Check if we got subgenre options
                    const stepData = this.currentStepData;

                    if (stepData.options && stepData.options.length > 0) {
                        // We have subgenres to show
                        this.subgenreOptions = stepData.options;
                        this.showSubgenres = true;
                        this.llmMessage = stepData.llmReasoning || 'Now let\'s get more specific with subgenres:';
                    } else {
                        // No subgenres, proceed to next step
                        await this.proceedToNextStep();
                    }
                }
            } catch (error) {
                console.error('Error processing genre selection:', error);
            } finally {
                this.isSubmitting = false;
            }
        },

        async selectSubgenre(subgenreId) {
            this.selectedSubgenre = subgenreId;

            // Update store
            this.$store.wizard.updateFormData('subgenre', subgenreId);

            // Process subgenre selection
            await this.processSubgenreSelection();
        },

        async processSubgenreSelection() {
            if (!this.selectedSubgenre) return;

            this.isSubmitting = true;

            try {
                const success = await this.$store.wizard.processStep(
                    2, // Still step 2, but with subgenre
                    this.selectedSubgenre
                );

                if (success) {
                    await this.proceedToNextStep();
                }
            } catch (error) {
                console.error('Error processing subgenre selection:', error);
            } finally {
                this.isSubmitting = false;
            }
        },

        async proceedToNextStep() {
            // Move to step 3 (target audience)
            this.$store.wizard.setCurrentStep(3);

            // Load step 3 data
            await this.loadTargetAudienceData();
        },

        async loadTargetAudienceData() {
            try {
                const success = await this.$store.wizard.processStep(3, null);
                // Step 3 data will be loaded in the wizard store
            } catch (error) {
                console.error('Error loading target audience data:', error);
            }
        },

        // UI Methods
        getOptionClasses(optionId) {
            const baseClasses = "border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md";
            const selectedClasses = "border-blue-500 bg-blue-50 ring-2 ring-blue-200";
            const recommendedClasses = "border-green-400 bg-green-50";
            const defaultClasses = "border-gray-200 hover:border-gray-300";

            const option = this.getOptionById(optionId);
            const isSelected = this.selectedGenre === optionId ||
                this.selectedSubgenre === optionId ||
                (option && this.selectedGenre === option.genre_id && this.selectedSubgenre === option.subgenre_id);

            if (isSelected) {
                return `${baseClasses} ${selectedClasses}`;
            }

            if (option && option.source === 'llm_analysis') {
                return `${baseClasses} ${recommendedClasses}`;
            }

            return `${baseClasses} ${defaultClasses}`;
        },

        getMarketAppealBadgeClasses(appeal) {
            const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";

            switch (appeal?.toLowerCase()) {
                case 'high':
                    return `${baseClasses} bg-green-100 text-green-800`;
                case 'medium':
                    return `${baseClasses} bg-yellow-100 text-yellow-800`;
                case 'low':
                    return `${baseClasses} bg-gray-100 text-gray-800`;
                default:
                    return `${baseClasses} bg-gray-100 text-gray-600`;
            }
        },

        getMarketAppeal(confidence) {
            if (confidence >= 0.8) return 'High';
            if (confidence >= 0.6) return 'Medium';
            return 'Low';
        },

        onOptionHover(optionId) {
            this.hoveredOption = optionId;
        },

        onOptionLeave() {
            this.hoveredOption = null;
        },

        toggleAnalysisDetails() {
            this.showAnalysisDetails = !this.showAnalysisDetails;
        },

        // Navigation
        goBack() {
            if (this.showSubgenres) {
                // Go back to genre selection
                this.showSubgenres = false;
                this.selectedSubgenre = '';
                this.$store.wizard.updateFormData('subgenre', '');
            } else {
                // Go back to step 1
                this.$store.wizard.setCurrentStep(1);
            }
        },

        // Data loading (with enhanced logging)
        loadStepData() {
            console.log('📥 Step2Genre - loadStepData called');

            const stepData = this.currentStepData;
            console.log('📥 Step2Genre - Retrieved currentStepData:', stepData);

            // Load options from step data or use enhanced options from analysis
            this.options = stepData.options || [];
            console.log('📥 Step2Genre - Set this.options:', this.options);

            // Set LLM message with more context
            if (this.hasConceptAnalysis) {
                const totalRecs = this.genreRecommendations.length;
                console.log('📥 Step2Genre - Has concept analysis, totalRecs:', totalRecs);

                this.llmMessage = stepData.llmReasoning ||
                    `Based on your concept "${this.userConcept?.substring(0, 50)}...", I found ${totalRecs} perfect genre matches:`;
            } else {
                console.log('📥 Step2Genre - No concept analysis available');
                this.llmMessage = stepData.llmReasoning || 'Based on your concept, I recommend these commercial genres:';
            }

            console.log('📥 Step2Genre - Set llmMessage:', this.llmMessage);

            // Load any existing selections
            this.selectedGenre = this.$store.wizard.formData.genre || '';
            this.selectedSubgenre = this.$store.wizard.formData.subgenre || '';

            console.log('📥 Step2Genre - Loaded selectedGenre:', this.selectedGenre);
            console.log('📥 Step2Genre - Loaded selectedSubgenre:', this.selectedSubgenre);
            console.log('📥 Step2Genre - loadStepData completed');
        },

        // Lifecycle (with comprehensive logging)
        init() {
            console.log('🏁 Step2Genre - INIT STARTING');
            console.log('🏁 Step2Genre - Component initialization...');

            // Log wizard store state
            console.log('🏪 Step2Genre - Wizard Store State:');
            console.log('🏪 Step2Genre - currentStep:', this.$store.wizard.currentStep);
            console.log('🏪 Step2Genre - sessionId:', this.$store.wizard.sessionId);
            console.log('🏪 Step2Genre - formData:', this.$store.wizard.formData);
            console.log('🏪 Step2Genre - conceptAnalysis:', this.$store.wizard.conceptAnalysis);
            console.log('🏪 Step2Genre - currentStepData:', this.$store.wizard.currentStepData);

            // Check concept analysis availability
            console.log('🔍 Step2Genre - Checking concept analysis...');
            console.log('🔍 Step2Genre - Has concept analysis:', this.hasConceptAnalysis);
            console.log('🔍 Step2Genre - Genre recommendations:', this.genreRecommendations);
            console.log('🔍 Step2Genre - Genre recommendations count:', this.genreRecommendations?.length || 0);

            // Load step data
            console.log('📥 Step2Genre - Loading step data...');
            this.loadStepData();

            // Check enhanced options
            console.log('🚀 Step2Genre - Checking enhanced options...');
            const enhanced = this.enhancedOptions;
            console.log('🚀 Step2Genre - Enhanced options result:', enhanced);
            console.log('🚀 Step2Genre - Enhanced options count:', enhanced?.length || 0);

            // If we don't have options, load them
            if (this.options.length === 0 && !this.hasConceptAnalysis) {
                console.log('⚠️ Step2Genre - No options and no concept analysis, loading genre options...');
                this.loadGenreOptions();
            } else {
                console.log('✅ Step2Genre - Options available or concept analysis present');
            }

            console.log('🏁 Step2Genre - INIT COMPLETED');
        },

        async loadGenreOptions() {
            console.log('🌐 Step2Genre - loadGenreOptions called');
            console.log('🌐 Step2Genre - Loading genre options from API...');
            // This could call the backend if no analysis is available
        },

        // Utility methods (with logging)
        getOptionById(optionId, optionsList = null) {
            const list = optionsList || this.enhancedOptions;
            const option = list.find(option => option.id === optionId);

            console.log('🔍 Step2Genre - getOptionById called with:', optionId);
            console.log('🔍 Step2Genre - Searching in list:', list);
            console.log('🔍 Step2Genre - Found option:', option);

            return option;
        },

        getSelectedGenreInfo() {
            const info = this.getOptionById(this.selectedGenre);
            console.log('ℹ️ Step2Genre - getSelectedGenreInfo:', info);
            return info;
        },

        getSelectedSubgenreInfo() {
            const info = this.getOptionById(this.selectedSubgenre, this.subgenreOptions);
            console.log('ℹ️ Step2Genre - getSelectedSubgenreInfo:', info);
            return info;
        },

        // Format recommendation score for display
        formatRecommendationScore(score) {
            const formatted = !score ? null : `${Math.round(score)}% Match`;
            console.log('📊 Step2Genre - formatRecommendationScore:', score, '->', formatted);
            return formatted;
        },

        getRecommendationBadge(option) {
            let badge = null;
            if (option.source === 'llm_analysis') {
                badge = {
                    text: 'AI Recommended',
                    classes: 'bg-blue-100 text-blue-800'
                };
            }
            console.log('🏷️ Step2Genre - getRecommendationBadge for option:', option.id, '->', badge);
            return badge;
        },

        // Sample genres for testing (fallback data)
        getSampleGenres() {
            console.log('📋 Step2Genre - getSampleGenres called (fallback data)');

            const samples = [
                {
                    id: 'fantasy',
                    name: 'Fantasy',
                    description: 'Stories with magical elements, mythical creatures, and imaginary worlds',
                    market_appeal: 'High',
                    recommendation_score: 92,
                    source: 'fallback'
                },
                {
                    id: 'romance',
                    name: 'Romance',
                    description: 'Stories focused on romantic relationships and emotional connections',
                    market_appeal: 'High',
                    recommendation_score: 78,
                    source: 'fallback'
                },
                {
                    id: 'mystery',
                    name: 'Mystery',
                    description: 'Stories involving puzzles, crimes, and detective work',
                    market_appeal: 'Medium',
                    recommendation_score: 85,
                    source: 'fallback'
                },
                {
                    id: 'coming_of_age',
                    name: 'Coming of Age',
                    description: 'Stories about personal growth and self-discovery, often featuring young protagonists',
                    market_appeal: 'Medium',
                    recommendation_score: 88,
                    source: 'fallback'
                }
            ];

            console.log('📋 Step2Genre - Returning sample genres:', samples);
            return samples;
        },

        // Debug helpers (enhanced)
        logAnalysisData() {
            console.log('🔧 Step2Genre - DEBUG ANALYSIS DATA:');
            console.log('🔧 Concept Analysis:', this.conceptAnalysis);
            console.log('🔧 Genre Recommendations:', this.genreRecommendations);
            console.log('🔧 Enhanced Options:', this.enhancedOptions);
            console.log('🔧 Current Step Data:', this.currentStepData);
            console.log('🔧 Wizard Store Full State:', this.$store.wizard);
        },

        logWizardState() {
            console.log('🔧 Step2Genre - FULL WIZARD STATE:');
            console.log('🔧 Current Step:', this.$store.wizard.currentStep);
            console.log('🔧 Session ID:', this.$store.wizard.sessionId);
            console.log('🔧 Form Data:', this.$store.wizard.formData);
            console.log('🔧 Concept Analysis:', this.$store.wizard.conceptAnalysis);
            console.log('🔧 Current Step Data:', this.$store.wizard.currentStepData);
            console.log('🔧 Is Loading:', this.$store.wizard.isLoading);
            console.log('🔧 Error:', this.$store.wizard.error);
        }
    };
}