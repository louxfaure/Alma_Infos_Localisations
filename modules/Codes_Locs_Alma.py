#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Modules externes
import os
import logging
import csv
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry 
from requests import request
import xml.etree.ElementTree as ET

class LocsAlma(object):

    def __init__(self, api_key,out_file):
        self.api_key = api_key
        self.report=open(out_file, "w",encoding='utf-8')
        self.report.write("Code_Bibliothèque\tNom_Blibliothèque\tCode_Localisation\tType_de_Localisation\tCode Unité de service aux usager\tUnité de service aux usager\tSupprimée de la découverte\tCode de Type de cote\tType de cote\n")
        # self.instance = instance
        self.logger = logging.getLogger("__main__.{}".format(__name__))
        # self.logger.debug(instance)
        url= "https://api-eu.hosted.exlibrisgroup.com/almaws/v1/conf/libraries"             
        self.statut, self.reponse = self.request('GET',url)
        if self.statut != 'Error' :
            self.list_bib = self.reponse.json()
            # self.logger.debug(self.list_bib)
            self.statut, self.alma_loc_list = self.get_loc_for_bib()
            self.report.close


    @property
    def get_error_message(self,response):
        """Extract error code & error message of an API response
        
        Arguments:
            response {object} -- API REsponse
        
        Returns:
            int -- error code
            str -- error message
        """
        error_code, error_message = '',''
        try :
            content = response.json()
        except : 
            # Parfois l'Api répond avec du xml même si l'en tête demande du Json cas des erreurs de clefs d'API 
            root = ET.fromstring(response.text)
            error_message = root.find(".//xmlb:errorMessage").text if root.find(".//xmlb:errorMessage").text else response.text 
            error_code = root.find(".//xmlb:errorCode").text if root.find(".//xmlb:errorCode").text else '???'
            return error_code, error_message 
        error_message = content['errorList']['error'][0]['errorMessage']
        error_code = content['errorList']['error'][0]['errorCode']
        return error_code, error_message
        
    def request(self,httpmethod, url,data=None):
        """Envoi un appel à l'api Alma pour injecter les codes des départements et leur libellés

        Args:
            httpmethod (string): Méthode d'appel PUT, GET, POST.
            url
            data (json, optional): . Defaults to None.
        Returns:
            array: status du traitement Success ou Error et Reponse de l'API
        """
        #20190905 retry request 3 time s in case of requests.exceptions.ConnectionError
        self.logger.debug("{}?apikey={}".format(url,self.api_key))
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.request(
            method=httpmethod,
            headers= {
            "User-Agent" : "pyalma/0.1.0",
            "Authorization" : "clef_api {}".format(self.api_key),
            "Accept" : 'application/json',
            "Content-Type" :'application/json',
        },
            url= "{}?apikey={}".format(url,self.api_key),
            data=data)
        try:
            response.raise_for_status()  
        except requests.exceptions.HTTPError:
            print(response.text)
            error_code, error_message= self.get_error_message(response)
            self.logger.error("Alma_Apis :: HTTP Status: {} || Method: {} || URL: {} || Response: {}".format(response.status_code,response.request.method, response.url, response.text))
            if error_code == '402263' :
                return 'Error_SetExist', "{} -- {}".format(error_code, error_message)
            return 'Error', "{} -- {}".format(error_code, error_message)
        except requests.exceptions.ConnectionError:
            error_code, error_message= self.get_error_message(response)
            self.logger.error("Alma_Apis :: Connection Error: {} || Method: {} || URL: {} || Response: {}".format(response.status_code,response.request.method, response.url, response.text))
            return 'Error', "{} -- {}".format(error_code, error_message)
        except requests.exceptions.RequestException:
            error_code, error_message= self.get_error_message(response)
            self.logger.error("Alma_Apis :: Connection Error: {} || Method: {} || URL: {} || Response: {}".format(response.status_code,response.request.method, response.url, response.text))
            return 'Error', "{} -- {}".format(error_code, error_message)
        return "Success", response

    def get_loc_for_bib(self) :
        """Liste les codes stats déjà déclarés dans Alma pour la network Zone
        Args:

        return :
        liste : liste contenant la totalité des codes statistiques déclarés dans Alma
        """
        alma_loc_list = []
        for bib in self.list_bib[ "library"] :
            if bib["number_of_locations"]["value"] == 0 :
                continue
            bib_code = bib["id"]
            bib_descr = bib["name"]
            url = bib["number_of_locations"]["link"]
            self.logger.info("\t>>{} :: {}".format(bib_code,bib_descr))
            statut, reponse = self.request('GET',url)
            if statut == 'Error' :
                return statut, reponse
            locs_list= reponse.json()
            for loc in locs_list["location"] :
                self.logger.info("\t\t>>>{}".format(loc["name"]))
                self.report.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    bib_code,
                    bib_descr,
                    loc["code"],
                    loc["name"],
                    self.test_dict_key(loc["type"],'value'),
                    self.test_dict_key(loc["fulfillment_unit"],'value'),
                    self.test_dict_key(loc["fulfillment_unit"],'desc'),
                    loc["suppress_from_publishing"],
                    self.test_dict_key(loc["call_number_type"],'value'),
                    self.test_dict_key(loc["call_number_type"],'desc')

                ))
        return "ok"
            
            
    def test_dict_key(self,dict,elemt) :
        if elemt in dict.keys():
            return dict[elemt]
        else :
            return "None"

        # return alma_codes_stat_list
        
    

    
