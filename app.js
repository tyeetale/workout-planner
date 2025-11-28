// Workout Planner App
class WorkoutPlanner {
    constructor() {
        this.workouts = {
            push: [],
            pull: [],
            legs: []
        };
        this.schedule = {
            monday: [],
            tuesday: [],
            wednesday: [],
            thursday: [],
            friday: [],
            saturday: []
        };
        this.progress = [];
        
        this.init();
    }

    init() {
        this.loadData();
        this.setupEventListeners();
        this.renderSchedule();
        this.renderWorkouts();
        this.renderProgress();
    }

    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.target.dataset.tab;
                this.switchTab(tab);
            });
        });

        // Add exercise buttons
        document.getElementById('add-push-btn').addEventListener('click', () => {
            this.addExercise('push');
        });
        document.getElementById('add-pull-btn').addEventListener('click', () => {
            this.addExercise('pull');
        });
        document.getElementById('add-legs-btn').addEventListener('click', () => {
            this.addExercise('legs');
        });

        // Enter key for inputs
        ['push', 'pull', 'legs'].forEach(type => {
            document.getElementById(`${type}-exercise-input`).addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.addExercise(type);
                }
            });
        });

        // Randomize buttons
        document.querySelectorAll('.randomize-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const day = e.target.dataset.day;
                this.randomizeDay(day);
            });
        });

        // Start workout buttons
        document.querySelectorAll('.start-workout-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const day = e.target.dataset.day;
                this.startWorkout(day);
            });
        });

        // Modal close
        document.querySelector('.close').addEventListener('click', () => {
            this.closeModal();
        });

        // Complete workout button
        document.getElementById('complete-workout-btn').addEventListener('click', () => {
            this.completeWorkout();
        });

        // Close modal on outside click
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('workout-modal');
            if (e.target === modal) {
                this.closeModal();
            }
        });
    }

    switchTab(tab) {
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        document.querySelector(`[data-tab="${tab}"]`).classList.add('active');
        document.getElementById(`${tab}-tab`).classList.add('active');
    }

    addExercise(type) {
        const input = document.getElementById(`${type}-exercise-input`);
        const name = input.value.trim();
        
        if (name && !this.workouts[type].includes(name)) {
            this.workouts[type].push(name);
            input.value = '';
            this.saveData();
            this.renderWorkouts();
            this.updateSchedule();
        }
    }

    removeExercise(type, index) {
        this.workouts[type].splice(index, 1);
        this.saveData();
        this.renderWorkouts();
        this.updateSchedule();
    }

    renderWorkouts() {
        ['push', 'pull', 'legs'].forEach(type => {
            const list = document.getElementById(`${type}-exercises-list`);
            list.innerHTML = '';
            
            if (this.workouts[type].length === 0) {
                list.innerHTML = '<li class="empty-state">No exercises added yet. Add some exercises above!</li>';
            } else {
                this.workouts[type].forEach((exercise, index) => {
                    const li = document.createElement('li');
                    li.className = 'exercise-list-item';
                    li.innerHTML = `
                        <span>${exercise}</span>
                        <button class="delete-btn" data-type="${type}" data-index="${index}">Delete</button>
                    `;
                    li.querySelector('.delete-btn').addEventListener('click', () => {
                        this.removeExercise(type, index);
                    });
                    list.appendChild(li);
                });
            }
        });
    }

    getDayType(day) {
        const dayMap = {
            monday: 'push',
            tuesday: 'pull',
            wednesday: 'legs',
            thursday: 'push',
            friday: 'pull',
            saturday: 'legs'
        };
        return dayMap[day];
    }

    updateSchedule() {
        ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'].forEach(day => {
            const type = this.getDayType(day);
            if (this.schedule[day].length === 0 || !this.isScheduleValid(day)) {
                this.schedule[day] = [...this.workouts[type]];
            }
            this.renderDay(day);
        });
    }

    isScheduleValid(day) {
        const type = this.getDayType(day);
        const scheduleExercises = this.schedule[day];
        const availableExercises = this.workouts[type];
        
        // Check if all scheduled exercises are still in available exercises
        return scheduleExercises.every(ex => availableExercises.includes(ex)) &&
               scheduleExercises.length === availableExercises.length;
    }

    randomizeDay(day) {
        const type = this.getDayType(day);
        const exercises = [...this.workouts[type]];
        
        // Fisher-Yates shuffle
        for (let i = exercises.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [exercises[i], exercises[j]] = [exercises[j], exercises[i]];
        }
        
        this.schedule[day] = exercises;
        this.saveData();
        this.renderDay(day);
    }

    renderSchedule() {
        ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'].forEach(day => {
            this.renderDay(day);
        });
    }

    renderDay(day) {
        const exercisesList = document.getElementById(`${day}-exercises`);
        const exercises = this.schedule[day] || [];
        
        exercisesList.innerHTML = '';
        
        if (exercises.length === 0) {
            exercisesList.innerHTML = '<div class="empty-state"><p>No exercises defined. Add exercises in the "Manage Workouts" tab.</p></div>';
        } else {
            exercises.forEach((exercise, index) => {
                const div = document.createElement('div');
                div.className = 'exercise-item';
                div.innerHTML = `
                    <span class="exercise-number">${index + 1}</span>
                    <span class="exercise-name">${exercise}</span>
                `;
                exercisesList.appendChild(div);
            });
        }
    }

    startWorkout(day) {
        const exercises = this.schedule[day];
        if (exercises.length === 0) {
            alert('No exercises defined for this day. Please add exercises first.');
            return;
        }

        this.currentWorkoutDay = day;
        this.currentWorkoutData = exercises.map(ex => ({
            name: ex,
            sets: []
        }));

        this.openModal(day, exercises);
    }

    openModal(day, exercises) {
        const modal = document.getElementById('workout-modal');
        const title = document.getElementById('modal-day-title');
        const exercisesContainer = document.getElementById('modal-exercises');
        
        const dayNames = {
            monday: 'Monday - Push',
            tuesday: 'Tuesday - Pull',
            wednesday: 'Wednesday - Legs',
            thursday: 'Thursday - Push',
            friday: 'Friday - Pull',
            saturday: 'Saturday - Legs'
        };
        
        title.textContent = dayNames[day];
        exercisesContainer.innerHTML = '';
        
        exercises.forEach((exercise, exerciseIndex) => {
            const exerciseDiv = document.createElement('div');
            exerciseDiv.className = 'modal-exercise';
            exerciseDiv.innerHTML = `
                <h4>${exercise}</h4>
                <div class="sets-input" id="sets-${exerciseIndex}"></div>
                <button class="add-set-btn" data-exercise="${exerciseIndex}">+ Add Set</button>
            `;
            
            const setsContainer = exerciseDiv.querySelector(`#sets-${exerciseIndex}`);
            const addSetBtn = exerciseDiv.querySelector('.add-set-btn');
            
            addSetBtn.addEventListener('click', () => {
                this.addSet(exerciseIndex, setsContainer);
            });
            
            exercisesContainer.appendChild(exerciseDiv);
        });
        
        modal.style.display = 'block';
    }

    addSet(exerciseIndex, container) {
        const setIndex = container.children.length;
        const setDiv = document.createElement('div');
        setDiv.className = 'set-input';
        setDiv.innerHTML = `
            <label>Set ${setIndex + 1}:</label>
            <input type="number" placeholder="Weight" class="weight-input" min="0" step="0.5">
            <label>x</label>
            <input type="number" placeholder="Reps" class="reps-input" min="1">
        `;
        container.appendChild(setDiv);
    }

    completeWorkout() {
        const exercises = this.schedule[this.currentWorkoutDay];
        const workoutData = {
            day: this.currentWorkoutDay,
            date: new Date().toISOString(),
            exercises: []
        };
        
        exercises.forEach((exerciseName, exerciseIndex) => {
            const setsContainer = document.getElementById(`sets-${exerciseIndex}`);
            const sets = [];
            
            Array.from(setsContainer.children).forEach(setDiv => {
                const weight = parseFloat(setDiv.querySelector('.weight-input').value) || 0;
                const reps = parseInt(setDiv.querySelector('.reps-input').value) || 0;
                
                if (reps > 0) {
                    sets.push({ weight, reps });
                }
            });
            
            if (sets.length > 0) {
                workoutData.exercises.push({
                    name: exerciseName,
                    sets: sets
                });
            }
        });
        
        if (workoutData.exercises.length > 0) {
            this.progress.push(workoutData);
            this.saveData();
            this.renderProgress();
            this.closeModal();
            alert('Workout completed! Great job! 💪');
        } else {
            alert('Please log at least one set to complete the workout.');
        }
    }

    closeModal() {
        document.getElementById('workout-modal').style.display = 'none';
        this.currentWorkoutDay = null;
        this.currentWorkoutData = null;
    }

    renderProgress() {
        const progressList = document.getElementById('progress-list');
        progressList.innerHTML = '';
        
        if (this.progress.length === 0) {
            progressList.innerHTML = '<div class="empty-state"><p>No workout history yet. Complete a workout to track your progress!</p></div>';
        } else {
            // Sort by date (newest first)
            const sortedProgress = [...this.progress].sort((a, b) => 
                new Date(b.date) - new Date(a.date)
            );
            
            sortedProgress.forEach(workout => {
                const div = document.createElement('div');
                div.className = 'progress-item';
                
                const date = new Date(workout.date);
                const dateStr = date.toLocaleDateString('en-US', { 
                    weekday: 'long', 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                });
                
                const dayNames = {
                    monday: 'Monday - Push',
                    tuesday: 'Tuesday - Pull',
                    wednesday: 'Wednesday - Legs',
                    thursday: 'Thursday - Push',
                    friday: 'Friday - Pull',
                    saturday: 'Saturday - Legs'
                };
                
                let exercisesHtml = '<div class="progress-exercises">';
                workout.exercises.forEach(ex => {
                    const setsStr = ex.sets.map(s => `${s.weight}lbs x ${s.reps}`).join(', ');
                    exercisesHtml += `<div class="progress-exercise"><strong>${ex.name}:</strong> ${setsStr}</div>`;
                });
                exercisesHtml += '</div>';
                
                div.innerHTML = `
                    <h3>${dayNames[workout.day]}</h3>
                    <div class="date">${dateStr}</div>
                    ${exercisesHtml}
                `;
                
                progressList.appendChild(div);
            });
        }
    }

    saveData() {
        const data = {
            workouts: this.workouts,
            schedule: this.schedule,
            progress: this.progress
        };
        localStorage.setItem('workoutPlannerData', JSON.stringify(data));
    }

    loadData() {
        const saved = localStorage.getItem('workoutPlannerData');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                this.workouts = data.workouts || { push: [], pull: [], legs: [] };
                this.schedule = data.schedule || {
                    monday: [],
                    tuesday: [],
                    wednesday: [],
                    thursday: [],
                    friday: [],
                    saturday: []
                };
                this.progress = data.progress || [];
            } catch (e) {
                console.error('Error loading data:', e);
            }
        } else {
            // Initialize with default exercises
            this.workouts = {
                push: ['Bench Press', 'Overhead Press', 'Incline Dumbbell Press', 'Lateral Raises', 'Tricep Dips'],
                pull: ['Pull-ups', 'Barbell Rows', 'Cable Rows', 'Face Pulls', 'Barbell Curls'],
                legs: ['Squats', 'Romanian Deadlifts', 'Leg Press', 'Leg Curls', 'Calf Raises']
            };
            this.saveData();
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WorkoutPlanner();
});
