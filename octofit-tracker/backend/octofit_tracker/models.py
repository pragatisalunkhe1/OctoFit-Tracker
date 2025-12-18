from djongo import models

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    is_superhero = models.BooleanField(default=False)
    def __str__(self):
        return self.email

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Activity(models.Model):
    user_id = models.CharField(max_length=50)  # Store user ID as string for Djongo compatibility
    user_email = models.EmailField()  # Store email for reference
    type = models.CharField(max_length=50)
    duration = models.IntegerField()  # in minutes
    date = models.DateField()
    def __str__(self):
        return f"{self.user_email} - {self.type}"
    def __init__(self, *args, **kwargs):
        # Accept legacy 'user' kwarg (User instance) for compatibility
        user = kwargs.pop('user', None)
        if user is not None:
            # Set user_id and user_email from provided User instance
            kwargs.setdefault('user_id', str(getattr(user, 'id', '')))
            kwargs.setdefault('user_email', getattr(user, 'email', ''))
        super().__init__(*args, **kwargs)

class Leaderboard(models.Model):
    user_id = models.CharField(max_length=50)  # Store user ID as string for Djongo compatibility
    user_email = models.EmailField()  # Store email for reference
    score = models.IntegerField()
    rank = models.IntegerField()
    def __str__(self):
        return f"{self.user_email} - {self.rank}"
    def __init__(self, *args, **kwargs):
        # Accept legacy 'user' kwarg (User instance) for compatibility
        user = kwargs.pop('user', None)
        if user is not None:
            kwargs.setdefault('user_id', str(getattr(user, 'id', '')))
            kwargs.setdefault('user_email', getattr(user, 'email', ''))
        super().__init__(*args, **kwargs)

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20)
    def __str__(self):
        return self.name
