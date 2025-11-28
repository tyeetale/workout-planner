#!/usr/bin/env python3
"""
Workout Planner - PPLING Routine Generator
Generates markdown workout schedules for Obsidian
"""

import json
import random
import argparse
import re
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class WorkoutPlanner:
    def __init__(self, data_dir: Path = Path.home() / ".workout_planner"):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
        self.workouts_file = self.data_dir / "workouts.json"
        self.progress_file = self.data_dir / "progress.json"
        
        # PPLING routine mapping
        self.day_types = {
            0: "Push",    # Monday
            1: "Pull",    # Tuesday
            2: "Legs",    # Wednesday
            3: "Push",    # Thursday
            4: "Pull",    # Friday
            5: "Legs",    # Saturday
            6: "Rest"     # Sunday
        }
        
        self.load_data()
    
    def load_data(self):
        """Load workouts and progress from JSON files"""
        if self.workouts_file.exists():
            with open(self.workouts_file, 'r') as f:
                data = json.load(f)
                self.workouts = data.get('workouts', {
                    'push': [],
                    'pull': [],
                    'legs': []
                })
        else:
            # Initialize with default exercises
            self.workouts = {
                'push': [
                    'Bench Press',
                    'Overhead Press',
                    'Incline Dumbbell Press',
                    'Lateral Raises',
                    'Tricep Dips',
                    'Cable Flyes'
                ],
                'pull': [
                    'Pull-ups',
                    'Barbell Rows',
                    'Cable Rows',
                    'Face Pulls',
                    'Barbell Curls',
                    'Hammer Curls'
                ],
                'legs': [
                    'Squats',
                    'Romanian Deadlifts',
                    'Leg Press',
                    'Leg Curls',
                    'Calf Raises',
                    'Bulgarian Split Squats'
                ]
            }
            self.save_workouts()
        
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                self.progress = json.load(f)
        else:
            self.progress = []
    
    def save_workouts(self):
        """Save workouts to JSON file"""
        with open(self.workouts_file, 'w') as f:
            json.dump({'workouts': self.workouts}, f, indent=2)
    
    def save_progress(self):
        """Save progress to JSON file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def add_exercise(self, workout_type: str, exercise: str):
        """Add an exercise to a workout type"""
        workout_type = workout_type.lower()
        if workout_type not in ['push', 'pull', 'legs']:
            raise ValueError(f"Invalid workout type: {workout_type}. Must be 'push', 'pull', or 'legs'")
        
        if exercise not in self.workouts[workout_type]:
            self.workouts[workout_type].append(exercise)
            self.save_workouts()
            return True
        return False
    
    def remove_exercise(self, workout_type: str, exercise: str):
        """Remove an exercise from a workout type"""
        workout_type = workout_type.lower()
        if workout_type not in ['push', 'pull', 'legs']:
            raise ValueError(f"Invalid workout type: {workout_type}")
        
        if exercise in self.workouts[workout_type]:
            self.workouts[workout_type].remove(exercise)
            self.save_workouts()
            return True
        return False
    
    def list_exercises(self, workout_type: Optional[str] = None):
        """List exercises for a workout type or all types"""
        if workout_type:
            workout_type = workout_type.lower()
            if workout_type not in ['push', 'pull', 'legs']:
                raise ValueError(f"Invalid workout type: {workout_type}")
            return {workout_type: self.workouts[workout_type]}
        return self.workouts
    
    def generate_week_schedule(self, start_date: Optional[datetime] = None, randomize: bool = True) -> Dict:
        """Generate a week's workout schedule"""
        if start_date is None:
            # Start from next Monday
            today = datetime.now()
            days_ahead = (7 - today.weekday()) % 7
            if days_ahead == 0:  # If today is Monday
                days_ahead = 7
            start_date = today + timedelta(days=days_ahead)
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        schedule = {}
        for day_offset in range(7):
            current_date = start_date + timedelta(days=day_offset)
            day_type = self.day_types[day_offset]
            
            if day_type == "Rest":
                schedule[current_date] = {
                    'day': day_type,
                    'exercises': []
                }
            else:
                exercises = self.workouts[day_type.lower()].copy()
                if randomize:
                    random.shuffle(exercises)
                
                schedule[current_date] = {
                    'day': day_type,
                    'exercises': exercises
                }
        
        return schedule
    
    def generate_markdown(self, schedule: Dict, output_path: Optional[Path] = None) -> str:
        """Generate markdown content for Obsidian"""
        markdown_lines = []
        
        # Header
        start_date = min(schedule.keys())
        end_date = max(schedule.keys())
        markdown_lines.append(f"# Workout Schedule: {start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}")
        markdown_lines.append("")
        markdown_lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        markdown_lines.append("")
        
        # Weekly overview
        markdown_lines.append("## Weekly Overview")
        markdown_lines.append("")
        markdown_lines.append("| Day | Type | Exercises |")
        markdown_lines.append("|-----|------|-----------|")
        
        for date in sorted(schedule.keys()):
            day_info = schedule[date]
            day_name = date.strftime('%A')
            day_type = day_info['day']
            exercise_count = len(day_info['exercises'])
            markdown_lines.append(f"| {day_name} | {day_type} | {exercise_count} exercises |")
        
        markdown_lines.append("")
        
        # Daily breakdown
        markdown_lines.append("## Daily Workouts")
        markdown_lines.append("")
        
        for date in sorted(schedule.keys()):
            day_info = schedule[date]
            day_name = date.strftime('%A')
            day_type = day_info['day']
            
            markdown_lines.append(f"### {day_name}, {date.strftime('%B %d, %Y')} - {day_type}")
            markdown_lines.append("")
            
            if day_type == "Rest":
                markdown_lines.append("- **Rest Day** - Recovery and rest")
            else:
                markdown_lines.append("#### Exercises:")
                markdown_lines.append("")
                for i, exercise in enumerate(day_info['exercises'], 1):
                    markdown_lines.append(f"{i}. **{exercise}**")
                    markdown_lines.append("   - Sets: ")
                    markdown_lines.append("   - Reps: ")
                    markdown_lines.append("   - Weight: ")
                    markdown_lines.append("")
            
            markdown_lines.append("---")
            markdown_lines.append("")
        
        markdown_content = "\n".join(markdown_lines)
        
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(markdown_content)
        
        return markdown_content
    
    def generate_daily_note(self, date: datetime, schedule: Dict) -> str:
        """Generate a single daily workout note for Obsidian"""
        day_info = schedule[date]
        day_name = date.strftime('%A')
        day_type = day_info['day']
        
        markdown_lines = []
        markdown_lines.append(f"# {day_name}, {date.strftime('%B %d, %Y')}")
        markdown_lines.append("")
        markdown_lines.append(f"## Workout: {day_type}")
        markdown_lines.append("")
        
        if day_type == "Rest":
            markdown_lines.append("- **Rest Day** - Recovery and rest")
        else:
            markdown_lines.append("### Exercises")
            markdown_lines.append("")
            for i, exercise in enumerate(day_info['exercises'], 1):
                markdown_lines.append(f"#### {i}. {exercise}")
                markdown_lines.append("")
                markdown_lines.append("| Set | Weight | Reps | Notes |")
                markdown_lines.append("|-----|--------|------|-------|")
                markdown_lines.append("| 1   |        |      |       |")
                markdown_lines.append("| 2   |        |      |       |")
                markdown_lines.append("| 3   |        |      |       |")
                markdown_lines.append("| 4   |        |      |       |")
                markdown_lines.append("")
        
        markdown_lines.append("---")
        markdown_lines.append("")
        markdown_lines.append("## Notes")
        markdown_lines.append("")
        
        return "\n".join(markdown_lines)
    
    def log_workout(self, date: datetime, day_type: str, exercises: List[Dict]):
        """Log a completed workout"""
        workout_log = {
            'date': date.isoformat(),
            'day_type': day_type,
            'exercises': exercises
        }
        self.progress.append(workout_log)
        self.save_progress()
    
    def get_progress_summary(self, days: int = 30) -> List[Dict]:
        """Get progress summary for the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            log for log in self.progress
            if datetime.fromisoformat(log['date']) >= cutoff_date
        ]
    
    def parse_markdown_workout(self, markdown_path: Path) -> Optional[Dict]:
        """Parse a markdown workout file and extract workout data"""
        try:
            content = markdown_path.read_text()
            
            # Extract date from filename or content
            workout_date = None
            
            # Try filename first (YYYY-MM-DD format)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', markdown_path.name)
            if date_match:
                try:
                    workout_date = datetime.strptime(date_match.group(1), '%Y-%m-%d')
                except ValueError:
                    pass
            
            # Try content for YYYY-MM-DD format
            if not workout_date:
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
                if date_match:
                    try:
                        workout_date = datetime.strptime(date_match.group(1), '%Y-%m-%d')
                    except ValueError:
                        pass
            
            # Try parsing date from header (e.g., "Monday, December 01, 2025")
            if not workout_date:
                date_match = re.search(r'([A-Za-z]+day),\s+([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})', content)
                if date_match:
                    try:
                        from dateutil import parser
                        date_str = date_match.group(0)
                        workout_date = parser.parse(date_str)
                    except (ImportError, ValueError):
                        # Fallback: try manual parsing
                        try:
                            month_name = date_match.group(2)
                            day = int(date_match.group(3))
                            year = int(date_match.group(4))
                            month_map = {
                                'january': 1, 'february': 2, 'march': 3, 'april': 4,
                                'may': 5, 'june': 6, 'july': 7, 'august': 8,
                                'september': 9, 'october': 10, 'november': 11, 'december': 12
                            }
                            month = month_map.get(month_name.lower())
                            if month:
                                workout_date = datetime(year, month, day)
                        except (ValueError, KeyError):
                            pass
            
            if not workout_date:
                return None
            
            # Extract workout type
            day_type_match = re.search(r'## Workout:\s*(\w+)', content)
            if not day_type_match:
                return None
            
            day_type = day_type_match.group(1)
            
            # Extract exercises with sets
            exercises = []
            # Match exercise header and content until next exercise or section divider
            exercise_pattern = r'####\s*\d+\.\s*(.+?)\n\n((?:[^#]|#(?!###))*)'
            
            for match in re.finditer(exercise_pattern, content, re.DOTALL):
                exercise_name = match.group(1).strip()
                exercise_content = match.group(2)
                
                # Parse sets from table - look for data rows (skip header row)
                sets = []
                # Match table rows: | number | weight | reps | notes |
                # Skip header row by checking if second column is numeric
                table_pattern = r'\|\s*(\d+)\s*\|\s*([\d.\s]+)\s*\|\s*(\d+)\s*\|'
                
                for set_match in re.finditer(table_pattern, exercise_content):
                    set_num = int(set_match.group(1))
                    weight_str = set_match.group(2).strip()
                    reps_str = set_match.group(3).strip()
                    
                    # Skip header row
                    if weight_str.lower() in ['weight', ''] or reps_str.lower() in ['reps', '']:
                        continue
                    
                    try:
                        weight = float(weight_str) if weight_str else 0
                        reps = int(reps_str) if reps_str else 0
                        if weight > 0 and reps > 0:
                            sets.append({
                                'set': set_num,
                                'weight': weight,
                                'reps': reps
                            })
                    except ValueError:
                        continue
                
                if sets:
                    exercises.append({
                        'name': exercise_name,
                        'sets': sets
                    })
            
            if exercises:
                return {
                    'date': workout_date.isoformat(),
                    'day_type': day_type,
                    'exercises': exercises
                }
            
            return None
        except Exception as e:
            print(f"Error parsing markdown: {e}")
            return None
    
    def log_workout_from_markdown(self, markdown_path: Path):
        """Log a workout from a markdown file"""
        workout_data = self.parse_markdown_workout(markdown_path)
        if workout_data:
            # Check if workout already exists for this date
            existing = [
                w for w in self.progress
                if w['date'] == workout_data['date'] and w['day_type'] == workout_data['day_type']
            ]
            
            if existing:
                # Update existing workout
                idx = self.progress.index(existing[0])
                self.progress[idx] = workout_data
                print(f"Updated workout for {workout_data['date']}")
            else:
                # Add new workout
                self.progress.append(workout_data)
                print(f"Logged workout for {workout_data['date']}")
            
            self.save_progress()
            return True
        else:
            # Provide more helpful error message
            print(f"Failed to parse workout from {markdown_path}")
            print("Make sure the file contains:")
            print("  - A date in YYYY-MM-DD format (in filename or content)")
            print("  - A '## Workout: Type' header")
            print("  - Exercise tables with weight and reps filled in")
        return False
    
    def log_workout_interactive(self, date: Optional[datetime] = None, day_type: Optional[str] = None):
        """Interactively log a workout"""
        if date is None:
            date_str = input("Enter workout date (YYYY-MM-DD) or press Enter for today: ").strip()
            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            else:
                date = datetime.now()
        
        if day_type is None:
            day_type = input("Enter workout type (push/pull/legs): ").strip().lower()
        
        exercises = []
        print(f"\nLogging {day_type} workout for {date.strftime('%Y-%m-%d')}")
        print("Enter exercises (press Enter with empty name to finish):\n")
        
        while True:
            exercise_name = input("Exercise name: ").strip()
            if not exercise_name:
                break
            
            sets = []
            print(f"  Enter sets for {exercise_name} (weight x reps, empty to finish):")
            set_num = 1
            while True:
                set_input = input(f"    Set {set_num}: ").strip()
                if not set_input:
                    break
                
                # Parse "weight x reps" or "weight reps"
                match = re.match(r'([\d.]+)\s*x?\s*(\d+)', set_input)
                if match:
                    weight = float(match.group(1))
                    reps = int(match.group(2))
                    sets.append({
                        'set': set_num,
                        'weight': weight,
                        'reps': reps
                    })
                    set_num += 1
                else:
                    print("    Invalid format. Use: weight x reps (e.g., 135 x 10)")
            
            if sets:
                exercises.append({
                    'name': exercise_name,
                    'sets': sets
                })
        
        if exercises:
            self.log_workout(date, day_type, exercises)
            print(f"\nWorkout logged successfully!")
            return True
        return False
    
    def analyze_progress(self, days: int = 30, use_ai: bool = True) -> str:
        """Analyze workout progress and provide insights"""
        recent_workouts = self.get_progress_summary(days)
        
        if not recent_workouts:
            return "No workout data found. Log some workouts first!"
        
        # Basic analysis
        analysis = []
        analysis.append(f"## Progress Analysis ({days} days)")
        analysis.append("")
        analysis.append(f"Total workouts logged: {len(recent_workouts)}")
        analysis.append("")
        
        # Group by exercise
        exercise_stats = {}
        for workout in recent_workouts:
            workout_date = datetime.fromisoformat(workout['date'])
            for exercise in workout['exercises']:
                ex_name = exercise['name']
                if ex_name not in exercise_stats:
                    exercise_stats[ex_name] = []
                
                for set_data in exercise['sets']:
                    exercise_stats[ex_name].append({
                        'date': workout_date,
                        'weight': set_data['weight'],
                        'reps': set_data['reps'],
                        'volume': set_data['weight'] * set_data['reps']
                    })
        
        # Calculate progressions
        analysis.append("### Exercise Progressions")
        analysis.append("")
        
        for ex_name, stats in sorted(exercise_stats.items()):
            if len(stats) < 2:
                continue
            
            # Sort by date
            stats.sort(key=lambda x: x['date'])
            
            first = stats[0]
            last = stats[-1]
            
            weight_change = last['weight'] - first['weight']
            volume_change = last['volume'] - first['volume']
            
            analysis.append(f"**{ex_name}**")
            analysis.append(f"- First recorded: {first['weight']}lbs x {first['reps']} ({first['volume']}lbs volume)")
            analysis.append(f"- Latest: {last['weight']}lbs x {last['reps']} ({last['volume']}lbs volume)")
            
            if weight_change > 0:
                analysis.append(f"- ✅ Weight increased by {weight_change}lbs")
            elif weight_change < 0:
                analysis.append(f"- ⚠️ Weight decreased by {abs(weight_change)}lbs")
            
            if volume_change > 0:
                analysis.append(f"- ✅ Volume increased by {volume_change}lbs")
            elif volume_change < 0:
                analysis.append(f"- ⚠️ Volume decreased by {abs(volume_change)}lbs")
            
            analysis.append("")
        
        # AI analysis if enabled
        if use_ai:
            ai_analysis = self._get_ai_analysis(recent_workouts, exercise_stats)
            if ai_analysis:
                analysis.append("### AI Recommendations")
                analysis.append("")
                analysis.append(ai_analysis)
                analysis.append("")
        
        return "\n".join(analysis)
    
    def _get_ai_analysis(self, workouts: List[Dict], exercise_stats: Dict) -> Optional[str]:
        """Get AI-powered analysis and recommendations"""
        try:
            # Try to use OpenAI API if available
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                return None
            
            import openai
            
            # Prepare context
            context = {
                'workouts': workouts[-10:],  # Last 10 workouts
                'exercise_stats': {k: v[-5:] for k, v in exercise_stats.items()}  # Last 5 entries per exercise
            }
            
            prompt = f"""Analyze this workout progress data and provide:
1. Key strengths and areas of improvement
2. Progression recommendations (weight/rep increases)
3. Exercise substitutions or additions if needed
4. Recovery and volume management suggestions

Workout Data:
{json.dumps(context, indent=2, default=str)}

Provide concise, actionable recommendations."""
            
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a fitness coach analyzing workout progress. Provide specific, actionable recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except ImportError:
            return None
        except Exception as e:
            print(f"AI analysis error: {e}")
            return None
    
    def suggest_progression(self, exercise_name: str) -> Optional[Dict]:
        """Suggest progression for a specific exercise"""
        exercise_stats = {}
        for workout in self.progress:
            for exercise in workout['exercises']:
                if exercise['name'].lower() == exercise_name.lower():
                    workout_date = datetime.fromisoformat(workout['date'])
                    if exercise['name'] not in exercise_stats:
                        exercise_stats[exercise['name']] = []
                    
                    for set_data in exercise['sets']:
                        exercise_stats[exercise['name']].append({
                            'date': workout_date,
                            'weight': set_data['weight'],
                            'reps': set_data['reps']
                        })
        
        if not exercise_stats:
            return None
        
        # Get the most recent entry
        for ex_name, stats in exercise_stats.items():
            if len(stats) == 0:
                continue
            
            stats.sort(key=lambda x: x['date'])
            latest = stats[-1]
            
            # Simple progression logic
            if latest['reps'] >= 12:
                # Increase weight, reduce reps
                suggestion = {
                    'weight': latest['weight'] + 5,
                    'reps': 8,
                    'reason': 'High reps achieved, increase weight'
                }
            elif latest['reps'] >= 8:
                # Try same weight, more reps
                suggestion = {
                    'weight': latest['weight'],
                    'reps': latest['reps'] + 1,
                    'reason': 'Progressive overload - add one rep'
                }
            else:
                # Build up reps first
                suggestion = {
                    'weight': latest['weight'],
                    'reps': latest['reps'] + 1,
                    'reason': 'Build up reps before increasing weight'
                }
            
            return {
                'exercise': ex_name,
                'current': latest,
                'suggestion': suggestion
            }
        
        return None


def main():
    parser = argparse.ArgumentParser(description='Workout Planner - PPLING Routine Generator')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate schedule command
    gen_parser = subparsers.add_parser('generate', help='Generate workout schedule')
    gen_parser.add_argument('--output', '-o', type=Path, help='Output file path for markdown')
    gen_parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD), defaults to next Monday')
    gen_parser.add_argument('--no-randomize', action='store_true', help='Keep exercises in original order')
    gen_parser.add_argument('--daily-notes', action='store_true', help='Generate separate files for each day')
    gen_parser.add_argument('--obsidian-vault', type=Path, help='Path to Obsidian vault (for daily notes)')
    
    # Add exercise command
    add_parser = subparsers.add_parser('add', help='Add an exercise')
    add_parser.add_argument('type', choices=['push', 'pull', 'legs'], help='Workout type')
    add_parser.add_argument('exercise', help='Exercise name')
    
    # Remove exercise command
    remove_parser = subparsers.add_parser('remove', help='Remove an exercise')
    remove_parser.add_argument('type', choices=['push', 'pull', 'legs'], help='Workout type')
    remove_parser.add_argument('exercise', help='Exercise name')
    
    # List exercises command
    list_parser = subparsers.add_parser('list', help='List exercises')
    list_parser.add_argument('--type', choices=['push', 'pull', 'legs'], help='Filter by workout type')
    
    # Show schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Show current week schedule')
    schedule_parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD)')
    schedule_parser.add_argument('--no-randomize', action='store_true', help='Keep exercises in original order')
    
    # Log workout command
    log_parser = subparsers.add_parser('log', help='Log a completed workout')
    log_parser.add_argument('--file', '-f', type=Path, help='Path to markdown file to parse')
    log_parser.add_argument('--date', type=str, help='Workout date (YYYY-MM-DD)')
    log_parser.add_argument('--type', choices=['push', 'pull', 'legs'], help='Workout type')
    log_parser.add_argument('--interactive', '-i', action='store_true', help='Interactive logging mode')
    
    # Analyze progress command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze workout progress')
    analyze_parser.add_argument('--days', type=int, default=30, help='Number of days to analyze (default: 30)')
    analyze_parser.add_argument('--no-ai', action='store_true', help='Disable AI analysis')
    analyze_parser.add_argument('--output', '-o', type=Path, help='Output file for analysis')
    
    # Suggest progression command
    suggest_parser = subparsers.add_parser('suggest', help='Get progression suggestions for an exercise')
    suggest_parser.add_argument('exercise', help='Exercise name')
    
    args = parser.parse_args()
    
    planner = WorkoutPlanner()
    
    if args.command == 'generate':
        start_date = None
        if args.start_date:
            start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        
        schedule = planner.generate_week_schedule(start_date, randomize=not args.no_randomize)
        
        if args.daily_notes:
            if args.obsidian_vault:
                vault_path = Path(args.obsidian_vault)
                daily_notes_path = vault_path / "Daily Notes"
                daily_notes_path.mkdir(exist_ok=True)
                
                for date in sorted(schedule.keys()):
                    note_content = planner.generate_daily_note(date, schedule)
                    note_file = daily_notes_path / f"{date.strftime('%Y-%m-%d')} - {schedule[date]['day']}.md"
                    note_file.write_text(note_content)
                    print(f"Generated: {note_file}")
            else:
                output_dir = args.output.parent if args.output else Path.cwd() / "daily_notes"
                output_dir.mkdir(exist_ok=True)
                
                for date in sorted(schedule.keys()):
                    note_content = planner.generate_daily_note(date, schedule)
                    note_file = output_dir / f"{date.strftime('%Y-%m-%d')} - {schedule[date]['day']}.md"
                    note_file.write_text(note_content)
                    print(f"Generated: {note_file}")
        else:
            markdown = planner.generate_markdown(schedule, args.output)
            if args.output:
                print(f"Generated schedule: {args.output}")
            else:
                print(markdown)
    
    elif args.command == 'add':
        if planner.add_exercise(args.type, args.exercise):
            print(f"Added '{args.exercise}' to {args.type} workouts")
        else:
            print(f"'{args.exercise}' already exists in {args.type} workouts")
    
    elif args.command == 'remove':
        if planner.remove_exercise(args.type, args.exercise):
            print(f"Removed '{args.exercise}' from {args.type} workouts")
        else:
            print(f"'{args.exercise}' not found in {args.type} workouts")
    
    elif args.command == 'list':
        exercises = planner.list_exercises(args.type)
        for workout_type, exercise_list in exercises.items():
            print(f"\n{workout_type.upper()}:")
            if exercise_list:
                for i, ex in enumerate(exercise_list, 1):
                    print(f"  {i}. {ex}")
            else:
                print("  (no exercises)")
    
    elif args.command == 'schedule':
        start_date = None
        if args.start_date:
            start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        
        schedule = planner.generate_week_schedule(start_date, randomize=not args.no_randomize)
        
        for date in sorted(schedule.keys()):
            day_info = schedule[date]
            day_name = date.strftime('%A')
            print(f"\n{day_name}, {date.strftime('%Y-%m-%d')} - {day_info['day']}")
            if day_info['day'] != 'Rest':
                for i, ex in enumerate(day_info['exercises'], 1):
                    print(f"  {i}. {ex}")
            else:
                print("  Rest Day")
    
    elif args.command == 'log':
        if args.file:
            # Log from markdown file
            if planner.log_workout_from_markdown(args.file):
                print("Workout logged successfully!")
            else:
                print("Failed to parse workout from markdown file")
        elif args.interactive:
            # Interactive logging
            date = None
            if args.date:
                date = datetime.strptime(args.date, '%Y-%m-%d')
            planner.log_workout_interactive(date, args.type)
        else:
            print("Use --file to log from markdown or --interactive for manual entry")
    
    elif args.command == 'analyze':
        analysis = planner.analyze_progress(days=args.days, use_ai=not args.no_ai)
        
        if args.output:
            args.output.write_text(analysis)
            print(f"Analysis saved to {args.output}")
        else:
            print(analysis)
    
    elif args.command == 'suggest':
        suggestion = planner.suggest_progression(args.exercise)
        if suggestion:
            print(f"\nExercise: {suggestion['exercise']}")
            print(f"Current: {suggestion['current']['weight']}lbs x {suggestion['current']['reps']} reps")
            print(f"\nSuggestion: {suggestion['suggestion']['weight']}lbs x {suggestion['suggestion']['reps']} reps")
            print(f"Reason: {suggestion['suggestion']['reason']}")
        else:
            print(f"No data found for exercise: {args.exercise}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
