# Generated by Django 4.0 on 2021-12-18 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering', '0006_alter_purchase_star'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='mon_sale',
            field=models.IntegerField(default=0, null=True, verbose_name='月销量'),
        ),
        migrations.AlterField(
            model_name='window',
            name='mon_sale',
            field=models.IntegerField(default=0, null=True, verbose_name='月销量'),
        ),
    ]
