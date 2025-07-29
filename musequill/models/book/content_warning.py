from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
import json
from datetime import datetime


class ContentWarning(str, Enum):
    """Content warnings for sensitive material in books."""
    
    # Violence & Harm
    MILD_VIOLENCE = "mild_violence"
    VIOLENCE = "violence"
    EXTREME_VIOLENCE = "extreme_violence"
    GRAPHIC_VIOLENCE = "graphic_violence"
    GORE = "gore"
    TORTURE = "torture"
    DOMESTIC_VIOLENCE = "domestic_violence"
    CHILD_ABUSE = "child_abuse"
    SEXUAL_VIOLENCE = "sexual_violence"
    WAR_VIOLENCE = "war_violence"
    ANIMAL_CRUELTY = "animal_cruelty"
    
    # Sexual Content
    SEXUAL_CONTENT = "sexual_content"
    EXPLICIT_SEXUAL_CONTENT = "explicit_sexual_content"
    SEXUAL_ASSAULT = "sexual_assault"
    NON_CONSENSUAL_CONTENT = "non_consensual_content"
    UNDERAGE_SEXUAL_CONTENT = "underage_sexual_content"
    
    # Mental Health & Self-Harm
    MENTAL_HEALTH = "mental_health"
    DEPRESSION = "depression"
    ANXIETY = "anxiety"
    SUICIDE = "suicide"
    SUICIDAL_IDEATION = "suicidal_ideation"
    SELF_HARM = "self_harm"
    PANIC_ATTACKS = "panic_attacks"
    PSYCHOSIS = "psychosis"
    EATING_DISORDERS = "eating_disorders"
    BODY_DYSMORPHIA = "body_dysmorphia"
    
    # Substance Use
    SUBSTANCE_ABUSE = "substance_abuse"
    DRUG_USE = "drug_use"
    ALCOHOL_ABUSE = "alcohol_abuse"
    ADDICTION = "addiction"
    OVERDOSE = "overdose"
    
    # Language & Behavior
    MILD_LANGUAGE = "mild_language"
    LANGUAGE = "language"
    STRONG_LANGUAGE = "strong_language"
    HATE_SPEECH = "hate_speech"
    SLURS = "slurs"
    BULLYING = "bullying"
    HARASSMENT = "harassment"
    
    # Death & Loss
    DEATH = "death"
    GRAPHIC_DEATH = "graphic_death"
    MURDER = "murder"
    GENOCIDE = "genocide"
    MASS_CASUALTIES = "mass_casualties"
    GRIEF = "grief"
    TERMINAL_ILLNESS = "terminal_illness"
    
    # Trauma & PTSD
    TRAUMA = "trauma"
    PTSD = "ptsd"
    FLASHBACKS = "flashbacks"
    MEDICAL_TRAUMA = "medical_trauma"
    CHILDHOOD_TRAUMA = "childhood_trauma"
    
    # Discrimination & Social Issues
    DISCRIMINATION = "discrimination"
    RACISM = "racism"
    SEXISM = "sexism"
    HOMOPHOBIA = "homophobia"
    TRANSPHOBIA = "transphobia"
    ABLEISM = "ableism"
    RELIGIOUS_DISCRIMINATION = "religious_discrimination"
    CLASSISM = "classism"
    
    # Sensitive Topics
    RELIGIOUS_CONTENT = "religious_content"
    BLASPHEMY = "blasphemy"
    RELIGIOUS_EXTREMISM = "religious_extremism"
    POLITICAL_CONTENT = "political_content"
    POLITICAL_EXTREMISM = "political_extremism"
    PROPAGANDA = "propaganda"
    
    # Horror & Disturbing Content
    HORROR_ELEMENTS = "horror_elements"
    PSYCHOLOGICAL_HORROR = "psychological_horror"
    BODY_HORROR = "body_horror"
    SUPERNATURAL_HORROR = "supernatural_horror"
    DISTURBING_IMAGERY = "disturbing_imagery"
    JUMP_SCARES = "jump_scares"
    
    # Medical & Health
    MEDICAL_CONTENT = "medical_content"
    GRAPHIC_MEDICAL_PROCEDURES = "graphic_medical_procedures"
    PANDEMIC = "pandemic"
    DISEASE = "disease"
    DISABILITY = "disability"
    
    # Family & Relationships
    FAMILY_DYSFUNCTION = "family_dysfunction"
    DIVORCE = "divorce"
    ABANDONMENT = "abandonment"
    INFIDELITY = "infidelity"
    TOXIC_RELATIONSHIPS = "toxic_relationships"
    
    # Specific Phobias & Triggers
    CLAUSTROPHOBIA = "claustrophobia"
    AGORAPHOBIA = "agoraphobia"
    DROWNING = "drowning"
    FIRE = "fire"
    INSECTS_SPIDERS = "insects_spiders"
    BLOOD = "blood"
    NEEDLES = "needles"
    
    # Age-Specific Warnings
    MATURE_THEMES = "mature_themes"
    ADULT_CONTENT = "adult_content"
    NOT_SUITABLE_FOR_CHILDREN = "not_suitable_for_children"

    # Crime
    CRIME = "crime"
    CRIME_INVESTIGATION = "crime_investigation"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        names = {
            # Violence & Harm
            self.MILD_VIOLENCE: "Mild Violence",
            self.VIOLENCE: "Violence",
            self.EXTREME_VIOLENCE: "Extreme Violence",
            self.GRAPHIC_VIOLENCE: "Graphic Violence",
            self.GORE: "Gore",
            self.TORTURE: "Torture",
            self.DOMESTIC_VIOLENCE: "Domestic Violence",
            self.CHILD_ABUSE: "Child Abuse",
            self.SEXUAL_VIOLENCE: "Sexual Violence",
            self.WAR_VIOLENCE: "War Violence",
            self.ANIMAL_CRUELTY: "Animal Cruelty",
            
            # Sexual Content
            self.SEXUAL_CONTENT: "Sexual Content",
            self.EXPLICIT_SEXUAL_CONTENT: "Explicit Sexual Content",
            self.SEXUAL_ASSAULT: "Sexual Assault",
            self.NON_CONSENSUAL_CONTENT: "Non-Consensual Content",
            self.UNDERAGE_SEXUAL_CONTENT: "Underage Sexual Content",
            
            # Mental Health & Self-Harm
            self.MENTAL_HEALTH: "Mental Health Issues",
            self.DEPRESSION: "Depression",
            self.ANXIETY: "Anxiety",
            self.SUICIDE: "Suicide",
            self.SUICIDAL_IDEATION: "Suicidal Ideation",
            self.SELF_HARM: "Self-Harm",
            self.PANIC_ATTACKS: "Panic Attacks",
            self.PSYCHOSIS: "Psychosis",
            self.EATING_DISORDERS: "Eating Disorders",
            self.BODY_DYSMORPHIA: "Body Dysmorphia",
            
            # Substance Use
            self.SUBSTANCE_ABUSE: "Substance Abuse",
            self.DRUG_USE: "Drug Use",
            self.ALCOHOL_ABUSE: "Alcohol Abuse",
            self.ADDICTION: "Addiction",
            self.OVERDOSE: "Overdose",
            
            # Language & Behavior
            self.MILD_LANGUAGE: "Mild Language",
            self.LANGUAGE: "Language",
            self.STRONG_LANGUAGE: "Strong Language",
            self.HATE_SPEECH: "Hate Speech",
            self.SLURS: "Slurs",
            self.BULLYING: "Bullying",
            self.HARASSMENT: "Harassment",
            
            # Death & Loss
            self.DEATH: "Death",
            self.GRAPHIC_DEATH: "Graphic Death",
            self.MURDER: "Murder",
            self.GENOCIDE: "Genocide",
            self.MASS_CASUALTIES: "Mass Casualties",
            self.GRIEF: "Grief",
            self.TERMINAL_ILLNESS: "Terminal Illness",
            
            # Trauma & PTSD
            self.TRAUMA: "Trauma",
            self.PTSD: "PTSD",
            self.FLASHBACKS: "Flashbacks",
            self.MEDICAL_TRAUMA: "Medical Trauma",
            self.CHILDHOOD_TRAUMA: "Childhood Trauma",
            
            # Discrimination & Social Issues
            self.DISCRIMINATION: "Discrimination",
            self.RACISM: "Racism",
            self.SEXISM: "Sexism",
            self.HOMOPHOBIA: "Homophobia",
            self.TRANSPHOBIA: "Transphobia",
            self.ABLEISM: "Ableism",
            self.RELIGIOUS_DISCRIMINATION: "Religious Discrimination",
            self.CLASSISM: "Classism",
            
            # Sensitive Topics
            self.RELIGIOUS_CONTENT: "Religious Content",
            self.BLASPHEMY: "Blasphemy",
            self.RELIGIOUS_EXTREMISM: "Religious Extremism",
            self.POLITICAL_CONTENT: "Political Content",
            self.POLITICAL_EXTREMISM: "Political Extremism",
            self.PROPAGANDA: "Propaganda",
            
            # Horror & Disturbing Content
            self.HORROR_ELEMENTS: "Horror Elements",
            self.PSYCHOLOGICAL_HORROR: "Psychological Horror",
            self.BODY_HORROR: "Body Horror",
            self.SUPERNATURAL_HORROR: "Supernatural Horror",
            self.DISTURBING_IMAGERY: "Disturbing Imagery",
            self.JUMP_SCARES: "Jump Scares",
            
            # Medical & Health
            self.MEDICAL_CONTENT: "Medical Content",
            self.GRAPHIC_MEDICAL_PROCEDURES: "Graphic Medical Procedures",
            self.PANDEMIC: "Pandemic",
            self.DISEASE: "Disease",
            self.DISABILITY: "Disability",
            
            # Family & Relationships
            self.FAMILY_DYSFUNCTION: "Family Dysfunction",
            self.DIVORCE: "Divorce",
            self.ABANDONMENT: "Abandonment",
            self.INFIDELITY: "Infidelity",
            self.TOXIC_RELATIONSHIPS: "Toxic Relationships",
            
            # Specific Phobias & Triggers
            self.CLAUSTROPHOBIA: "Claustrophobia Triggers",
            self.AGORAPHOBIA: "Agoraphobia Triggers",
            self.DROWNING: "Drowning",
            self.FIRE: "Fire",
            self.INSECTS_SPIDERS: "Insects/Spiders",
            self.BLOOD: "Blood",
            self.NEEDLES: "Needles",
            
            # Age-Specific Warnings
            self.MATURE_THEMES: "Mature Themes",
            self.ADULT_CONTENT: "Adult Content",
            self.NOT_SUITABLE_FOR_CHILDREN: "Not Suitable for Children",

            # Crime
            self.CRIME: "Crime",
            self.CRIME_INVESTIGATION: "Crime Investigation",
        }
        return names.get(self, self.value.replace("_", " ").title())
    
    @property
    def description(self) -> str:
        """Detailed description of the content warning."""
        descriptions = {
            self.MILD_VIOLENCE: "Contains scenes of minor confrontations, verbal arguments, mild physical altercations like pushing or shoving, or non-serious aggressive behavior without lasting harm or severe injury.",
            self.VIOLENCE: "Contains scenes of physical altercations, fights, combat situations, or aggressive behavior that may result in injury, including punching, kicking, weapon use, or other forms of intentional harm.",
            self.EXTREME_VIOLENCE: "Contains intensely disturbing and brutal depictions of violence including severe beatings, mass casualties, war crimes, torture, or sadistic behavior with detailed descriptions of extreme suffering.",
            self.GRAPHIC_VIOLENCE: "Contains explicit, detailed descriptions of violent acts including specific injuries, wounds, blood loss, and the physical consequences of violence with vivid depictions of pain and bodily harm.",
            self.GORE: "Contains graphic descriptions of blood, open wounds, dismemberment, mutilation, internal organs, severe bodily trauma, or other disturbing imagery involving bodily injuries and decomposition.",
            self.SEXUAL_CONTENT: "Contains sexual themes, romantic intimacy, sexual situations, discussions of sexuality, intimate physical contact, or romantic relationships with sexual undertones or implications.",
            self.EXPLICIT_SEXUAL_CONTENT: "Contains graphic, detailed descriptions of sexual acts, sexual anatomy, intimate physical encounters, explicit sexual language, or pornographic content with vivid sexual imagery.",
            self.MILD_LANGUAGE: "Contains occasional use of mild profanity, teenage slang, casual swearing, or language that might be considered inappropriate in formal settings but commonly used among young adults.",
            self.LANGUAGE: "Contains moderate profanity, crude language, sexual innuendos, inappropriate jokes, offensive slang, or language that some readers might find distasteful or unsuitable for younger audiences.",
            self.STRONG_LANGUAGE: "Contains frequent use of profanity, crude sexual language, blasphemy, extremely offensive terminology, strong expletives, vulgar expressions, or language used in anger or for emphasis.",
            self.SUBSTANCE_ABUSE: "Depicts problematic use of drugs, alcohol, or other substances including addiction, overdose, withdrawal symptoms, illegal drug use, and the negative consequences on individuals and families.",
            self.MENTAL_HEALTH: "Addresses various mental health conditions, psychological disorders, therapy sessions, psychiatric treatment, medication, or the impact of mental illness on daily life and relationships.",
            self.SUICIDE: "Contains depictions of suicide attempts, completed suicide, suicidal planning, methods of self-harm with intent to die, or detailed discussions of characters taking their own lives.",
            self.SELF_HARM: "Depicts deliberate self-injury such as cutting, burning, hitting oneself, or other forms of intentional physical harm without suicidal intent, including descriptions of self-harm methods and resulting injuries.",
            self.DEATH: "Contains character deaths from various causes including natural death, accidents, violence, or illness, along with discussions of mortality, funerals, or the emotional impact of loss on survivors.",
            self.TRAUMA: "Depicts traumatic experiences and their lasting psychological effects including flashbacks, emotional triggers, avoidance behaviors, difficulty functioning, or the long-term impact of distressing events.",
            self.DISCRIMINATION: "Contains depictions of unfair treatment, prejudice, or bias based on race, gender, religion, sexuality, disability, or other characteristics, including systemic inequalities and their social impact.",
            self.RELIGIOUS_CONTENT: "Contains religious themes, spiritual practices, discussions of faith, religious ceremonies, conflicts between belief systems, detailed religious doctrine, or challenges to religious beliefs.",
            self.POLITICAL_CONTENT: "Contains political themes, ideologies, government criticism, election processes, commentary on political systems, partisan viewpoints, or discussions of controversial political topics.",
            self.HORROR_ELEMENTS: "Contains scary, frightening, or suspenseful content designed to create fear, dread, or unease including supernatural threats, monsters, psychological terror, or disturbing scenarios.",
            self.DOMESTIC_VIOLENCE: "Depicts violence, abuse, or threatening behavior within family relationships, romantic partnerships, or household settings including physical, emotional, psychological, or economic abuse.",
            self.EATING_DISORDERS: "Addresses disordered eating behaviors including anorexia, bulimia, binge eating, unhealthy relationships with food, body image issues, weight obsession, or related compulsive behaviors.",
            self.CHILD_ABUSE: "Contains depictions of physical, emotional, sexual, or psychological abuse directed toward minors including neglect, exploitation, or other forms of harm inflicted by adults or authority figures.",
            self.SEXUAL_ASSAULT: "Contains depictions of non-consensual sexual contact, rape, sexual coercion, attempted sexual assault, or the psychological aftermath and trauma experienced by survivors of sexual violence.",
            self.RACISM: "Contains racist attitudes, language, behaviors, racial slurs, stereotypes, systematic discrimination based on race or ethnicity, or depictions of historical or contemporary racist incidents.",
            self.HOMOPHOBIA: "Contains anti-LGBTQ+ attitudes, discriminatory language or behaviors, prejudice against lesbian, gay, bisexual, transgender, or queer individuals, including hate crimes or social rejection.",
            self.DEPRESSION: "Depicts characters experiencing persistent sadness, hopelessness, loss of interest in activities, fatigue, or other symptoms of clinical depression including discussions of treatment and medication.",
            self.ANXIETY: "Contains depictions of excessive worry, fear, social anxiety, generalized anxiety disorder, phobias, panic symptoms, or anxiety's impact on daily functioning and relationships.",
            self.ADDICTION: "Explores themes of physical or psychological dependence on substances, activities, or behaviors including detailed descriptions of addictive cycles, withdrawal, relapse, and recovery processes.",
            self.GRIEF: "Deals with the emotional process of mourning, bereavement, and coping with loss including detailed descriptions of grief stages, memorial services, and the long-term impact of losing loved ones.",
            self.MEDICAL_TRAUMA: "Contains traumatic medical experiences including painful procedures, medical emergencies, surgical complications, hospital stays, or negative healthcare experiences that result in psychological trauma.",
            self.BODY_HORROR: "Contains disturbing transformations, mutations, violations of the human body, graphic descriptions of bodily distortion, infection, disease, or unnatural physical changes and deformities.",
            self.PSYCHOLOGICAL_HORROR: "Uses psychological fear, mental manipulation, and emotional terror including mind games, gaslighting, characters questioning their sanity, or terror arising from mental disturbance.",
            self.HATE_SPEECH: "Contains language specifically intended to demean, threaten, or incite violence against individuals or groups based on race, religion, gender, sexual orientation, or other protected characteristics.",
            self.BULLYING: "Depicts systematic harassment, intimidation, abuse of power, cyberbullying, workplace harassment, school bullying, social exclusion, or the psychological effects of persistent targeted abuse.",
            self.TOXIC_RELATIONSHIPS: "Portrays unhealthy relationship dynamics including emotional manipulation, control, jealousy, psychological abuse, codependency, or damaging patterns between romantic partners, friends, or family.",
            self.TERMINAL_ILLNESS: "Addresses fatal diseases, degenerative conditions, end-of-life care, characters facing death from illness, discussions of medical treatment, hospice care, or preparations for death.",
            self.FLASHBACKS: "Contains scenes where characters re-experience traumatic events through vivid, involuntary memories including detailed descriptions of the original trauma and its ongoing psychological impact.",
            self.PANIC_ATTACKS: "Depicts panic attacks and severe anxiety episodes including physical symptoms like rapid heartbeat, sweating, trembling, difficulty breathing, and feelings of impending doom or loss of control.",
            self.ABANDONMENT: "Explores themes of being left behind, rejected, or deserted by loved ones including children abandoned by parents, partners leaving relationships, or emotional abandonment and its lasting effects.",
            self.FAMILY_DYSFUNCTION: "Depicts unhealthy family dynamics including emotional abuse, neglect, manipulation, toxic relationships between family members, generational trauma, family secrets, or dysfunctional communication patterns.",
            self.CRIME: "Depicts scenes of criminal activities including theft, fraud, smuggling, organized crime, violent crimes, criminal organizations, heists, or interactions with the criminal justice system.",
            self.CRIME_INVESTIGATION: "Contains detailed depictions of police work, detective investigations, forensic procedures, criminal justice processes, crime scene analysis, interrogations, or legal proceedings related to criminal cases.",
            self.TORTURE: "Contains scenes of deliberate infliction of severe pain or suffering for punishment, coercion, intimidation, or sadistic pleasure, including physical, psychological, or emotional torture methods and their effects on victims.",
            self.SEXUAL_VIOLENCE: "Contains depictions of violence with sexual motivations, sexual coercion through force or threats, or acts of violence specifically targeting victims because of their gender or sexuality.",
            self.WAR_VIOLENCE: "Contains depictions of military combat, battlefield injuries, civilian casualties, war crimes, or other violence related to armed conflicts including descriptions of weapons, strategic attacks, and the psychological impact of warfare.",
            self.ANIMAL_CRUELTY: "Contains scenes of intentional harm, abuse, neglect, torture, or killing of animals including descriptions of animal suffering, exploitation, or inhumane treatment of creatures.",
            self.NON_CONSENSUAL_CONTENT: "Contains sexual or intimate situations where one or more parties have not provided clear consent, including scenarios involving manipulation, coercion, intoxication, or situations where consent cannot be legally given.",
            self.UNDERAGE_SEXUAL_CONTENT: "Contains sexual content involving characters under the age of 18, including romantic or sexual situations between minors and adults, or sexualized depictions of children in any context.",
            self.SUICIDAL_IDEATION: "Contains characters expressing thoughts of suicide, death wishes, passive suicidal thoughts, or discussions about wanting to die without depicting actual suicide attempts or completed suicide.",
            self.PSYCHOSIS: "Depicts characters experiencing breaks from reality including hallucinations, delusions, paranoia, disorganized thinking, or other symptoms of psychotic disorders that affect perception and cognition.",
            self.BODY_DYSMORPHIA: "Contains themes related to distorted body image, obsessive focus on perceived physical flaws, excessive concern about appearance, or compulsive behaviors related to body image and appearance.",
            self.DRUG_USE: "Contains depictions of illegal drug use, prescription drug misuse, drug dealing, or the culture surrounding illicit substances including descriptions of drug effects, paraphernalia, or drug-related activities.",
            self.ALCOHOL_ABUSE: "Depicts excessive drinking, alcoholism, binge drinking, drunk driving, or the negative consequences of alcohol consumption on relationships, work, health, and family including withdrawal symptoms.",
            self.OVERDOSE: "Contains scenes depicting drug or alcohol overdose, including symptoms, medical emergencies, near-death experiences, or fatal outcomes from substance abuse including emergency medical treatment.",
            self.SLURS: "Contains derogatory terms or epithets targeting specific groups of people based on race, religion, gender, sexuality, disability, or other characteristics that are historically used to marginalize or dehumanize.",
            self.HARASSMENT: "Contains depictions of persistent unwanted contact, stalking, sexual harassment, workplace harassment, online harassment, or other forms of repeated intimidating or threatening behavior toward individuals.",
            self.GRAPHIC_DEATH: "Contains explicit, detailed descriptions of death including the dying process, graphic death scenes, disturbing imagery of deceased bodies, or detailed depictions of how characters die.",
            self.MURDER: "Contains depictions of intentional killing, premeditated homicide, assassination, or planned killings including murder weapons, crime scenes, motives, and the psychological profiles of killers.",
            self.GENOCIDE: "Contains depictions of systematic killing, persecution, or attempted extermination of entire groups of people based on ethnicity, religion, nationality, or other characteristics including mass atrocities.",
            self.MASS_CASUALTIES: "Contains scenes involving multiple deaths or injuries from disasters, terrorist attacks, accidents, natural disasters, or other catastrophic events including descriptions of emergency response and survivor trauma.",
            self.PTSD: "Contains detailed depictions of Post-Traumatic Stress Disorder symptoms including nightmares, hypervigilance, emotional numbing, intrusive memories, avoidance behaviors, and difficulty functioning after trauma.",
            self.CHILDHOOD_TRAUMA: "Depicts traumatic experiences occurring during childhood and their lasting effects on adult characters including abuse, neglect, witnessing violence, or other adverse childhood experiences and their psychological impact.",
            self.SEXISM: "Contains discriminatory attitudes or behaviors based on gender including misogyny, gender stereotypes, workplace discrimination, unequal treatment based on sex, or systematic oppression based on gender.",
            self.TRANSPHOBIA: "Contains discriminatory attitudes or behaviors specifically targeting transgender individuals including deadnaming, misgendering, exclusion from spaces, violence based on gender identity, or denial of transgender rights.",
            self.ABLEISM: "Contains discrimination against people with disabilities including negative stereotypes, inaccessible environments, treating disabled individuals as inferior, inspiration porn, or systemic barriers faced by disabled people.",
            self.RELIGIOUS_DISCRIMINATION: "Contains prejudice or unfair treatment based on religious beliefs including persecution of religious minorities, forced conversion, denial of religious freedom, or systematic oppression based on faith.",
            self.CLASSISM: "Contains discrimination based on social or economic class including stereotypes about wealth or poverty, systematic inequality, prejudice against different socioeconomic groups, or exploitation based on class status.",
            self.BLASPHEMY: "Contains content that may be considered disrespectful, offensive, or sacrilegious to religious beliefs including mockery of sacred texts, deities, religious practices, or deliberate violation of religious taboos.",
            self.RELIGIOUS_EXTREMISM: "Contains depictions of radical religious ideology, fundamentalism, religious violence, terrorism motivated by religious beliefs, cult behavior, or extreme interpretations of religious doctrine.",
            self.POLITICAL_EXTREMISM: "Contains depictions of radical political ideologies, political violence, terrorism, extremist movements, revolutionary activities, or dangerous political rhetoric that promotes violence or hatred.",
            self.PROPAGANDA: "Contains biased or misleading information designed to promote particular political, religious, or ideological viewpoints including manipulation tactics, misinformation campaigns, or deliberate distortion of facts.",
            self.SUPERNATURAL_HORROR: "Contains frightening supernatural elements including ghosts, demons, witchcraft, otherworldly entities, possession, curses, paranormal phenomena, or supernatural threats that create fear and dread.",
            self.DISTURBING_IMAGERY: "Contains unsettling visual descriptions or scenarios designed to create discomfort, revulsion, or psychological unease including grotesque imagery, nightmare-like scenarios, or deeply unsettling situations.",
            self.JUMP_SCARES: "Contains sudden, unexpected frightening moments designed to startle the reader including surprise attacks, sudden appearances of threats, shocking revelations, or other techniques meant to create immediate fear.",
            self.MEDICAL_CONTENT: "Contains medical procedures, hospital settings, illness, injury treatment, healthcare scenarios, medical terminology, or discussions of symptoms, diagnoses, treatments, and medical decision-making.",
            self.GRAPHIC_MEDICAL_PROCEDURES: "Contains detailed descriptions of surgical procedures, invasive medical examinations, medical operations, graphic depictions of medical instruments, or vivid descriptions of medical treatments and their effects.",
            self.PANDEMIC: "Contains themes related to widespread disease outbreaks, global health crises, quarantine, social isolation, mass illness, death tolls, or the societal breakdown and fear associated with infectious diseases.",
            self.DISEASE: "Contains depictions of illness, symptoms, medical conditions, contagious diseases, chronic conditions, or the physical and emotional impact of disease on individuals, families, and communities.",
            self.DISABILITY: "Contains characters with physical, mental, or cognitive disabilities and may address accessibility issues, discrimination, medical care, assistive technology, or the daily experiences and challenges of disabled individuals.",
            self.DIVORCE: "Contains themes related to marriage dissolution, separation, custody battles, family breakdown, legal proceedings, or the emotional impact of divorce on adults, children, and extended family members.",
            self.INFIDELITY: "Contains themes of cheating, extramarital affairs, emotional affairs, betrayal within romantic relationships, or the discovery of infidelity and its devastating impact on relationships and families.",
            self.CLAUSTROPHOBIA: "Contains scenarios involving confined spaces, being trapped, enclosed areas, small rooms, underground spaces, or other situations that might trigger fear of enclosed or restrictive environments.",
            self.AGORAPHOBIA: "Contains scenarios involving crowded places, open spaces, public transportation, large gatherings, or situations that might trigger fear of being unable to escape or find help in certain environments.",
            self.DROWNING: "Contains scenes of characters drowning, near-drowning experiences, being underwater and unable to breathe, water-related accidents, or detailed descriptions of the experience of drowning and water-related deaths.",
            self.FIRE: "Contains scenes involving fires, burns, characters trapped in burning buildings, detailed descriptions of fire-related injuries, arson, fire-related disasters, or the experience of being burned.",
            self.INSECTS_SPIDERS: "Contains detailed descriptions of insects, spiders, other arthropods, swarms, bites, stings, infestations, or scenarios that may trigger entomophobia, arachnophobia, or fear of creeping creatures.",
            self.BLOOD: "Contains descriptions of blood, bleeding, blood loss, blood tests, transfusions, or other blood-related medical procedures that may trigger hemophobia, squeamishness, or medical anxiety.",
            self.NEEDLES: "Contains depictions of injections, IV insertions, blood draws, vaccinations, or other medical procedures involving needles that may trigger trypanophobia, medical anxiety, or fear of medical procedures.",
            self.MATURE_THEMES: "Contains complex adult themes including moral ambiguity, existential questions, sophisticated emotional content, adult decision-making, or psychological complexity that may be better understood by mature readers.",
            self.ADULT_CONTENT: "Contains content specifically intended for adult audiences including explicit material, complex psychological themes, extreme situations, or content that is inappropriate for minors due to its nature or intensity.",
            self.NOT_SUITABLE_FOR_CHILDREN: "Contains content that is inappropriate for children due to violence, sexual content, language, frightening themes, or psychological complexity that could be harmful, confusing, or distressing to young minds."
        }
        return descriptions.get(self, f"Content warning for {self.display_name.lower()}")
    
    @property
    def severity_level(self) -> str:
        """Severity level of the content warning (mild, moderate, severe, extreme)."""
        mild = {
            self.STRONG_LANGUAGE, self.RELIGIOUS_CONTENT, self.POLITICAL_CONTENT,
            self.MATURE_THEMES, self.DIVORCE, self.GRIEF, self.DISABILITY
        }
        
        moderate = {
            self.VIOLENCE, self.SEXUAL_CONTENT, self.SUBSTANCE_ABUSE, self.MENTAL_HEALTH,
            self.DEATH, self.DISCRIMINATION, self.RELIGIOUS_CONTENT, self.POLITICAL_CONTENT,
            self.HORROR_ELEMENTS, self.BULLYING, self.FAMILY_DYSFUNCTION, self.MEDICAL_CONTENT,
            self.DEPRESSION, self.ANXIETY, self.INFIDELITY, self.TOXIC_RELATIONSHIPS,
            self.ABANDONMENT, self.CLAUSTROPHOBIA, self.AGORAPHOBIA, self.BLOOD, self.NEEDLES
        }
        
        severe = {
            self.GRAPHIC_VIOLENCE, self.EXPLICIT_SEXUAL_CONTENT, self.TRAUMA, self.DOMESTIC_VIOLENCE,
            self.EATING_DISORDERS, self.SELF_HARM, self.SUICIDAL_IDEATION, self.HATE_SPEECH,
            self.RACISM, self.HOMOPHOBIA, self.TRANSPHOBIA, self.SEXISM, self.ABLEISM,
            self.PSYCHOLOGICAL_HORROR, self.GRAPHIC_DEATH, self.MURDER, self.ADDICTION,
            self.PANIC_ATTACKS, self.PTSD, self.FLASHBACKS, self.HARASSMENT, self.TERMINAL_ILLNESS,
            self.MEDICAL_TRAUMA, self.CHILDHOOD_TRAUMA, self.DISTURBING_IMAGERY, self.SLURS,
            self.DRUG_USE, self.ALCOHOL_ABUSE, self.OVERDOSE, self.FIRE, self.DROWNING,
            self.PSYCHOSIS, self.BODY_DYSMORPHIA, self.PANDEMIC, self.DISEASE
        }
        
        extreme = {
            self.GORE, self.TORTURE, self.CHILD_ABUSE, self.SEXUAL_VIOLENCE, self.SEXUAL_ASSAULT,
            self.NON_CONSENSUAL_CONTENT, self.UNDERAGE_SEXUAL_CONTENT, self.SUICIDE,
            self.GENOCIDE, self.MASS_CASUALTIES, self.ANIMAL_CRUELTY, self.WAR_VIOLENCE,
            self.BODY_HORROR, self.GRAPHIC_MEDICAL_PROCEDURES, self.RELIGIOUS_EXTREMISM,
            self.POLITICAL_EXTREMISM, self.PROPAGANDA, self.BLASPHEMY, self.RELIGIOUS_DISCRIMINATION,
            self.CLASSISM, self.SUPERNATURAL_HORROR, self.JUMP_SCARES, self.INSECTS_SPIDERS,
            self.NOT_SUITABLE_FOR_CHILDREN, self.ADULT_CONTENT
        }
        
        if self in mild:
            return "mild"
        elif self in moderate:
            return "moderate"
        elif self in severe:
            return "severe"
        elif self in extreme:
            return "extreme"
        else:
            return "moderate"  # Default
    
    @property
    def age_appropriateness(self) -> str:
        """Minimum age recommendation for content with this warning."""
        age_map = {
            # All ages (with parental guidance)
            self.MILD_VIOLENCE: "8+",
            self.MILD_LANGUAGE: "8+",
            self.DIVORCE: "8+",
            self.GRIEF: "8+",
            
            # Young teen
            self.STRONG_LANGUAGE: "13+",
            self.VIOLENCE: "13+",
            self.DEATH: "13+",
            self.MENTAL_HEALTH: "13+",
            self.BULLYING: "13+",
            self.FAMILY_DYSFUNCTION: "13+",
            self.ANXIETY: "13+",
            self.DEPRESSION: "13+",
            
            # Older teen
            self.SEXUAL_CONTENT: "16+",
            self.SUBSTANCE_ABUSE: "16+",
            self.TRAUMA: "16+",
            self.DOMESTIC_VIOLENCE: "16+",
            self.DISCRIMINATION: "16+",
            self.HORROR_ELEMENTS: "16+",
            self.EATING_DISORDERS: "16+",
            self.SELF_HARM: "16+",
            self.SUICIDAL_IDEATION: "16+",
            self.GRAPHIC_VIOLENCE: "16+",
            self.POLITICAL_CONTENT: "16+",
            self.RELIGIOUS_CONTENT: "16+",
            
            # Adult only
            self.EXPLICIT_SEXUAL_CONTENT: "18+",
            self.GORE: "18+",
            self.TORTURE: "18+",
            self.CHILD_ABUSE: "18+",
            self.SEXUAL_VIOLENCE: "18+",
            self.SEXUAL_ASSAULT: "18+",
            self.SUICIDE: "18+",
            self.GRAPHIC_DEATH: "18+",
            self.MURDER: "18+",
            self.GENOCIDE: "18+",
            self.HATE_SPEECH: "18+",
            self.PSYCHOLOGICAL_HORROR: "18+",
            self.BODY_HORROR: "18+",
            self.UNDERAGE_SEXUAL_CONTENT: "18+",
            self.NON_CONSENSUAL_CONTENT: "18+",
            self.EXTREME_VIOLENCE: "18+",
            self.POLITICAL_EXTREMISM: "18+",
            self.RELIGIOUS_EXTREMISM: "18+",
            self.NOT_SUITABLE_FOR_CHILDREN: "18+",
            self.ADULT_CONTENT: "18+",
        }
        return age_map.get(self, "16+")  # Default to teen
    
    @property
    def category(self) -> str:
        """Category grouping for the content warning."""
        categories = {
            # Violence & Harm
            self.VIOLENCE: "violence",
            self.GRAPHIC_VIOLENCE: "violence",
            self.GORE: "violence",
            self.TORTURE: "violence",
            self.DOMESTIC_VIOLENCE: "violence",
            self.CHILD_ABUSE: "violence",
            self.SEXUAL_VIOLENCE: "violence",
            self.WAR_VIOLENCE: "violence",
            self.ANIMAL_CRUELTY: "violence",
            
            # Sexual Content
            self.SEXUAL_CONTENT: "sexual",
            self.EXPLICIT_SEXUAL_CONTENT: "sexual",
            self.SEXUAL_ASSAULT: "sexual",
            self.NON_CONSENSUAL_CONTENT: "sexual",
            self.UNDERAGE_SEXUAL_CONTENT: "sexual",
            
            # Mental Health
            self.MENTAL_HEALTH: "mental_health",
            self.DEPRESSION: "mental_health",
            self.ANXIETY: "mental_health",
            self.SUICIDE: "mental_health",
            self.SUICIDAL_IDEATION: "mental_health",
            self.SELF_HARM: "mental_health",
            self.PANIC_ATTACKS: "mental_health",
            self.PSYCHOSIS: "mental_health",
            self.EATING_DISORDERS: "mental_health",
            self.BODY_DYSMORPHIA: "mental_health",
            
            # Substance Use
            self.SUBSTANCE_ABUSE: "substance_use",
            self.DRUG_USE: "substance_use",
            self.ALCOHOL_ABUSE: "substance_use",
            self.ADDICTION: "substance_use",
            self.OVERDOSE: "substance_use",
            
            # Language & Behavior
            self.STRONG_LANGUAGE: "language",
            self.HATE_SPEECH: "language",
            self.SLURS: "language",
            self.BULLYING: "social",
            self.HARASSMENT: "social",
            
            # Death & Loss
            self.DEATH: "death",
            self.GRAPHIC_DEATH: "death",
            self.MURDER: "death",
            self.GENOCIDE: "death",
            self.MASS_CASUALTIES: "death",
            self.GRIEF: "emotional",
            self.TERMINAL_ILLNESS: "medical",
            
            # Trauma
            self.TRAUMA: "trauma",
            self.PTSD: "trauma",
            self.FLASHBACKS: "trauma",
            self.MEDICAL_TRAUMA: "trauma",
            self.CHILDHOOD_TRAUMA: "trauma",
            
            # Discrimination
            self.DISCRIMINATION: "discrimination",
            self.RACISM: "discrimination",
            self.SEXISM: "discrimination",
            self.HOMOPHOBIA: "discrimination",
            self.TRANSPHOBIA: "discrimination",
            self.ABLEISM: "discrimination",
            self.RELIGIOUS_DISCRIMINATION: "discrimination",
            self.CLASSISM: "discrimination",
            
            # Sensitive Topics
            self.RELIGIOUS_CONTENT: "ideological",
            self.BLASPHEMY: "ideological",
            self.RELIGIOUS_EXTREMISM: "ideological",
            self.POLITICAL_CONTENT: "ideological",
            self.POLITICAL_EXTREMISM: "ideological",
            self.PROPAGANDA: "ideological",
            
            # Horror
            self.HORROR_ELEMENTS: "horror",
            self.PSYCHOLOGICAL_HORROR: "horror",
            self.BODY_HORROR: "horror",
            self.SUPERNATURAL_HORROR: "horror",
            self.DISTURBING_IMAGERY: "horror",
            self.JUMP_SCARES: "horror",
            
            # Medical
            self.MEDICAL_CONTENT: "medical",
            self.GRAPHIC_MEDICAL_PROCEDURES: "medical",
            self.PANDEMIC: "medical",
            self.DISEASE: "medical",
            self.DISABILITY: "medical",
            
            # Relationships
            self.FAMILY_DYSFUNCTION: "relationships",
            self.DIVORCE: "relationships",
            self.ABANDONMENT: "emotional",
            self.INFIDELITY: "relationships",
            self.TOXIC_RELATIONSHIPS: "relationships",
            
            # Phobias
            self.CLAUSTROPHOBIA: "phobias",
            self.AGORAPHOBIA: "phobias",
            self.DROWNING: "phobias",
            self.FIRE: "phobias",
            self.INSECTS_SPIDERS: "phobias",
            self.BLOOD: "phobias",
            self.NEEDLES: "phobias",
        }
        return categories.get(self, "general")
    
    @classmethod
    def from_string(cls, value: str) -> 'ContentWarning':
        """Create ContentWarning from string with fuzzy matching."""
        if not value or not isinstance(value, str):
            raise ValueError(f"Invalid content warning value: {value}")
        
        # Normalize input
        normalized_value = value.lower().strip().replace("-", "_").replace(" ", "_")
        
        # Direct match
        for warning in cls:
            if warning.value == normalized_value:
                return warning
        
        # Fuzzy matching
        fuzzy_matches = {
            # Violence variations
            "violent": cls.VIOLENCE,
            "graphic": cls.GRAPHIC_VIOLENCE,
            "bloody": cls.GORE,
            "torture": cls.TORTURE,
            "abuse": cls.DOMESTIC_VIOLENCE,
            "domestic": cls.DOMESTIC_VIOLENCE,
            "war": cls.WAR_VIOLENCE,
            "animal": cls.ANIMAL_CRUELTY,
            
            # Sexual content variations
            "sex": cls.SEXUAL_CONTENT,
            "sexual": cls.SEXUAL_CONTENT,
            "explicit": cls.EXPLICIT_SEXUAL_CONTENT,
            "rape": cls.SEXUAL_ASSAULT,
            "assault": cls.SEXUAL_ASSAULT,
            
            # Mental health variations
            "mental": cls.MENTAL_HEALTH,
            "depressed": cls.DEPRESSION,
            "anxious": cls.ANXIETY,
            "suicide": cls.SUICIDE,
            "harm": cls.SELF_HARM,
            "cutting": cls.SELF_HARM,
            "eating": cls.EATING_DISORDERS,
            "anorexia": cls.EATING_DISORDERS,
            "bulimia": cls.EATING_DISORDERS,
            
            # Substance variations
            "drugs": cls.DRUG_USE,
            "alcohol": cls.ALCOHOL_ABUSE,
            "drinking": cls.ALCOHOL_ABUSE,
            "overdose": cls.OVERDOSE,
            
            # Language variations
            "language": cls.STRONG_LANGUAGE,
            "profanity": cls.STRONG_LANGUAGE,
            "swearing": cls.STRONG_LANGUAGE,
            "cursing": cls.STRONG_LANGUAGE,
            "hate": cls.HATE_SPEECH,
            "slur": cls.SLURS,
            
            # Death variations
            "dying": cls.DEATH,
            "kill": cls.MURDER,
            "killing": cls.MURDER,
            "murder": cls.MURDER,
            
            # Discrimination variations
            "racist": cls.RACISM,
            "sexist": cls.SEXISM,
            "homophobic": cls.HOMOPHOBIA,
            "transphobic": cls.TRANSPHOBIA,
            
            # Horror variations
            "scary": cls.HORROR_ELEMENTS,
            "frightening": cls.HORROR_ELEMENTS,
            "spooky": cls.HORROR_ELEMENTS,
            "horror": cls.HORROR_ELEMENTS,
            "disturbing": cls.DISTURBING_IMAGERY,
            
            # Religious/Political variations
            "religion": cls.RELIGIOUS_CONTENT,
            "religious": cls.RELIGIOUS_CONTENT,
            "politics": cls.POLITICAL_CONTENT,
            "political": cls.POLITICAL_CONTENT,
            
            # Medical variations
            "medical": cls.MEDICAL_CONTENT,
            "illness": cls.TERMINAL_ILLNESS,
            "disease": cls.DISEASE,
            "pandemic": cls.PANDEMIC,
            
            # Phobia variations
            "claustrophobic": cls.CLAUSTROPHOBIA,
            "agoraphobic": cls.AGORAPHOBIA,
            "drowning": cls.DROWNING,
            "spiders": cls.INSECTS_SPIDERS,
            "needles": cls.NEEDLES,
            "blood": cls.BLOOD,
            
            # Age variations
            "mature": cls.MATURE_THEMES,
            "adult": cls.ADULT_CONTENT,
            "children": cls.NOT_SUITABLE_FOR_CHILDREN,
        }
        
        if normalized_value in fuzzy_matches:
            return fuzzy_matches[normalized_value]
        
        # Partial matching
        for key, warning in fuzzy_matches.items():
            if key in normalized_value or normalized_value in key:
                return warning
        
        # Check if the normalized value contains any warning as a substring
        for warning in cls:
            if warning.value in normalized_value or normalized_value in warning.value:
                return warning
        
        available_warnings = [w.value for w in cls]
        raise ValueError(
            f"Unknown content warning: '{value}'. "
            f"Available warnings include: {', '.join(sorted(available_warnings[:10]))}..."
        )
    
    @classmethod
    def get_warnings_for_genre(cls, genre: str) -> List['ContentWarning']:
        """Get common content warnings for a specific genre."""
        genre_lower = genre.lower()
        
        genre_mappings = {
            "horror": [
                cls.HORROR_ELEMENTS, cls.VIOLENCE, cls.GORE, cls.DEATH,
                cls.PSYCHOLOGICAL_HORROR, cls.DISTURBING_IMAGERY, cls.SUPERNATURAL_HORROR,
                cls.BODY_HORROR, cls.JUMP_SCARES
            ],
            "thriller": [
                cls.VIOLENCE, cls.DEATH, cls.MURDER, cls.TRAUMA, cls.PSYCHOLOGICAL_HORROR,
                cls.STRONG_LANGUAGE, cls.DOMESTIC_VIOLENCE
            ],
            "mystery": [
                cls.DEATH, cls.MURDER, cls.VIOLENCE, cls.CRIME_INVESTIGATION,
                cls.STRONG_LANGUAGE, cls.TRAUMA
            ],
            "crime": [
                cls.VIOLENCE, cls.MURDER, cls.STRONG_LANGUAGE, cls.SUBSTANCE_ABUSE,
                cls.DOMESTIC_VIOLENCE, cls.SEXUAL_VIOLENCE
            ],
            "war": [
                cls.WAR_VIOLENCE, cls.DEATH, cls.GRAPHIC_VIOLENCE, cls.TRAUMA,
                cls.PTSD, cls.MASS_CASUALTIES, cls.GORE
            ],
            "romance": [
                cls.SEXUAL_CONTENT, cls.MATURE_THEMES, cls.STRONG_LANGUAGE,
                cls.INFIDELITY, cls.TOXIC_RELATIONSHIPS
            ],
            "literary_fiction": [
                cls.MATURE_THEMES, cls.MENTAL_HEALTH, cls.TRAUMA, cls.FAMILY_DYSFUNCTION,
                cls.DISCRIMINATION, cls.POLITICAL_CONTENT
            ],
            "dystopian": [
                cls.VIOLENCE, cls.POLITICAL_CONTENT, cls.DISCRIMINATION,
                cls.MASS_CASUALTIES, cls.TRAUMA, cls.PROPAGANDA
            ],
            "young_adult": [
                cls.MATURE_THEMES, cls.BULLYING, cls.MENTAL_HEALTH, cls.FAMILY_DYSFUNCTION,
                cls.ANXIETY, cls.DEPRESSION, cls.EATING_DISORDERS
            ],
            "historical_fiction": [
                cls.VIOLENCE, cls.DISCRIMINATION, cls.RELIGIOUS_CONTENT,
                cls.POLITICAL_CONTENT, cls.TRAUMA, cls.DEATH
            ],
            "science_fiction": [
                cls.VIOLENCE, cls.POLITICAL_CONTENT, cls.DISCRIMINATION,
                cls.MEDICAL_CONTENT, cls.PANDEMIC, cls.MATURE_THEMES
            ],
            "fantasy": [
                cls.VIOLENCE, cls.DEATH, cls.HORROR_ELEMENTS, cls.SUPERNATURAL_HORROR,
                cls.RELIGIOUS_CONTENT, cls.MATURE_THEMES
            ],
            "contemporary": [
                cls.MENTAL_HEALTH, cls.SUBSTANCE_ABUSE, cls.FAMILY_DYSFUNCTION,
                cls.SEXUAL_CONTENT, cls.STRONG_LANGUAGE, cls.DISCRIMINATION
            ],
            "biography": [
                cls.MATURE_THEMES, cls.TRAUMA, cls.MENTAL_HEALTH, cls.DISCRIMINATION,
                cls.POLITICAL_CONTENT, cls.DEATH
            ],
            "memoir": [
                cls.TRAUMA, cls.MENTAL_HEALTH, cls.FAMILY_DYSFUNCTION, cls.SUBSTANCE_ABUSE,
                cls.DISCRIMINATION, cls.MATURE_THEMES
            ]
        }
        
        # Find matching warnings
        recommended = set()
        for genre_key, warnings in genre_mappings.items():
            if genre_key in genre_lower:
                recommended.update(warnings)
        
        # If no specific mapping found, return general warnings
        if not recommended:
            recommended = {cls.MATURE_THEMES, cls.STRONG_LANGUAGE}
        
        return sorted(list(recommended), key=lambda x: x.display_name)
    
    @classmethod
    def get_warnings_by_severity(cls, severity: str) -> List['ContentWarning']:
        """Get warnings filtered by severity level."""
        return [w for w in cls if w.severity_level == severity.lower()]
    
    @classmethod
    def get_warnings_by_category(cls, category: str) -> List['ContentWarning']:
        """Get warnings filtered by category."""
        return [w for w in cls if w.category == category.lower()]
    
    @classmethod
    def get_warnings_by_age(cls, min_age: int) -> List['ContentWarning']:
        """Get warnings appropriate for a minimum age."""
        appropriate_warnings = []
        for warning in cls:
            age_str = warning.age_appropriateness
            if age_str.endswith('+'):
                warning_age = int(age_str[:-1])
                if warning_age <= min_age:
                    appropriate_warnings.append(warning)
        return appropriate_warnings
    
    def __str__(self) -> str:
        return self.display_name


@dataclass
class ContentWarningProfile:
    """A profile of content warnings for a book."""
    warnings: Set[ContentWarning] = field(default_factory=set)
    severity_override: Optional[str] = None  # Override auto-calculated severity
    custom_notes: str = ""
    age_rating: Optional[str] = None  # Override auto-calculated age rating
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_warning(self, warning: ContentWarning) -> None:
        """Add a content warning to the profile."""
        self.warnings.add(warning)
    
    def remove_warning(self, warning: ContentWarning) -> None:
        """Remove a content warning from the profile."""
        self.warnings.discard(warning)
    
    def has_warning(self, warning: ContentWarning) -> bool:
        """Check if the profile has a specific warning."""
        return warning in self.warnings
    
    @property
    def overall_severity(self) -> str:
        """Calculate overall severity level."""
        if self.severity_override:
            return self.severity_override
        
        if not self.warnings:
            return "none"
        
        severity_scores = {"mild": 1, "moderate": 2, "severe": 3, "extreme": 4}
        max_severity = max(severity_scores.get(w.severity_level, 0) for w in self.warnings)
        
        for severity, score in severity_scores.items():
            if score == max_severity:
                return severity
        
        return "moderate"
    
    @property
    def minimum_age(self) -> str:
        """Calculate minimum recommended age."""
        if self.age_rating:
            return self.age_rating
        
        if not self.warnings:
            return "All Ages"
        
        age_scores = {}
        for warning in self.warnings:
            age_str = warning.age_appropriateness
            if age_str.endswith('+'):
                age = int(age_str[:-1])
                age_scores[age] = age_scores.get(age, 0) + 1
        
        if not age_scores:
            return "13+"
        
        max_age = max(age_scores.keys())
        return f"{max_age}+"
    
    @property
    def warnings_by_category(self) -> Dict[str, List[ContentWarning]]:
        """Group warnings by category."""
        categories = {}
        for warning in self.warnings:
            category = warning.category
            if category not in categories:
                categories[category] = []
            categories[category].append(warning)
        
        # Sort warnings within each category
        for category in categories:
            categories[category].sort(key=lambda x: x.display_name)
        
        return categories
    
    @property
    def summary_text(self) -> str:
        """Generate a human-readable summary of content warnings."""
        if not self.warnings:
            return "No content warnings."
        
        categories = self.warnings_by_category
        summary_parts = []
        
        for category, warnings in categories.items():
            category_name = category.replace("_", " ").title()
            warning_names = [w.display_name for w in warnings]
            
            if len(warning_names) == 1:
                summary_parts.append(f"{category_name}: {warning_names[0]}")
            elif len(warning_names) == 2:
                summary_parts.append(f"{category_name}: {warning_names[0]} and {warning_names[1]}")
            else:
                summary_parts.append(f"{category_name}: {', '.join(warning_names[:-1])}, and {warning_names[-1]}")
        
        base_summary = "; ".join(summary_parts)
        
        age_info = f"Recommended for ages {self.minimum_age}"
        severity_info = f"Overall severity: {self.overall_severity}"
        
        full_summary = f"{base_summary}. {age_info}. {severity_info}."
        
        if self.custom_notes:
            full_summary += f" Note: {self.custom_notes}"
        
        return full_summary
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "warnings": [w.value for w in self.warnings],
            "severity_override": self.severity_override,
            "custom_notes": self.custom_notes,
            "age_rating": self.age_rating,
            "created_at": self.created_at.isoformat(),
            "overall_severity": self.overall_severity,
            "minimum_age": self.minimum_age,
            "warnings_by_category": {k: [w.value for w in v] for k, v in self.warnings_by_category.items()},
            "summary_text": self.summary_text
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ContentWarningProfile':
        """Create from dictionary."""
        warnings = {ContentWarning(w) for w in data.get("warnings", [])}
        return cls(
            warnings=warnings,
            severity_override=data.get("severity_override"),
            custom_notes=data.get("custom_notes", ""),
            age_rating=data.get("age_rating"),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now()
        )
    
    def export_to_json(self) -> str:
        """Export profile to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    @classmethod
    def import_from_json(cls, json_str: str) -> 'ContentWarningProfile':
        """Import profile from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


class ContentWarningGenerator:
    """Generates content warning profiles based on book parameters."""
    
    @classmethod
    def generate_profile(cls,
                        genre: str,
                        target_audience: str = "adult",
                        content_intensity: str = "moderate",
                        include_sensitive_topics: bool = True) -> ContentWarningProfile:
        """
        Generate a content warning profile for a book.
        
        Args:
            genre: Genre of the book
            target_audience: Target audience (children, young_adult, adult)
            content_intensity: Intensity level (mild, moderate, intense, extreme)
            include_sensitive_topics: Whether to include sensitive topic warnings
            
        Returns:
            ContentWarningProfile with appropriate warnings
        """
        profile = ContentWarningProfile()
        
        # Get genre-appropriate warnings
        genre_warnings = ContentWarning.get_warnings_for_genre(genre)
        
        # Filter by intensity level
        intensity_filters = {
            "mild": ["mild", "moderate"],
            "moderate": ["mild", "moderate", "severe"],
            "intense": ["moderate", "severe", "extreme"],
            "extreme": ["severe", "extreme"]
        }
        
        allowed_severities = intensity_filters.get(content_intensity, ["mild", "moderate"])
        filtered_warnings = [w for w in genre_warnings if w.severity_level in allowed_severities]
        
        # Filter by target audience age appropriateness
        audience_age_map = {
            "children": 8,
            "middle_grade": 10,
            "young_adult": 13,
            "new_adult": 16,
            "adult": 18
        }
        
        max_age = audience_age_map.get(target_audience.lower(), 18)
        age_appropriate_warnings = []
        
        for warning in filtered_warnings:
            age_str = warning.age_appropriateness
            if age_str.endswith('+'):
                warning_age = int(age_str[:-1])
                if warning_age <= max_age:
                    age_appropriate_warnings.append(warning)
        
        # Add the filtered warnings to the profile
        for warning in age_appropriate_warnings:
            profile.add_warning(warning)
        
        # Remove sensitive topics if requested
        if not include_sensitive_topics:
            sensitive_warnings = {
                ContentWarning.CHILD_ABUSE, ContentWarning.SEXUAL_ASSAULT,
                ContentWarning.SUICIDE, ContentWarning.SELF_HARM,
                ContentWarning.UNDERAGE_SEXUAL_CONTENT, ContentWarning.TORTURE,
                ContentWarning.GENOCIDE, ContentWarning.HATE_SPEECH
            }
            
            for warning in sensitive_warnings:
                profile.remove_warning(warning)
        
        return profile
    
    @classmethod
    def analyze_text_for_warnings(cls, text: str) -> List[ContentWarning]:
        """
        Analyze text content for potential warnings (basic keyword detection).
        
        Args:
            text: Text content to analyze
            
        Returns:
            List of potential content warnings found
        """
        text_lower = text.lower()
        found_warnings = []
        
        # Keyword mappings for detection
        keyword_mappings = {
            ContentWarning.VIOLENCE: ["fight", "punch", "hit", "attack", "violence", "violent"],
            ContentWarning.DEATH: ["death", "died", "dead", "kill", "murder", "suicide"],
            ContentWarning.STRONG_LANGUAGE: ["damn", "hell", "shit", "fuck", "bitch"],
            ContentWarning.SEXUAL_CONTENT: ["sex", "sexual", "intimacy", "bedroom", "naked"],
            ContentWarning.SUBSTANCE_ABUSE: ["drug", "alcohol", "drunk", "high", "addiction"],
            ContentWarning.MENTAL_HEALTH: ["depression", "anxiety", "panic", "therapy", "psychiatrist"],
            ContentWarning.HORROR_ELEMENTS: ["scary", "terrifying", "nightmare", "monster", "ghost"],
            ContentWarning.DISCRIMINATION: ["racist", "sexist", "homophobic", "prejudice", "discrimination"],
            ContentWarning.TRAUMA: ["trauma", "ptsd", "flashback", "triggered", "abuse"],
            ContentWarning.MEDICAL_CONTENT: ["hospital", "surgery", "doctor", "medical", "illness"],
        }
        
        for warning, keywords in keyword_mappings.items():
            if any(keyword in text_lower for keyword in keywords):
                found_warnings.append(warning)
        
        return found_warnings


# Example usage and testing
if __name__ == "__main__":
    print("=== MuseQuill Content Warning System Demo ===\n")
    
    # Test ContentWarning enum
    print("1. Content Warning Examples:")
    test_warnings = [
        ContentWarning.VIOLENCE, ContentWarning.SEXUAL_CONTENT, 
        ContentWarning.MENTAL_HEALTH, ContentWarning.HORROR_ELEMENTS
    ]
    
    for warning in test_warnings:
        print(f"  • {warning.display_name}")
        print(f"    Severity: {warning.severity_level}")
        print(f"    Age: {warning.age_appropriateness}")
        print(f"    Category: {warning.category}")
        print(f"    Description: {warning.description[:50]}...")
        print()
    
    # Test string conversion
    print("2. String Conversion Examples:")
    test_strings = ["violence", "sexual content", "mental health", "scary", "drugs"]
    for test_str in test_strings:
        try:
            warning = ContentWarning.from_string(test_str)
            print(f"  '{test_str}' -> {warning.display_name}")
        except ValueError as e:
            print(f"  '{test_str}' -> ERROR: {e}")
    
    # Test genre recommendations
    print("\n3. Genre-based Warning Recommendations:")
    test_genres = ["horror", "romance", "young_adult", "thriller"]
    for genre in test_genres:
        warnings = ContentWarning.get_warnings_for_genre(genre)
        print(f"  {genre.title()}: {', '.join([w.display_name for w in warnings[:4]])}...")
    
    # Test content warning profile
    print("\n4. Content Warning Profile:")
    profile = ContentWarningGenerator.generate_profile(
        genre="horror",
        target_audience="adult",
        content_intensity="moderate",
        include_sensitive_topics=True
    )
    
    print(f"  Warnings ({len(profile.warnings)}):")
    for warning in sorted(profile.warnings, key=lambda x: x.display_name):
        print(f"    - {warning.display_name} ({warning.severity_level})")
    
    print(f"\n  Overall Severity: {profile.overall_severity}")
    print(f"  Minimum Age: {profile.minimum_age}")
    print(f"  Summary: {profile.summary_text[:100]}...")
    
    # Test categorization
    print("\n5. Warnings by Category:")
    categories = profile.warnings_by_category
    for category, warnings in categories.items():
        print(f"  {category.title()}: {len(warnings)} warnings")
    
    # Test JSON export/import
    print("\n6. JSON Export/Import Test:")
    json_export = profile.export_to_json()
    imported_profile = ContentWarningProfile.import_from_json(json_export)
    print(f"  Export successful: {len(json_export)} characters")
    print(f"  Import successful: {len(imported_profile.warnings)} warnings restored")
    
    print("\n=== Demo Complete ===")