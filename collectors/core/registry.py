import importlib
import inspect
import pkgutil

from collectors.core.collector import DataSource


def discover_sources():
    import collectors.sources as package

    found = []
    for module_info in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(
            f"collectors.sources.{module_info.name}"
        )
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(cls, DataSource)
                and cls is not DataSource
                and cls.__module__ == module.__name__
            ):
                instance = cls()
                if instance.enabled:
                    found.append(instance)

    return sorted(found, key=lambda item: item.name)


def get_source(name: str):
    for source in discover_sources():
        if source.name == name:
            return source
    available = ", ".join(s.name for s in discover_sources())
    raise ValueError(f"Unknown source '{name}'. Available: {available}")
