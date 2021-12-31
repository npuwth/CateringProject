# Generated by Django 4.0 on 2021-12-17 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering', '0003_alter_provider_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='avg_star',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='商品评分'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='mon_sale',
            field=models.IntegerField(default=0, verbose_name='月销量'),
        ),
        migrations.AlterField(
            model_name='window',
            name='avg_price',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='平均价格'),
        ),
        migrations.AlterField(
            model_name='window',
            name='avg_star',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='平均评分'),
        ),
        migrations.AlterField(
            model_name='window',
            name='mon_sale',
            field=models.IntegerField(default=0, verbose_name='月销量'),
        ),
    ]
