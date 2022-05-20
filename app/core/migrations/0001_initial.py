# Generated by Django 3.1.7 on 2022-05-20 00:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Endereço de email')),
                ('nome', models.CharField(max_length=256)),
                ('data_nascimento', models.DateField(auto_now=True, verbose_name='Data de nascimento')),
                ('discipulo_vinculado', models.BooleanField(default=True, verbose_name='Está vinculado?')),
                ('apelido', models.CharField(blank=True, max_length=256, verbose_name='Apelido')),
                ('data_vinculacao_igreja_local', models.DateField(blank=True, null=True, verbose_name='Qual a data de vinculação?')),
                ('data_afastamento', models.DateField(blank=True, null=True)),
                ('sexo', models.CharField(blank=True, choices=[('F', 'Feminino'), ('M', 'Masculino'), ('N', 'Nenhuma das opções')], max_length=1, null=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='É da equipe?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Está ativo?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('companheiros', models.ManyToManyField(blank=True, related_name='_pessoa_companheiros_+', to=settings.AUTH_USER_MODEL, verbose_name='Companheiros')),
            ],
            options={
                'verbose_name': 'Pessoa',
            },
        ),
        migrations.CreateModel(
            name='Bloco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=256, verbose_name='Bloco')),
            ],
            options={
                'verbose_name': 'Bloco',
            },
        ),
        migrations.CreateModel(
            name='EstadoCivil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=256, verbose_name='Estado civil')),
            ],
            options={
                'verbose_name': 'Estado civil',
                'verbose_name_plural': 'Estados civis',
            },
        ),
        migrations.CreateModel(
            name='Funcao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=256, verbose_name='Descrição da função')),
            ],
            options={
                'verbose_name': 'Função',
                'verbose_name_plural': 'Funções',
            },
        ),
        migrations.CreateModel(
            name='Localidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=256, verbose_name='Descrição do local')),
            ],
            options={
                'verbose_name': 'Localidade',
            },
        ),
        migrations.CreateModel(
            name='MotivoAfastamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=256, verbose_name='Descrição do motivo de afastamento')),
            ],
            options={
                'verbose_name': 'Motivo do afastmento',
                'verbose_name_plural': 'Motivos dos afastamentos',
            },
        ),
        migrations.CreateModel(
            name='NivelServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=256, verbose_name='Decrição do nivel do serviço')),
            ],
            options={
                'verbose_name': 'Nível do serviço',
                'verbose_name_plural': 'Niveis dos serviços',
            },
        ),
        migrations.CreateModel(
            name='OrigemDiscipulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=256, verbose_name='Origem do discípulo')),
            ],
            options={
                'verbose_name': 'Origens dos discípulos',
            },
        ),
        migrations.CreateModel(
            name='Profissao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=256, verbose_name='Profissão')),
            ],
            options={
                'verbose_name': 'Profissão',
                'verbose_name_plural': 'Profissões',
            },
        ),
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=256, verbose_name='Telefone')),
                ('descricao', models.CharField(max_length=256, verbose_name='Descrição do telefone')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telefones', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Telefone',
            },
        ),
        migrations.CreateModel(
            name='GrupoCaseiro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=256, verbose_name='Grupo Caseiro')),
                ('bloco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grupo_caseiro', to='core.bloco')),
            ],
            options={
                'verbose_name': 'Grupo caseiro',
                'verbose_name_plural': 'Grupos caseiros',
            },
        ),
        migrations.CreateModel(
            name='Conjugue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esposa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='esposa', to=settings.AUTH_USER_MODEL)),
                ('marido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='marido', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cônjugue',
            },
        ),
        migrations.AddField(
            model_name='pessoa',
            name='estado_civil',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='estado_civil', to='core.estadocivil', verbose_name='Estado civil'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='funcao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funcao', to='core.funcao', verbose_name='Função'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='grupo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grupo', to='auth.group', verbose_name='Grupo'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='grupo_caseiro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grupo_caseiro', to='core.grupocaseiro', verbose_name='Grupo caseiro'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='localidade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='localidade', to='core.localidade', verbose_name='Localidade'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='mae',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pessoa_mae', to=settings.AUTH_USER_MODEL, verbose_name='Mãe'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='motivo_afastamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='motivo_afastamento', to='core.motivoafastamento', verbose_name='Motivo do afastamento'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='nivel_servico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nivel', to='core.nivelservico', verbose_name='Nível do servico'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='origem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='origem', to='core.origemdiscipulo', verbose_name='Origem do discípulo'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='pai',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pessoa_pai', to=settings.AUTH_USER_MODEL, verbose_name='Pai'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='profissao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profissao', to='core.profissao', verbose_name='Profissão'),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='JuntaDiscipulado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discipulador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discipulador', to=settings.AUTH_USER_MODEL)),
                ('discipulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discipulo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Discipulado',
                'unique_together': {('discipulador', 'discipulo')},
            },
        ),
    ]
