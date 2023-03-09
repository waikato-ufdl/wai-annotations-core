from .constants import DOMAIN_CODE_MATCHER


class DomainCode:
    def __init__(self, domain_code: str):
        if DOMAIN_CODE_MATCHER(domain_code) is None:
            raise Exception(f"Invalid domain-code '{domain_code}'")
        self._domain_code = domain_code

    def __str__(self) -> str:
        return self._domain_code

    def __eq__(self, other):
        return str(other) == self._domain_code

    def __hash__(self) -> int:
        return hash(self._domain_code)
