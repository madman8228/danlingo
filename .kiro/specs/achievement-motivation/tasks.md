# Implementation Plan

## ✅ Completed Core Services (Tasks 1-5)

- [x] 1. Set up core data models and type definitions
  - Created comprehensive TypeScript interfaces in `src/models/achievement.ts`
  - Defined all enums for badge rarity, milestone types, achievement categories
  - Created data models for UserAchievements, ProgressHistory, BadgeDefinitions
  - Set up storage schema with achievementStorage.ts
  - _Requirements: 4.2, 4.5, 8.1, 11.4_

- [x] 2. Implement AchievementEngine service
  - Implemented in `src/services/achievementEngine.ts`
  - recordActivity() processes learning activities and updates XP
  - checkMicroAchievements() detects session-based achievements
  - getAvatarReaction() provides real-time avatar expressions
  - XP accumulation with monotonicity guarantee
  - _Requirements: 1.1, 1.2, 1.3, 1.5, 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 3. Implement StreakManager service
  - Implemented in `src/services/streakManager.ts`
  - recordPractice() updates daily streak with consistency logic
  - getStreakInfo() retrieves current streak data
  - isStreakAtRisk() detects streak risk (past noon, not practiced)
  - Streak reset logic for missed days
  - _Requirements: 8.2, 8.3, 12.2_

- [x] 4. Implement BadgeManager service
  - Implemented in `src/services/badgeManager.ts`
  - checkUnlocks() detects newly unlocked badges
  - getAllBadges() retrieves badge collection with status
  - getBadgeProgress() tracks progress toward locked badges
  - Badge definitions in `src/data/achievements/badgeDefinitions.ts`
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 5. Implement MilestoneDetector service
  - Implemented in `src/services/milestoneDetector.ts`
  - checkMilestones() detects reached milestones
  - getUpcomingMilestones() provides preview with progress
  - Milestone configs in `src/data/achievements/milestoneConfigs.ts`
  - Integrated with CEFR scoring system
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 6. Implement data persistence layer
  - Implemented in `src/storage/achievementStorage.ts`
  - AsyncStorage wrapper for all achievement data
  - Save/load for UserAchievements, ProgressHistory, UserPreferences
  - Date serialization/deserialization with proper handling
  - Default data creation functions
  - _Requirements: 4.5, 8.1, 14.4_

## 🚧 Remaining Implementation Tasks

- [x] 7. Implement ProgressTracker service
  - Created ProgressTracker class with IProgressTracker interface
  - Implemented updateStats() to record activity statistics
  - Implemented getCalendarData() for learning calendar visualization (90-day view)
  - Implemented getAbilityRadar() for skill radar chart
  - Implemented getCEFRProgress() for level progress bars
  - Implemented getProgressComparison() for historical analysis
  - Added daily/weekly aggregation logic
  - Integrated with existing ProgressHistory data model
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 8.1, 8.4, 10.1, 10.2, 10.3, 10.4_

- [ ]* 7.1 Write property test for calendar data completeness
  - **Property 4: Calendar data completeness**
  - **Validates: Requirements 2.1, 8.1**

- [ ]* 7.2 Write property test for progress visualization consistency
  - **Property 8: Progress visualization consistency**
  - **Validates: Requirements 2.4**

- [ ]* 7.3 Write property test for CEFR progress calculation
  - **Property 19: CEFR progress calculation**
  - **Validates: Requirements 2.3**

- [x] 8. Implement RecommendationEngine service for Quick Start





  - Create RecommendationEngine class with IRecommendationEngine interface
  - Implement getRecommendation() for Quick Start suggestions
  - Implement getRecommendations() with filtering criteria
  - Add time-of-day preference logic (morning: listening, evening: conversation)
  - Integrate with errorCollectionService for weak area analysis
  - Add priority scoring algorithm based on user history
  - Note: A different RecommendationEngine exists for course recommendations - this is for Quick Start
  - _Requirements: 3.3, 3.4, 3.5, 14.2, 14.3_

- [ ]* 8.1 Write property test for recommendation relevance
  - **Property 11: Recommendation relevance**
  - **Validates: Requirements 3.3, 3.4**

- [x] 9. Implement GoalTracker service





  - Create GoalTracker class with IGoalTracker interface
  - Implement setGoal() to create new learning goals
  - Implement getActiveGoals() to retrieve current goals with progress
  - Implement updateProgress() to track goal advancement
  - Add goal achievement detection and celebration
  - Integrate with UserAchievements.activeGoals
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ]* 9.1 Write property test for goal achievement detection
  - **Property 10: Goal achievement detection**
  - **Validates: Requirements 13.3**



- [x] 10. Implement ShareCardGenerator service



  - Create ShareCardGenerator class with IShareCardGenerator interface
  - Implement generateMilestoneCard() for achievement sharing
  - Implement generateProgressCard() for periodic reports
  - Add image generation logic using React Native SVG or canvas
  - Design share card templates with DuoXX branding
  - Enhance existing share-achievement.tsx screen with generated cards
  - _Requirements: 5.3, 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ]* 10.1 Write property test for share card data accuracy
  - **Property 12: Share card data accuracy**
  - **Validates: Requirements 9.2**


- [x] 11. Implement NotificationService



  - Create NotificationService class for push notifications
  - Implement streak reminder notifications (24 hours inactive)
  - Implement milestone alert notifications
  - Implement daily practice reminders
  - Add notification scheduling with user preferences
  - Integrate with Expo Notifications API
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ]* 11.1 Write property test for notification timing compliance
  - **Property 13: Notification timing compliance**
  - **Validates: Requirements 12.4**

- [x] 12. Create UI component: QuickStartButton





  - Design prominent button for home screen (app/(tabs)/index.tsx)
  - Implement tap handler to trigger RecommendationEngine
  - Add loading state during recommendation fetch
  - Display practice preview (title, duration, reason)
  - Add navigation to selected module
  - Ensure < 2 second response time
  - _Requirements: 3.1, 3.2, 3.5_

- [ ]* 12.1 Write property test for Quick Start response time
  - **Property 6: Quick Start response time**
  - **Validates: Requirements 3.2**


- [x] 13. Create UI component: AchievementToast



  - Design animated toast notification for micro-achievements
  - Implement confetti, sparkle, and pulse animation types
  - Add XP counter animation
  - Ensure < 500ms display after trigger
  - Add auto-dismiss after 3 seconds
  - Create in src/components/feedback/ directory
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 14. Create UI component: LearningCalendar




  - Design calendar grid for 90-day view
  - Implement color intensity based on practice duration
  - Add tooltip/modal on day tap showing details
  - Integrate with ProgressTracker.getCalendarData()
  - Add smooth scrolling
  - Create in src/components/progress/ directory
  - _Requirements: 2.1, 8.1_


- [x] 15. Create UI component: AbilityRadar




  - Design radar chart for skill dimensions
  - Implement multi-layer radar for historical comparison
  - Add interactive tooltips for each dimension
  - Integrate with ProgressTracker.getAbilityRadar()
  - Use React Native SVG or react-native-chart-kit
  - Create in src/components/progress/ directory
  - _Requirements: 2.2, 10.3_


- [x] 16. Create UI component: ProgressDashboard screen




  - Create new screen at app/progress-dashboard.tsx
  - Design comprehensive progress overview screen
  - Integrate LearningCalendar component
  - Integrate AbilityRadar component
  - Add CEFR progress bars for each skill dimension
  - Add streak indicator and milestone preview
  - Add navigation from home screen
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 8.4, 10.1, 10.2_

- [x] 17. Enhance BadgeGallery screen (app/achievements.tsx)
  - Update existing achievements.tsx to use BadgeManager
  - Replace hardcoded ACHIEVEMENTS with BADGE_DEFINITIONS
  - Display unlocked badges with unlock dates
  - Display locked badges with progress bars from getBadgeProgress()
  - Add badge detail modal on tap
  - Add filter by category and rarity
  - Remove emoji icons and use Ionicons instead
  - _Requirements: 4.2, 4.3, 4.4_

- [x] 18. Create UI component: MilestoneModal

  - Design full-screen celebration modal
  - Implement standard, enhanced, and epic animation levels
  - Display milestone name, description, and rewards
  - Add share button integration
  - Add "Continue" button to dismiss
  - Integrate with MilestoneDetector
  - Create in src/components/feedback/ directory
  - _Requirements: 5.1, 5.2, 5.3, 5.4_


- [x] 19. Enhance StreakIndicator component ✅
  - ✅ Enhanced existing StreakCounter component in src/components/progress/
  - ✅ Added "at risk" warning indicator with isAtRisk prop (integrates with StreakManager.isStreakAtRisk())
  - ✅ Added risk warning badge with pulsing animation
  - ✅ Added detailed risk warning message when past noon with no activity
  - ✅ Display next milestone preview with progress bar
  - ✅ Added tap handler via onPress prop to view detailed streak info
  - ✅ Replaced emoji flame with Ionicons flame/flame-outline
  - ✅ Added chevron indicator when tappable
  - ✅ Created comprehensive documentation (STREAK_COUNTER_README.md)
  - _Requirements: 8.2, 8.3, 8.5_

- [x] 20. Create UI component: GoalSettingsScreen

  - Create new screen at app/goal-settings.tsx
  - Design goal creation and management interface
  - Add goal type selection (daily XP, weekly sessions, skill level)
  - Add target value input
  - Display active goals with progress bars
  - Add goal completion celebration
  - Integrate with GoalTracker
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [x] 21. Integrate achievement system with existing modules
  - Update listening-speaking module to call AchievementEngine.recordActivity() ✅
  - Created achievementIntegration.ts helper service ✅
  - Created ACHIEVEMENT_INTEGRATION_GUIDE.md documentation ✅
  - Update sentence-building module to call AchievementEngine.recordActivity() (TODO)
  - Update survival-phrases module to call AchievementEngine.recordActivity() (TODO)
  - Update imperfect-dialogue module to call AchievementEngine.recordActivity() (TODO)
  - Update vocab-recognition module to call AchievementEngine.recordActivity() (TODO)
  - Update dynamic-lexicon module to call AchievementEngine.recordActivity() (TODO)
  - Create helper function in each module's completion handler
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ]* 21.1 Write property test for module integration transparency
  - **Property 15: Module integration transparency**
  - **Validates: Requirements 11.1, 11.5**

- [ ] 22. Integrate with speaking-avatar for real-time reactions
  - Connect AchievementEngine.getAvatarReaction() to SpeakingAvatarController
  - Update avatar expressions on exercise completion in all modules
  - Add expression transitions for streaks and achievements
  - Ensure < 300ms reaction time
  - Test with all avatar characters
  - Update SpeakingAvatarView component to accept achievement-driven expressions
  - _Requirements: 1.5, 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 23. Integrate with error collection service
  - Connect RecommendationEngine to errorCollectionService
  - Use weak area analysis for Quick Start recommendations
  - Update recommendations based on recent errors
  - Ensure error data doesn't trigger negative feedback
  - errorCollectionService already exists in src/services/errorCollectionService.ts
  - _Requirements: 3.3, 11.2_

- [ ] 24. Integrate with scoring service
  - Connect ProgressTracker to scoringService for CEFR updates
  - Trigger level-up celebrations on CEFR advancement
  - Update ability radar when scores change
  - Ensure CEFR progress bars reflect current scores
  - scoringService already exists in src/services/scoringService.ts
  - _Requirements: 2.3, 5.2, 11.3_


- [ ] 25. Implement UserPreferences management
  - Create preferences screen at app/achievement-preferences.tsx
  - Add notification settings UI
  - Add Quick Start preference configuration
  - Add display preference toggles
  - Add privacy settings
  - Persist all preferences immediately on change using achievementStorage
  - _Requirements: 12.4, 14.1, 14.2, 14.3, 14.4_


- [ ] 26. Implement anonymous leaderboard (optional social feature)
  - Create leaderboard service for percentile calculations
  - Implement anonymous ranking display
  - Add global challenge progress tracking
  - Ensure all data is anonymized
  - Add opt-out option in privacy settings
  - Create screen at app/leaderboard.tsx
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ]* 26.1 Write property test for percentile ranking anonymity
  - **Property 17: Percentile ranking anonymity**
  - **Validates: Requirements 6.1, 6.5**


- [x] 27. Update home screen with achievement features
  - Enhance QuickStartButton integration in app/(tabs)/index.tsx (already added) ✅
  - Enhance StreakCounter in header with "at risk" indicator ✅
  - Add "Today's Progress" summary card showing XP earned today ✅
  - Add quick access to ProgressDashboard (already exists at app/progress-dashboard.tsx) ✅
  - Add quick access to BadgeGallery (achievements.tsx already exists) ✅
  - Ensure layout follows DuoXX design system (use Ionicons, not emoji) ✅
  - _Requirements: 3.1, 8.2, 8.3_

- [ ] 28. Implement error handling and graceful degradation
  - Add try-catch blocks to all service methods
  - Implement retry logic with exponential backoff in storage operations
  - Add offline queue for activities
  - Display cached data when services unavailable
  - Add error logging for debugging
  - Test all error scenarios
  - _Requirements: All (error handling is cross-cutting)_

- [ ] 29. Add performance optimizations

  - Optimize calendar rendering for 90 days (use FlatList or virtualization)
  - Optimize radar chart rendering (memoize calculations)
  - Add memoization for expensive calculations in ProgressTracker
  - Implement lazy loading for badge gallery
  - Add debouncing for rapid activity reporting
  - Ensure Quick Start < 2 second response
  - Ensure avatar reactions < 500ms
  - _Requirements: 3.2, 1.1, 1.5_

- [ ] 30. Checkpoint - Ensure all tests pass
  - Run all existing tests
  - Ensure all tests pass, ask the user if questions arise





- [ ]* 31. Write property-based tests for core services
  - Write test for XP accumulation monotonicity (Property 1)
  - Write test for streak consistency (Property 2)
  - Write test for badge unlock idempotence (Property 3)
  - Write test for milestone detection accuracy (Property 5)
  - Write test for avatar reaction timeliness (Property 7)
  - Write test for streak risk detection (Property 14)
  - Use fast-check library (already in project)
  - Create tests in src/services/__tests__/
  - _Validates: Requirements 1.3, 4.5, 8.2, 8.3, 5.1, 5.2, 5.5, 1.1, 1.5, 7.1, 7.2_





- [x] 32. Write integration tests for module interactions




  - Test AchievementEngine with all learning modules
  - Test avatar integration with achievement events
  - Test scoring service integration with milestones
  - Test notification scheduling with preferences
  - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [ ]* 33. Write UI component tests
  - Test QuickStartButton navigation and timing
  - Test AchievementToast animations
  - Test LearningCalendar rendering and interactions
  - Test AbilityRadar rendering and overlays
  - Test MilestoneModal animations and dismissal
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 5.1, 9.3_


- [ ]* 34. Final polish and documentation
  - Add JSDoc comments to all public interfaces
  - Update AGENTS.md with achievement system guidelines
  - Create user-facing help documentation
  - Add analytics tracking for key events
  - Perform final UI/UX review
  - _Requirements: All (documentation and polish)_

## Notes

### Already Implemented
- Core data models and types (achievement.ts)
- AchievementEngine with XP, badges, milestones, micro-achievements
- StreakManager with streak tracking and risk detection
- BadgeManager with unlock detection and progress tracking
- MilestoneDetector with CEFR integration
- AchievementStorage with AsyncStorage persistence
- Badge definitions and milestone configs
- ProgressTracker with calendar, radar, CEFR progress tracking
- QuickStartButton component (src/components/quick-start/)
- RecommendationEngine for Quick Start (src/services/quickStartRecommendationEngine.ts)
- GoalTracker service (src/services/goalTracker.ts)
- ShareCardGenerator service (src/services/shareCardGenerator.ts)
- NotificationService (src/services/notificationService.ts)
- AchievementToast component (src/components/feedback/)
- LearningCalendar component (src/components/progress/)
- AbilityRadar component (src/components/progress/)
- ProgressDashboard screen (app/progress-dashboard.tsx)
- Basic achievements screen (needs enhancement with BadgeManager)
- Basic share achievement screen (needs enhancement)
- Integration tests for achievement system

### Key Integration Points
- errorCollectionService: Already exists at src/services/errorCollectionService.ts, use for weak area analysis
- scoringService: Already exists at src/services/scoringService.ts, use for CEFR level tracking
- speaking-avatar: Already exists at src/modules/speaking-avatar/, integrate for real-time reactions
- All learning modules: Need to add recordActivity() calls
  - listening-speaking: src/modules/listening-speaking/
  - sentence-building: src/modules/sentence-building/
  - survival-phrases: src/modules/survival-phrases/
  - imperfect-dialogue: src/modules/imperfect-dialogue/
  - vocab-recognition: src/modules/vocab-recognition/
  - dynamic-lexicon: src/modules/dynamic-lexicon/

### Design Guidelines
- Use Ionicons instead of emoji for all icons
- Follow existing DuoXX color scheme and design patterns
- Ensure all UI is consistent with existing components
- Use TypeScript strict mode
- Follow kebab-case for file names, PascalCase for components
