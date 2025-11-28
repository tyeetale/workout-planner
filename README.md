# Workout Planner - PPLING Routine Generator

A Python CLI tool that generates workout schedules for a PPLING (Push, Pull, Legs, Push, Pull, Legs, Rest) routine and exports them as markdown files for Obsidian.

## Features

- **PPLING Routine**: 6-day workout split (Push, Pull, Legs, Push, Pull, Legs) + Rest day
- **Exercise Management**: Add/remove exercises for each workout type
- **Randomization**: Randomize exercise order within each day
- **Obsidian Integration**: Generate markdown files ready for Obsidian
- **Progress Tracking**: Log completed workouts from markdown files or interactive input
- **Progress Analysis**: Analyze your progress with automatic progression tracking
- **AI-Powered Recommendations**: Get AI suggestions for progression and routine optimization (optional)

## Installation

```bash
# Install optional dependencies for AI features (optional)
pip install -r requirements.txt

# Make the script executable
chmod +x workout_planner.py

# For AI analysis, set your OpenAI API key:
export OPENAI_API_KEY="your-api-key-here"
```

**Note**: The core functionality works without any external dependencies. Only install `openai` if you want AI-powered analysis features. All other features (generation, logging, basic analysis) work with just Python standard library.

## Usage

### Generate Workout Schedule

Generate a weekly schedule and output to a markdown file:

```bash
python workout_planner.py generate -o schedule.md
```

Generate separate daily notes for Obsidian:

```bash
python workout_planner.py generate --daily-notes --obsidian-vault /path/to/your/vault
```

Or generate daily notes in a local directory:

```bash
python workout_planner.py generate --daily-notes -o ./daily_notes/
```

### Manage Exercises

Add an exercise:

```bash
python workout_planner.py add push "Bench Press"
python workout_planner.py add pull "Pull-ups"
python workout_planner.py add legs "Squats"
```

Remove an exercise:

```bash
python workout_planner.py remove push "Bench Press"
```

List all exercises:

```bash
python workout_planner.py list
```

List exercises for a specific type:

```bash
python workout_planner.py list --type push
```

### View Schedule

Preview the current week's schedule:

```bash
python workout_planner.py schedule
```

Generate schedule starting from a specific date:

```bash
python workout_planner.py generate --start-date 2024-01-15
```

Keep exercises in original order (no randomization):

```bash
python workout_planner.py generate --no-randomize
```

### Log Workouts

After completing a workout in Obsidian, log it back to track progress:

**From markdown file:**
```bash
python workout_planner.py log --file "2024-01-15 - Push.md"
```

**Interactive logging:**
```bash
python workout_planner.py log --interactive
```

The markdown parser automatically extracts:
- Date from filename or content
- Workout type (Push/Pull/Legs)
- Exercises with sets, reps, and weights from tables

### Analyze Progress

Get insights on your workout progress:

```bash
# Analyze last 30 days (default)
python workout_planner.py analyze

# Analyze last 60 days
python workout_planner.py analyze --days 60

# Save analysis to file
python workout_planner.py analyze --output progress_report.md

# Disable AI analysis (faster, basic stats only)
python workout_planner.py analyze --no-ai
```

The analysis includes:
- Total workouts logged
- Exercise-by-exercise progression (weight/volume changes)
- AI-powered recommendations (if API key is set)

### Get Progression Suggestions

Get specific suggestions for an exercise:

```bash
python workout_planner.py suggest "Bench Press"
```

This will show:
- Current weight/reps
- Suggested next weight/reps
- Reasoning for the suggestion

## Data Storage

Workout data is stored in `~/.workout_planner/`:
- `workouts.json` - Your exercise lists
- `progress.json` - Workout history and logged workouts

## Obsidian Integration

### Weekly Schedule

Generate a single markdown file with the full week:

```bash
python workout_planner.py generate -o ~/Documents/Obsidian/Workouts/Week.md
```

### Daily Notes

Generate separate daily notes that you can use in Obsidian's Daily Notes:

```bash
python workout_planner.py generate --daily-notes --obsidian-vault ~/Documents/Obsidian
```

This will create files like:
- `2024-01-15 - Push.md`
- `2024-01-16 - Pull.md`
- etc.

Each daily note includes:
- Exercise list with tables for logging sets/reps/weight
- Space for notes
- Proper markdown formatting for Obsidian

## Example Workflow

1. **Set up your exercises:**
   ```bash
   python workout_planner.py add push "Bench Press"
   python workout_planner.py add push "Overhead Press"
   # ... add more exercises
   ```

2. **Generate weekly schedule:**
   ```bash
   python workout_planner.py generate --daily-notes --obsidian-vault ~/Documents/Obsidian
   ```

3. **Open in Obsidian** and log your workouts in the markdown files

4. **Log completed workouts:**
   ```bash
   # After filling in your workout data in Obsidian
   python workout_planner.py log --file "2024-01-15 - Push.md"
   ```

5. **Analyze your progress:**
   ```bash
   python workout_planner.py analyze --days 30
   ```

6. **Get progression suggestions:**
   ```bash
   python workout_planner.py suggest "Bench Press"
   ```

## Markdown File Format

The planner can parse markdown files with this structure:

```markdown
# Monday, January 15, 2024

## Workout: Push

### Exercises

#### 1. Bench Press

| Set | Weight | Reps | Notes |
|-----|--------|------|-------|
| 1   | 135    | 10   |       |
| 2   | 135    | 10   |       |
| 3   | 135    | 8    |       |
```

The parser extracts:
- Date from filename (`YYYY-MM-DD`) or content
- Workout type from `## Workout: Type` header
- Exercise names from `#### N. Exercise Name` headers
- Sets/reps/weight from markdown tables

## Default Exercises

The planner comes with default exercises for each type:

**Push:**
- Bench Press
- Overhead Press
- Incline Dumbbell Press
- Lateral Raises
- Tricep Dips
- Cable Flyes

**Pull:**
- Pull-ups
- Barbell Rows
- Cable Rows
- Face Pulls
- Barbell Curls
- Hammer Curls

**Legs:**
- Squats
- Romanian Deadlifts
- Leg Press
- Leg Curls
- Calf Raises
- Bulgarian Split Squats

Customize these by adding/removing exercises as needed!
