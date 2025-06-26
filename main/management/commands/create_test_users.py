from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Create test users for Admin, Trainer, and Trainee groups'

    def handle(self, *args, **kwargs):
        users_data = [
            {'username': 'adminuser', 'password': 'AdminPass123!', 'group': 'Admin'},
            {'username': 'traineruser', 'password': 'TrainerPass123!', 'group': 'Trainer'},
            {'username': 'traineeuser', 'password': 'TraineePass123!', 'group': 'Trainee'},
        ]

        for data in users_data:
            username = data['username']
            password = data['password']
            group_name = data['group']

            if User.objects.filter(username=username).exists():
                self.stdout.write(f"User '{username}' already exists.")
                continue

            user = User.objects.create_user(username=username, password=password)
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            user.save()
            self.stdout.write(f"Created user '{username}' with group '{group_name}'.")
