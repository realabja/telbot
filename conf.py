import configparser as cfg



def read_conf(conf, item):
    pars =cfg.ConfigParser()
    pars.read(conf)
    return pars.get('creds' ,item)