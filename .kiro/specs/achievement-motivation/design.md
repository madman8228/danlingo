# Design Document

## Overview

The Achievement and Motivation System is a comprehensive engagement layer that sits atop DuoXX's existing learning modules. It transforms discrete practice activities into a cohesive, rewarding experience through real-time feedback, visual progress tracking, and personalized motivation mechanisms.

The system follows a three-tier feedback architecture:
1. **Immediate Layer** (0-1 second): Micro-achievements, avatar reactions, XP animations
2. **Session Layer** (per practice session): Summary screens, badge unlocks, streak updates
3. **Long-term Layer** (days/weeks): Milestone celebrations, progress reports, CEFR level-ups

Key design principles:
- **Zero Friction**: Quick Start eliminates decision paralysis
- **Positive Reinforcement**: All feedback is encouraging, never punitive
- **Visible Progress**: Multiple visualization methods cater to different user preferences
- **Seamless Integration**: Works with all existing modules without requiring module-specific code

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                       │
├─────────────────────────────────────────────────────────────┤
│  QuickStartButton  │  ProgressDashboard  │  BadgeGallery    │
│  MilestoneModal    │  ShareCard          │  LearningCalendar│
│  AchievementToast  │  StreakIndicator    │  AbilityRadar    │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      Service Layer                           │
├─────────────────────────────────────────────────────────────┤
│  AchievementEngine │  ProgressTracker  │  RecommendationEngine│
│  BadgeManager      │  MilestoneDetector│  NotificationService │
│  ShareCardGenerator│  StreakManager    │  GoalTracker         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                       Data Layer                             │
├─────────────────────────────────────────────────────────────┤
│  UserAchievements  │  ProgressHistory  │  BadgeDefinitions   │
│  MilestoneConfig   │  UserPreferences  │  GoalSettings       │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Integration Points                         │
├─────────────────────────────────────────────────────────────┤
│  All Learning Modules → Exercise Completion Events           │
│  Error Collection Service → Weakness Analysis                │
│  Scoring Service → CEFR Level Changes                        │
│  Speaking Avatar → Expression Updates                        │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Exercise Completion Flow**:
   ```
   Module → AchievementEngine.recordActivity()
         → ProgressTracker.updateStats()
         → BadgeManager.checkUnlocks()
         → MilestoneDetector.checkMilestones()
         → UI Updates (toasts, animations, counters)
   ```

2. **Quick Start Flow**:
   ```
   User taps Quick Start → RecommendationEngine.getRecommendation()
                        → Consider: time of day, weak areas, recent activity
                        → Select module + content
                        → Navigate to practice screen
   ```

3. **Progress Visualization Flow**:
   ```
   User opens dashboard → ProgressTracker.getHistoricalData()
                       → Generate: calendar, radar, graphs
                       → Render visualizations
   ```

## Components and Interfaces

### AchievementEngine

Central service that processes all learning activities and triggers appropriate feedback.

```typescript
interface IAchievementEngine {
  // Record a completed activity
  recordActivity(activity: LearningActivity): AchievementResult;
  
  // Check for micro-achievements in current session
  checkMicroAchievements(sessionData: SessionData): MicroAchievement[];
  
  // Get real-time avatar expression based on performance
  getAvatarReaction(performance: PerformanceData): AvatarExpression;
}

interface LearningActivity {
  moduleId: string;
  exerciseType: string;
  isCorrect: boolean;
  xpEarned: number;
  timestamp: Date;
  metadata?: Record<string, any>;
}

interface AchievementResult {
  xpAdded: number;
  badgesUnlocked: Badge[];
  milestonesReached: Milestone[];
  microAchievements: MicroAchievement[];
  streakUpdated: boolean;
  newStreak: number;
}

interface MicroAchievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  animationType: 'confetti' | 'sparkle' | 'pulse';
}
```

### ProgressTracker

Manages all progress data and provides historical analysis.

```typescript
interface IProgressTracker {
  // Update statistics after activity
  updateStats(activity: LearningActivity): void;
  
  // Get calendar data for visualization
  getCalendarData(days: number): CalendarDay[];
  
  // Get ability radar data
  getAbilityRadar(): AbilityRadarData;
  
  // Get progress toward next CEFR level
  getCEFRProgress(dimension: AbilityDimension): CEFRProgress;
  
  // Get historical comparison
  getProgressComparison(daysAgo: number): ProgressComparison;
}

interface CalendarDay {
  date: Date;
  practiceMinutes: number;
  sessionsCompleted: number;
  xpEarned: number;
  intensity: 'none' | 'low' | 'medium' | 'high';
}

interface AbilityRadarData {
  dimensions: {
    name: string;
    currentScore: number; // 0-100
    previousScore?: number; // for comparison overlay
  }[];
}

interface CEFRProgress {
  currentLevel: CEFRLevel;
  currentScore: number; // 0-100
  nextLevel: CEFRLevel;
  percentToNext: number; // 0-100
}
```

### BadgeManager

Handles badge definitions, unlock logic, and collection management.

```typescript
interface IBadgeManager {
  // Check if any badges should be unlocked
  checkUnlocks(userStats: UserStatistics): Badge[];
  
  // Get all badges (locked and unlocked)
  getAllBadges(): BadgeWithStatus[];
  
  // Get progress toward locked badges
  getBadgeProgress(badgeId: string): BadgeProgress;
}

interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
  category: 'streak' | 'xp' | 'skill' | 'social' | 'special';
}

interface BadgeWithStatus extends Badge {
  unlocked: boolean;
  unlockedAt?: Date;
  progress?: BadgeProgress;
}

interface BadgeProgress {
  current: number;
  required: number;
  unit: string; // e.g., "days", "XP", "exercises"
}

interface BadgeUnlockCondition {
  type: 'streak' | 'xp_total' | 'xp_single_session' | 'perfect_score' | 'module_complete';
  threshold: number;
  metadata?: Record<string, any>;
}
```

### MilestoneDetector

Identifies when users reach significant achievements.

```typescript
interface IMilestoneDetector {
  // Check for milestone achievements
  checkMilestones(userStats: UserStatistics): Milestone[];
  
  // Get upcoming milestones
  getUpcomingMilestones(limit: number): MilestonePreview[];
}

interface Milestone {
  id: string;
  type: 'xp' | 'cefr_level' | 'streak' | 'total_time' | 'module_mastery';
  name: string;
  description: string;
  celebrationLevel: 'standard' | 'enhanced' | 'epic';
  rewards?: MilestoneReward[];
}

interface MilestoneReward {
  type: 'badge' | 'avatar_unlock' | 'module_unlock' | 'feature_unlock';
  itemId: string;
}

interface MilestonePreview {
  milestone: Milestone;
  progress: number; // 0-100
  estimatedDaysToComplete: number;
}
```

### RecommendationEngine

Provides intelligent content recommendations for Quick Start.

```typescript
interface IRecommendationEngine {
  // Get recommended practice for Quick Start
  getRecommendation(): PracticeRecommendation;
  
  // Get recommendations based on specific criteria
  getRecommendations(criteria: RecommendationCriteria): PracticeRecommendation[];
}

interface PracticeRecommendation {
  moduleId: string;
  contentId?: string;
  title: string;
  description: string;
  estimatedMinutes: number;
  reason: string; // e.g., "Based on your weak areas" or "Perfect for morning practice"
  priority: number;
}

interface RecommendationCriteria {
  timeOfDay?: 'morning' | 'afternoon' | 'evening';
  availableMinutes?: number;
  focusAreas?: string[];
  excludeModules?: string[];
}
```

### StreakManager

Manages daily streak tracking and notifications.

```typescript
interface IStreakManager {
  // Record today's practice
  recordPractice(): StreakUpdate;
  
  // Get current streak information
  getStreakInfo(): StreakInfo;
  
  // Check if streak is at risk
  isStreakAtRisk(): boolean;
}

interface StreakUpdate {
  newStreak: number;
  longestStreak: number;
  streakExtended: boolean;
  milestoneReached: boolean;
}

interface StreakInfo {
  currentStreak: number;
  longestStreak: number;
  lastPracticeDate: Date;
  nextMilestone: number;
  daysUntilMilestone: number;
}
```

### ShareCardGenerator

Creates shareable achievement cards.

```typescript
interface IShareCardGenerator {
  // Generate share card for milestone
  generateMilestoneCard(milestone: Milestone, userStats: UserStatistics): ShareCard;
  
  // Generate periodic progress report card
  generateProgressCard(period: 'week' | 'month'): ShareCard;
}

interface ShareCard {
  imageUri: string; // Base64 or file URI
  title: string;
  statistics: {
    label: string;
    value: string;
  }[];
  shareText: string;
}
```

### GoalTracker

Manages personal learning goals.

```typescript
interface IGoalTracker {
  // Set a new goal
  setGoal(goal: LearningGoal): void;
  
  // Get all active goals
  getActiveGoals(): GoalWithProgress[];
  
  // Update goal progress
  updateProgress(activity: LearningActivity): GoalUpdate[];
}

interface LearningGoal {
  id: string;
  type: 'daily_xp' | 'weekly_sessions' | 'skill_level' | 'custom';
  target: number;
  deadline?: Date;
  createdAt: Date;
}

interface GoalWithProgress extends LearningGoal {
  current: number;
  percentComplete: number;
  onTrack: boolean;
}

interface GoalUpdate {
  goalId: string;
  achieved: boolean;
  newProgress: number;
}
```

## Data Models

### UserAchievements

```typescript
interface UserAchievements {
  userId: string;
  
  // XP and Level
  totalXP: number;
  currentLevel: number;
  
  // Streaks
  currentStreak: number;
  longestStreak: number;
  lastPracticeDate: Date;
  
  // Badges
  unlockedBadges: {
    badgeId: string;
    unlockedAt: Date;
  }[];
  
  // Milestones
  completedMilestones: {
    milestoneId: string;
    completedAt: Date;
  }[];
  
  // Session stats
  totalSessions: number;
  totalPracticeMinutes: number;
  
  // Micro-achievements (recent only, for session continuity)
  recentMicroAchievements: {
    achievementId: string;
    count: number;
    lastTriggered: Date;
  }[];
  
  // Goals
  activeGoals: LearningGoal[];
  completedGoals: {
    goal: LearningGoal;
    completedAt: Date;
  }[];
}
```

### ProgressHistory

```typescript
interface ProgressHistory {
  userId: string;
  
  // Daily records (keep last 90 days)
  dailyRecords: {
    date: Date;
    xpEarned: number;
    sessionsCompleted: number;
    practiceMinutes: number;
    exercisesCompleted: number;
    accuracy: number; // 0-100
  }[];
  
  // Ability snapshots (weekly)
  abilitySnapshots: {
    date: Date;
    abilities: {
      dimension: AbilityDimension;
      score: number; // 0-100
      cefrLevel: CEFRLevel;
    }[];
  }[];
  
  // Module-specific progress
  moduleProgress: {
    moduleId: string;
    sessionsCompleted: number;
    lastPracticed: Date;
    masteryLevel: number; // 0-100
  }[];
}
```

### BadgeDefinitions

```typescript
interface BadgeDefinition {
  id: string;
  name: string;
  description: string;
  icon: string;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
  category: 'streak' | 'xp' | 'skill' | 'social' | 'special';
  unlockCondition: BadgeUnlockCondition;
  hidden: boolean; // Secret badges not shown until unlocked
}

// Example badge definitions
const BADGE_DEFINITIONS: BadgeDefinition[] = [
  {
    id: 'streak_7',
    name: 'Week Warrior',
    description: 'Practice for 7 days in a row',
    icon: 'flame',
    rarity: 'common',
    category: 'streak',
    unlockCondition: { type: 'streak', threshold: 7 },
    hidden: false,
  },
  {
    id: 'streak_30',
    name: 'Monthly Master',
    description: 'Practice for 30 days in a row',
    icon: 'trophy',
    rarity: 'rare',
    category: 'streak',
    unlockCondition: { type: 'streak', threshold: 30 },
    hidden: false,
  },
  {
    id: 'xp_1000',
    name: 'XP Collector',
    description: 'Earn 1000 total XP',
    icon: 'star',
    rarity: 'common',
    category: 'xp',
    unlockCondition: { type: 'xp_total', threshold: 1000 },
    hidden: false,
  },
  {
    id: 'perfect_session',
    name: 'Perfectionist',
    description: 'Complete a session with 100% accuracy',
    icon: 'checkmark-circle',
    rarity: 'rare',
    category: 'skill',
    unlockCondition: { type: 'perfect_score', threshold: 100 },
    hidden: false,
  },
];
```

### MilestoneConfig

```typescript
interface MilestoneConfig {
  id: string;
  type: 'xp' | 'cefr_level' | 'streak' | 'total_time' | 'module_mastery';
  threshold: number;
  name: string;
  description: string;
  celebrationLevel: 'standard' | 'enhanced' | 'epic';
  rewards: MilestoneReward[];
}

// Example milestone configurations
const MILESTONE_CONFIGS: MilestoneConfig[] = [
  {
    id: 'xp_100',
    type: 'xp',
    threshold: 100,
    name: 'First Century',
    description: 'You've earned your first 100 XP!',
    celebrationLevel: 'standard',
    rewards: [{ type: 'badge', itemId: 'xp_100_badge' }],
  },
  {
    id: 'cefr_a2',
    type: 'cefr_level',
    threshold: 2, // A2 level
    name: 'Level Up: A2',
    description: 'You've reached A2 level!',
    celebrationLevel: 'enhanced',
    rewards: [
      { type: 'badge', itemId: 'cefr_a2_badge' },
      { type: 'avatar_unlock', itemId: 'proud_expression' },
    ],
  },
  {
    id: 'streak_100',
    type: 'streak',
    threshold: 100,
    name: 'Century Streak',
    description: '100 days of consistent practice!',
    celebrationLevel: 'epic',
    rewards: [
      { type: 'badge', itemId: 'streak_100_legendary' },
      { type: 'feature_unlock', itemId: 'custom_avatar' },
    ],
  },
];
```

### UserPreferences

```typescript
interface UserPreferences {
  userId: string;
  
  // Notification settings
  notifications: {
    enabled: boolean;
    streakReminders: boolean;
    milestoneAlerts: boolean;
    dailyReminder: boolean;
    preferredReminderTime?: string; // HH:MM format
  };
  
  // Quick Start preferences
  quickStart: {
    preferredModules: string[];
    preferredDuration: number; // minutes
    adaptToTimeOfDay: boolean;
  };
  
  // Display preferences
  display: {
    showComparativeStats: boolean;
    showStreakOnHome: boolean;
    animationIntensity: 'minimal' | 'normal' | 'full';
  };
  
  // Privacy
  privacy: {
    allowAnonymousLeaderboard: boolean;
    allowDataSharing: boolean;
  };
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: XP accumulation monotonicity
*For any* sequence of learning activities, the total XP SHALL never decrease, and SHALL increase by exactly the sum of XP earned from each activity.
**Validates: Requirements 1.3, 4.5**

### Property 2: Streak consistency
*For any* user with a current streak of N days, if the user practices today, the new streak SHALL be N+1, and if the user does not practice today and the last practice was yesterday, the streak SHALL reset to 0 tomorrow.
**Validates: Requirements 8.2, 8.3**

### Property 3: Badge unlock idempotence
*For any* badge that has been unlocked, subsequent checks for the same badge SHALL not unlock it again, and the unlock timestamp SHALL remain unchanged.
**Validates: Requirements 4.1, 4.5**

### Property 4: Calendar data completeness
*For any* date range requested, the calendar data SHALL include exactly one entry per day in the range, with no gaps or duplicates.
**Validates: Requirements 2.1, 8.1**

### Property 5: Milestone detection accuracy
*For any* milestone with threshold T, the milestone SHALL trigger when and only when the relevant metric reaches or exceeds T for the first time.
**Validates: Requirements 5.1, 5.2, 5.5**

### Property 6: Quick Start response time
*For any* Quick Start request, the system SHALL return a recommendation and begin navigation within 2 seconds.
**Validates: Requirements 3.2**

### Property 7: Avatar reaction timeliness
*For any* exercise completion event, the avatar expression SHALL update within 500 milliseconds of the event.
**Validates: Requirements 1.1, 1.5, 7.1, 7.2**

### Property 8: Progress visualization consistency
*For any* two visualizations (calendar, radar, progress bars) displayed simultaneously, they SHALL reflect the same underlying data state.
**Validates: Requirements 2.4**

### Property 9: Badge progress accuracy
*For any* locked badge with progress tracking, the displayed progress SHALL equal the actual count of completed criteria divided by required criteria.
**Validates: Requirements 4.4**

### Property 10: Goal achievement detection
*For any* active goal with target T, when the user's progress reaches or exceeds T, the goal SHALL be marked as achieved exactly once.
**Validates: Requirements 13.3**

### Property 11: Recommendation relevance
*For any* Quick Start recommendation, the suggested content SHALL target at least one of the user's identified weak areas OR match the current time-of-day preference.
**Validates: Requirements 3.3, 3.4**

### Property 12: Share card data accuracy
*For any* generated share card, all displayed statistics SHALL match the user's actual achievement data at the time of generation.
**Validates: Requirements 9.2**

### Property 13: Notification timing compliance
*For any* user with notification preferences set, notifications SHALL only be sent within the user's specified time windows and frequency limits.
**Validates: Requirements 12.4**

### Property 14: Streak risk detection
*For any* user with a current streak > 0, if the last practice date is yesterday and the current time is past noon today, the streak SHALL be marked as "at risk".
**Validates: Requirements 8.3**

### Property 15: Module integration transparency
*For any* learning module that reports an activity, the achievement system SHALL process it without requiring module-specific code, using only the generic LearningActivity interface.
**Validates: Requirements 11.1, 11.5**

### Property 16: Historical data retention
*For any* user, daily records SHALL be retained for at least 90 days, and ability snapshots SHALL be retained for at least 52 weeks.
**Validates: Requirements 10.1, 10.3**

### Property 17: Percentile ranking anonymity
*For any* displayed percentile ranking, the calculation SHALL use only anonymized aggregate data and SHALL not expose individual user identities.
**Validates: Requirements 6.1, 6.5**

### Property 18: Micro-achievement uniqueness
*For any* practice session, the same micro-achievement SHALL not trigger more than once within a 5-minute window.
**Validates: Requirements 1.2**

### Property 19: CEFR progress calculation
*For any* ability dimension, the percentage progress to the next CEFR level SHALL equal (current_score - current_level_min) / (next_level_min - current_level_min) * 100.
**Validates: Requirements 2.3**

### Property 20: Preference persistence
*For any* user preference change, the new value SHALL be stored immediately and SHALL persist across app restarts.
**Validates: Requirements 14.4**

## Error Handling

### Error Categories

1. **Data Persistence Errors**
   - Failed to save achievement data
   - Failed to load user progress
   - Corrupted badge or milestone data
   - **Strategy**: Retry with exponential backoff, fallback to cached data, log error for manual recovery

2. **Integration Errors**
   - Module fails to report activity
   - Scoring service unavailable
   - Avatar service unresponsive
   - **Strategy**: Queue events for retry, continue with degraded functionality, notify user only if critical

3. **Calculation Errors**
   - Invalid XP value (negative or NaN)
   - Streak calculation with invalid dates
   - Badge condition evaluation failure
   - **Strategy**: Validate inputs, use safe defaults, log anomalies, prevent data corruption

4. **UI Rendering Errors**
   - Failed to generate share card
   - Animation crash
   - Chart rendering failure
   - **Strategy**: Graceful degradation, show simplified UI, allow user to continue

5. **Notification Errors**
   - Failed to schedule notification
   - Permission denied
   - **Strategy**: Silently fail, respect user preferences, don't block core functionality

### Error Recovery Strategies

```typescript
class AchievementEngine {
  async recordActivity(activity: LearningActivity): Promise<AchievementResult> {
    try {
      // Validate input
      if (activity.xpEarned < 0) {
        throw new ValidationError('XP cannot be negative');
      }
      
      // Process activity
      const result = await this.processActivity(activity);
      
      // Persist changes
      await this.saveWithRetry(result);
      
      return result;
    } catch (error) {
      if (error instanceof ValidationError) {
        // Log and return safe default
        logger.error('Invalid activity data', { activity, error });
        return this.getSafeDefaultResult();
      } else if (error instanceof PersistenceError) {
        // Queue for retry
        await this.queueForRetry(activity);
        // Return optimistic result
        return this.getOptimisticResult(activity);
      } else {
        // Unknown error - log and rethrow
        logger.error('Unexpected error in recordActivity', { error });
        throw error;
      }
    }
  }
  
  private async saveWithRetry(data: any, maxRetries = 3): Promise<void> {
    for (let i = 0; i < maxRetries; i++) {
      try {
        await this.storage.save(data);
        return;
      } catch (error) {
        if (i === maxRetries - 1) throw error;
        await this.delay(Math.pow(2, i) * 1000);
      }
    }
  }
}
```

### Graceful Degradation

When services are unavailable, the system SHALL:
- Continue accepting practice activities (queue for later processing)
- Display cached progress data with "last updated" timestamp
- Show simplified UI without animations if rendering fails
- Allow Quick Start even if recommendations fail (use fallback logic)
- Disable social features if leaderboard service is down

## Testing Strategy

### Unit Testing

Focus on core business logic and data transformations:

- **AchievementEngine**: Test XP calculation, badge unlock logic, milestone detection
- **ProgressTracker**: Test calendar data generation, ability radar calculations, CEFR progress
- **BadgeManager**: Test unlock conditions, progress tracking, badge status
- **StreakManager**: Test streak increment, reset logic, risk detection
- **RecommendationEngine**: Test recommendation selection, priority scoring, time-of-day logic
- **GoalTracker**: Test goal progress updates, achievement detection, deadline tracking

Example unit test:
```typescript
describe('StreakManager', () => {
  it('should increment streak when practicing on consecutive days', () => {
    const manager = new StreakManager();
    manager.recordPractice(new Date('2024-01-01'));
    manager.recordPractice(new Date('2024-01-02'));
    
    const info = manager.getStreakInfo();
    expect(info.currentStreak).toBe(2);
  });
  
  it('should reset streak when missing a day', () => {
    const manager = new StreakManager();
    manager.recordPractice(new Date('2024-01-01'));
    manager.recordPractice(new Date('2024-01-03')); // Skipped 01-02
    
    const info = manager.getStreakInfo();
    expect(info.currentStreak).toBe(1);
  });
});
```

### Property-Based Testing

We will use `fast-check` for property-based testing to verify universal properties across many randomly generated inputs.

**Testing Framework**: fast-check (already used in DuoXX project)
**Configuration**: Minimum 100 iterations per property test

Property tests will be tagged with the format: `**Feature: achievement-motivation, Property {number}: {property_text}**`

Key properties to test:

1. **XP Monotonicity**: Generate random sequences of activities, verify total XP never decreases
2. **Streak Consistency**: Generate random date sequences, verify streak logic
3. **Badge Idempotence**: Generate random unlock sequences, verify badges unlock exactly once
4. **Calendar Completeness**: Generate random date ranges, verify no gaps or duplicates
5. **Milestone Detection**: Generate random progress values, verify milestones trigger at correct thresholds
6. **Progress Consistency**: Generate random activities, verify all visualizations show consistent data
7. **Goal Achievement**: Generate random progress updates, verify goals marked achieved exactly once

Example property test:
```typescript
describe('Property Tests', () => {
  it('**Feature: achievement-motivation, Property 1: XP accumulation monotonicity**', () => {
    fc.assert(
      fc.property(
        fc.array(fc.record({
          xpEarned: fc.integer({ min: 0, max: 100 }),
          moduleId: fc.constantFrom('listening', 'speaking', 'vocab'),
          isCorrect: fc.boolean(),
        })),
        (activities) => {
          const engine = new AchievementEngine();
          let previousTotal = 0;
          
          for (const activity of activities) {
            const result = engine.recordActivity(activity);
            const newTotal = engine.getTotalXP();
            
            // XP should never decrease
            expect(newTotal).toBeGreaterThanOrEqual(previousTotal);
            // XP should increase by exactly the earned amount
            expect(newTotal - previousTotal).toBe(activity.xpEarned);
            
            previousTotal = newTotal;
          }
          
          return true;
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

### Integration Testing

Test interactions between components:

- **Module Integration**: Verify all learning modules can report activities successfully
- **Avatar Integration**: Verify avatar expressions update based on achievement events
- **Scoring Integration**: Verify CEFR level changes trigger milestone celebrations
- **Storage Integration**: Verify data persists and loads correctly across sessions

### UI Testing

Test user-facing components:

- **Quick Start Button**: Verify navigation and timing
- **Achievement Toasts**: Verify animations and display
- **Progress Dashboard**: Verify all visualizations render correctly
- **Badge Gallery**: Verify locked/unlocked states display correctly
- **Share Cards**: Verify image generation and sharing functionality

### Performance Testing

- **Quick Start Response Time**: Verify < 2 second response (Requirement 3.2)
- **Avatar Reaction Time**: Verify < 500ms update (Requirement 1.1, 1.5)
- **Calendar Rendering**: Verify smooth rendering for 90 days of data
- **Radar Chart**: Verify smooth rendering with 6+ dimensions

### Edge Case Testing

- Empty state (new user with no achievements)
- Maximum values (user with 10,000+ XP, 365+ day streak)
- Date boundaries (streak across month/year boundaries)
- Concurrent activities (multiple modules reporting simultaneously)
- Offline mode (activities queued while offline)
- Data migration (upgrading from older achievement data format)
