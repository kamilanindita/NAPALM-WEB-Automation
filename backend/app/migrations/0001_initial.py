# Generated by Django 2.2.17 on 2021-03-13 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id_device', models.AutoField(primary_key=True, serialize=False)),
                ('ip_address', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('type_device', models.CharField(max_length=50)),
                ('network_driver', models.CharField(max_length=10)),
                ('optional_args', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DevicePolicies',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type_traffic', models.CharField(blank=True, max_length=50)),
                ('apply_interface', models.CharField(blank=True, max_length=50)),
                ('number_policies', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policies', to='app.Device')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceRole',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('protocol', models.CharField(blank=True, max_length=50)),
                ('src_add', models.CharField(blank=True, max_length=50)),
                ('src_port', models.CharField(blank=True, max_length=50)),
                ('dst_add', models.CharField(blank=True, max_length=50)),
                ('dst_port', models.CharField(blank=True, max_length=50)),
                ('des', models.CharField(blank=True, max_length=50)),
                ('action', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('policies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='app.DevicePolicies')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceRestore',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('restore', models.TextField(blank=True)),
                ('compare', models.TextField(blank=True)),
                ('before', models.TextField(blank=True)),
                ('status', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restores', to='app.Device')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceLogConfiguration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('config', models.TextField()),
                ('status', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='configs', to='app.Device')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='DeviceInterface',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(blank=True, max_length=50)),
                ('is_enabled', models.BooleanField()),
                ('is_up', models.BooleanField()),
                ('mac_address', models.CharField(blank=True, max_length=50)),
                ('mtu', models.CharField(blank=True, max_length=50)),
                ('speed', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='app.Device')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceInformation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fqdn', models.CharField(blank=True, max_length=50)),
                ('hostname', models.CharField(blank=True, max_length=50)),
                ('interfaces_list', models.TextField(blank=True)),
                ('model', models.CharField(blank=True, max_length=50)),
                ('os_version', models.TextField(blank=True)),
                ('serial_number', models.CharField(blank=True, max_length=50)),
                ('uptime', models.CharField(blank=True, max_length=50)),
                ('vendor', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='informations', to='app.Device')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceBackup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('backup', models.TextField(blank=True)),
                ('ftp', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='backups', to='app.Device')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceArp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('interface', models.CharField(blank=True, max_length=50)),
                ('mac', models.CharField(blank=True, max_length=50)),
                ('ip', models.CharField(blank=True, max_length=50)),
                ('age', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arp', to='app.Device')),
            ],
        ),
    ]
