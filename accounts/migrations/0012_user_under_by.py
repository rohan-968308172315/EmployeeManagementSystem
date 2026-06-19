from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_user_original_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='under_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='managed_employees',
                to='accounts.user',
            ),
        ),
    ]