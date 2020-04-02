import os
import click


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument("lang")
    def init(lang):
        """Initialize a new language."""
        if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
            raise RuntimeError("extract command failed")
        if os.system("pybabel init -i messages.pot -d app/translations -l " + lang):
            raise RuntimeError("init command failed")
        os.remove("messages.pot")

    @translate.command()
    def update():
        """Update all languages."""
        if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
            raise RuntimeError("extract command failed")
        if os.system("pybabel update -i messages.pot -d app/translations"):
            raise RuntimeError("update command failed")
        os.remove("messages.pot")

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system("pybabel compile -d app/translations"):
            raise RuntimeError("compile command failed")

    @app.cli.group()
    def filldata():
        """Insert data into database for debugging and testing purposes."""
        pass

    @filldata.command()
    @click.option('--sure', required=True, default='no', show_default=True)
    def deleteall(sure):
        """Delete ALL data."""

        if sure.lower().startswith(('y', 'j')):
            from app import db
            db.drop_all()
            db.create_all()
            print("Cleared the database.")
        else:
            print("Add argument '--sure y' to empty the database.")

    @filldata.command()
    def aircrafts():
        """Drops ALL aircraft_types and import aircraft_types again (ressource file)."""
        from app.filldata import import_aircrafts

        import_aircrafts()

    @filldata.command()
    def fakedata():
        """Fills db with fake data for debugging purposes."""
        from app.filldata import import_fakedata

        import_fakedata()

    @filldata.command()
    def devices():
        """Fills db with data from ddb (ressource file)."""
        from app.filldata import import_devices

        import_devices()
