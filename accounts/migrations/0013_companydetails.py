from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_user_under_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company/')),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('website', models.URLField(blank=True, max_length=255)),
                ('address', models.TextField(blank=True)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('state', models.CharField(blank=True, max_length=100)),
                ('pincode', models.CharField(blank=True, max_length=10)),
                ('gst_number', models.CharField(blank=True, max_length=30)),
                ('registration_number', models.CharField(blank=True, max_length=50)),
                ('established_on', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]