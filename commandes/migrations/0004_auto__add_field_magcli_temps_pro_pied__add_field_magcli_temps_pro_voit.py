# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Magcli.temps_pro_pied'
        db.add_column('commandes_magcli', 'temps_pro_pied', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # Adding field 'Magcli.temps_pro_voiture'
        db.add_column('commandes_magcli', 'temps_pro_voiture', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Magcli.temps_pro_pied'
        db.delete_column('commandes_magcli', 'temps_pro_pied')

        # Deleting field 'Magcli.temps_pro_voiture'
        db.delete_column('commandes_magcli', 'temps_pro_voiture')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'categories.categories': {
            'Meta': {'object_name': 'Categories'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'clients.customer': {
            'Meta': {'object_name': 'Customer'},
            'adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_pro': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['categories.Categories']", 'symmetrical': 'False'}),
            'cp': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'cp_pro': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'date_inscription': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'distance_max_home': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'distance_max_pro': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_adresse': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_home': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'lat_pro': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'lng_home': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'lng_pro': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'pays': ('django.db.models.fields.CharField', [], {'default': "'France'", 'max_length': '128'}),
            'pays_pro': ('django.db.models.fields.CharField', [], {'default': "'France'", 'max_length': '128'}),
            'phoneapp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ville_pro': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'commandes.magcli': {
            'Meta': {'unique_together': "(('client', 'magasin'),)", 'object_name': 'Magcli'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Customer']"}),
            'distance_home': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'distance_pro': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magasin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['magasins.Magasin']"}),
            'match_category': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'temps_home_pied': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'temps_home_voiture': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'temps_pro_pied': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'temps_pro_voiture': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'magasins.magasin': {
            'Meta': {'object_name': 'Magasin'},
            'adresse': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Categories']"}),
            'cp': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_commercial': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pays': ('django.db.models.fields.CharField', [], {'default': "'France'", 'max_length': '128'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['commandes']
