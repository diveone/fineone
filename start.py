from finone import app

config_file = ('APP_CONFIG_FILE'
               if not app.testing
               else 'TEST_CONFIG_FILE')

if __name__ == '__main__':
    app.config.from_envvar(config_file)
    app.run()
