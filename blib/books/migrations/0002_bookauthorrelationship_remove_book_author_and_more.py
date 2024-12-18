# Generated by Django 4.2.14 on 2024-09-30 14:20

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookAuthorRelationship',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.DeleteModel(
            name='AuthorBookRelationship',
        ),
        migrations.AddField(
            model_name='bookauthorrelationship',
            name='Book',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_author_relationship', to='books.book'),
        ),
        migrations.AddField(
            model_name='bookauthorrelationship',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='books.author'),
        ),
    ]
