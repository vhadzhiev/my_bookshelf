# Generated by Django 4.0.4 on 2022-04-29 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('Adventure', 'Adventure'), ('Biographies', 'Biographies'), ('Business', 'Business'), ("Children's", "Children's"), ('Crime', 'Crime'), ('Health', 'Health'), ('History', 'History'), ('Hobbies', 'Hobbies'), ('Fantasy', 'Fantasy'), ('Fiction', 'Fiction'), ('Novel', 'Novel'), ('Science', 'Science'), ('Sports', 'Sports'), ('Tech', 'Tech'), ('Other', 'Other')], max_length=11),
        ),
    ]