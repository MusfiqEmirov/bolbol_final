# Generated by Django 5.1.6 on 2025-02-12 22:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_remove_product_view_count_product_views_count_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoryfilterfield',
            options={'ordering': ('category',), 'verbose_name': 'Category Filter Field', 'verbose_name_plural': 'Category Filter Fields'},
        ),
        migrations.RemoveField(
            model_name='categoryfilterfield',
            name='categories',
        ),
        migrations.AddField(
            model_name='categoryfilterfield',
            name='choices',
            field=models.TextField(blank=True, help_text="Example: red;green; Warning! Use '‒' instead of normal dash ('-') in brands like: Mercedes‒Benz. Copy ‒", max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='categoryfilterfield',
            name='is_hidden_field',
            field=models.BooleanField(default=False, verbose_name='Hide Field'),
        ),
        migrations.AddField(
            model_name='categoryfilterfield',
            name='is_required',
            field=models.BooleanField(default=False, verbose_name='Is required'),
        ),
        migrations.AddField(
            model_name='categoryfilterfield',
            name='max_value_length',
            field=models.PositiveSmallIntegerField(blank=True, default=16, null=True, verbose_name='Max value length'),
        ),
        migrations.AddField(
            model_name='categoryfilterfield',
            name='order',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Display order'),
        ),
        migrations.AddField(
            model_name='categoryfilterfield',
            name='placeholder_text',
            field=models.TextField(blank=True, null=True, verbose_name='Placeholder text'),
        ),
        migrations.AddField(
            model_name='categoryfilterfield',
            name='tooltip_text',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Tooltip text'),
        ),
        migrations.AddField(
            model_name='categoryfilterfield',
            name='type',
            field=models.CharField(blank=True, choices=[('number', 'Number'), ('text', 'Text'), ('choices', 'Choices')], default='text', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='categoryfilterfield',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_filter_fields', related_query_name='category_filter_field', to='products.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='categoryfilterfield',
            name='field_display_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Field display name'),
        ),
    ]
