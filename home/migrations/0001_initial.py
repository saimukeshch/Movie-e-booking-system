# Generated by Django 4.1.6 on 2023-04-14 22:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('accountID', models.AutoField(primary_key=True, serialize=False)),
                ('cardNo', models.CharField(blank=True, default='', max_length=250)),
                ('exp', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CardEncr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CardType',
            fields=[
                ('cardTypeID', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('title', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('cast', models.CharField(max_length=100)),
                ('synopsis', models.CharField(max_length=500)),
                ('rating', models.CharField(blank=True, max_length=5)),
                ('playing_now', models.BooleanField(default=False)),
                ('trailer_picture', models.URLField(max_length=300)),
                ('release_date', models.DateField(blank=True, default=None)),
                ('genre', models.CharField(blank=True, max_length=10)),
                ('trailer_video', models.URLField(blank=True, max_length=250)),
                ('director', models.CharField(blank=True, default='', max_length=100)),
                ('producer', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MovieCategory',
            fields=[
                ('category', models.CharField(choices=[('G', 'General audience'), ('M', 'Mature audience'), ('R', 'Restricted audience'), ('X', 'No one under 18')], default='U', max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderID', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.IntegerField(default=0)),
                ('numTickets', models.FloatField(default=0)),
                ('accountID', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.account')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('promoID', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=1)),
                ('valid_thru', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('screen', models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5')], default='A1', max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('shownum', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.CharField(default='12/12/12 12:12', max_length=50)),
                ('movieID', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='home.movie')),
                ('screenID', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='home.screen')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticketID', models.AutoField(primary_key=True, serialize=False)),
                ('seatNum', models.IntegerField(default=1)),
                ('price', models.IntegerField(default=10)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.order')),
                ('showtimeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.showtime')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('movie', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.movie')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='showtimeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.showtime'),
        ),
        migrations.AddField(
            model_name='order',
            name='userID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movie',
            name='certificate',
            field=models.ForeignKey(default='G', on_delete=django.db.models.deletion.CASCADE, to='home.moviecategory'),
        ),
    ]