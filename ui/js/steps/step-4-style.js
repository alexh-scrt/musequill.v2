/**
 * Step 4: Writing Style Component
 * Enhanced with LLM data access and comprehensive debug logging
 */

function step4Style() {
    return {
        // Data
        selectedStyle: '',
        isSubmitting: false,

        // Step data from API
        options: [],
        llmMessage: '',

        // UI state
        hoveredOption: null,
        showStyleDetails: false,
        showAnalysisDetails: false,

        // Computed properties to access wizard store data (with logging)
        get conceptAnalysis() {
            const analysis = this.$store.wizard.conceptAnalysis;
            console.log('🔍 Step4Style - Accessing conceptAnalysis:', analysis);
            return analysis;
        },

        get hasConceptAnalysis() {
            const hasAnalysis = this.conceptAnalysis && this.conceptAnalysis.analysis_successful;
            console.log('✅ Step4Style - hasConceptAnalysis:', hasAnalysis);
            return hasAnalysis;
        },

        get currentStepData() {
            const stepData = this.$store.wizard.currentStepData;
            console.log('📊 Step4Style - currentStepData:', stepData);
            return stepData;
        },

        get userConcept() {
            const concept = this.$store.wizard.formData.concept;
            console.log('💭 Step4Style - userConcept:', concept);
            return concept;
        },

        get selectedGenre() {
            const genre = this.$store.wizard.formData.genre;
            console.log('🎭 Step4Style - selectedGenre:', genre);
            return genre;
        },

        get selectedSubgenre() {
            const subgenre = this.$store.wizard.formData.subgenre;
            console.log('🎪 Step4Style - selectedSubgenre:', subgenre);
            return subgenre;
        },

        get selectedAudience() {
            const audience = this.$store.wizard.formData.audience;
            console.log('👥 Step4Style - selectedAudience:', audience);
            return audience;
        },

        // Enhanced options that combine API data with analysis context (with logging)
        get enhancedOptions() {
            console.log('🚀 Step4Style - Building enhancedOptions...');
            console.log('🚀 Step4Style - hasConceptAnalysis:', this.hasConceptAnalysis);
            console.log('🚀 Step4Style - currentStepData.options:', this.currentStepData?.options?.length || 0);
            console.log('🚀 Step4Style - this.options.length:', this.options?.length || 0);

            let baseOptions = [];

            // Use API data if available
            if (this.currentStepData?.options && this.currentStepData.options.length > 0) {
                console.log('✨ Step4Style - Using currentStepData.options');
                baseOptions = this.currentStepData.options;
            } else if (this.options.length > 0) {
                console.log('⚡ Step4Style - Using this.options');
                baseOptions = this.options;
            } else {
                console.log('⚠️ Step4Style - Using fallback sample options');
                baseOptions = this.getSampleStyles();
            }

            console.log('🚀 Step4Style - baseOptions selected:', baseOptions);
            console.log('🚀 Step4Style - baseOptions length:', baseOptions?.length || 0);

            // Enhance options with analysis context
            const enhancedOptions = baseOptions.map((option, index) => {
                console.log(`🎯 Step4Style - Processing option ${index + 1}:`, option);

                const enhanced = {
                    ...option,
                    // Add analysis-based enhancements
                    analysis_context: this.getAnalysisContext(option.id),
                    genre_compatibility: this.getGenreCompatibility(option.id),
                    audience_fit: this.getAudienceFit(option.id),
                    market_insights: this.getMarketInsights(option.id),
                    source: this.currentStepData?.options ? 'api_data' : 'component_fallback'
                };

                console.log(`🎯 Step4Style - Enhanced option ${index + 1}:`, enhanced);
                return enhanced;
            });

            console.log('✨ Step4Style - Final enhanced options:', enhancedOptions);
            console.log('✨ Step4Style - Final enhanced options count:', enhancedOptions?.length || 0);
            return enhancedOptions;
        },

        // Computed
        get hasSelection() {
            const hasSelection = this.selectedStyle !== '';
            console.log('🎯 Step4Style - hasSelection:', hasSelection);
            return hasSelection;
        },

        get canProceed() {
            const canProceed = this.hasSelection;
            console.log('✅ Step4Style - canProceed:', canProceed);
            return canProceed;
        },

        // Methods (with enhanced logging)
        async selectStyle(styleId) {
            console.log('🎬 Step4Style - selectStyle called with:', styleId);

            this.selectedStyle = styleId;
            console.log('🎬 Step4Style - Set selectedStyle:', this.selectedStyle);

            // Update store
            this.$store.wizard.updateFormData('style', styleId);
            console.log('🎬 Step4Style - Updated wizard store formData');
            console.log('🎬 Step4Style - Current formData:', this.$store.wizard.formData);

            // Process style selection
            await this.processStyleSelection();
        },

        async processStyleSelection() {
            console.log('🔥 Step4Style - processStyleSelection called');

            if (!this.selectedStyle) {
                console.log('❌ Step4Style - No style selected, aborting');
                return;
            }

            this.isSubmitting = true;
            console.log('🔥 Step4Style - Set isSubmitting to true');

            try {
                const stepData = {
                    session_id: this.$store.wizard.sessionId,
                    selection: this.selectedStyle,
                    additional_input: this.getSelectionContext()
                };

                console.log('🔥 Step4Style - Calling processStep with:', stepData);

                const success = await this.$store.wizard.processStep(
                    4, // Step number
                    this.selectedStyle,
                    this.getSelectionContext()
                );

                console.log('🔥 Step4Style - processStep result:', success);

                if (success) {
                    console.log('🔥 Step4Style - Processing successful, proceeding to next step');
                    await this.proceedToNextStep();
                } else {
                    console.error('❌ Step4Style - processStep failed');
                }
            } catch (error) {
                console.error('💥 Step4Style - Error in processStyleSelection:', error);
            } finally {
                this.isSubmitting = false;
                console.log('🔥 Step4Style - processStyleSelection finished');
            }
        },

        async proceedToNextStep() {
            console.log('➡️ Step4Style - proceedToNextStep called');

            // Move to step 5 (book length)
            this.$store.wizard.setCurrentStep(5);
            console.log('➡️ Step4Style - Set current step to 5');

            // Load step 5 data
            await this.loadBookLengthData();
        },

        async loadBookLengthData() {
            console.log('🌐 Step4Style - loadBookLengthData called');

            try {
                const success = await this.$store.wizard.processStep(5, null);
                console.log('🌐 Step4Style - loadBookLengthData result:', success);
                // Step 5 data will be loaded in the wizard store
            } catch (error) {
                console.error('💥 Step4Style - Error loading book length data:', error);
            }
        },

        // Enhanced context methods
        getSelectionContext() {
            const context = {
                selected_genre: this.selectedGenre,
                selected_subgenre: this.selectedSubgenre,
                selected_audience: this.selectedAudience,
                concept_summary: this.userConcept?.substring(0, 100),
                has_analysis: this.hasConceptAnalysis
            };

            console.log('📝 Step4Style - getSelectionContext:', context);
            return JSON.stringify(context);
        },

        getAnalysisContext(styleId) {
            if (!this.hasConceptAnalysis) {
                console.log('📝 Step4Style - No analysis context for:', styleId);
                return null;
            }

            // Extract relevant analysis information for this style
            const context = {
                genre_compatibility: this.getGenreCompatibility(styleId),
                audience_fit: this.getAudienceFit(styleId),
                concept_themes: this.extractThemesFromConcept(),
                tone_indicators: this.conceptAnalysis.tone_signals || []
            };

            console.log('📝 Step4Style - Analysis context for', styleId, ':', context);
            return context;
        },

        getGenreCompatibility(styleId) {
            const compatibilityMap = {
                accessible_contemporary: {
                    high: ['romance', 'contemporary', 'young_adult', 'new_adult'],
                    medium: ['mystery', 'thriller', 'fantasy'],
                    low: ['literary_fiction', 'horror']
                },
                literary_commercial: {
                    high: ['literary_fiction', 'historical_fiction', 'contemporary'],
                    medium: ['mystery', 'thriller', 'romance'],
                    low: ['young_adult', 'fantasy']
                },
                genre_specific: {
                    high: ['fantasy', 'science_fiction', 'horror', 'mystery'],
                    medium: ['thriller', 'romance'],
                    low: ['literary_fiction', 'contemporary']
                },
                simple_clear: {
                    high: ['young_adult', 'middle_grade', 'children', 'coming_of_age'],
                    medium: ['contemporary', 'romance'],
                    low: ['literary_fiction', 'complex_genres']
                }
            };

            const compatibility = compatibilityMap[styleId];
            if (!compatibility) return 'medium';

            const selectedGenre = this.selectedGenre?.toLowerCase();
            if (compatibility.high.some(genre => selectedGenre?.includes(genre))) return 'high';
            if (compatibility.medium.some(genre => selectedGenre?.includes(genre))) return 'medium';
            return 'low';
        },

        getAudienceFit(styleId) {
            const audienceFitMap = {
                accessible_contemporary: {
                    high: ['adult', 'young_adult', 'new_adult'],
                    medium: ['middle_grade'],
                    low: ['picture_book', 'early_reader']
                },
                literary_commercial: {
                    high: ['adult'],
                    medium: ['new_adult', 'young_adult'],
                    low: ['middle_grade', 'children']
                },
                simple_clear: {
                    high: ['picture_book', 'early_reader', 'middle_grade'],
                    medium: ['young_adult'],
                    low: ['adult', 'new_adult']
                }
            };

            const fit = audienceFitMap[styleId];
            if (!fit) return 'medium';

            const selectedAudience = this.selectedAudience?.toLowerCase();
            if (fit.high.some(aud => selectedAudience?.includes(aud))) return 'high';
            if (fit.medium.some(aud => selectedAudience?.includes(aud))) return 'medium';
            return 'low';
        },

        getMarketInsights(styleId) {
            const insights = {
                accessible_contemporary: {
                    market_appeal: 'Very High',
                    difficulty: 'Easy',
                    commercial_viability: 'High',
                    publishing_preference: 'Traditional and Self-publishing'
                },
                literary_commercial: {
                    market_appeal: 'High',
                    difficulty: 'Moderate',
                    commercial_viability: 'High',
                    publishing_preference: 'Traditional publishing preferred'
                },
                genre_specific: {
                    market_appeal: 'High',
                    difficulty: 'Moderate',
                    commercial_viability: 'Very High',
                    publishing_preference: 'Genre publishers'
                },
                simple_clear: {
                    market_appeal: 'High',
                    difficulty: 'Easy',
                    commercial_viability: 'High',
                    publishing_preference: 'Educational and trade publishers'
                }
            };

            const insight = insights[styleId] || {};
            console.log('💡 Step4Style - Market insights for', styleId, ':', insight);
            return insight;
        },

        extractThemesFromConcept() {
            if (!this.userConcept) return [];

            const concept = this.userConcept.toLowerCase();
            const themes = [];

            // Simple theme detection based on keywords
            if (concept.includes('love') || concept.includes('romance')) themes.push('Romance');
            if (concept.includes('adventure') || concept.includes('journey')) themes.push('Adventure');
            if (concept.includes('mystery') || concept.includes('detective')) themes.push('Mystery');
            if (concept.includes('magic') || concept.includes('fantasy')) themes.push('Fantasy');
            if (concept.includes('future') || concept.includes('technology')) themes.push('Science Fiction');
            if (concept.includes('child') || concept.includes('young') || concept.includes('bunny')) themes.push('Children/YA');
            if (concept.includes('family') || concept.includes('relationship')) themes.push('Family');

            console.log('🎨 Step4Style - Extracted themes:', themes);
            return themes;
        },

        // UI Methods (with logging)
        getOptionClasses(optionId) {
            const baseClasses = "border rounded-lg p-6 cursor-pointer transition-all duration-200 hover:shadow-md";
            const selectedClasses = "border-blue-500 bg-blue-50 ring-2 ring-blue-200";
            const compatibleClasses = "border-green-400 bg-green-50";
            const defaultClasses = "border-gray-200 hover:border-gray-300";

            const option = this.getOptionById(optionId);
            const isSelected = this.selectedStyle === optionId;
            const compatibility = this.getGenreCompatibility(optionId);

            console.log('🎨 Step4Style - getOptionClasses for', optionId, '- selected:', isSelected, 'compatibility:', compatibility);

            if (isSelected) {
                return `${baseClasses} ${selectedClasses}`;
            }

            if (compatibility === 'high') {
                return `${baseClasses} ${compatibleClasses}`;
            }

            return `${baseClasses} ${defaultClasses}`;
        },

        getComplexityBadgeClasses(complexity) {
            const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";

            switch (complexity?.toLowerCase()) {
                case 'simple':
                case 'easy':
                    return `${baseClasses} bg-green-100 text-green-800`;
                case 'moderate':
                case 'medium':
                    return `${baseClasses} bg-yellow-100 text-yellow-800`;
                case 'complex':
                case 'hard':
                    return `${baseClasses} bg-red-100 text-red-800`;
                default:
                    return `${baseClasses} bg-gray-100 text-gray-600`;
            }
        },

        getCompatibilityBadge(styleId) {
            const genreCompat = this.getGenreCompatibility(styleId);
            const audienceFit = this.getAudienceFit(styleId);

            // Overall compatibility based on both genre and audience
            let overallCompatibility = 'medium';
            if (genreCompat === 'high' && audienceFit === 'high') {
                overallCompatibility = 'high';
            } else if (genreCompat === 'low' || audienceFit === 'low') {
                overallCompatibility = 'low';
            }

            const badges = {
                high: { text: 'Perfect Match', classes: 'bg-green-100 text-green-800' },
                medium: { text: 'Good Match', classes: 'bg-yellow-100 text-yellow-800' },
                low: { text: 'Consider Carefully', classes: 'bg-red-100 text-red-800' }
            };

            const badge = badges[overallCompatibility] || badges.medium;
            console.log('🏷️ Step4Style - getCompatibilityBadge for', styleId, ':', badge);
            return badge;
        },

        onOptionHover(optionId) {
            console.log('🖱️ Step4Style - onOptionHover:', optionId);
            this.hoveredOption = optionId;
        },

        onOptionLeave() {
            console.log('🖱️ Step4Style - onOptionLeave');
            this.hoveredOption = null;
        },

        toggleAnalysisDetails() {
            console.log('🔍 Step4Style - toggleAnalysisDetails');
            this.showAnalysisDetails = !this.showAnalysisDetails;
        },

        toggleStyleDetails() {
            console.log('📖 Step4Style - toggleStyleDetails');
            this.showStyleDetails = !this.showStyleDetails;
        },

        // Data loading (with enhanced logging)
        loadStepData() {
            console.log('📥 Step4Style - loadStepData called');

            const stepData = this.currentStepData;
            console.log('📥 Step4Style - Retrieved currentStepData:', stepData);

            // Load options from step data
            this.options = stepData.options || [];
            console.log('📥 Step4Style - Set this.options:', this.options);
            console.log('📥 Step4Style - Options array length:', this.options.length);

            // CRITICAL: Log the actual content of options array
            if (this.options.length > 0) {
                console.log('🔍 Step4Style - Detailed options analysis:');
                this.options.forEach((option, index) => {
                    console.log(`🔍 Step4Style - Option ${index + 1}:`, {
                        id: option?.id || 'NO_ID',
                        name: option?.name || 'NO_NAME',
                        description: option?.description || 'NO_DESCRIPTION',
                        complete_option: option
                    });
                });
            } else {
                console.log('❌ Step4Style - Options array is empty!');
            }

            // Set LLM message with context
            this.llmMessage = stepData.llmReasoning || this.getDefaultMessage();
            console.log('📥 Step4Style - Set llmMessage:', this.llmMessage);

            // Load any existing selection
            this.selectedStyle = this.$store.wizard.formData.style || '';
            console.log('📥 Step4Style - Loaded selectedStyle:', this.selectedStyle);

            console.log('📥 Step4Style - Final options count:', this.options.length);
            console.log('📥 Step4Style - loadStepData completed');
        },

        getDefaultMessage() {
            const selectedGenre = this.selectedGenre;
            const selectedAudience = this.selectedAudience;
            const message = `For commercial ${selectedGenre || 'your chosen genre'} targeting ${selectedAudience || 'your audience'}, these styles work best:`;
            console.log('💬 Step4Style - getDefaultMessage:', message);
            return message;
        },

        // Lifecycle (with comprehensive logging) - FIXED to prevent premature API calls
        init() {
            console.log('🏁 Step4Style - INIT STARTING');
            console.log('🏁 Step4Style - Component initialization...');

            // Log wizard store state
            console.log('🏪 Step4Style - Wizard Store State:');
            console.log('🏪 Step4Style - currentStep:', this.$store.wizard.currentStep);
            console.log('🏪 Step4Style - sessionId:', this.$store.wizard.sessionId);

            // IMPORTANT: Never make API calls during init()
            // Components are initialized for ALL steps when page loads
            console.log('⚠️ Step4Style - Init should never make API calls');

            // Only load existing data from store
            this.selectedStyle = this.$store.wizard.formData.style || '';
            console.log('📥 Step4Style - Loaded existing selection:', this.selectedStyle);

            // Set up fallback data immediately (no API calls)
            this.options = this.getSampleStyles();
            this.llmMessage = this.getDefaultMessage();
            console.log('📋 Step4Style - Set fallback data');

            // Set up a watcher to load data when we actually reach Step 4
            this.$watch('$store.wizard.currentStep', (newStep, oldStep) => {
                console.log('👀 Step4Style - Step changed from', oldStep, 'to', newStep);
                if (newStep === 4 && oldStep !== 4) {
                    console.log('🎯 Step4Style - Now entering Step 4, loading data...');
                    this.onEnterStep4();
                }
            });

            console.log('🏁 Step4Style - INIT COMPLETED (no API calls)');
        },

        // New method called only when actually entering Step 4
        async onEnterStep4() {
            console.log('🚀 Step4Style - onEnterStep4 called');

            // Check if we have a valid session
            if (!this.$store.wizard.sessionId) {
                console.log('❌ Step4Style - No session ID, keeping fallback data');
                return;
            }

            // Check concept analysis availability
            console.log('🔍 Step4Style - Checking concept analysis...');
            console.log('🔍 Step4Style - Has concept analysis:', this.hasConceptAnalysis);

            // Load current step data from wizard store
            console.log('📥 Step4Style - Loading step data from store...');
            this.loadStepData();

            // Check if we have step data from previous navigation
            if (this.currentStepData?.options && this.currentStepData.options.length > 0) {
                console.log('✅ Step4Style - Found existing step data, using it');
                this.options = this.currentStepData.options;
                this.llmMessage = this.currentStepData.llmReasoning || this.getDefaultMessage();
                return;
            }

            // Only make API call if we don't have options
            console.log('🌐 Step4Style - No step data found, loading from API...');
            await this.loadStyleOptions();
        },

        async loadStyleOptions() {
            console.log('🌐 Step4Style - loadStyleOptions called');

            // Final safety checks
            if (this.$store.wizard.currentStep !== 4) {
                console.log('❌ Step4Style - Not on Step 4, aborting API call');
                return;
            }

            if (!this.$store.wizard.sessionId) {
                console.log('❌ Step4Style - No session ID, aborting API call');
                return;
            }

            try {
                console.log('🌐 Step4Style - Making API call to load options...');
                const success = await this.$store.wizard.processStep(4, null);
                console.log('🌐 Step4Style - API call result:', success);

                if (success) {
                    console.log('🌐 Step4Style - Reloading step data after successful API call');
                    this.loadStepData();
                } else {
                    console.log('⚠️ Step4Style - API call returned false, keeping fallback data');
                }
            } catch (error) {
                console.error('💥 Step4Style - Error loading style options:', error);
                console.log('⚠️ Step4Style - Keeping fallback sample data due to error');
                // Keep existing fallback data, don't overwrite
            }
        },

        // Utility methods (with logging)
        getOptionById(optionId) {
            const option = this.enhancedOptions.find(option => option.id === optionId);
            console.log('🔍 Step4Style - getOptionById called with:', optionId);
            console.log('🔍 Step4Style - Found option:', option);
            return option;
        },

        getSelectedStyleInfo() {
            const info = this.getOptionById(this.selectedStyle);
            console.log('ℹ️ Step4Style - getSelectedStyleInfo:', info);
            return info;
        },

        formatRecommendationScore(score) {
            const formatted = !score ? null : `${Math.round(score)}% Match`;
            console.log('📊 Step4Style - formatRecommendationScore:', score, '->', formatted);
            return formatted;
        },

        // Sample styles for testing/fallback
        getSampleStyles() {
            console.log('📋 Step4Style - getSampleStyles called (fallback data)');
            const selectedGenre = this.selectedGenre;
            const selectedAudience = this.selectedAudience;
            console.log('📋 Step4Style - selectedGenre for samples:', selectedGenre);
            console.log('📋 Step4Style - selectedAudience for samples:', selectedAudience);

            // Base styles that work for most combinations
            const styles = [
                {
                    id: 'accessible_contemporary',
                    name: 'Accessible Contemporary',
                    description: 'Clear, modern prose that\'s easy to read and commercially appealing',
                    characteristics: ['Clear language', 'Modern voice', 'Broad appeal'],
                    complexity: 'Simple',
                    market_appeal: 'High',
                    recommendation_score: 88,
                    example: '"Sarah stepped into the coffee shop, the familiar aroma of espresso wrapping around her like a warm hug."',
                    source: 'fallback'
                },
                {
                    id: 'simple_clear',
                    name: 'Simple & Clear',
                    description: 'Perfect for children\'s books and bunny adventures! Easy to read and understand',
                    characteristics: ['Very simple language', 'Child-friendly', 'Easy comprehension'],
                    complexity: 'Simple',
                    market_appeal: 'High',
                    recommendation_score: 95, // High for bunny story
                    example: '"The little bunny hopped through the tall grass. She was looking for her way home."',
                    source: 'fallback'
                },
                {
                    id: 'literary_commercial',
                    name: 'Literary Commercial',
                    description: 'Elevated prose with commercial appeal, balancing artistry with readability',
                    characteristics: ['Sophisticated language', 'Character-driven', 'Literary merit'],
                    complexity: 'Moderate',
                    market_appeal: 'High',
                    recommendation_score: 75,
                    example: '"The city breathed around her, its pulse a symphony of car horns and distant conversations."',
                    source: 'fallback'
                },
                {
                    id: 'genre_specific',
                    name: 'Genre-Specific',
                    description: 'Tailored to your chosen genre with specialized language and conventions',
                    characteristics: ['Genre conventions', 'Target reader expectations', 'Market-tested'],
                    complexity: 'Moderate',
                    market_appeal: 'Very High',
                    recommendation_score: 82,
                    example: '"The ancient magic stirred within her, responding to the call of the forest spirits."',
                    source: 'fallback'
                }
            ];

            console.log('📋 Step4Style - Returning sample styles:', styles);
            return styles;
        },

        // Navigation
        goBack() {
            console.log('⬅️ Step4Style - goBack called');
            this.$store.wizard.setCurrentStep(3);
        },

        // Debug helpers (enhanced)
        logAnalysisData() {
            console.log('🔧 Step4Style - DEBUG ANALYSIS DATA:');
            console.log('🔧 Concept Analysis:', this.conceptAnalysis);
            console.log('🔧 Current Step Data:', this.currentStepData);
            console.log('🔧 Enhanced Options:', this.enhancedOptions);
            console.log('🔧 Selected Genre:', this.selectedGenre);
            console.log('🔧 Selected Subgenre:', this.selectedSubgenre);
            console.log('🔧 Selected Audience:', this.selectedAudience);
            console.log('🔧 Wizard Store Full State:', this.$store.wizard);
        },

        logNavigationState() {
            console.log('🧭 Step4Style - NAVIGATION DEBUG:');
            console.log('🧭 Current Step:', this.$store.wizard.currentStep);
            console.log('🧭 Selected Style:', this.selectedStyle);
            console.log('🧭 Has Selection:', this.hasSelection);
            console.log('🧭 Can Proceed:', this.canProceed);
            console.log('🧭 Is Submitting:', this.isSubmitting);
            console.log('🧭 Available Options Count:', this.enhancedOptions?.length || 0);
            console.log('🧭 Form Data:', this.$store.wizard.formData);

            // Check if wizard thinks we can proceed
            console.log('🧭 Wizard canProceed():', this.$store.wizard.canProceed());

            // Check enhanced options
            if (this.enhancedOptions && this.enhancedOptions.length > 0) {
                console.log('🧭 Available style options:');
                this.enhancedOptions.forEach((option, index) => {
                    console.log(`🧭   ${index + 1}. ${option.id} - ${option.name} (score: ${option.recommendation_score})`);
                });
            }
        },

        testSelection(styleId) {
            console.log('🧪 Step4Style - Testing selection:', styleId);
            console.log('🧪 Before - hasSelection:', this.hasSelection);
            console.log('🧪 Before - canProceed:', this.canProceed);

            this.selectedStyle = styleId;
            this.$store.wizard.updateFormData('style', styleId);

            console.log('🧪 After - selectedStyle:', this.selectedStyle);
            console.log('🧪 After - hasSelection:', this.hasSelection);
            console.log('🧪 After - canProceed:', this.canProceed);
            console.log('🧪 Wizard canProceed():', this.$store.wizard.canProceed());
        }
    };
}