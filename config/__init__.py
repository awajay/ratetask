from dotenv import load_dotenv


def load_config(testing, envfile='.env'):
    """Load environment variables."""
    if testing is True:
        return load_dotenv(dotenv_path=envfile)
    else:
        return load_dotenv(dotenv_path=envfile)
