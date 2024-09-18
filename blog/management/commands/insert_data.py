from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from accounts.models import User, Profile
from blog.models import Post, Category
from django.utils import timezone
import random

category_list = ['fun', 'tech', 'technology']


class Command(BaseCommand):
    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.fake.email(), password='test@123456')
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=5)
        profile.save()

        for category in category_list:
            Category.objects.get_or_create(name=category)

        for _ in range(10):
            post = Post.objects.create(
                author=profile,
                title=self.fake.paragraph(nb_sentences=1),
                context=self.fake.paragraph(nb_sentences=5),
                status=True,
                published_date=timezone.now(),  # Use timezone.now() for a timezone-aware datetime

            )
            # Now add a random category to the post
            random_category = Category.objects.get(name=random.choice(category_list))
            post.category.add(random_category)  # Use the add() method to associate the category
