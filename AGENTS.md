# AGENTS.md

This file contains guidelines and commands for agentic coding agents working in the DuoXX Expo React Native codebase.

## Project Overview

DuoXX is a gamified language learning app built with Expo and React Native. It features:
- Multiple exercise types (multiple choice, fill blank, matching, sorting, etc.)
- Avatar system with expressions and animations
- Progress tracking with XP, hearts, and streaks
- Scene-based learning courses
- Achievement system
- Property-based testing with fast-check

## Build Commands

### Development
- `npm start` - Start Expo development server
- `npm run android` - Run on Android device/emulator
- `npm run ios` - Run on iOS device/simulator
- `npm run web` - Run in web browser

### Code Quality
- `npm run lint` - Run ESLint for code linting
- `npm run test` - Run all Jest tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Run tests with coverage report

### Running Single Tests
```bash
# Run a specific test file
npm test -- src/models/types.test.ts

# Run tests matching a pattern
npm test -- --testNamePattern="Enum"

# Run tests in watch mode for a specific file
npm run test:watch -- src/models/types.test.ts
```

## Code Style Guidelines

### TypeScript Configuration
- Strict mode enabled (`"strict": true`)
- Path alias `@/*` points to project root
- All files must be included in tsconfig

### Import Organization
```typescript
// 1. React/React Native imports
import React, { useState } from 'react';
import { View, Text } from 'react-native';

// 2. Expo imports
import { useRouter } from 'expo-router';

// 3. Internal imports (use @/* alias)
import { ExerciseType } from '@/models/types';
import { validateMultipleChoice } from '@/validators';

// 4. Type-only imports (prefer for types only)
import type { ExerciseContent } from '@/models/exercise';
```

### Naming Conventions
- **Files**: kebab-case for components (`multiple-choice-exercise.tsx`), camelCase for services (`lessonEngine.ts`)
- **Components**: PascalCase (`MultipleChoiceExercise`)
- **Functions/Variables**: camelCase (`validateAnswer`, `currentIndex`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_HEARTS`, `DEFAULT_XP`)
- **Enums**: PascalCase with descriptive values (`ExerciseType.MULTIPLE_CHOICE`)
- **Interfaces**: Prefix with `I` for service interfaces (`ILessonEngine`), no prefix for component props

### Component Structure
```typescript
/**
 * Component description
 * Requirements: X.X
 */

import React, { useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';

export interface ComponentProps {
  // Props with TypeScript types
  requiredProp: string;
  optionalProp?: number;
}

export function Component({ requiredProp, optionalProp = 0 }: ComponentProps) {
  // State hooks
  const [state, setState] = useState<Type>(initialValue);

  // Handler functions
  const handlePress = () => {
    // Implementation
  };

  // Render
  return (
    <View style={styles.container}>
      <Text>{requiredProp}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    // Style properties
  },
});
```

### Service Class Structure
```typescript
/**
 * Service description
 * Requirements: X.X, Y.Y
 */

import { DependencyType } from '../models/types';

export interface IServiceName {
  method1(param: Type): ReturnType;
  method2(): void;
}

export class ServiceName implements IServiceName {
  private property: Type;

  constructor(dependency?: DependencyType) {
    this.property = dependency ?? defaultValue;
  }

  public method1(param: Type): ReturnType {
    // Implementation
  }

  private helperMethod(): void {
    // Implementation
  }
}
```

### Error Handling
- Use descriptive error messages
- Throw errors for invalid states
- Use proper error types
```typescript
if (!exercise) {
  throw new Error('No current exercise to submit answer for');
}

if (exercise.type !== ExerciseType.MULTIPLE_CHOICE) {
  throw new Error('Answer type does not match exercise type');
}
```

### Testing Guidelines
- Use Jest with ts-jest preset
- Property-based testing with fast-check for complex logic
- Test files: `*.test.ts` in same directory as source
- Coverage excludes `index.ts` and test files
- Test timeout: 30 seconds for property-based tests

```typescript
describe('Module Name', () => {
  describe('Feature Group', () => {
    it('should behave correctly', () => {
      // Arrange
      const input = createTestInput();
      
      // Act
      const result = functionUnderTest(input);
      
      // Assert
      expect(result).toBe(expected);
    });

    it('should handle property-based tests', () => {
      fc.assert(
        fc.property(fc.integer(), (n) => {
          return typeof n === 'number';
        }),
        { numRuns: 100 }
      );
    });
  });
});
```

### Styling Guidelines
- Use StyleSheet.create for component styles
- Follow the existing color scheme from `constants/theme.ts`
- Use semantic color names from Colors object
- Platform-specific fonts from Fonts object
- Consistent spacing and sizing

### File Organization
```
src/
├── components/     # Reusable UI components
├── models/        # TypeScript interfaces and types
├── services/      # Business logic and state management
├── validators/    # Input validation functions
├── storage/       # Data persistence layer
├── data/         # Static data and course content
├── hooks/        # Custom React hooks
└── constants/    # App constants and themes
```

### Comments and Documentation
- Use JSDoc style comments for all public interfaces
- Include requirement numbers in component descriptions
- Comment complex business logic
- No inline comments for obvious code

### Git Workflow
- Branch naming: `feature/description`, `fix/description`
- Commit messages: conventional commits with scope
- Always run lint and tests before committing
- Use semantic versioning for releases

## Development Notes

- The app uses Expo Router for navigation
- State management is handled through service classes
- AsyncStorage is used for data persistence
- All exercise types have corresponding validators
- Avatar system supports multiple age groups and expressions
- Progress tracking includes XP, hearts, streaks, and achievements


## Achievement System Guidelines

### Overview
The Achievement and Motivation System provides engagement features including XP, badges, milestones, streaks, and progress tracking.

### Core Services
- `achievementEngine.ts` - Central service for processing learning activities
- `streakManager.ts` - Daily streak tracking
- `badgeManager.ts` - Badge unlocking and progress
- `progressTracker.ts` - Historical progress tracking
- `goalTracker.ts` - Personal learning goals

### Integration Pattern
All learning modules should report activities using `achievementIntegration.ts`:

```typescript
import { recordLearningActivity } from '@/src/services/achievementIntegration';

// After exercise completion
await recordLearningActivity(
  userId,
  'module-id',
  'exercise-type',
  isCorrect,
  xpEarned,
  { /* optional metadata */ }
);
```

### Avatar Integration
Update avatar expressions based on performance:

```typescript
import { updateAvatarAfterExercise } from '@/src/services/avatarAchievementIntegration';

await updateAvatarAfterExercise(
  userId,
  isCorrect,
  consecutiveCorrect,
  responseTimeMs,
  difficulty
);
```

### Performance Requirements
- Quick Start response: <2 seconds
- Avatar reactions: <500ms
- Achievement toast display: <500ms

### Documentation
- `ACHIEVEMENT_SYSTEM_SUMMARY.md` - System overview
- `ACHIEVEMENT_INTEGRATION_GUIDE.md` - Integration instructions
- `ACHIEVEMENT_TESTING_GUIDE.md` - Testing guidelines
- `ACHIEVEMENT_SYSTEM_FINAL_SUMMARY.md` - Complete implementation summary

### Key Files
- Models: `src/models/achievement.ts`
- Storage: `src/storage/achievementStorage.ts`
- Data: `src/data/achievements/`
- Components: `src/components/feedback/`, `src/components/progress/`
- Screens: `app/progress-dashboard.tsx`, `app/achievements.tsx`, `app/goal-settings.tsx`
