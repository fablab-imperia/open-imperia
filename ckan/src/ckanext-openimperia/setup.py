from setuptools import find_packages, setup

setup(
    name="ckanext-openimperia",
    version="0.1.0",
    description="CKAN customization for OpenImperia",
    author="OpenImperia contributors",
    license="AGPL-3.0-or-later",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "ckan.plugins": [
            "openimperia=ckanext.openimperia.plugin:OpenImperiaPlugin",
        ],
    },
)
