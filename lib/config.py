import os.path
import validators
import yaml

def load_config(in_config_file):
        if os.path.isfile(in_config_file) == False:
                print ("Error opening settings.yaml\n");
                return False
        with open(in_config_file,'r') as ymlfile:
                try:
                        cfg = yaml.load(ymlfile)
                except yaml.YAMLError as exc:
                        print ("Error Parsing settings.yaml\n");
                        return false
        return cfg

def validate_config(in_cfg):
        success = True
        if (('region' not in in_cfg['aws']) or (in_cfg['aws']['region'] == None)):
                success = False

        return success

def validate_email(email):
        if not validators.email(email):
                return False
        return True

