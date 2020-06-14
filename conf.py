import configparser as cfg



def read_conf(conf):
    pars =cfg.ConfigParser()
    pars.read(conf)
    return pars.get('creds' ,'token')