from django.core.management.base import BaseCommand
from app.escrutinio.models import LocalVotacion, Partido

class Command(BaseCommand):
    help = 'Carga el padrón oficial de locales de votación de Puno y El Collao, e inicializa partidos de prueba.'

    def handle(self, *args, **options):
        self.stdout.write("Cargando partidos iniciales...")
        partidos_data = [
            {"id_partido": 1,  "nombre_partido": "SOMOS PERU",                                      "categoria": "PARTIDO"},
            {"id_partido": 2,  "nombre_partido": "PARTIDO CIVICO OBRAS",                             "categoria": "PARTIDO"},
            {"id_partido": 3,  "nombre_partido": "AHORA NACION",                                     "categoria": "PARTIDO"},
            {"id_partido": 4,  "nombre_partido": "ALIANZA ELECTORAL VENCEREMOS",                     "categoria": "PARTIDO"},
            {"id_partido": 5,  "nombre_partido": "SALVEMOS AL PERU",                                 "categoria": "PARTIDO"},
            {"id_partido": 6,  "nombre_partido": "ASI - JUNTOS POR EL PERU",                         "categoria": "PARTIDO"},
            {"id_partido": 7,  "nombre_partido": "PAIS PARA TODOS",                                  "categoria": "PARTIDO"},
            {"id_partido": 8,  "nombre_partido": "PROGRESEMOS",                                      "categoria": "PARTIDO"},
            {"id_partido": 9,  "nombre_partido": "PERU PRIMERO",                                     "categoria": "PARTIDO"},
            {"id_partido": 10, "nombre_partido": "PUEBLO CONSCIENTE",                                "categoria": "PARTIDO"},
            {"id_partido": 11, "nombre_partido": "VIVA PUNO",                                        "categoria": "PARTIDO"},
            {"id_partido": 12, "nombre_partido": "ALIANZA PARA EL PROGRESO",                         "categoria": "PARTIDO"},
            {"id_partido": 13, "nombre_partido": "PERU LIBRE",                                       "categoria": "PARTIDO"},
            {"id_partido": 14, "nombre_partido": "PRIMERO LA GENTE",                                 "categoria": "PARTIDO"},
            {"id_partido": 15, "nombre_partido": "TODO CON EL PUEBLO",                               "categoria": "PARTIDO"},
            {"id_partido": 16, "nombre_partido": "PARTIDO DE LOS TRABAJADORES Y EMPRENDEDORES PTE PERU", "categoria": "PARTIDO"},
            {"id_partido": 99, "nombre_partido": "VOTOS EN BLANCO",                                  "categoria": "OTRO"},
            {"id_partido": 100,"nombre_partido": "VOTOS NULOS",                                      "categoria": "OTRO"},
            {"id_partido": 101,"nombre_partido": "VOTOS IMPUGNADOS",                                 "categoria": "OTRO"},
        ]


        for p in partidos_data:
            Partido.objects.update_or_create(
                id_partido=p["id_partido"],
                defaults={
                    "nombre_partido": p["nombre_partido"],
                    "categoria": p["categoria"]
                }
            )

        self.stdout.write("Cargando locales de votación del padrón...")

        locales_data = [
            # PUNO - PUNO
            (15958, "PUNO", "PUNO", "IE 70010 GRAN UNIDAD ESCOLAR SAN CARLOS", "JR CARABAYA 155", 12, 3600, 0, 3600, None),
            (15975, "PUNO", "PUNO", "IE PRIVADA CRAMER", "JR 4 DE NOVIEMBRE 548", 14, 4200, 0, 4200, None),
            (15978, "PUNO", "PUNO", "IE PRIVADA JAMES BALDWIN", "PJE SANCHEZ 153", 20, 6000, 0, 6000, None),
            (15980, "PUNO", "PUNO", "IE SAN IGNACIO DE LOYOLA", "JR ANDRES RAZURI 475", 18, 5400, 0, 5400, None),
            (15985, "PUNO", "PUNO", "IE ADVENTISTA PUNO", "JR PIURA 166", 16, 4800, 0, 4800, None),
            (15994, "PUNO", "PUNO", "IESP PUBLICO PUNO", "AV LA CULTURA SN", 18, 5400, 0, 5400, None),
            (17890, "PUNO", "PUNO", "IE EMBLEMATICA 70029 MARIA AUXILIADORA", "JR MANUEL PINO 136", 20, 5929, 0, 5929, None),
            (40775, "PUNO", "PUNO", "IE PARROQUIAL INMACULADA", "PASAJE SAN VICENTE DE PAUL SN", 21, 6086, 0, 6086, None),
            (40776, "PUNO", "PUNO", "IE PRIVADA COLVER", "JR MOQUEGUA 585", 16, 4800, 0, 4800, None),
            (4340, "PUNO", "PUNO", "IE GLORIOSO SAN CARLOS", "JR FERMIN ARBULU CDRA 2", 18, 5400, 0, 5400, None),
            (4342, "PUNO", "PUNO", "IE 70003 SAGRADO CORAZON DE JESUS", "JR RICARDO PALMA 215", 12, 3600, 0, 3600, None),
            (4344, "PUNO", "PUNO", "IE 70005 CORAZON DE JESUS", "JR CAJAMARCA 211", 13, 3900, 0, 3900, None),
            (4345, "PUNO", "PUNO", "IEP 70028 LAYKAKOTA", "JR BANCHERO ROSSI 291", 9, 2700, 0, 2700, None),
            (4349, "PUNO", "PUNO", "IE COMERCIAL 45 EMILIO ROMERO PADILLA", "JR CARABAYA 154", 13, 3900, 0, 3900, None),
            (4350, "PUNO", "PUNO", "IE GRAN UNIDAD ESCOLAR SAN CARLOS", "JR EL PUERTO 150", 22, 6496, 0, 6496, None),
            (4351, "PUNO", "PUNO", "IE JOSE ANTONIO ENCINAS", "JR LOS ANDES 246", 10, 3000, 0, 3000, None),
            (4353, "PUNO", "PUNO", "IE SANTA ROSA", "JR DEUSTUA 715", 23, 6856, 0, 6856, None),
            (5184, "PUNO", "PUNO", "IE INDUSTRIAL 32", "JR SIMON BOLIVAR 1505", 11, 3300, 0, 3300, None),
            (5185, "PUNO", "PUNO", "IE 71013 GLORIOSO SAN CARLOS", "AV EL SOL 434", 13, 3900, 0, 3900, None),
            (5192, "PUNO", "PUNO", "IE 71001 ALMIRANTE MIGUEL GRAU", "JR PUERTO 297", 13, 3900, 0, 3900, None),
            (53576, "PUNO", "PUNO", "IE 70032 TUNHUIRI", "SECTOR TUNHUIRI CHICO", 2, 464, 0, 464, "ICHU"),
            (53702, "PUNO", "PUNO", "IE 70025 INDEPENDENCIA", "PSJ HIPOLITO UNANUE 152", 12, 3600, 0, 3600, None),
            (7652, "PUNO", "PUNO", "IE EMBLEMATICA MARIA AUXILIADORA", "LAMBAYEQUE 551", 22, 6600, 0, 6600, None),

            # PUNO - ACORA
            (15997, "PUNO", "ACORA", "IE ALFONSO TORRES LUNA", "AV JOSE ANTONIO ENCINAS 135", 12, 3594, 0, 3594, None),
            (40714, "PUNO", "ACORA", "IE 194 CORAZON DE JESUS", "AV JOSE ANTONIO ENCINAS 221", 4, 1198, 0, 1198, None),
            (40715, "PUNO", "ACORA", "IE 70716 CARITAMAYA", "CARRETERA PANAMERICANA SUR KM 38", 6, 1800, 0, 1800, None),
            (40718, "PUNO", "ACORA", "IE 70158 CARUMAS", "AV CARUMAS SN", 2, 503, 0, 503, "AYRUMAS CARUMAS"),
            (40719, "PUNO", "ACORA", "IE PRIVADA NUR", "AV JOSE ANTONIO ENCINAS SN", 4, 1200, 0, 1200, None),
            (40809, "PUNO", "ACORA", "IE RICARDO PALMA TOTORANI", "JR LAVE SN", 4, 1153, 0, 1153, "TOTORANI"),
            (4335, "PUNO", "ACORA", "IE 70075 ACORA", "JR JOSE ANTONIO ENCINAS 151", 9, 2489, 0, 2489, None),
            (4336, "PUNO", "ACORA", "IE 70076", "JR LIMA 171", 9, 2056, 0, 2056, "SACUYO"),
            (53519, "PUNO", "ACORA", "IE FRANCISCO BOLOGNESI CERVANTES", "CARRETERA SACUYO ARUMAS", 1, 203, 0, 203, None),
            (55130, "PUNO", "ACORA", "IES CARLOS DANTE NAVA - CORP JAYU JAYU", "AV TITICACA SN", 5, 1331, 0, 1331, "JAYU JAYU"),
            (55136, "PUNO", "ACORA", "IES ENRIQUE ENCINAS FRANCO", "CCRP SANTA ROSA DE YANAQUE", 2, 401, 0, 401, "SANTA ROSA DE YANAQUE"),
            (55745, "PUNO", "ACORA", "IEP 70816 DE HUANTACACHI - CHILA", "CCRP COPAQUIRA", 1, 253, 0, 253, "COPAQUIRA"),
            (53711, "PUNO", "ACORA", "IE AYMARA", "AV TUPAC AMARU SN", 6, 1800, 0, 1800, None),

            # PUNO - ATUNCOLLA
            (15993, "PUNO", "ATUNCOLLA", "IE 70019 VIRGEN DEL CARMEN", "JR LIMA SN", 4, 1200, 0, 1200, None),
            (5317, "PUNO", "ATUNCOLLA", "IE SAN ANDRES", "JR PUNO SN", 9, 2698, 0, 2698, None),
            (7569, "PUNO", "ATUNCOLLA", "IE 70017 SAN JOSE PRINCIPIO", "CCRP SAN JOSE DE PRINCIPIO SANTA CRUZ", 2, 560, 0, 560, "SAN JOSE DE PRINCIPIO SANTA CRUZ"),

            # PUNO - CAPACHICA
            (40701, "PUNO", "CAPACHICA", "IE 70029 CHAPA", "SECTOR CHAPA SN", 6, 1800, 0, 1800, None),
            (40711, "PUNO", "CAPACHICA", "IE ENRIQUE TORRES BELON", "SECTOR CHAPA SN", 6, 1721, 0, 1721, None),
            (4360, "PUNO", "CAPACHICA", "IE 70026", "JR DOS DE MAYO 649", 9, 2575, 0, 2575, None),
            (4361, "PUNO", "CAPACHICA", "IE JOSE CARLOS MARIATEGUI", "JR DOS DE MAYO 631", 8, 2371, 0, 2371, None),
            (53944, "PUNO", "CAPACHICA", "IE 70020 YAPURA", "CARRETERA PRINCIPAL CAPACHICA LLACHON SN", 2, 303, 0, 303, "YAPURA"),

            # PUNO - COATA
            (15979, "PUNO", "COATA", "IE 70023", "JR CULTURA SN", 5, 1499, 0, 1499, None),
            (4362, "PUNO", "COATA", "IE SAN AGUSTIN", "JR JOSE CARLOS MARIATEGUI SN", 9, 2405, 0, 2405, None),
            (53460, "PUNO", "COATA", "IE 70057", "JR PUNO SN", 2, 310, 0, 310, "JOCHI SAN FRANCISCO"),
            (55744, "PUNO", "COATA", "IE 1252 CCRP CARATA", "BARRIO LA ARBOLEDA SN", 3, 700, 0, 700, "CARATA"),
            (73211, "PUNO", "COATA", "IE 70024 NUESTRA SEÑORA DE LA MERCED", "JR PUNO SN", 3, 969, 0, 969, "SORAZA"),
            (7556, "PUNO", "COATA", "IESTP TAHUANTINSUYO SUCASCO", "JR 20 DE MAYO SN", 4, 1034, 0, 1034, "SUCASCO"),

            # PUNO - CHUCUITO
            (4363, "PUNO", "CHUCUITO", "IE 70015", "JR TRUJILLO 5", 6, 1800, 0, 1800, None),
            (4364, "PUNO", "CHUCUITO", "IE EMILIO ROMERO PADILLA", "JR TRUJILLO 403", 6, 1628, 0, 1628, None),
            (4365, "PUNO", "CHUCUITO", "IE INCA GARCILASO DE LA VEGA", "CCRP HUAYRAPATA", 3, 926, 0, 926, "HUAYRAPATA"),
            (53589, "PUNO", "CHUCUITO", "IE AGROPECUARIO INDUSTRIAL POTOJANI GRANDE", "COMUNIDAD POTOJANI GRANDE SN", 5, 1467, 0, 1467, None),
            (54153, "PUNO", "CHUCUITO", "IE 70084", "CARRETERA PANAMERICANA SN", 1, 291, 0, 291, "LUQUINA GRANDE"),
            (55746, "PUNO", "CHUCUITO", "IE MARIANO MELGAR VILDOSO CCRP TACASAYA", "CCRP TACASAYA", 2, 355, 0, 355, "TACASAYA"),
            (71189, "PUNO", "CHUCUITO", "IE 70068 COCHIRAYA", "CCRP COCHIRAYA", 2, 314, 0, 314, "COCHIRAYA"),
            (71190, "PUNO", "CHUCUITO", "IE 70723 PARINA", "CCRP PARINA", 1, 200, 0, 200, "PARINA"),

            # PUNO - HUATA
            (4366, "PUNO", "HUATA", "IE SAN JUAN DE HUATA", "JR LIMA SN", 11, 3161, 0, 3161, None),

            # PUNO - MAÑAZO
            (15925, "PUNO", "MAÑAZO", "IE MAÑAZO", "AV LA CULTURA SN", 8, 2256, 0, 2256, None),
            (4367, "PUNO", "MAÑAZO", "IE 70011", "AV PANAMERICANA 402", 8, 2364, 0, 2364, None),

            # PUNO - PAUCARCOLLA
            (13505, "PUNO", "PAUCARCOLLA", "IE 70008", "PLAZA DE ARMAS", 5, 1239, 0, 1239, None),
            (4368, "PUNO", "PAUCARCOLLA", "IE TUPAC AMARU", "JR CAHUIDE 200", 9, 2553, 0, 2553, None),
            (53262, "PUNO", "PAUCARCOLLA", "IE 70022", "CALLE SN", 2, 461, 0, 461, "COLLANA"),
            (53590, "PUNO", "PAUCARCOLLA", "IE 70072", "JR MORO SN", 2, 370, 0, 370, "SANTA BARBARA DE MORO"),

            # PUNO - PICHACANI
            (40752, "PUNO", "PICHACANI", "IE EDUARDO BENIGNO LUQUE ROMERO", "JR 28 DE JULIO SN", 8, 2146, 0, 2146, None),
            (53102, "PUNO", "PICHACANI", "IE 70018 LARAQUERI", "JR AUGUSTO B LEGUIA 242", 8, 2125, 0, 2125, None),
            (55732, "PUNO", "PICHACANI", "IE 70133 DE PICHACANI", "PICHACANI", 2, 483, 0, 483, "PICHACANI"),
            (55752, "PUNO", "PICHACANI", "IE PRIMARIA HUACCOCHULLO", "JR HUALLCA SN", 1, 180, 0, 180, "HUACCOCHULLO JATUCACHI"),
            (7361, "PUNO", "PICHACANI", "IE 70034", "AV VILUYO SN", 1, 221, 0, 221, "VILUYO"),

            # PUNO - SAN ANTONIO
            (4370, "PUNO", "SAN ANTONIO", "IE 70062 JUNCAL", "JR ICHUÑA SN", 4, 1132, 0, 1132, None),

            # PUNO - TIQUILLACA
            (40704, "PUNO", "TIQUILLACA", "IE 70033", "JR 4 DE NOVIEMBRE SN", 4, 1189, 0, 1189, None),
            (4371, "PUNO", "TIQUILLACA", "IE SAN FRANCISCO", "JR 4 DE NOVIEMBRE 162", 5, 1450, 0, 1450, None),

            # PUNO - VILQUE
            (40703, "PUNO", "VILQUE", "IE 70014", "AV MANCO CAPAC 201", 5, 1472, 0, 1472, None),
            (51926, "PUNO", "VILQUE", "IE JUAN BUSTAMANTE DUEÑAS", "JR CABANILLAS 134", 5, 1321, 0, 1321, None),

            # PUNO - PLATERIA
            (2567, "PUNO", "PLATERIA", "IESBA MANUEL Z CAMACHO", "AV PLATERIA SN", 5, 1454, 0, 1454, None),
            (40755, "PUNO", "PLATERIA", "IE AGRO INDUSTRIAL DE CCOTA", "SECTOR CENTRAL SN", 4, 1011, 0, 1011, None),
            (4373, "PUNO", "PLATERIA", "IE 70013 PLATERIA", "AV PLATERIA 567", 4, 1146, 0, 1146, None),
            (53203, "PUNO", "PLATERIA", "IE GAMALIEL CHURATA", "CCRP CARUCAYA", 2, 330, 0, 330, "CARUCAYA"),
            (54408, "PUNO", "PLATERIA", "IE VICTOR RAUL HAYA DE LA TORRE", "CCRP DE PERKA", 3, 846, 0, 846, "PERKA"),
            (55735, "PUNO", "PLATERIA", "IEP ADVENTISTA FERNANDO STAHL", "AV FERNANDO STAHL SN", 6, 1639, 0, 1639, None),

            # PUNO - AMANTANI
            (4374, "PUNO", "AMANTANI", "IE AGRO ARTESANAL JOSE MIGUEL GRAU", "JR CAMINERA SUR LAMPAYUNI SN", 8, 2315, 0, 2315, None),
            (4375, "PUNO", "AMANTANI", "IE 70037 VIRGEN DE LAS MERCEDES", "JR LIMA SN", 4, 1108, 0, 1108, None),
            (53681, "PUNO", "AMANTANI", "70092 NUESTRA SEÑORA DE LOS CAMPOS", "SECTOR QUINUAPATA SN", 4, 911, 0, 911, "TAQUILE"),

            # EL COLLAO - ILAVE
            (15799, "EL COLLAO", "ILAVE", "IE 70074 SAN MARTIN DE PORRES", "JR ANDINO 601", 14, 4158, 0, 4158, None),
            (15785, "EL COLLAO", "ILAVE", "IE EMBLEMATICA NUESTRA SEÑORA DEL CARMEN", "JR SANTA BARBARA 420", 20, 5765, 0, 5765, None),
            (15800, "EL COLLAO", "ILAVE", "IE POLITECNICO REGIONAL DON BOSCO", "JR MARIA AUXILIADORA 276", 14, 4200, 0, 4200, None),
            (40802, "EL COLLAO", "ILAVE", "IE 70054 ROBACANI", "SECTOR ROBACANI", 4, 995, 0, 995, "ROBACANI"),
            (4319, "EL COLLAO", "ILAVE", "IE 70735 GLORIOSO 895", "AV DEL NIÑO 125", 16, 4795, 0, 4795, None),
            (4320, "EL COLLAO", "ILAVE", "IE 70736 SAGRADO CORAZON DE JESUS", "JR AMAZONAS 532", 16, 4770, 0, 4770, None),
            (4322, "EL COLLAO", "ILAVE", "IE 71007 MARIANO ZEVALLOS GONZALES", "JR ICA 451", 17, 4951, 0, 4951, None),
            (4324, "EL COLLAO", "ILAVE", "IE JOSE CARLOS MARIATEGUI", "JR ICA 510", 19, 5439, 0, 5439, None),
            (53567, "EL COLLAO", "ILAVE", "IE 70717 CHURO MAQUERA", "SECTOR MAQUERA", 1, 162, 0, 162, "VILLA LOPEZ"),
            (53963, "EL COLLAO", "ILAVE", "IE AGROPECUARIO CANGALLI", "IE AGROPECUARIO CANGALLI", 1, 244, 0, 244, "CANGALLI"),
            (54209, "EL COLLAO", "ILAVE", "IE CARLOS DANTE NAVA", "FHARATA COPANI", 3, 903, 0, 903, "FHARATA COPANI"),
            (54787, "EL COLLAO", "ILAVE", "IE JORGE BASADRE", "CARRETERA ASFALTADA CAMICACHI", 3, 723, 0, 723, "CAMICACHI"),
            (54961, "EL COLLAO", "ILAVE", "IES AGROINDUSTRIAL YACANGO", "CENTRO POBLADO KANCCORA YACANGO", 3, 703, 0, 703, "KANCCORA YACANGO"),
            (55211, "EL COLLAO", "ILAVE", "IE SAN ANTONIO DE CHECCA", "CALLE SN", 2, 576, 0, 576, "CHECCA LACAYA YAURIMA CHUOTAMAYA"),
            (55212, "EL COLLAO", "ILAVE", "IE CHUICHAYA", "CALLE EN CCPP CHUICHAYA", 2, 520, 0, 520, "CHUICHAYA"),

            # EL COLLAO - PILCUYO
            (40848, "EL COLLAO", "PILCUYO", "ESCUELA SUPERIOR DE FORMACION ARTISTICA PUBLICA", "AV CESAR VALLEJO SN", 5, 1453, 0, 1453, None),
            (4325, "EL COLLAO", "PILCUYO", "IE 70049 GLORIOSO JOSE ANTONIO ENCINAS", "JR LIMA SN", 6, 1753, 0, 1753, None),
            (4326, "EL COLLAO", "PILCUYO", "IE CESAR VALLEJO", "JR CESAR VALLEJO SN", 7, 2003, 0, 2003, None),
            (4327, "EL COLLAO", "PILCUYO", "IE MICAELA BASTIDAS", "JR INCA PIURA SN", 4, 1199, 0, 1199, None),
            (54962, "EL COLLAO", "PILCUYO", "IE 70738 PERU BIRF", "PILCUYO SN", 4, 1164, 0, 1164, None),
            (54963, "EL COLLAO", "PILCUYO", "IEP 70339 CHIPANA", "CENTRO POBLADO VILLA CHIPANA", 5, 1442, 0, 1442, "VILLA CHIPANA"),

            # EL COLLAO - SANTA ROSA
            (4328, "EL COLLAO", "SANTA ROSA", "IE 70343 MAZOCRUZ", "AV DE LOS NIÑOS SN", 10, 2867, 0, 2867, None),

            # EL COLLAO - CAPAZO
            (4329, "EL COLLAO", "CAPAZO", "IE TECNICO AGROPECUARIO", "TUPALA", 1, 209, 0, 209, "TUPALA"),
            (5336, "EL COLLAO", "CAPAZO", "IE PECUARIA", "JR INDEPENDENCIA SN", 2, 557, 0, 557, None),

            # EL COLLAO - CONDURIRI
            (5339, "EL COLLAO", "CONDURIRI", "IE 70670", "JR 28 DE JULIO SN", 4, 1150, 0, 1150, None),
            (5357, "EL COLLAO", "CONDURIRI", "IE TUPAC AMARU II", "JR INDEPENDENCIA SN", 4, 1071, 0, 1071, None),
            (54964, "EL COLLAO", "CONDURIRI", "IE 70731 SALES GRANDE", "CCRP SALES GRANDE", 2, 466, 0, 466, "SALES GRANDE"),
        ]

        count = 0
        for loc in locales_data:
            id_local, prov, dist, nombre, direc, mesas, hab_reg, ext, hab_mun, msi = loc
            LocalVotacion.objects.update_or_create(
                id_local=id_local,
                defaults={
                    "provincia": prov,
                    "distrito": dist,
                    "nombre_local": nombre,
                    "direccion_local": direc,
                    "cant_mesas": mesas,
                    "electores_regional": hab_reg,
                    "extranjeros_inscritos": ext,
                    "electores_municipal": hab_mun,
                    "localidades_msi": msi
                }
            )
            count += 1

        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval(pg_get_serial_sequence('partido', 'id_partido'), coalesce(max(id_partido), 1)) FROM partido;")

        self.stdout.write(self.style.SUCCESS(f"¡Éxito! Se cargaron {count} locales de votación y los partidos políticos base."))

