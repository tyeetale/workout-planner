# Push to GitHub

Your repository is ready! Follow these steps to push to GitHub:

## Option 1: Create repo on GitHub.com (Recommended)

1. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name it `workout-planner` (or any name you prefer)
   - Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
   - Click "Create repository"

2. **Push your code:**
   ```bash
   # Add the remote (replace YOUR_USERNAME with your GitHub username)
   git remote add origin https://github.com/YOUR_USERNAME/workout-planner.git
   
   # Rename branch to main (GitHub's default)
   git branch -M main
   
   # Push to GitHub
   git push -u origin main
   ```

## Option 2: Use GitHub CLI (if installed)

```bash
# Create repo and push in one command
gh repo create workout-planner --public --source=. --remote=origin --push
```

## Option 3: SSH (if you have SSH keys set up)

```bash
# Add SSH remote instead
git remote add origin git@github.com:YOUR_USERNAME/workout-planner.git
git branch -M main
git push -u origin main
```

## After pushing

Your code will be available at:
`https://github.com/YOUR_USERNAME/workout-planner`

You can then:
- Add a description on GitHub
- Add topics/tags (e.g., `python`, `fitness`, `workout`, `obsidian`)
- Star the repo
- Share it with others!
