# Generated by Django 3.2.10 on 2022-08-25 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_auto_20220824_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.grade'),
        ),
    ]