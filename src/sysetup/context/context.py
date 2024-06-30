from package_utils.context import Context

from sysetup.models import Config, Options, Secrets

context = Context(Options, Config, Secrets)
