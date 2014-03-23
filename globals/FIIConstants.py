class FIIConstants:
    ###Constants for output files name
    class OutputFileName:
        USER_PROFILE_BASE = "user_profile_base.json"
        USER_PROFILE_FAVORITES = "user_profile_favorites.json"
        USER_PROFILE_INTERESTS = "user_profile_interests.json"
        USER_PROFILE_KNOWLEDGE = "user_profile_knowledge.json"
        USER_PROFILE_REWARDS = "user_profile_rewards.json"
    ###Constants for table schema's
    class Schema:
        USER_PROFILE_BASE = "user_profile_base.json"
        USER_PROFILE_FAVORITES = "user_profile_favorites.json"
        USER_PROFILE_INTERESTS = "user_profile_interests.json"
        USER_PROFILE_KNOWLEDGE = "user_profile_knowledge.json"
        USER_PROFILE_REWARDS = "user_profile_rewards.json" 
    ###Login Credentials
    class Credentials:
        class Facebook:
            EMAIL = ""
            PASSWORD = ""
        class LinkedIn:
            EMAIL = ""
            PASSWORD = ""
        class Google:
            EMAIL = ""
            PASSWORD = ""
        class Twitter:
            EMAIL = ""
            PASSWORD = ""
        class KLout:
            EMAIL = ""
            PASSWORD = ""
    ###URL's
    FACEBOOK_ROOT_URL = "https://www.facebook.com/login.php"
    FACEBOOK_OAUTH_ACCESS_TOKEN_URL = "https://developers.facebook.com/tools/access_token/"
    GOOGLE_LOGIN_URL = "https://accounts.google.com/ServiceLogin?hl=en&continue=https://www.google.com/"
    ###BigQuery Info
    class BigQueryInfo:
        PROJECT_ID = "fiibigdata"
        DATASET_ID = "fii_datacard"
    ###Data Tables Id
    class Tables:
        GENERAL = "user_profile_base"
        FAVORITES = "user_profile_favorites"
        INTERESTS = "user_profile_interests"
        KNOWLEDGE = "user_profile_knowledge"
        REWARDS = "user_profile_rewards"
    LOG_FILE_NAME = "FIIBigdata.log"
    LOG_FILE_PATH = ""
    CONFIG_FILE_NAME = "FIIConfigData.cfg"
    CONFIG_FILE_PATH = ""
    LIKES_CONTENT_BATCH_COUNT = 8 
    class DIRS:
        GOOGLE_PLUS_DIR = ""
        FACEBOOK_DIR = ""
        LINKEDIN_DIR = ""
        