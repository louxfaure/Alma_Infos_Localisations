#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Modules externes
import os
import re
import logging

from modules import Codes_Locs_Alma,logs
import xml.etree.ElementTree as ET
######################
#PARAMETRES DU SCRIPT#
######################


# Paramètre Alma
INSITUTIONS_LIST = ['UB','UBM','BXSA','INP','IEP']
# CLEF_API = os.getenv("TEST_NETWORK_API")

# Logs
APP_NAME = "Alma-Infos_Localisations"
LOGS_LEVEL = 'INFO'
LOGS_FILE = "{}/{}".format(os.getenv('LOGS_PATH'),APP_NAME)



#Répertoires de traitement
OUT_FILE_PATH = '/media/sf_LouxBox' #Fichier siganlant les codes manquants avec leur catégorie



#On initialise le logger
logs.setup_logging(name=APP_NAME, level=LOGS_LEVEL,log_dir=LOGS_FILE)
logger = logging.getLogger(__name__)



# POur chaque institution on récupére la liste des bibliothèques et des codes
for inst in INSITUTIONS_LIST :
    logger.info("> {}".format(inst))
    api_key = CLEF_API = os.getenv("PROD_{}_USER_API".format(inst))
    out_file = "{}/{}_Liste_des_localisations.csv".format(OUT_FILE_PATH,inst)
    locs = Codes_Locs_Alma.LocsAlma(api_key,out_file)
    if locs.statut == "error" :
        continue
# users_codes_stats = Codes_Stats_Alma.UsersCodesStats(CLEF_API)
# if users_codes_stats.statut == "Error" :
#     logger.error("Récupération de la table UserStatCategories :: Impossible de récupérer la table ::{}".format(users_codes_stats.reponse))
#     exit()
# logger.info("Récupération de la table UserStatsCategories :: OK")




# # Traitement des fichiers

# report = open(OUT_FILE, "w")
# report.write("Institution\tPopulation\tCode stat.\tDescription\tCatégorie\n")
# unknow_codes_list = []
# compteur = 0
# for file in os.listdir(LOCAL_FILE_PATH_IN): 
#     logger.info(file)
#     file_name = re.findall('^.{8}(.*?)_(.*?)\.xml', file)
#     institution= file_name[0][0]
#     population = file_name[0][1]
#     # logger.debug("{} - {}".format(institution,population))
#     root = ET.parse(os.path.abspath(file))
#     # print(root.tag)
#     for stat in root.findall('.//user_statistic'):
#         statistic_category = stat.find('./statistic_category').text
#         category_type = stat.find('./category_type').text
#         if statistic_category not in users_codes_stats.alma_codes_stat_list and statistic_category not in unknow_codes_list :
#             description = "{} - Description à renseigner".format(statistic_category)
#             compteur =+ 1
#             unknow_codes_list.append(statistic_category)
#             report.write("{}\t{}\t{}\t{}\n".format(institution,population,statistic_category,category_type))
#             logger.info("{} :: {} :: {} :: {}".format(institution,population,statistic_category,description,category_type))
# logger.info("Traitement terminé. {} codes à ajouter dans la table UserStatsCategories")
# report.close
