from itertools import chain

__all__ = ["constants", "errors", "functions", "types"]


def _get_system_name() -> str:
    import platform

    system = platform.system().lower()
    if system.startswith("cygwin"):
        system = "cygwin"
    return system


def _library_locations(abi_version):
    import os

    system = _get_system_name()
    if system == "darwin":
        library_names = ["libgnutls.%d.dylib" % abi_version]
        dynamic_loader_env_vars = ["DYLD_LIBRARY_PATH", "LD_LIBRARY_PATH"]
        additional_paths = ["/usr/local/lib", "/opt/local/lib", "/sw/lib"]
    elif system == "windows":
        library_names = ["libgnutls-%d.dll" % abi_version]
        dynamic_loader_env_vars = ["PATH"]
        additional_paths = ["."]
    elif system == "cygwin":
        library_names = ["cyggnutls-%d.dll" % abi_version]
        dynamic_loader_env_vars = ["LD_LIBRARY_PATH"]
        additional_paths = ["/usr/bin"]
    else:
        # Debian uses libgnutls-deb0.so.28, go figure
        library_names = [
            "libgnutls.so.%d" % abi_version,
            "libgnutls-deb0.so.%d" % abi_version,
        ]
        dynamic_loader_env_vars = ["LD_LIBRARY_PATH"]
        additional_paths = ["/usr/local/lib"]
    for library_name in library_names:
        for path in (
            path
            for env_var in dynamic_loader_env_vars
            for path in os.environ.get(env_var, "").split(":")
            if os.path.isdir(path)
        ):
            yield os.path.join(path, library_name)
        yield library_name
        for path in additional_paths:
            yield os.path.join(path, library_name)


def _load_library(abi_versions):
    from ctypes import CDLL

    for library in chain.from_iterable(
        _library_locations(abi_version)
        for abi_version in sorted(abi_versions, reverse=True)
    ):
        try:
            return CDLL(library)
        except OSError:
            pass
        else:
            break
    else:
        raise RuntimeError(
            "cannot find a supported version of libgnutls on this system"
        )


libgnutls = _load_library(
    abi_versions=(28, 30)
)  # will use the highest of the available ABI versions


from PyGnuTLS.library import constants
from PyGnuTLS.library import errors
from PyGnuTLS.library import functions
from PyGnuTLS.library import types


__need_version__ = "3.2.0"

if functions.gnutls_check_version(__need_version__.encode()) is None:  # type: ignore
    version = functions.gnutls_check_version(None)  # type: ignore
    raise RuntimeError(
        "Found GNUTLS library version %s, but at least version %s is required"
        % (version, __need_version__)
    )

# calling gnutls_global_init is no longer required starting with gnutls 3.3
if functions.gnutls_check_version("3.3".encode()) is None:  # type: ignore
    libgnutls.gnutls_global_init()
