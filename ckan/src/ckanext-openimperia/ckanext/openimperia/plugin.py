import os

import click
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


DEFAULT_LICENSE_ID = "cc-by"

DEFAULT_ORGANIZATION = {
    "name": "fablab-imperia-aps",
    "title": "Fablab Imperia APS",
    "description": (
        "Associazione Fablab Imperia APS, soggetto promotore del portale "
        "Open Data Imperia."
    ),
}

DEFAULT_SITE_TITLE = "Open Data Imperia"
DEFAULT_SITE_DESCRIPTION = "Portale open data del territorio di Imperia"
DEFAULT_SITE_LOGO = "/images/openimperia-logo.svg"
DEFAULT_SITE_FAVICON = "/images/openimperia-icon.svg"
DEFAULT_SITE_INTRO = (
    "I dati aperti del territorio di Imperia: informazioni pubbliche "
    "rilasciate in formati aperti, liberamente riutilizzabili da cittadini, "
    "imprese e associazioni."
)
DEFAULT_LOCALE = "it"

# Valori di default di CKAN: se una di queste opzioni ha ancora il valore di
# default di CKAN significa che non è stata personalizzata, quindi possiamo
# applicare il branding di Open Data Imperia. Un valore impostato in ckan.ini
# o tramite variabili d'ambiente ha invece la precedenza.
BRANDING = {
    "ckan.site_title": ("CKAN", DEFAULT_SITE_TITLE),
    "ckan.site_description": ("", DEFAULT_SITE_DESCRIPTION),
    "ckan.site_logo": ("/base/images/ckan-logo.png", DEFAULT_SITE_LOGO),
    "ckan.favicon": ("/base/images/ckan.ico", DEFAULT_SITE_FAVICON),
    "ckan.site_intro_text": ("", DEFAULT_SITE_INTRO),
    "ckan.locale_default": ("en", DEFAULT_LOCALE),
}


def _licenses_group_url():
    path = os.path.join(os.path.dirname(__file__), "licenses_group.json")
    return "file://" + os.path.abspath(path)


@toolkit.chained_action
def package_create(next_action, context, data_dict):
    """Assegna la licenza aperta di default ai nuovi dataset."""
    if isinstance(data_dict, dict) and not data_dict.get("license_id"):
        data_dict["license_id"] = DEFAULT_LICENSE_ID
    return next_action(context, data_dict)


@click.group()
def openimperia():
    """Comandi di amministrazione del portale Open Data Imperia."""


@openimperia.command()
def init():
    """Inizializza il portale (organizzazione di default e configurazione)."""
    ensure_organization()
    click.echo("Organizzazione '%s' pronta." % DEFAULT_ORGANIZATION["name"])


def ensure_organization():
    user = toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    user_name = user["name"]

    try:
        toolkit.get_action("organization_show")(
            {"ignore_auth": True, "user": user_name},
            {"id": DEFAULT_ORGANIZATION["name"]},
        )
        return
    except toolkit.ObjectNotFound:
        pass

    toolkit.get_action("organization_create")(
        {"ignore_auth": True, "user": user_name},
        dict(DEFAULT_ORGANIZATION),
    )


class OpenImperiaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IClick)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")

        for key, (ckan_default, our_default) in BRANDING.items():
            if config_.get(key) in (None, ckan_default):
                config_[key] = our_default

        # La lista licenze deve essere impostata prima che il registro
        # licenze di CKAN venga istanziato al primo utilizzo. Non
        # sovrascriviamo un valore fornito esplicitamente (ini o env).
        if not config_.get("licenses_group_url"):
            config_["licenses_group_url"] = _licenses_group_url()

    # IActions
    def get_actions(self):
        return {"package_create": package_create}

    # IClick
    def get_commands(self):
        return [openimperia]
