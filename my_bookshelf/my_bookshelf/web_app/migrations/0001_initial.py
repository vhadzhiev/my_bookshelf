# Generated by Django 4.0.3 on 2022-04-19 06:55

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import my_bookshelf.web_app.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=50)),
                ('isbn', models.CharField(max_length=13, validators=[my_bookshelf.web_app.validators.validate_only_digits, my_bookshelf.web_app.validators.validate_correct_length], verbose_name='ISBN')),
                ('genre', models.CharField(choices=[('Adventure', 'Adventure'), ('Biographies', 'Biographies'), ('Business', 'Business'), ("Children's", "Children's"), ('Crime', 'Crime'), ('Health', 'Health'), ('History', 'History'), ('Hobbies', 'Hobbies'), ('Fantasy', 'Fantasy'), ('Fiction', 'Fiction'), ('Science', 'Science'), ('Sports', 'Sports'), ('Tech', 'Tech'), ('Other', 'Other')], max_length=11)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookCover',
            fields=[
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='web_app.book')),
            ],
        ),
        migrations.CreateModel(
            name='Bookshelf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('books', models.ManyToManyField(blank=True, null=True, to='web_app.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
