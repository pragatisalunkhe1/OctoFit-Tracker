#!/usr/bin/env python
"""
Script to populate the OctoFit Tracker database with test data.
Run this script using: python populate_db.py
"""

import os
import django
from datetime import datetime, timedelta

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


def clear_database():
    """Clear existing data from all models."""
    try:
        # Delete in reverse order of dependencies
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()
        print("✓ Database cleared")
    except Exception as e:
        print(f"⚠ Warning during database clear: {e}")
        print("  Continuing with database population...")


def create_teams():
    """Create test teams."""
    teams = [
        {"name": "Octo Warriors", "description": "The strongest fitness team in the ocean"},
        {"name": "Code Crushers", "description": "Crushing code and fitness goals"},
        {"name": "Git Gains", "description": "Building muscle through version control"},
    ]
    
    created_teams = []
    for team_data in teams:
        try:
            team = Team.objects.get(name=team_data["name"])
            print(f"✓ Team '{team.name}' exists")
        except Team.DoesNotExist:
            team = Team.objects.create(**team_data)
            print(f"✓ Team '{team.name}' created")
        created_teams.append(team)
    
    return created_teams


def create_users(teams):
    """Create test users."""
    users_data = [
        {"email": "alice@example.com", "name": "Alice Johnson", "team": teams[0].name, "is_superhero": True},
        {"email": "bob@example.com", "name": "Bob Smith", "team": teams[0].name, "is_superhero": False},
        {"email": "charlie@example.com", "name": "Charlie Brown", "team": teams[1].name, "is_superhero": False},
        {"email": "diana@example.com", "name": "Diana Prince", "team": teams[1].name, "is_superhero": True},
        {"email": "eve@example.com", "name": "Eve Wilson", "team": teams[2].name, "is_superhero": False},
        {"email": "frank@example.com", "name": "Frank Miller", "team": teams[2].name, "is_superhero": False},
    ]
    
    created_users = []
    for user_data in users_data:
        try:
            # Try to get existing user first
            user = User.objects.get(email=user_data["email"])
            print(f"✓ User '{user.name}' ({user.email}) exists")
        except User.DoesNotExist:
            # Create new user if it doesn't exist
            user = User.objects.create(**user_data)
            print(f"✓ User '{user.name}' ({user.email}) created")
        created_users.append(user)
    
    return created_users


def create_activities(users):
    """Create test activities."""
    activity_types = ["Running", "Cycling", "Swimming", "Weight Training", "Yoga"]
    activities = []
    
    base_date = datetime.now().date()
    activity_count = 0
    
    for i, user in enumerate(users):
        for j, activity_type in enumerate(activity_types):
            try:
                # Create activities with unique date combinations
                activity_date = base_date - timedelta(days=(i * len(activity_types) + j))
                activity = Activity.objects.create(
                    user_id=str(user.id),
                    user_email=user.email,
                    type=activity_type,
                    duration=30 + (i * 10),  # Vary duration by user
                    date=activity_date
                )
                activities.append(activity)
                activity_count += 1
                print(f"  ✓ Activity created: {user.email} - {activity_type}")
            except Exception as e:
                print(f"  ✗ Error creating activity for {user.email}: {e}")
    
    print(f"  Total activities created: {activity_count}")
    return activities


def create_leaderboard(users):
    """Create test leaderboard entries."""
    leaderboard_entries = []
    
    try:
        # Clear existing leaderboard entries first
        Leaderboard.objects.all().delete()
        
        # Create leaderboard entries based on user superhero status and team
        for rank, user in enumerate(sorted(users, key=lambda u: (not u.is_superhero, u.name)), start=1):
            score = 1000 - (rank * 50)  # Descending scores for ranking
            
            leaderboard = Leaderboard.objects.create(
                user_id=str(user.id),
                user_email=user.email,
                score=score,
                rank=rank
            )
            leaderboard_entries.append(leaderboard)
            print(f"  ✓ Leaderboard entry created: Rank {rank} - {user.name} ({score} points)")
        
        print(f"  Total leaderboard entries created: {len(leaderboard_entries)}")
    except Exception as e:
        print(f"  ✗ Error creating leaderboard entries: {e}")
    
    return leaderboard_entries


def create_workouts():
    """Create test workouts."""
    workouts_data = [
        {"name": "Morning Run", "description": "5km easy run", "difficulty": "Easy"},
        {"name": "HIIT Circuit", "description": "High intensity interval training", "difficulty": "Hard"},
        {"name": "Strength Training", "description": "Full body workout", "difficulty": "Medium"},
        {"name": "Yoga Flow", "description": "Relaxing yoga session", "difficulty": "Easy"},
        {"name": "Spin Class", "description": "Indoor cycling workout", "difficulty": "Medium"},
        {"name": "CrossFit WOD", "description": "Challenging workout of the day", "difficulty": "Hard"},
    ]
    
    created_workouts = []
    for workout_data in workouts_data:
        try:
            workout = Workout.objects.get(name=workout_data["name"])
            print(f"✓ Workout '{workout.name}' ({workout.difficulty}) exists")
        except Workout.DoesNotExist:
            workout = Workout.objects.create(**workout_data)
            print(f"✓ Workout '{workout.name}' ({workout.difficulty}) created")
        created_workouts.append(workout)
    
    return created_workouts


def populate_database():
    """Main function to populate the database."""
    print("\n" + "="*50)
    print("OctoFit Tracker - Database Population Script")
    print("="*50 + "\n")
    
    print("Clearing existing data...")
    clear_database()
    
    print("\nCreating Teams...")
    teams = create_teams()
    
    print("\nCreating Users...")
    users = create_users(teams)
    
    print("\nCreating Activities...")
    create_activities(users)
    
    print("\nCreating Leaderboard...")
    create_leaderboard(users)
    
    print("\nCreating Workouts...")
    create_workouts()
    
    print("\n" + "="*50)
    print("✓ Database population completed successfully!")
    print("="*50 + "\n")
    
    # Print summary statistics
    print("Summary:")
    print(f"  Teams: {Team.objects.count()}")
    print(f"  Users: {User.objects.count()}")
    print(f"  Activities: {Activity.objects.count()}")
    print(f"  Leaderboard Entries: {Leaderboard.objects.count()}")
    print(f"  Workouts: {Workout.objects.count()}")
    print()


if __name__ == "__main__":
    populate_database()
