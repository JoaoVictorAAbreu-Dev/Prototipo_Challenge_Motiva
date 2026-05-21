"""
Domain Exceptions - Application-specific exceptions
"""


class DomainException(Exception):
    """Base exception for domain layer"""

    pass


class ResourceNotFoundError(DomainException):
    """Raised when a requested resource is not found"""

    def __init__(self, resource_type: str, identifier: str):
        self.resource_type = resource_type
        self.identifier = identifier
        super().__init__(
            f"{resource_type} with identifier '{identifier}' not found"
        )


class ValidationError(DomainException):
    """Raised when domain validation fails"""

    pass


class DuplicateResourceError(DomainException):
    """Raised when attempting to create a duplicate resource"""

    def __init__(self, resource_type: str, field: str, value: str):
        self.resource_type = resource_type
        self.field = field
        self.value = value
        super().__init__(
            f"{resource_type} with {field} '{value}' already exists"
        )


class UnauthorizedError(DomainException):
    """Raised when user lacks required permissions"""

    pass


class InvalidStateTransitionError(DomainException):
    """Raised when an invalid state transition is attempted"""

    def __init__(self, current_state: str, requested_state: str):
        super().__init__(
            f"Cannot transition from '{current_state}' to '{requested_state}'"
        )
