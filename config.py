import os
import tweepy
import logging

logger = logging.getLogger()

def create_api():
    # As linhas abaixo são responsáveis por coletar os dados de entrada da conta

    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    acess_token = os.getenv("ACESS_TOKEN")
    acess_token_secret = os.getenv("ACESS_TOKEN_SECRET")

    # As linhas abaixo colocam em variáveis os dados obtidos

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(acess_token, acess_token_secret)

    # Esta linha cria o objeto que representa uma instância da API do twitter

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    # EXECUÇÃO (verifica validade das credenciais)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True) #REGISTRO PARA DEBUG
        raise e

    logger.info("API created")
    return api
