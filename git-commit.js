#!/usr/bin/env node

/**
 * Git Commit Helper Script
 * Provides an interactive interface for creating conventional commits with proper validation
 */

const { execSync } = require('child_process');
const readline = require('readline');

// Conventional commit types
const COMMIT_TYPES = {
  'feat': 'A new feature',
  'fix': 'A bug fix', 
  'docs': 'Documentation only changes',
  'style': 'Changes that do not affect the meaning of the code',
  'refactor': 'A code change that neither fixes a bug nor adds a feature',
  'perf': 'A code change that improves performance',
  'test': 'Adding missing tests or correcting existing tests',
  'build': 'Changes that affect the build system or external dependencies',
  'ci': 'Changes to our CI configuration files and scripts',
  'chore': 'Other changes that don\'t modify src or test files',
  'revert': 'Reverts a previous commit'
};

// Create readline interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

/**
 * Prompt user for input
 */
function prompt(question) {
  return new Promise((resolve) => {
    rl.question(question, resolve);
  });
}

/**
 * Run git command and return output
 */
function runGitCommand(command) {
  try {
    return execSync(command, { encoding: 'utf8' }).trim();
  } catch (error) {
    console.error(`Error running git command: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Check if there are changes to commit
 */
function checkForChanges() {
  try {
    const status = runGitCommand('git status --porcelain');
    return status.length > 0;
  } catch (error) {
    console.error('Error checking git status');
    process.exit(1);
  }
}

/**
 * Get staged and unstaged changes
 */
function getChanges() {
  const staged = runGitCommand('git diff --cached --name-only');
  const unstaged = runGitCommand('git diff --name-only');
  const untracked = runGitCommand('git ls-files --others --exclude-standard');
  
  return {
    staged: staged ? staged.split('\n') : [],
    unstaged: unstaged ? unstaged.split('\n') : [],
    untracked: untracked ? untracked.split('\n') : []
  };
}

/**
 * Display changes to user
 */
function displayChanges(changes) {
  console.log('\n📋 Current Changes:');
  
  if (changes.staged.length > 0) {
    console.log('\n✅ Staged files:');
    changes.staged.forEach(file => console.log(`   ${file}`));
  }
  
  if (changes.unstaged.length > 0) {
    console.log('\n⚠️  Unstaged files:');
    changes.unstaged.forEach(file => console.log(`   ${file}`));
  }
  
  if (changes.untracked.length > 0) {
    console.log('\n📄 Untracked files:');
    changes.untracked.forEach(file => console.log(`   ${file}`));
  }
}

/**
 * Show commit type options
 */
function showCommitTypes() {
  console.log('\n🏷️  Commit Types:');
  Object.entries(COMMIT_TYPES).forEach(([type, description]) => {
    console.log(`   ${type.padEnd(8)} - ${description}`);
  });
}

/**
 * Validate commit message
 */
function validateCommitMessage(message) {
  if (!message || message.trim().length === 0) {
    return 'Commit message cannot be empty';
  }
  
  if (message.length > 72) {
    return 'Commit message should be 72 characters or less';
  }
  
  // Check for conventional commit format
  const conventionalPattern = /^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+/;
  if (!conventionalPattern.test(message)) {
    return 'Commit message should follow conventional format: type(scope): description';
  }
  
  return null;
}

/**
 * Stage files interactively
 */
async function stageFiles(changes) {
  if (changes.unstaged.length === 0 && changes.untracked.length === 0) {
    return;
  }
  
  console.log('\n📦 Select files to stage (comma-separated numbers, or "all"):');
  
  const allFiles = [
    ...changes.unstaged.map(file => ({ file, type: 'unstaged' })),
    ...changes.untracked.map(file => ({ file, type: 'untracked' }))
  ];
  
  allFiles.forEach((item, index) => {
    const icon = item.type === 'unstaged' ? '⚠️' : '📄';
    console.log(`   ${index + 1}. ${icon} ${item.file}`);
  });
  
  const selection = await prompt('\nFiles to stage: ');
  
  if (selection.toLowerCase() === 'all') {
    runGitCommand('git add .');
    console.log('✅ All files staged');
  } else {
    const indices = selection.split(',').map(s => parseInt(s.trim()) - 1);
    indices.forEach(index => {
      if (index >= 0 && index < allFiles.length) {
        runGitCommand(`git add "${allFiles[index].file}"`);
      }
    });
    console.log('✅ Selected files staged');
  }
}

/**
 * Main commit function
 */
async function createCommit() {
  try {
    console.log('🔧 Git Commit Helper\n');
    
    // Check for changes
    if (!checkForChanges()) {
      console.log('ℹ️  No changes to commit');
      rl.close();
      return;
    }
    
    // Get and display changes
    const changes = getChanges();
    displayChanges(changes);
    
    // Ask to stage files if needed
    if (changes.unstaged.length > 0 || changes.untracked.length > 0) {
      const shouldStage = await prompt('\n📦 Do you want to stage files? (y/n): ');
      if (shouldStage.toLowerCase() === 'y') {
        await stageFiles(changes);
      }
    }
    
    // Show commit types
    showCommitTypes();
    
    // Get commit type
    const type = await prompt('\n🏷️  Commit type: ');
    if (!COMMIT_TYPES[type]) {
      console.error('❌ Invalid commit type');
      rl.close();
      return;
    }
    
    // Get scope (optional)
    const scope = await prompt('📁 Scope (optional, press Enter to skip): ');
    
    // Get description
    const description = await prompt('📝 Description: ');
    if (!description.trim()) {
      console.error('❌ Description is required');
      rl.close();
      return;
    }
    
    // Get body (optional)
    const body = await prompt('📄 Body (optional, press Enter to skip): ');
    
    // Get breaking change flag
    const breaking = await prompt('💥 Breaking change? (y/n): ');
    
    // Build commit message
    let commitMessage = type;
    if (scope.trim()) {
      commitMessage += `(${scope.trim()})`;
    }
    commitMessage += `: ${description.trim()}`;
    
    if (breaking.toLowerCase() === 'y') {
      commitMessage += '\n\nBREAKING CHANGE: ' + (body.trim() || 'This change introduces breaking changes');
    } else if (body.trim()) {
      commitMessage += `\n\n${body.trim()}`;
    }
    
    // Validate commit message
    const validationError = validateCommitMessage(commitMessage);
    if (validationError) {
      console.error(`❌ ${validationError}`);
      rl.close();
      return;
    }
    
    // Show final commit message
    console.log('\n📋 Final commit message:');
    console.log('─'.repeat(50));
    console.log(commitMessage);
    console.log('─'.repeat(50));
    
    // Confirm commit
    const confirm = await prompt('\n✅ Commit? (y/n): ');
    if (confirm.toLowerCase() !== 'y') {
      console.log('❌ Commit cancelled');
      rl.close();
      return;
    }
    
    // Create commit
    runGitCommand(`git commit -m "${commitMessage.replace(/"/g, '\\"')}"`);
    console.log('✅ Commit created successfully!');
    
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
  } finally {
    rl.close();
  }
}

// Run the commit helper
if (require.main === module) {
  createCommit();
}

module.exports = { createCommit, validateCommitMessage, COMMIT_TYPES };