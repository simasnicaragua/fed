# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Indicador'
        db.create_table('encuesta_indicador', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resultado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['encuesta.Resultado'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('encuesta', ['Indicador'])


    def backwards(self, orm):
        
        # Deleting model 'Indicador'
        db.delete_table('encuesta_indicador')


    models = {
        'encuesta.accionefectuadadocumento': {
            'Meta': {'object_name': 'AccionEfectuadaDocumento'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participantes': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.accionefectuadamedio': {
            'Meta': {'object_name': 'AccionEfectuadaMedio'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participantes': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.accionefectuadaregion': {
            'Meta': {'object_name': 'AccionEfectuadaRegion'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participantes': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.accionfortalececapacidad': {
            'Meta': {'object_name': 'AccionFortaleceCapacidad'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'acciones': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_efectivas': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participantes': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.accionfortalececapadmitiva': {
            'Meta': {'object_name': 'AccionFortaleceCapAdmitiva'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mejorar_apoyo': ('django.db.models.fields.IntegerField', [], {}),
            'mejorar_plan': ('django.db.models.fields.IntegerField', [], {}),
            'mejorar_sistema': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.accionimpulsadagrupo': {
            'Meta': {'object_name': 'AccionImpulsadaGrupo'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'acciones_cambio_discapa': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_cambio_etnia': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_cambio_jovenes': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_cambio_sex': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_emprendidas_discapa': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_emprendidas_etnia': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_emprendidas_jovenes': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_emprendidas_sex': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'encuesta.accionimpulsadaorg': {
            'Meta': {'object_name': 'AccionImpulsadaOrg'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'acciones_cambios_actitud': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_cambios_masculinidad': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_emprendidas': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_impulsadas_masculinidad': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'encuesta.accionobservatorio': {
            'Meta': {'object_name': 'AccionObservatorio'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cantidad_acciones_realiz': ('django.db.models.fields.IntegerField', [], {}),
            'cantidad_acciones_web': ('django.db.models.fields.IntegerField', [], {}),
            'cantidad_observatorios': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'encuesta.accionpromuevenintercambio': {
            'Meta': {'object_name': 'AccionPromuevenIntercambio'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'acciones_efectivas': ('django.db.models.fields.IntegerField', [], {}),
            'acciones_org_part': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participantes': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.accionrealizadareflexion': {
            'Meta': {'object_name': 'AccionRealizadaReflexion'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'discapacidad': ('django.db.models.fields.IntegerField', [], {}),
            'div_sexual': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'etnica': ('django.db.models.fields.IntegerField', [], {}),
            'hombres': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jovenes': ('django.db.models.fields.IntegerField', [], {}),
            'mujeres': ('django.db.models.fields.IntegerField', [], {}),
            'vih': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.accionrelizadareflexionpersona': {
            'Meta': {'object_name': 'AccionRelizadaReflexionPersona'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'discapacidad': ('django.db.models.fields.IntegerField', [], {}),
            'div_sexual': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'etnica': ('django.db.models.fields.IntegerField', [], {}),
            'hombres': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jovenes': ('django.db.models.fields.IntegerField', [], {}),
            'mujeres': ('django.db.models.fields.IntegerField', [], {}),
            'vih': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.atencionvictima': {
            'Meta': {'object_name': 'AtencionVictima'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'servicio_psicologia': ('django.db.models.fields.IntegerField', [], {}),
            'servicio_salud': ('django.db.models.fields.IntegerField', [], {}),
            'sevicio_legal': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.atencionvictimaalbergue': {
            'Meta': {'object_name': 'AtencionVictimaAlbergue'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jovenes': ('django.db.models.fields.IntegerField', [], {}),
            'mujeres': ('django.db.models.fields.IntegerField', [], {}),
            'ninos_ninas': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.denunciajuridica': {
            'Meta': {'object_name': 'DenunciaJuridica'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona_discapacidad': ('django.db.models.fields.IntegerField', [], {}),
            'persona_div_sexual': ('django.db.models.fields.IntegerField', [], {}),
            'persona_joven': ('django.db.models.fields.IntegerField', [], {}),
            'persona_racial': ('django.db.models.fields.IntegerField', [], {}),
            'persona_vih': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.denunciasocialefectiva': {
            'Meta': {'object_name': 'DenunciaSocialEfectiva'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona_discapacidad': ('django.db.models.fields.IntegerField', [], {}),
            'persona_div_sexual': ('django.db.models.fields.IntegerField', [], {}),
            'persona_joven': ('django.db.models.fields.IntegerField', [], {}),
            'persona_racial': ('django.db.models.fields.IntegerField', [], {}),
            'persona_vih': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.denunciasocialrealizada': {
            'Meta': {'object_name': 'DenunciaSocialRealizada'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persona_discapacidad': ('django.db.models.fields.IntegerField', [], {}),
            'persona_div_sexual': ('django.db.models.fields.IntegerField', [], {}),
            'persona_joven': ('django.db.models.fields.IntegerField', [], {}),
            'persona_racial': ('django.db.models.fields.IntegerField', [], {}),
            'persona_vih': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.denunciaviolencia': {
            'Meta': {'object_name': 'DenunciaViolencia'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'comisariato': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'fiscalia': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'encuesta.encuesta': {
            'Meta': {'object_name': 'Encuesta'},
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Organizacion']"}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Proyecto']"})
        },
        'encuesta.estadocapacidadadmitiva': {
            'Meta': {'object_name': 'EstadoCapacidadAdmitiva'},
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organizaciones': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'plan': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sistema': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.indicador': {
            'Meta': {'object_name': 'Indicador'},
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'resultado': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Resultado']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'encuesta.organizacion': {
            'Meta': {'object_name': 'Organizacion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        'encuesta.participacioncomisionagenda': {
            'Meta': {'object_name': 'ParticipacionComisionAgenda'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cantidad_acciones_efec': ('django.db.models.fields.IntegerField', [], {'db_column': "'cant_acc_efec'"}),
            'cantidad_acciones_prom': ('django.db.models.fields.IntegerField', [], {'db_column': "'cant_acc_prom'"}),
            'cantidad_instancias': ('django.db.models.fields.IntegerField', [], {'db_column': "'cat_instancias'"}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'encuesta.participacioncomisiondecision': {
            'Meta': {'object_name': 'ParticipacionComisionDecision'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cantidad_acciones_efectivas': ('django.db.models.fields.IntegerField', [], {}),
            'cantidad_acciones_promovidas': ('django.db.models.fields.IntegerField', [], {}),
            'cantidad_instancias': ('django.db.models.fields.IntegerField', [], {}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'encuesta.proyecto': {
            'Meta': {'object_name': 'Proyecto'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'organizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Organizacion']"})
        },
        'encuesta.referenciacontraref': {
            'Meta': {'object_name': 'ReferenciaContraRef'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jovenes': ('django.db.models.fields.IntegerField', [], {}),
            'mujeres': ('django.db.models.fields.IntegerField', [], {}),
            'ninos_ninas': ('django.db.models.fields.IntegerField', [], {})
        },
        'encuesta.resultado': {
            'Meta': {'object_name': 'Resultado'},
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'encuesta.resultadotrabajado': {
            'Meta': {'object_name': 'ResultadoTrabajado'},
            'encuesta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Encuesta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lugar.Municipio']", 'symmetrical': 'False'}),
            'resultado': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['encuesta.Resultado']"})
        },
        'lugar.departamento': {
            'Meta': {'object_name': 'Departamento'},
            'extension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        },
        'lugar.municipio': {
            'Meta': {'object_name': 'Municipio'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Departamento']"}),
            'extension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'latitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'longitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['encuesta']