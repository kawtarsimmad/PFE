from django.db import migrations

def add_new_category(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    Category.objects.create(name='Urgent')  # Replace 'New Category Name' with your desired category name

class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_alter_category_options_alter_category_id'),  # Update with the correct previous migration
    ]

    operations = [
        migrations.RunPython(add_new_category),
    ]
