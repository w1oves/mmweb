# Generated by Django 3.2.5 on 2022-05-01 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('project_dir', models.CharField(max_length=256)),
                ('interpreter_path', models.CharField(choices=[('/home/wzx/.conda/envs/enseg/bin/python', '/home/wzx/.conda/envs/enseg/bin/python'), ('/home/wzx/.conda/envs/wzx/bin/python', '/home/wzx/.conda/envs/wzx/bin/python'), ('/home/wzx/.conda/envs/tsit/bin/python', '/home/wzx/.conda/envs/tsit/bin/python'), ('/home/wzx/.conda/envs/.conda_envs_dir_test/bin/python', '/home/wzx/.conda/envs/.conda_envs_dir_test/bin/python'), ('/home/wzx/.conda/envs/web/bin/python', '/home/wzx/.conda/envs/web/bin/python'), ('/home/anchen/anaconda3/envs/n2v/bin/python', '/home/anchen/anaconda3/envs/n2v/bin/python'), ('/home/anchen/anaconda3/envs/pytorch/bin/python', '/home/anchen/anaconda3/envs/pytorch/bin/python'), ('/home/anchen/anaconda3/envs/.conda_envs_dir_test/bin/python', '/home/anchen/anaconda3/envs/.conda_envs_dir_test/bin/python'), ('/home/anchen/anaconda3/envs/kinetics/bin/python', '/home/anchen/anaconda3/envs/kinetics/bin/python'), ('/home/anchen/anaconda3/envs/tensorflow2.4/bin/python', '/home/anchen/anaconda3/envs/tensorflow2.4/bin/python'), ('/home/chenlin/anaconda3/envs/dass/bin/python', '/home/chenlin/anaconda3/envs/dass/bin/python'), ('/home/chenlin/anaconda3/envs/mmseg/bin/python', '/home/chenlin/anaconda3/envs/mmseg/bin/python'), ('/home/chenlin/anaconda3/envs/semseg/bin/python', '/home/chenlin/anaconda3/envs/semseg/bin/python'), ('/home/chenlin/anaconda3/envs/UDA/bin/python', '/home/chenlin/anaconda3/envs/UDA/bin/python'), ('/home/chenlin/anaconda3/envs/test/bin/python', '/home/chenlin/anaconda3/envs/test/bin/python'), ('/home/chenlin/anaconda3/envs/proda/bin/python', '/home/chenlin/anaconda3/envs/proda/bin/python'), ('/home/chenlin/anaconda3/envs/ml/bin/python', '/home/chenlin/anaconda3/envs/ml/bin/python'), ('/home/chenlin/anaconda3/envs/tune/bin/python', '/home/chenlin/anaconda3/envs/tune/bin/python'), ('/home/chenlin/anaconda3/envs/mmselfsup/bin/python', '/home/chenlin/anaconda3/envs/mmselfsup/bin/python'), ('/home/chenlin/anaconda3/envs/segdark/bin/python', '/home/chenlin/anaconda3/envs/segdark/bin/python'), ('/home/chenlin/anaconda3/envs/mmgen/bin/python', '/home/chenlin/anaconda3/envs/mmgen/bin/python'), ('/home/chenlin/anaconda3/envs/mmcls/bin/python', '/home/chenlin/anaconda3/envs/mmcls/bin/python'), ('/home/chenlin/anaconda3/envs/ssseg/bin/python', '/home/chenlin/anaconda3/envs/ssseg/bin/python'), ('/home/chenlin/anaconda3/envs/msda-seg/bin/python', '/home/chenlin/anaconda3/envs/msda-seg/bin/python'), ('/home/wangjf/anaconda3/envs/py38/bin/python', '/home/wangjf/anaconda3/envs/py38/bin/python'), ('/home/wangjf/anaconda3/envs/.conda_envs_dir_test/bin/python', '/home/wangjf/anaconda3/envs/.conda_envs_dir_test/bin/python'), ('/home/wangjf/anaconda3/envs/py375/bin/python', '/home/wangjf/anaconda3/envs/py375/bin/python'), ('/home/wangjf/anaconda3/envs/py39/bin/python', '/home/wangjf/anaconda3/envs/py39/bin/python'), ('/opt/anaconda3/bin/python', '/opt/anaconda3/bin/python')], default='/home/wzx/.conda/envs/enseg/bin/python', max_length=256)),
                ('code_base', models.CharField(choices=[('mmseg', 'mmseg')], default='mmseg', max_length=32)),
            ],
        ),
    ]
