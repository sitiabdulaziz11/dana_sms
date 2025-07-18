# Generated by Django 4.2.23 on 2025-07-11 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_payment_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(blank=True, choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('monthly', 'Monthly'), ('after_class', 'After Class Reading')], max_length=120, null=True),
        ),
    ]
