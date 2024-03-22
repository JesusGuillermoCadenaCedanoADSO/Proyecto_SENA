BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"action_time"	datetime NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "LimsAire_unidaddemedicion" (
	"id"	integer NOT NULL,
	"nombre"	varchar(45) NOT NULL,
	"simbolo"	varchar(45) NOT NULL,
	"fechacreacion"	datetime NOT NULL,
	"user_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "LimsAire_parametros" (
	"id"	integer NOT NULL,
	"nombre"	varchar(200) NOT NULL,
	"simbolo"	varchar(10) NOT NULL UNIQUE,
	"pmolecular"	real NOT NULL,
	"fechacreacion"	datetime NOT NULL,
	"user_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "LimsAire_mediciones" (
	"id"	integer NOT NULL,
	"fechamedicion"	date NOT NULL,
	"hora"	time NOT NULL,
	"resultado"	real NOT NULL,
	"resultado_conversion"	real NOT NULL,
	"fechacreacion"	datetime NOT NULL,
	"cadena_custodia_id"	bigint NOT NULL,
	"parametro_id"	bigint NOT NULL,
	"unidad_de_conversion_id"	bigint NOT NULL,
	"unidad_de_medida_id"	bigint NOT NULL,
	"user_id"	integer NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("cadena_custodia_id") REFERENCES "LimsAire_cadenadecustodia"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("unidad_de_medida_id") REFERENCES "LimsAire_unidaddemedicion"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("unidad_de_conversion_id") REFERENCES "LimsAire_unidaddemedicion"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("parametro_id") REFERENCES "LimsAire_parametros"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "LimsAire_cadenadecustodia_parametro" (
	"id"	integer NOT NULL,
	"cadenadecustodia_id"	bigint NOT NULL,
	"parametros_id"	bigint NOT NULL,
	FOREIGN KEY("parametros_id") REFERENCES "LimsAire_parametros"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("cadenadecustodia_id") REFERENCES "LimsAire_cadenadecustodia"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "LimsAire_cadenadecustodia" (
	"id"	integer NOT NULL,
	"idcadena"	varchar(20) NOT NULL,
	"cliente"	varchar(45) NOT NULL,
	"proyecto"	varchar(45) NOT NULL,
	"ciudad"	varchar(45) NOT NULL,
	"muestreado_por"	varchar(45) NOT NULL,
	"punto_de_muestreo"	varchar(45) NOT NULL,
	"coordenada_norte"	varchar(45) NOT NULL,
	"coordenada_este"	varchar(45) NOT NULL,
	"altura"	real NOT NULL,
	"observaciones"	text NOT NULL,
	"fechacreacion"	datetime NOT NULL,
	"user_id"	integer NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "LimsAire_factordeconversion" (
	"id"	integer NOT NULL,
	"factor"	real NOT NULL,
	"fechacreacion"	datetime NOT NULL,
	"unidad_destino_id"	bigint NOT NULL,
	"unidad_origen_id"	bigint NOT NULL,
	"user_id"	integer NOT NULL,
	"parametro_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("parametro_id") REFERENCES "LimsAire_parametros"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("unidad_destino_id") REFERENCES "LimsAire_unidaddemedicion"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("unidad_origen_id") REFERENCES "LimsAire_unidaddemedicion"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2024-03-12 15:43:45.711320');
INSERT INTO "django_migrations" VALUES (2,'auth','0001_initial','2024-03-12 15:43:46.036459');
INSERT INTO "django_migrations" VALUES (4,'admin','0001_initial','2024-03-12 15:43:46.518641');
INSERT INTO "django_migrations" VALUES (5,'admin','0002_logentry_remove_auto_add','2024-03-12 15:43:46.651376');
INSERT INTO "django_migrations" VALUES (6,'admin','0003_logentry_add_action_flag_choices','2024-03-12 15:43:46.817520');
INSERT INTO "django_migrations" VALUES (7,'contenttypes','0002_remove_content_type_name','2024-03-12 15:43:46.991205');
INSERT INTO "django_migrations" VALUES (8,'auth','0002_alter_permission_name_max_length','2024-03-12 15:43:47.179561');
INSERT INTO "django_migrations" VALUES (9,'auth','0003_alter_user_email_max_length','2024-03-12 15:43:47.334823');
INSERT INTO "django_migrations" VALUES (10,'auth','0004_alter_user_username_opts','2024-03-12 15:43:47.514335');
INSERT INTO "django_migrations" VALUES (11,'auth','0005_alter_user_last_login_null','2024-03-12 15:43:47.653027');
INSERT INTO "django_migrations" VALUES (12,'auth','0006_require_contenttypes_0002','2024-03-12 15:43:47.808593');
INSERT INTO "django_migrations" VALUES (13,'auth','0007_alter_validators_add_error_messages','2024-03-12 15:43:47.927663');
INSERT INTO "django_migrations" VALUES (14,'auth','0008_alter_user_username_max_length','2024-03-12 15:43:48.077156');
INSERT INTO "django_migrations" VALUES (15,'auth','0009_alter_user_last_name_max_length','2024-03-12 15:43:48.277605');
INSERT INTO "django_migrations" VALUES (16,'auth','0010_alter_group_name_max_length','2024-03-12 15:43:48.440625');
INSERT INTO "django_migrations" VALUES (17,'auth','0011_update_proxy_permissions','2024-03-12 15:43:48.596053');
INSERT INTO "django_migrations" VALUES (18,'auth','0012_alter_user_first_name_max_length','2024-03-12 15:43:48.726582');
INSERT INTO "django_migrations" VALUES (19,'sessions','0001_initial','2024-03-12 15:43:49.000625');
INSERT INTO "django_migrations" VALUES (30,'LimsAire','0001_initial','2024-03-15 19:52:02.177323');
INSERT INTO "django_migrations" VALUES (31,'LimsAire','0002_rename_parametros_factordeconversion_parametro','2024-03-15 21:18:23.508488');
INSERT INTO "django_migrations" VALUES (32,'LimsAire','0003_alter_cadenadecustodia_idcadena_and_more','2024-03-16 17:16:19.930085');
INSERT INTO "django_admin_log" VALUES (1,'2024-03-12 15:51:20.062281','c6ec900f-486e-4c8c-92cf-5d249ec973a3','Partes por billon simbolo : ppb','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (2,'2024-03-12 15:51:33.500212','9149b9bc-09b1-429d-99ec-cec334b2957f','partes por millon simbolo : ppm','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (3,'2024-03-12 15:51:58.102341','328b0e8a-18e4-40fe-a47e-bd209dccf8d4','microgramo por metro cubico simbolo : ug/m3','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (4,'2024-03-12 15:57:14.648699','1','ozono','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (5,'2024-03-12 15:57:38.716344','2','monoxido de carbono','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (6,'2024-03-12 15:58:06.563685','3','dioxido de azufre','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (7,'2024-03-12 15:58:30.901561','4','dioxido de nitrogeno','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (8,'2024-03-12 15:59:58.590373','5','particulas con diametro menor a 10 um','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (9,'2024-03-12 16:00:15.116926','6','particulas con diametro menor a 2.5 um','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (10,'2024-03-12 16:27:14.461548','1','ozono de ppb a ug/m3','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (11,'2024-03-12 16:28:34.110442','2','ozono de ug/m3 a ppb','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (12,'2024-03-12 16:35:35.499368','1','001 de proyecto CALIDAD DE AIRE','[{"added": {}}]',12,1,1);
INSERT INTO "django_admin_log" VALUES (13,'2024-03-12 16:37:52.791157','1','ozono de cadena 001','[{"added": {}}]',7,1,1);
INSERT INTO "django_admin_log" VALUES (14,'2024-03-12 19:22:00.444687','1','medicion de ozono por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (15,'2024-03-12 19:38:38.117286','1','medicion de ozono de plan 001 tomada el dia 2024-03-12 por jesuscadena','',10,1,3);
INSERT INTO "django_admin_log" VALUES (16,'2024-03-12 19:39:03.823846','2','medicion de ozono de plan 001 tomada el dia 2024-03-12 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (17,'2024-03-12 19:43:57.595718','2','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 14:38:44 por jesuscadena','',10,1,3);
INSERT INTO "django_admin_log" VALUES (18,'2024-03-12 19:46:31.777843','1','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 14:46:20 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (19,'2024-03-12 19:53:42.382227','3','ozono de ppb a ppb','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (20,'2024-03-12 19:53:53.759849','4','ozono de ug/m3 a ug/m3','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (21,'2024-03-12 20:26:56.701676','1','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 14:46:20 por jesuscadena','',10,1,3);
INSERT INTO "django_admin_log" VALUES (22,'2024-03-12 20:31:47.439975','1','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:31:37 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (23,'2024-03-12 20:40:27.747459','1','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:31:37 por jesuscadena','',10,1,3);
INSERT INTO "django_admin_log" VALUES (24,'2024-03-12 20:40:45.266379','2','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:40:37 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (25,'2024-03-12 20:43:22.337379','2','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:40:37 por jesuscadena','',10,1,3);
INSERT INTO "django_admin_log" VALUES (26,'2024-03-12 20:43:38.136968','3','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:43:30 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (27,'2024-03-12 20:49:27.795200','3','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:43:30 por jesuscadena','',10,1,3);
INSERT INTO "django_admin_log" VALUES (28,'2024-03-12 20:49:42.645165','4','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:49:33 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (29,'2024-03-12 20:52:22.295054','4','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:49:33 por jesuscadena','[]',10,1,2);
INSERT INTO "django_admin_log" VALUES (30,'2024-03-12 20:57:24.291805','4','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:49:33 por jesuscadena','[]',10,1,2);
INSERT INTO "django_admin_log" VALUES (31,'2024-03-12 21:15:14.182188','4','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:49:33 por jesuscadena','[{"changed": {"fields": ["Unidad de conversion"]}}]',10,1,2);
INSERT INTO "django_admin_log" VALUES (32,'2024-03-12 21:17:59.809917','4','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:49:33 por jesuscadena','[]',10,1,2);
INSERT INTO "django_admin_log" VALUES (33,'2024-03-12 21:18:23.187563','4','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:49:33 por jesuscadena','[{"changed": {"fields": ["Unidad de conversion"]}}]',10,1,2);
INSERT INTO "django_admin_log" VALUES (34,'2024-03-12 21:33:06.128815','4','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:49:33 por jesuscadena','[]',10,1,2);
INSERT INTO "django_admin_log" VALUES (35,'2024-03-12 21:42:13.302603','4','medicion de ozono de plan 001 tomada el dia 2024-03-12 a las 15:49:33 por jesuscadena','[{"changed": {"fields": ["Unidad de conversion"]}}]',10,1,2);
INSERT INTO "django_admin_log" VALUES (36,'2024-03-13 13:08:19.686829','1','001 de proyecto CALIDAD DE AIRE','[{"changed": {"fields": ["Parametro"]}}]',12,1,2);
INSERT INTO "django_admin_log" VALUES (37,'2024-03-13 13:10:26.977530','1','001 de proyecto CALIDAD DE AIRE','[]',12,1,2);
INSERT INTO "django_admin_log" VALUES (38,'2024-03-13 13:18:31.799070','4','medicion de   plan 001 tomada el dia 2024-03-12 a las 15:49:33 por jesuscadena','[]',10,1,2);
INSERT INTO "django_admin_log" VALUES (39,'2024-03-13 13:46:56.475752','4','medicion de   plan 001 tomada el dia 2024-03-12 a las 15:49:33 por jesuscadena','[{"changed": {"fields": ["Resultado", "Unidad de conversion"]}}]',10,1,2);
INSERT INTO "django_admin_log" VALUES (40,'2024-03-13 13:47:58.072790','5','medicion de   plan 001 tomada el dia 2024-03-13 a las 08:47:25 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (41,'2024-03-13 13:55:13.735281','5','medicion de   plan 001 de parametro ozono tomada el dia 2024-03-13 a las 08:47:25 por jesuscadena','',10,1,3);
INSERT INTO "django_admin_log" VALUES (42,'2024-03-13 13:55:17.773426','4','medicion de   plan 001 de parametro ozono tomada el dia 2024-03-12 a las 15:49:33 por jesuscadena','',10,1,3);
INSERT INTO "django_admin_log" VALUES (43,'2024-03-13 13:55:35.577537','6','medicion de   plan 001 de parametro ozono tomada el dia 2024-03-13 a las 08:55:27 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (44,'2024-03-13 13:57:41.444238','7','medicion de   plan 001 de parametro ozono tomada el dia 2024-03-13 a las 08:57:30 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (45,'2024-03-13 15:05:49.857584','5','monoxido de carbono de ppm a ug/m3','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (46,'2024-03-13 15:06:18.535133','6','monoxido de carbono de ug/m3 a ppm','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (47,'2024-03-13 15:06:38.422143','5','monoxido de carbono de ppm a ug/m3','[{"changed": {"fields": ["Factor"]}}]',11,1,2);
INSERT INTO "django_admin_log" VALUES (48,'2024-03-13 15:07:03.816982','7','monoxido de carbono de ppm a ppm','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (49,'2024-03-13 15:07:17.018976','8','monoxido de carbono de ug/m3 a ug/m3','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (50,'2024-03-13 15:08:35.555571','2','002 de proyecto proyecto 2','[{"added": {}}]',12,1,1);
INSERT INTO "django_admin_log" VALUES (51,'2024-03-13 15:09:23.151099','8','medicion de   plan 002 de parametro ozono tomada el dia 2024-03-13 a las 10:09:14 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (52,'2024-03-13 15:10:36.217286','9','medicion de   plan 002 de parametro monoxido de carbono tomada el dia 2024-03-13 a las 10:09:47 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (53,'2024-03-15 19:52:44.694308','1','partes por millón simbolo : ppm','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (54,'2024-03-15 19:53:19.780512','2','Partes por billón simbolo : ppb','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (55,'2024-03-15 19:54:00.841733','3','microgramo por metro cúbico simbolo : mcg/m3','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (56,'2024-03-15 19:54:19.068207','4','nanogramo por metro cúbico simbolo : nng/m3','[{"added": {}}]',8,1,1);
INSERT INTO "django_admin_log" VALUES (57,'2024-03-15 19:54:47.162151','1','ozono','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (58,'2024-03-15 19:55:11.174159','2','dióxido de nitrógeno','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (59,'2024-03-15 19:55:31.410640','3','monóxido de carbono','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (60,'2024-03-15 19:56:03.916094','4','dióxido de azufre','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (61,'2024-03-15 19:56:37.954979','5','material particulado 2.5 micras','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (62,'2024-03-15 19:56:57.900819','6','material particulado 10 micras','[{"added": {}}]',9,1,1);
INSERT INTO "django_admin_log" VALUES (63,'2024-03-15 19:57:28.509822','1','ozono de ppm a ppm','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (64,'2024-03-15 19:58:02.312470','2','ozono de ppb a mcg/m3','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (65,'2024-03-15 19:58:32.556814','3','ozono de mcg/m3 a ppb','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (66,'2024-03-15 19:58:45.572582','4','ozono de ppb a ppb','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (67,'2024-03-15 19:59:01.374044','5','ozono de mcg/m3 a mcg/m3','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (68,'2024-03-15 19:59:18.991832','6','monóxido de carbono de ppm a ppm','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (69,'2024-03-15 19:59:37.532467','7','monóxido de carbono de ppm a mcg/m3','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (70,'2024-03-15 19:59:56.100915','8','monóxido de carbono de mcg/m3 a ppm','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (71,'2024-03-15 20:00:10.512605','9','monóxido de carbono de mcg/m3 a mcg/m3','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (72,'2024-03-15 20:01:21.855258','1','001 de proyecto proyecto 1','[{"added": {}}]',12,1,1);
INSERT INTO "django_admin_log" VALUES (73,'2024-03-15 20:02:55.893127','1','medicion de   plan 001 de parametro ozono tomada el dia 2024-03-15 a las 15:02:44 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_admin_log" VALUES (74,'2024-03-15 20:03:36.784871','2','medicion de   plan 001 de parametro monóxido de carbono tomada el dia 2024-03-15 a las 15:03:04 por jesuscadena','[{"added": {}}]',10,1,1);
INSERT INTO "django_content_type" VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" VALUES (2,'auth','permission');
INSERT INTO "django_content_type" VALUES (3,'auth','group');
INSERT INTO "django_content_type" VALUES (4,'auth','user');
INSERT INTO "django_content_type" VALUES (5,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES (6,'sessions','session');
INSERT INTO "django_content_type" VALUES (7,'LimsAire','asignacionesdeparametros');
INSERT INTO "django_content_type" VALUES (8,'LimsAire','unidaddemedicion');
INSERT INTO "django_content_type" VALUES (9,'LimsAire','parametros');
INSERT INTO "django_content_type" VALUES (10,'LimsAire','mediciones');
INSERT INTO "django_content_type" VALUES (11,'LimsAire','factordeconversion');
INSERT INTO "django_content_type" VALUES (12,'LimsAire','cadenadecustodia');
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (14,4,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (15,4,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (16,4,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (17,5,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (18,5,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (19,5,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (20,5,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (21,6,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (22,6,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (23,6,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (24,6,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (25,7,'add_asignacionesdeparametros','Can add asignaciones de parametros');
INSERT INTO "auth_permission" VALUES (26,7,'change_asignacionesdeparametros','Can change asignaciones de parametros');
INSERT INTO "auth_permission" VALUES (27,7,'delete_asignacionesdeparametros','Can delete asignaciones de parametros');
INSERT INTO "auth_permission" VALUES (28,7,'view_asignacionesdeparametros','Can view asignaciones de parametros');
INSERT INTO "auth_permission" VALUES (29,8,'add_unidaddemedicion','Can add unidad de medicion');
INSERT INTO "auth_permission" VALUES (30,8,'change_unidaddemedicion','Can change unidad de medicion');
INSERT INTO "auth_permission" VALUES (31,8,'delete_unidaddemedicion','Can delete unidad de medicion');
INSERT INTO "auth_permission" VALUES (32,8,'view_unidaddemedicion','Can view unidad de medicion');
INSERT INTO "auth_permission" VALUES (33,9,'add_parametros','Can add parametros');
INSERT INTO "auth_permission" VALUES (34,9,'change_parametros','Can change parametros');
INSERT INTO "auth_permission" VALUES (35,9,'delete_parametros','Can delete parametros');
INSERT INTO "auth_permission" VALUES (36,9,'view_parametros','Can view parametros');
INSERT INTO "auth_permission" VALUES (37,10,'add_mediciones','Can add mediciones');
INSERT INTO "auth_permission" VALUES (38,10,'change_mediciones','Can change mediciones');
INSERT INTO "auth_permission" VALUES (39,10,'delete_mediciones','Can delete mediciones');
INSERT INTO "auth_permission" VALUES (40,10,'view_mediciones','Can view mediciones');
INSERT INTO "auth_permission" VALUES (41,11,'add_factordeconversion','Can add factor de conversion');
INSERT INTO "auth_permission" VALUES (42,11,'change_factordeconversion','Can change factor de conversion');
INSERT INTO "auth_permission" VALUES (43,11,'delete_factordeconversion','Can delete factor de conversion');
INSERT INTO "auth_permission" VALUES (44,11,'view_factordeconversion','Can view factor de conversion');
INSERT INTO "auth_permission" VALUES (45,12,'add_cadenadecustodia','Can add cadena de custodia');
INSERT INTO "auth_permission" VALUES (46,12,'change_cadenadecustodia','Can change cadena de custodia');
INSERT INTO "auth_permission" VALUES (47,12,'delete_cadenadecustodia','Can delete cadena de custodia');
INSERT INTO "auth_permission" VALUES (48,12,'view_cadenadecustodia','Can view cadena de custodia');
INSERT INTO "auth_user" VALUES (1,'pbkdf2_sha256$600000$rsE0P7BnOCTsuaQuo4gY9M$c7dRvO05dKtADJji4nAiSG71bpkAInzOiRWb2ZuQMAU=','2024-03-22 15:36:45.507047',1,'jesuscadena','','uranium_bells@hotmail.com',1,1,'2024-03-12 15:46:10.814141','');
INSERT INTO "auth_user" VALUES (2,'pbkdf2_sha256$600000$jgOYZvviyzr96p9IKUAekj$U8ZL49ISeyk2bfLD5Z3uhvopUA98QFenMc5qsvlmbgU=','2024-03-14 19:00:09.760495',0,'nuevo_usuario','','',0,1,'2024-03-14 19:00:09.096576','');
INSERT INTO "django_session" VALUES ('viet5mhpb2s1pv69r9ex0ku6z1lb84sz','.eJxVjEEOwiAQRe_C2hAoUzq4dO8ZyMBMpWpoUtqV8e7apAvd_vfef6lI21ri1mSJE6uzsur0uyXKD6k74DvV26zzXNdlSnpX9EGbvs4sz8vh_h0UauVbw4gUkoAxA_rAeQyIvkNAGwQNgbOdd9AHccQyABvIkqzpwXIKjkS9P8cKN1M:1rk4Kw:UgTxd5Djx25jNyEUw1Ho-wbuNIjkJZAwv8aR0hHGNnE','2024-03-26 15:46:42.558801');
INSERT INTO "django_session" VALUES ('ji6mipbnnlzqck1a8liwtx7g0ljzove9','.eJxVjEEOwiAQRe_C2hBgKAWX7nsGMsCMrRqalHZlvLtt0oVu_3vvv0XEbR3j1miJUxFXocXld0uYn1QPUB5Y77PMc12XKclDkSdtcpgLvW6n-3cwYhv3umOlSweMneuto6QMEoAFbRKAcyV4RutZ8Y4Ug8-90ZwVBCo2ewri8wXVgDfP:1rkYOG:b4BcNfBaCyH--c3Xqkprs4r_KF-uaEMZFaps0M6A-E0','2024-03-27 23:52:08.196891');
INSERT INTO "django_session" VALUES ('atw7x0z8c806vrwe563esve15r2dtt6f','.eJxVjEEOwiAQRe_C2hBgKAWX7nsGMsCMrRqalHZlvLtt0oVu_3vvv0XEbR3j1miJUxFXocXld0uYn1QPUB5Y77PMc12XKclDkSdtcpgLvW6n-3cwYhv3umOlSweMneuto6QMEoAFbRKAcyV4RutZ8Y4Ug8-90ZwVBCo2ewri8wXVgDfP:1rkYV1:6Fiu2cIeJFzKK7SYHG04v5rK9vuBlKH67TGrAo7HMdc','2024-03-27 23:59:07.211538');
INSERT INTO "django_session" VALUES ('e5r6n584z6sybsxl9uolvzqdex92i9j2','.eJxVjEEOwiAQRe_C2hBgKAWX7nsGMsCMrRqalHZlvLtt0oVu_3vvv0XEbR3j1miJUxFXocXld0uYn1QPUB5Y77PMc12XKclDkSdtcpgLvW6n-3cwYhv3umOlSweMneuto6QMEoAFbRKAcyV4RutZ8Y4Ug8-90ZwVBCo2ewri8wXVgDfP:1rkYZ1:PlA5_6dzPiZRF5fCypLObTD-N8iEPIC6EMlaOjqO_vY','2024-03-28 00:03:15.772355');
INSERT INTO "django_session" VALUES ('44hxkg5npbn7uw5il1j9r22l8lq2kuvm','.eJxVjEEOwiAQRe_C2hBgKAWX7nsGMsCMrRqalHZlvLtt0oVu_3vvv0XEbR3j1miJUxFXocXld0uYn1QPUB5Y77PMc12XKclDkSdtcpgLvW6n-3cwYhv3umOlSweMneuto6QMEoAFbRKAcyV4RutZ8Y4Ug8-90ZwVBCo2ewri8wXVgDfP:1rkYaV:WAO08QAXuNMnmdKAUMAFwfhywgLLjgvxe2mS0WNtfWw','2024-03-28 00:04:47.586057');
INSERT INTO "django_session" VALUES ('31oxtdiayzlq6a968w3wklid5xfiipz0','.eJxVjEEOwiAQRe_C2hBgKAWX7nsGMsCMrRqalHZlvLtt0oVu_3vvv0XEbR3j1miJUxFXocXld0uYn1QPUB5Y77PMc12XKclDkSdtcpgLvW6n-3cwYhv3umOlSweMneuto6QMEoAFbRKAcyV4RutZ8Y4Ug8-90ZwVBCo2ewri8wXVgDfP:1rktWm:8PLfDmKgYdRHoGTZZ7toXSEc3zstKtRfdLKtvTNRpwg','2024-03-28 22:26:20.322364');
INSERT INTO "django_session" VALUES ('1z1b1k1mns8wa0f2i1gzxuu15ofz46yp','.eJxVjEEOwiAQRe_C2hBgKAWX7nsGMsCMrRqalHZlvLtt0oVu_3vvv0XEbR3j1miJUxFXocXld0uYn1QPUB5Y77PMc12XKclDkSdtcpgLvW6n-3cwYhv3umOlSweMneuto6QMEoAFbRKAcyV4RutZ8Y4Ug8-90ZwVBCo2ewri8wXVgDfP:1rktjw:Hs_SZCUJ9hTSpdXrU2pzZL3iP6ISZ4Djs3qLHhAFhKw','2024-03-28 22:39:56.951136');
INSERT INTO "django_session" VALUES ('f3s55lpt8c4flt9hnyotifedw5gjfcwq','.eJxVjEEOwiAQRe_C2hBgKAWX7nsGMsCMrRqalHZlvLtt0oVu_3vvv0XEbR3j1miJUxFXocXld0uYn1QPUB5Y77PMc12XKclDkSdtcpgLvW6n-3cwYhv3umOlSweMneuto6QMEoAFbRKAcyV4RutZ8Y4Ug8-90ZwVBCo2ewri8wXVgDfP:1rlE1O:Sa9YT8n0a1s-5UPvfGDWNiamoAsaJ0k07qPGQGQWvfc','2024-03-29 20:19:18.417591');
INSERT INTO "django_session" VALUES ('j9lxfgf53qxz7ix14ju1hd45rx1vumcf','.eJxVjEEOwiAQRe_C2hBgKAWX7nsGMsCMrRqalHZlvLtt0oVu_3vvv0XEbR3j1miJUxFXocXld0uYn1QPUB5Y77PMc12XKclDkSdtcpgLvW6n-3cwYhv3umOlSweMneuto6QMEoAFbRKAcyV4RutZ8Y4Ug8-90ZwVBCo2ewri8wXVgDfP:1rmLmC:9w56hy2OzpX4TcQjggGmmqY1ndDbSp_U5uWxdaJQfPw','2024-04-01 22:48:16.285379');
INSERT INTO "django_session" VALUES ('hmak6a5p5p0wng8wh2u2676vmwk8rydu','.eJxVjEEOwiAQRe_C2hBgKAWX7nsGMsCMrRqalHZlvLtt0oVu_3vvv0XEbR3j1miJUxFXocXld0uYn1QPUB5Y77PMc12XKclDkSdtcpgLvW6n-3cwYhv3umOlSweMneuto6QMEoAFbRKAcyV4RutZ8Y4Ug8-90ZwVBCo2ewri8wXVgDfP:1rnI0e:mWVe__FXDVxmK3TrFY2NxXKJkIxf8pK2S7hoc8-X6IY','2024-04-04 12:59:04.655754');
INSERT INTO "django_session" VALUES ('4ixjkxjiewgxu3248pb7a1ehtbhzlowi','.eJxVjEEOwiAQRe_C2hBgKAWX7nsGMsCMrRqalHZlvLtt0oVu_3vvv0XEbR3j1miJUxFXocXld0uYn1QPUB5Y77PMc12XKclDkSdtcpgLvW6n-3cwYhv3umOlSweMneuto6QMEoAFbRKAcyV4RutZ8Y4Ug8-90ZwVBCo2ewri8wXVgDfP:1rnIGG:IRAmeItR30YcAzwHC6BY7h_lDYu6KUuxlj_wUNjUpOU','2024-04-04 13:15:12.714721');
INSERT INTO "django_session" VALUES ('xgsuga7tpw0eojk9nun8i4apis1e5l2l','.eJxVjEEOwiAQRe_C2hBgKAWX7nsGMsCMrRqalHZlvLtt0oVu_3vvv0XEbR3j1miJUxFXocXld0uYn1QPUB5Y77PMc12XKclDkSdtcpgLvW6n-3cwYhv3umOlSweMneuto6QMEoAFbRKAcyV4RutZ8Y4Ug8-90ZwVBCo2ewri8wXVgDfP:1rngwn:5iVqhaoQcm_h-6UfgHqCDYv981hYNtZaqRjCviyYztA','2024-04-05 15:36:45.608148');
INSERT INTO "LimsAire_unidaddemedicion" VALUES (1,'partes por millón','ppm','2024-03-15 19:52:44.681311',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (2,'Partes por billón','ppb','2024-03-15 19:53:19.767523',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (3,'microgramo por metro cúbico','mcg/m3','2024-03-15 19:54:00.828582',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (4,'nanogramo por metro cúbico','nng/m3','2024-03-15 19:54:19.066213',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (6,'nueva unidad','nuevo simbolo6','2024-03-19 01:35:54.983313',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (25,'ni','ii','2024-03-21 19:31:48.605956',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (26,'iu','iuy','2024-03-21 19:33:25.974768',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (27,'lkjh','kjh','2024-03-21 19:34:34.986618',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (28,'kjhkj','kjh','2024-03-21 19:35:07.365483',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (29,'hh','kjh','2024-03-21 19:49:04.854503',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (38,'hjggh','gg','2024-03-21 20:19:52.125598',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (39,'hgghhg','hh','2024-03-21 20:21:31.986931',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (46,'g','g','2024-03-21 20:57:01.449450',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (47,'f','f','2024-03-21 21:02:26.794816',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (48,'f','f','2024-03-21 21:02:58.520421',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (49,'f','f','2024-03-21 21:03:28.672007',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (50,'f','f','2024-03-21 21:03:53.235934',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (51,'f','f','2024-03-21 21:05:36.362308',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (52,'kk','kk','2024-03-21 21:05:44.828419',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (53,'g','g','2024-03-21 21:06:49.637864',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (54,'k','k','2024-03-21 21:07:29.361029',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (55,'jkk','kljh','2024-03-21 21:07:56.777215',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (56,'tt','tt','2024-03-21 21:11:31.685368',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (57,'ff','ff','2024-03-21 21:11:49.316727',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (58,'r','r','2024-03-21 21:12:27.256820',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (59,'g','g','2024-03-21 21:17:54.808736',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (60,'hh','hh','2024-03-21 21:19:22.995832',1);
INSERT INTO "LimsAire_unidaddemedicion" VALUES (67,'partes por mil','ppt','2024-03-22 15:56:33.856365',1);
INSERT INTO "LimsAire_parametros" VALUES (1,'ozono','O3',47.9982,'2024-03-15 19:54:47.149158',1);
INSERT INTO "LimsAire_parametros" VALUES (2,'dióxido de nitrógeno','NO2',46.0055,'2024-03-15 19:55:11.172163',1);
INSERT INTO "LimsAire_parametros" VALUES (3,'monóxido de carbono','CO',28.0101,'2024-03-15 19:55:31.397668',1);
INSERT INTO "LimsAire_parametros" VALUES (4,'dióxido de azufre','SO2',64.064,'2024-03-15 19:56:03.902394',1);
INSERT INTO "LimsAire_parametros" VALUES (5,'material particulado 2.5 micras','pm2.5',1.0,'2024-03-15 19:56:37.941946',1);
INSERT INTO "LimsAire_parametros" VALUES (6,'material particulado 10 micras','PM10',1.0,'2024-03-15 19:56:57.887961',1);
INSERT INTO "LimsAire_parametros" VALUES (9,'np','nps',1.5,'2024-03-21 13:51:01.241755',1);
INSERT INTO "LimsAire_mediciones" VALUES (1,'2024-03-15','15:02:44',1.22,2.390114444,'2024-03-15 20:02:55.878898',1,1,3,2,1);
INSERT INTO "LimsAire_mediciones" VALUES (2,'2024-03-15','15:03:04',0.00071,0.8117212669,'2024-03-15 20:03:36.770017',1,3,3,1,1);
INSERT INTO "LimsAire_mediciones" VALUES (3,'2024-03-16','17:31:00',2.5,1.0,'2024-03-16 21:32:13.666201',1,1,3,2,1);
INSERT INTO "LimsAire_mediciones" VALUES (4,'2024-03-16','17:14:00',1.22,1.22,'2024-03-16 22:15:19.944151',1,1,2,2,1);
INSERT INTO "LimsAire_mediciones" VALUES (6,'2024-03-21','08:09:00',5.0,5.0,'2024-03-21 16:26:35.213471',4,1,1,1,1);
INSERT INTO "LimsAire_mediciones" VALUES (7,'2024-03-20','10:00:00',5.0,5.0,'2024-03-21 16:29:46.215259',1,1,1,1,1);
INSERT INTO "LimsAire_mediciones" VALUES (8,'2024-03-21','14:00:00',10.0,19.591102,'2024-03-21 16:32:19.152170',1,1,3,2,1);
INSERT INTO "LimsAire_mediciones" VALUES (9,'2024-03-21','14:00:02',8.0,1.0,'2024-03-21 16:33:42.081009',1,1,1,3,1);
INSERT INTO "LimsAire_mediciones" VALUES (13,'2024-03-21','08:00:00',1.22,1.22,'2024-03-21 21:46:35.651054',1,1,1,1,1);
INSERT INTO "LimsAire_mediciones" VALUES (14,'2024-03-21','08:00:00',1.25,1.25,'2024-03-21 21:47:17.632324',1,1,1,1,1);
INSERT INTO "LimsAire_mediciones" VALUES (15,'2024-03-22','08:00:00',1.5,1.5,'2024-03-21 21:49:44.401493',1,1,1,1,1);
INSERT INTO "LimsAire_mediciones" VALUES (16,'2024-03-21','08:00:00',1.0,1.0,'2024-03-21 21:50:22.132567',1,1,1,1,1);
INSERT INTO "LimsAire_cadenadecustodia_parametro" VALUES (1,1,1);
INSERT INTO "LimsAire_cadenadecustodia_parametro" VALUES (2,1,3);
INSERT INTO "LimsAire_cadenadecustodia_parametro" VALUES (7,7,1);
INSERT INTO "LimsAire_cadenadecustodia_parametro" VALUES (8,7,3);
INSERT INTO "LimsAire_cadenadecustodia_parametro" VALUES (11,8,1);
INSERT INTO "LimsAire_cadenadecustodia" VALUES (1,'001','cliente 1','proyecto 1','ciudad 1','tecnico 1','punto','100','200',1500.0,'Ninguna','2024-03-15 20:01:21.850679',1);
INSERT INTO "LimsAire_cadenadecustodia" VALUES (2,'002','cliente 2','proyecto 2','ciudad 2','tecnico 2','punto 2','12345','6789',1399.0,'ninguna','2024-03-16 17:20:20.214085',1);
INSERT INTO "LimsAire_cadenadecustodia" VALUES (4,'003','abc','def','cc','xyz','puj','123','1234',1500.0,'na','2024-03-21 15:34:47.326861',1);
INSERT INTO "LimsAire_cadenadecustodia" VALUES (7,'004','cliente 1','proyecto 1','ciudad 1','tecnico 1','punto','100','200',1500.0,'Ninguna','2024-03-21 17:18:06.393658',1);
INSERT INTO "LimsAire_cadenadecustodia" VALUES (8,'008','j','j','j','j','j','j','j',100.0,'cfd','2024-03-21 17:20:06.607244',1);
INSERT INTO "LimsAire_factordeconversion" VALUES (1,1.0,'2024-03-15 19:57:28.494681',1,1,1,1);
INSERT INTO "LimsAire_factordeconversion" VALUES (2,1.9591102,'2024-03-15 19:58:02.299068',3,2,1,1);
INSERT INTO "LimsAire_factordeconversion" VALUES (3,0.51043581,'2024-03-15 19:58:32.554807',2,3,1,1);
INSERT INTO "LimsAire_factordeconversion" VALUES (4,1.0,'2024-03-15 19:58:45.559318',2,2,1,1);
INSERT INTO "LimsAire_factordeconversion" VALUES (5,1.0,'2024-03-15 19:59:01.361044',3,3,1,1);
INSERT INTO "LimsAire_factordeconversion" VALUES (6,1.0,'2024-03-15 19:59:18.989831',1,1,1,3);
INSERT INTO "LimsAire_factordeconversion" VALUES (7,1143.26939,'2024-03-15 19:59:37.530469',3,1,1,3);
INSERT INTO "LimsAire_factordeconversion" VALUES (8,0.00087469,'2024-03-15 19:59:56.086740',1,3,1,3);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "LimsAire_unidaddemedicion_user_id_d4778513" ON "LimsAire_unidaddemedicion" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_parametros_user_id_0f430289" ON "LimsAire_parametros" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_mediciones_cadena_custodia_id_4960b2bb" ON "LimsAire_mediciones" (
	"cadena_custodia_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_mediciones_parametro_id_a05598f8" ON "LimsAire_mediciones" (
	"parametro_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_mediciones_unidad_de_conversion_id_89198303" ON "LimsAire_mediciones" (
	"unidad_de_conversion_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_mediciones_unidad_de_medida_id_51aa161d" ON "LimsAire_mediciones" (
	"unidad_de_medida_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_mediciones_user_id_d9780443" ON "LimsAire_mediciones" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "LimsAire_cadenadecustodia_parametro_cadenadecustodia_id_parametros_id_b0e6be03_uniq" ON "LimsAire_cadenadecustodia_parametro" (
	"cadenadecustodia_id",
	"parametros_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_cadenadecustodia_parametro_cadenadecustodia_id_5a0159c7" ON "LimsAire_cadenadecustodia_parametro" (
	"cadenadecustodia_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_cadenadecustodia_parametro_parametros_id_b7d23260" ON "LimsAire_cadenadecustodia_parametro" (
	"parametros_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_cadenadecustodia_user_id_021cca77" ON "LimsAire_cadenadecustodia" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_factordeconversion_unidad_destino_id_0917fa18" ON "LimsAire_factordeconversion" (
	"unidad_destino_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_factordeconversion_unidad_origen_id_5e76e6d5" ON "LimsAire_factordeconversion" (
	"unidad_origen_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_factordeconversion_user_id_cd3775bf" ON "LimsAire_factordeconversion" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "LimsAire_factordeconversion_parametro_id_bce59b08" ON "LimsAire_factordeconversion" (
	"parametro_id"
);
COMMIT;
