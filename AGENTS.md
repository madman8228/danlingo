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


## Long-Term Memory (Mandatory)
- Update `PROJECT_MEMORY.md` after each session:
  - What changed (files + intent)
  - What was learned (architecture/behavior)
  - Next steps / open questions
- Keep the memory file concise and current.
- Update `PROJECT_PROGRESS.md` after each completed task so the current implementation status stays visible without reading the whole session log.

## Rule Priority (Mandatory)
- If rules conflict, follow this priority:
  1) Constitutions (Admin UI, UX/Cognitive-Load, Product/Data, Development-Phase, Encoding/Text)
  2) Closed-Loop Autopilot Protocol
  3) Style examples/snippets
- Development-stage default is architecture-first: do not use workaround/fallback paths as a substitute for fixing root design issues.
- Exception path (rare): if a temporary mitigation is unavoidable for a blocker, document scope, owner, and removal date in task notes before merge.

## Closed-Loop Autopilot Protocol (Default)

When the user gives a task, run this default execution flow unless the user asks for a different process:

1. Scope and acceptance
- Translate the user request into explicit acceptance criteria.
- If details are missing but can be inferred from repo context, proceed without blocking.

2. Parallel execution strategy
- Split work into non-conflicting subtasks (UI, API, data, tests, docs).
- Execute independent reads/checks in parallel whenever possible.

3. Implementation
- Apply production-safe, root-cause-first changes aligned with target architecture.
- Do not prefer "minimal patch" if it preserves a known bad data model or creates recurring cleanup debt.
- Prefer simple operator UX over exposing internal technical controls.

4. Verification gate (must run before delivery)
- Run targeted syntax/type checks.
- Run relevant tests (unit/integration/e2e or feature smoke path).
- Validate key user path end-to-end for the changed feature.
- Fix failures before final response.

5. Delivery contract
- Report: changed files, key behavior changes, commands/tests run, results.
- Include known risks and concrete next-step options only when needed.

6. Session persistence
- Follow `Long-Term Memory (Mandatory)` exactly.

Reference: `AUTOPILOT_WORKFLOW.md`

## Build Commands

All commands below are expected to run in `duoxx/` unless explicitly stated otherwise.

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

### Admin UI Constitution (Mandatory)
- Scope: applies to all admin pages (global mandatory), not only `/admin/pipeline`.
- Flat layout first: avoid nested "card inside card" container stacks.
- Do not use "big ring wrapping small rings" visual patterns in admin pages.
- Prefer single-layer row/list presentation with direct actions over multi-level boxed wrappers.
- If hierarchy must be shown, use text metadata (e.g., `Unit/Lesson`) instead of extra nested frames.

### UX/Cognitive-Load Constitution (Mandatory)
- Core metric: minimize cognitive load is a hard requirement for all UI/UX changes.
- One-screen rule: each screen must have one dominant user goal and one visually dominant primary action.
- Decision minimization: avoid exposing many peer-level choices at once; prefer progressive disclosure for low-frequency actions.
- Entry governance: do not add a new top-level entry unless it replaces, merges, or clearly outperforms an existing one.
- Mobile ergonomics: high-frequency actions should be placed in easy-to-reach lower zones; low-frequency actions should be moved away from prime tap areas.
- Naming clarity: use user-task wording over internal/system wording; avoid ambiguous labels that create duplicate mental models.
- Delivery gate: every UI task response must include a brief "cognitive-load check" statement (what was reduced, what was deferred/hidden, and why).

### Product/Data Constitution (Mandatory)
- Root-cause over quick patch: for new-project foundations, do not accept tactical fixes that create long-term debt.
- Source-first correction: if issue originates from raw source assets (CSV/Markdown/etc.), fix source files and re-import; runtime patching is only temporary incident mitigation.
- Contract-first publishing: data must satisfy exercise contract before entering DB; reject invalid rows in lint/import.
- Fill-in-the-blank must be structured: avoid plain marker-dependent strings as the only source of truth.

### Development-Phase Constitution (Mandatory)
- Current stage default: active development. Do not optimize for minimal diff if it harms architecture quality.
- Architecture and code simplicity first: prefer clean boundaries and readable code over short-term patching.
- No debt by default: do not introduce temporary structures that are expected to become long-term burden.
- No workaround/fallback padding by default: do not add "just-in-case" guard paths that hide root-cause issues during development.
- Fix the model, not the symptom: if current structure is wrong, refactor toward the correct design instead of layering compensating logic.

### Encoding/Text Constitution (Mandatory)
- UTF-8 first: all source code, JSON/Markdown docs, and user-facing copy MUST be saved and reviewed as UTF-8 text.
- No mojibake strings in shipped code: strings that look like `鏀惰棌/閲婁箟/渚嬪彞/姝...` MUST be treated as defects and fixed before merge.
- Any user-facing Chinese copy change MUST run a targeted scan on touched files before delivery (search for mojibake patterns and replacement char `�`).
- Do not use shell append/replace flows that may inject control chars or escape corruption into docs/content; prefer direct file patch edits.
- If mojibake is found, block release for the affected page/API until corrected and re-verified in runtime view.

### File Organization
```
src/
|- components/     # Reusable UI components
|- models/         # TypeScript interfaces and types
|- services/       # Business logic and state management
|- validators/     # Input validation functions
|- storage/        # Data persistence layer
|- data/           # Static data and course content
|- hooks/          # Custom React hooks
`- constants/      # App constants and themes
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

