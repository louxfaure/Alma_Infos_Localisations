# LISTER LES LOCALISATIONS ALMA

Ce petit script développé en python permet d'extraire pour chaque institution et chaque bibliothèque la liste des localisations crées dans le système. Pour chaque localisation, le programme extrait les informations suivantes :
  - Code_Bibliothèque
  - Nom_Blibliothèque
  - Code_Localisation
  - Type_de_Localisation
  - Code d'unité de service aux usager
  - Unité de service aux usager
  - Information sur l'affichage des exemplaires au catalogue
  - Code de Type de cote
  - Type de cote

Le programme créé un fichier csv (separateur tab) pour chaque institution. Le répertoire de destination des fichiers est à renseigner dans la variable OUT_FILE_PATH du fichier main.py
Les clefs d'API doivent être déclarées dans des variable d'environnement (une varible pour chque institution). La vraible doit être nommée comme suit : PROD_[Code de l'institution]_USER_API ex : PROD_UBM_USER_API 